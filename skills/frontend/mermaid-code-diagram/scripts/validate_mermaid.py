#!/usr/bin/env python3
"""
Mermaid 语法验证器 (Python)

使用方式:
    python validate_mermaid.py <file>                  — 从文件读取并校验
    python validate_mermaid.py --code "flowchart TD    — 从参数读取
        A-->B"
    python validate_mermaid.py                          — 从 stdin 读取
    python validate_mermaid.py <file> --export [dir]   — 校验通过后下载渲染图(默认 PNG)
    python validate_mermaid.py <file> --export --svg   — 下载 SVG 而非 PNG
    python validate_mermaid.py <file> --export --width 3000 — 指定 PNG 宽度;默认 auto(自动推荐)

退出码:
    0 = 语法正确
    1 = 语法错误 (详细信息输出到 stderr)
    2 = 用法错误

工作原理:
    1. 本地预检 — 基于正则的规则快速捕获常见语法错误
    2. 远程校验 — 调用 mermaid.ink API 做真实渲染验证
"""

import sys
import re
import base64
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from typing import NamedTuple

# ─── 常量 ───────────────────────────────────────────────────

MERMAID_INK_URL = "https://mermaid.ink/img/"
MERMAID_INK_SVG_URL = "https://mermaid.ink/svg/"
REQUEST_TIMEOUT = 3  # 秒
# PNG 推荐宽度区间:mermaid.ink 默认按视口宽度渲染(约 1000-1300px),大图文字发糊。
AUTO_WIDTH_MIN = 2400   # 自动推荐的下限
AUTO_WIDTH_MAX = 4800   # 自动推荐的上限(再大渲染慢且没必要)

# Mermaid 保留关键字（不能用作节点 ID）
RESERVED_KEYWORDS = {
    "end", "subgraph", "graph", "flowchart", "sequenceDiagram",
    "classDiagram", "stateDiagram", "stateDiagram-v2", "erDiagram",
    "gantt", "pie", "gitGraph", "mindmap", "timeline", "journey",
    "click", "style", "classDef", "linkStyle", "class",
    "direction", "participant", "actor",
}

# 合法的图表类型声明（首行）
DIAGRAM_TYPES = [
    r"flowchart\s+(TD|TB|BT|LR|RL)",
    r"graph\s+(TD|TB|BT|LR|RL)",
    r"sequenceDiagram",
    r"classDiagram",
    r"stateDiagram(-v2)?",
    r"erDiagram",
    r"gantt",
    r"pie(\s+showData)?",
    r"gitGraph",
    r"mindmap",
    r"timeline",
    r"journey",
    r"C4Context",
    r"C4Container",
    r"C4Component",
    r"C4Deployment",
    r"xychart",
    r"kanban",
    r"block-beta",
    r"quadrantChart",
    r"requirementDiagram",
    r"sankey-beta",
    r"packet-beta",
    r"architecture-beta",
]


class Issue(NamedTuple):
    line: int          # 行号（1-based）
    severity: str      # "error" | "warning"
    message: str       # 问题描述
    suggestion: str    # 修复建议


# ─── 提取 mermaid 代码块 ────────────────────────────────────

def extract_mermaid_blocks(text: str) -> list[str]:
    """从文本中提取 mermaid 代码块。支持 ```mermaid 围栏和纯代码。"""
    pattern = r"```mermaid\s*\n([\s\S]*?)```"
    blocks = [m.group(1).strip() for m in re.finditer(pattern, text)]
    if blocks:
        return blocks
    # 如果没有围栏，整段视为 mermaid 代码
    stripped = text.strip()
    if stripped:
        return [stripped]
    return []


# ─── 本地预检规则 ───────────────────────────────────────────

