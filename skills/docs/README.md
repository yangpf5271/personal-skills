# Documents & Content Skills

生成和处理文档、办公文件、文字内容的技能组。从 Word/PDF/PPT/Excel 到文章写作和文字润色。

## Skills

| Skill | 用途 |
|---|---|
| [docx](./docx/) | Word 文档处理：创建/读取/编辑 .docx（含目录、页眉、修订、批注） |
| [pdf](./pdf/) | PDF 处理：提取文本/表格、创建、合并/拆分、填表单 |
| [pptx](./pptx/) | PPT 演示文稿：创建/编辑/分析 .pptx（含版式、批注、演讲者备注） |
| [xlsx](./xlsx/) | Excel 表格：创建/分析/编辑 .xlsx（公式、格式、数据分析、可视化、重算） |
| [office](./office/) | Office 综合操作：Excel/Word/PowerPoint/Google Workspace 公式、格式、自动化 |
| [content-research-writer](./content-research-writer/) | 研究驱动的内容写作搭档：调研+引用+逐段反馈，写博客/教程/案例 |
| [humanizer-zh](./humanizer-zh/) | 中文文本人性化：去除 AI 生成痕迹，让文字更自然像人写 |
| [hv-analysis](./hv-analysis/) | 横纵分析法深度研究：纵轴追踪生命历程，横轴系统性对比，产 PDF 研究报告 |
| [tender-bid-writer](./tender-bid-writer/) | 标书自动编写与排版：招标需求+大纲 → 带目录/五级标题/图表/页码的正式 .docx 投标文件 |

## 推荐搭配

- **写一篇带来源的长文**：`content-research-writer`（调研+起草）→ `humanizer-zh`（去 AI 味润色）→ `docx`（导出 Word）
- **深度研究**：`hv-analysis`（横纵分析 + PDF 报告）
- **招投标**：`tender-bid-writer`（招标文件+大纲 → 正式技术标 .docx）
- **生成办公文档**：按格式选 `docx`/`pdf`/`pptx`/`xlsx`；`office` 提供跨套件的综合操作指南
- **数据分析报告**：`xlsx`（处理数据）→ `content-research-writer`（写分析）→ `pdf`（出报告）

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill docx --skill pdf --skill pptx --skill xlsx --skill office --skill content-research-writer --skill humanizer-zh --skill hv-analysis --skill tender-bid-writer
```