def check_local(code: str) -> list[Issue]:
    """基于正则的本地语法预检，捕获常见错误。"""
    issues: list[Issue] = []
    lines = code.split("\n")

    if not lines:
        return [Issue(1, "error", "代码为空", "请提供 mermaid 代码")]

    # --- 规则 1: 首行必须是合法图表类型声明 ---
    first_line = lines[0].strip()
    type_pattern = "|".join(f"(?:{t})" for t in DIAGRAM_TYPES)
    if not re.match(rf"^\s*(?:{type_pattern})\s*$", first_line):
        # 可能有 %%{init: ...}%% 指令在前面
        has_init = first_line.startswith("%%{")
        if not has_init:
            issues.append(Issue(
                1, "error",
                f"首行不是合法的图表类型声明: '{first_line}'",
                "首行应为 'flowchart TD', 'sequenceDiagram' 等"
            ))

    # --- 逐行检查 ---
    subgraph_depth = 0
    for i, raw_line in enumerate(lines, 1):
        line = raw_line.strip()

        # 跳过空行和注释
        if not line or line.startswith("%%"):
            continue

        # --- 规则 2: graph 应改为 flowchart ---
        if re.match(r"^graph\s+(TD|TB|BT|LR|RL)", line):
            issues.append(Issue(
                i, "warning",
                "建议使用 'flowchart' 替代 'graph'",
                f"将 '{line}' 改为 '{line.replace('graph', 'flowchart', 1)}'"
            ))

        # --- 规则 3: 列表语法陷阱 [数字. 空格] ---
        list_trap = re.search(r'\[\d+\.\s', line)
        if list_trap:
            issues.append(Issue(
                i, "error",
                f"检测到列表语法陷阱: '{list_trap.group()}'",
                "删除数字后点号与空格之间的空格，如 [1.Item] 或用 [① Item]"
            ))

        # --- 规则 4: subgraph 命名不规范 ---
        sg_match = re.match(r'^subgraph\s+(.+)$', line)
        if sg_match:
            subgraph_depth += 1
            sg_rest = sg_match.group(1).strip()
            # 如果有空格但没用 id["name"] 格式
            if " " in sg_rest and not re.match(r'^\w+\s*\[', sg_rest):
                issues.append(Issue(
                    i, "error",
                    f"subgraph 名称含空格但未使用 ID[\"名称\"] 格式: '{line}'",
                    f'改为: subgraph id["{sg_rest}"]'
                ))
            # 中文 subgraph 名（没有引号包裹）
            if re.search(r'[\u4e00-\u9fff]', sg_rest) and "[" not in sg_rest:
                issues.append(Issue(
                    i, "error",
                    f"subgraph 使用了中文名但未用 ID[\"名称\"] 格式: '{line}'",
                    '改为: subgraph myId["中文名称"]'
                ))

        # --- 规则 5: end 关键字（关闭 subgraph） ---
        if line == "end":
            subgraph_depth -= 1

        # --- 规则 6: 节点文本中的中文未加引号 ---
        # 匹配 A[中文] 但不匹配 A["中文"]
        unquoted_cn = re.findall(r'(\w+)\[((?=[^\"])[^\]]*[\u4e00-\u9fff][^\]]*)\]', line)
        for node_id, text in unquoted_cn:
            # 排除已经有引号的,以及复合形状([(" ")] 圆柱 / [{" "}] 六边形 / [[" "]] 子例程)
            if text.startswith('"'):
                continue
            if re.match(r'^[\(\{\[]\s*"', text):
                continue
            issues.append(Issue(
                i, "warning",
                f"节点 '{node_id}' 的中文文本未加引号: [{text}]",
                f'建议改为: {node_id}["{text}"]'
            ))

        # --- 规则 7: 箭头标签中的中文未加引号 ---
        unquoted_label = re.findall(r'-->\|([^"｜][^|]*[\u4e00-\u9fff][^|]*)\|', line)
        for label in unquoted_label:
            issues.append(Issue(
                i, "warning",
                f"箭头标签中的中文未加引号: |{label}|",
                f'建议改为: -->|"{label}"|'
            ))

        # --- 规则 8: 节点 ID 含连字符 ---
        hyphen_ids = re.findall(r'(?:^|\s)(\w+-\w+)(?:\s*[\[\({]|\s*-->|\s*-\.->|\s*==>)', line)
        for hid in hyphen_ids:
            if hid not in ("stateDiagram-v2", "block-beta", "sankey-beta",
                           "packet-beta", "architecture-beta", "C4Context",
                           "C4Container", "C4Component", "C4Deployment"):
                issues.append(Issue(
                    i, "warning",
                    f"节点 ID 含连字符: '{hid}'",
                    f"建议改为驼峰: '{hid.replace('-', '')}' 或下划线"
                ))

        # --- 规则 9: 括号匹配 ---
        for open_ch, close_ch, name in [("[", "]", "方括号"), ("(", ")", "圆括号"), ("{", "}", "花括号")]:
            # 简单计数（不处理字符串内的括号，但能捕获明显错误）
            opens = line.count(open_ch)
            closes = line.count(close_ch)
            if opens != closes:
                # 排除 subgraph / style / classDef 等行
                if not any(line.startswith(kw) for kw in ("style ", "classDef ", "linkStyle ", "class ", "%%")):
                    issues.append(Issue(
                        i, "warning",
                        f"{name}不匹配: '{open_ch}' 出现 {opens} 次, '{close_ch}' 出现 {closes} 次",
                        "检查该行括号是否配对"
                    ))

        # --- 规则 10: 引号匹配 ---
        quote_count = line.count('"')
        if quote_count % 2 != 0:
            issues.append(Issue(
                i, "error",
                f"引号不匹配: 发现 {quote_count} 个双引号（应为偶数）",
                "检查该行引号是否配对"
            ))

    # --- 规则 11: subgraph 未关闭 ---
    if subgraph_depth > 0:
        issues.append(Issue(
            len(lines), "error",
            f"有 {subgraph_depth} 个 subgraph 未关闭",
            "确保每个 subgraph 都有对应的 end"
        ))
    elif subgraph_depth < 0:
        issues.append(Issue(
            len(lines), "error",
            f"多余的 end: 比 subgraph 多 {-subgraph_depth} 个",
            "删除多余的 end"
        ))

    return issues


# ─── 远程 API 校验 ──────────────────────────────────────────

def check_remote(code: str) -> tuple[bool | None, str]:
    """
    调用 mermaid.ink API 做真实渲染校验。
    返回 (is_valid, error_message).
    is_valid: True = 渲染通过; False = 渲染失败(语法错误); None = 网络不可用,跳过远程校验
    """
    try:
        # 简单 base64url 编码（mermaid.ink 支持）
        encoded = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii")
        url = f"{MERMAID_INK_URL}{encoded}"

        req = Request(url, method="GET")
        req.add_header("User-Agent", "Mozilla/5.0 MermaidValidator/1.0")

        with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            if resp.status == 200:
                content = resp.read()
                # 检查返回内容是否为有效图片（SVG 或 PNG，通常 >100 字节）
                if len(content) > 100:
                    return True, ""
                else:
                    return False, "API 返回内容过短，可能渲染失败"

    except HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        if e.code == 400:
            return False, f"语法错误（mermaid.ink 返回 400）: {body}"
        return False, f"HTTP {e.code}: {body}"
    except URLError as e:
        return None, f"网络错误: {e.reason}"
    except Exception as e:
        return False, f"未知错误: {e}"

    return False, "未知错误"


def render_image(code: str, as_svg: bool = False, width: int | None = None) -> bytes | None:
    """
    从 mermaid.ink 下载渲染好的图片字节。
    成功返回图片 bytes,失败(网络/渲染错误)返回 None。
    width 仅对 PNG 生效(None = mermaid.ink 默认视口宽度;SVG 是矢量不需要)。
    """
    prefix = MERMAID_INK_SVG_URL if as_svg else MERMAID_INK_URL
    encoded = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii")
    if as_svg or width is None:
        url = f"{prefix}{encoded}" + ("" if as_svg else "?type=png")
    else:
        url = f"{prefix}{encoded}?type=png&width={width}"
    try:
        req = Request(url, method="GET")
        req.add_header("User-Agent", "Mozilla/5.0 MermaidValidator/1.0")
        with urlopen(req, timeout=REQUEST_TIMEOUT * 3) as resp:
            if resp.status == 200:
                content = resp.read()
                if len(content) > 100:
                    return content
    except Exception:
        return None
    return None


def _png_size(data: bytes) -> tuple[int, int]:
    """从 PNG 字节流解析 (宽, 高);非 PNG 返回 (0, 0)。"""
    import struct
    if len(data) > 24 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    return 0, 0


def export_png_auto_width(code: str) -> tuple[bytes | None, str]:
    """
    PNG 导出 + 推荐宽度算法(两次请求探测):
    1. 先按 mermaid.ink 默认视口渲染一次,读出"自然宽度"(按内容紧凑布局的实际宽度);
    2. 推荐宽度 = clamp(自然宽度 × 2, AUTO_WIDTH_MIN, AUTO_WIDTH_MAX) —— 放大两倍
       让缩放查看时文字依然清晰,小图不低于 MIN,超大图封顶 MAX;
    3. 推荐值 > 自然宽度才二次请求,否则直接用首次结果(小图不浪费)。
    返回 (图片字节, 说明文字)。
    """
    img0 = render_image(code, as_svg=False, width=None)
    if img0 is None:
        return None, ""
    w0, _ = _png_size(img0)
    if w0 == 0:
        return img0, "宽度探测失败,使用默认渲染"
    # 大图 ×2 保证缩放可读(下限 2400);小图 ×3 逐步放大即可,不强行拉到 2400(避免字号失比)
    lower = min(AUTO_WIDTH_MIN, max(w0 * 3, 1200))
    recommended = max(lower, min(AUTO_WIDTH_MAX, w0 * 2))
    if recommended <= w0:
        return img0, f"自然宽度 {w0}px 已足够清晰,无需放大"
    img1 = render_image(code, as_svg=False, width=recommended)
    if img1 is None:
        return img0, f"自然宽度 {w0}px;放大请求失败,回退默认渲染"
    return img1, f"自然宽度 {w0}px → 自动放大至 {recommended}px"


# ─── 格式化输出 ─────────────────────────────────────────────

RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"


def format_issues(issues: list[Issue]) -> str:
    lines = []
    for iss in issues:
        color = RED if iss.severity == "error" else YELLOW
        tag = "ERROR" if iss.severity == "error" else "WARN"
        lines.append(f"  {color}[{tag}]{RESET} 行 {iss.line}: {iss.message}")
        lines.append(f"         💡 {iss.suggestion}")
    return "\n".join(lines)


# ─── 主流程 ─────────────────────────────────────────────────

def validate_block(code: str, index: int, multi: bool = False,
                   export_dir: str | None = None, as_svg: bool = False,
                   stem: str = "diagram", width: int | None = None) -> bool:
    """校验单个 mermaid 代码块。返回 True 表示通过。"""
    block_label = f"代码块 {index + 1}"
    print(f"\n{'─' * 50}")
    print(f"  {BOLD}校验 {block_label}{RESET}")
    print(f"{'─' * 50}")

    # 显示代码预览（前 8 行）
    preview_lines = code.strip().split("\n")[:8]
    preview = "\n".join(f"    {ln}" for ln in preview_lines)
    if len(code.strip().split("\n")) > 8:
        preview += "\n    ..."
    print(f"\n{preview}\n")

    # Step 1: 本地预检
    local_issues = check_local(code)
    errors = [i for i in local_issues if i.severity == "error"]
    warnings = [i for i in local_issues if i.severity == "warning"]

    if errors:
        print(f"  {RED}✗ 本地预检发现 {len(errors)} 个错误, {len(warnings)} 个警告:{RESET}")
        print(format_issues(local_issues))
        print()
        return False

    if warnings:
        print(f"  {YELLOW}⚠ 本地预检发现 {len(warnings)} 个警告:{RESET}")
        print(format_issues(warnings))
        print()

    if not errors:
        print(f"  {GREEN}✓ 本地预检通过{RESET}{'（有警告）' if warnings else ''}")

    # Step 2: 远程 API 校验
    print(f"  ⏳ 调用 mermaid.ink API 校验...")
    is_valid, err_msg = check_remote(code)

    if is_valid is True:
        print(f"  {GREEN}✓ 远程渲染校验通过{RESET}")
    elif is_valid is None:
        print(f"  {YELLOW}⚠ 无法连接 mermaid.ink，跳过远程校验（仅本地预检，本地已通过）{RESET}")
        print(f"    {err_msg}")
    else:
        print(f"  {RED}✗ 远程渲染校验失败:{RESET}")
        print(f"    {err_msg}")
        return False

    # Step 3: 导出渲染图(仅在 --export 且远程校验通过时)
    if export_dir is not None:
        if is_valid is not True:
            print(f"  {YELLOW}⚠ 跳过导出: 远程渲染不可用{RESET}")
        else:
            note = ""
            if as_svg:
                img = render_image(code, as_svg=True)
            elif width is not None:
                img = render_image(code, as_svg=False, width=width)
                note = f"width={width}px(手动)"
            else:
                img, note = export_png_auto_width(code)
            if img is None:
                print(f"  {YELLOW}⚠ 图片下载失败,跳过导出{RESET}")
            else:
                ext = "svg" if as_svg else "png"
                suffix = f"-{index + 1}" if multi else ""
                out_path = Path(export_dir)
                out_path.mkdir(parents=True, exist_ok=True)
                file_path = out_path / f"{stem}{suffix}.{ext}"
                file_path.write_bytes(img)
                note_part = f" [{note}]" if note else ""
                print(f"  {GREEN}⬇ 已导出: {file_path} ({len(img)} bytes){note_part}{RESET}")

    return True


def main():
    # 确保 stdout/stderr 使用 utf-8 编码（Windows 兼容）
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    if sys.stderr.encoding != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

    input_text = ""

    args = sys.argv[1:]

    # 解析导出参数(不影响原有输入解析)
    export_dir: str | None = None
    as_svg = False
    export_width: int | None = None  # None = auto(自动推荐宽度)
    rest: list[str] = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--export":
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                export_dir = args[i + 1]
                i += 2
            else:
                export_dir = "."
                i += 1
        elif a == "--svg":
            as_svg = True
            i += 1
        elif a == "--width" and i + 1 < len(args):
            v = args[i + 1]
            if v.lower() == "auto":
                export_width = None
                i += 2
            elif v.isdigit():
                export_width = int(v)
                i += 2
            else:
                rest.append(a)
                i += 1
        else:
            rest.append(a)
            i += 1
    args = rest

    stem = "diagram"
    if "--code" in args:
        idx = args.index("--code")
        input_text = " ".join(args[idx + 1:])
    elif "--help" in args or "-h" in args:
        print(__doc__)
        sys.exit(0)
    elif args and not args[0].startswith("-"):
        try:
            with open(args[0], "r", encoding="utf-8") as f:
                input_text = f.read()
        except FileNotFoundError:
            print(f"文件不存在: {args[0]}", file=sys.stderr)
            sys.exit(2)
        stem = Path(args[0]).stem
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()

    if not input_text.strip():
        print("用法:")
        print('  python validate_mermaid.py <file.md>')
        print('  python validate_mermaid.py --code "flowchart TD\\n  A-->B"')
        print('  echo "flowchart TD" | python validate_mermaid.py')
        sys.exit(2)

    blocks = extract_mermaid_blocks(input_text)

    if not blocks:
        print("未找到 mermaid 代码块。", file=sys.stderr)
        sys.exit(2)

    print(f"\n{BOLD}🔍 Mermaid 语法校验器{RESET}")
    print(f"   找到 {len(blocks)} 个代码块\n")

    all_valid = True
    for i, block in enumerate(blocks):
        if not validate_block(block, i, multi=len(blocks) > 1,
                              export_dir=export_dir, as_svg=as_svg, stem=stem,
                              width=export_width):
            all_valid = False

    print(f"\n{'═' * 50}")
    if all_valid:
        print(f"  {GREEN}{BOLD}✅ 全部校验通过！{RESET}")
        sys.exit(0)
    else:
        print(f"  {RED}{BOLD}❌ 校验未通过，请修复上述错误后重试{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
