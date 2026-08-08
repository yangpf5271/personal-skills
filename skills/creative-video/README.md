# Creative Video Skills（创意视频制作）

使用 HTML + GSAP + HyperFrames 制作创意视频：从分镜规划、动效设计到视频合成与渲染的完整链路。

## Skills

| Skill | 用途 |
|---|---|
| [video-spec-builder](./video-spec-builder/) | 分镜规划：生成 video-spec.md，确定每页讲什么、怎么动、何时切换 |
| [video-agency-roles](./video-agency-roles/) | 制作链路审查：7 角色逐层检查——选题/事实/技术/视觉/审美/节奏/平台包装 |
| [motion-design](./motion-design/) | 动效设计：判断每个镜头该用什么运动，缓动/时长/编排/性能/无障碍 |
| [hyperframes](./hyperframes/) | 视频合成与动效编排：HTML 驱动，GSAP 动画，字幕/旁白/音频响应/转场/视觉样式 |
| [hyperframes-cli](./hyperframes-cli/) | HyperFrames CLI：init/lint/inspect/preview/render/transcribe/tts |
| [hyperframes-media](./hyperframes-media/) | 素材预处理：TTS 旁白、Whisper 转录、背景移除（u2net） |
| [gsap](./gsap/) | GSAP 动画参考：核心补间方法（core）、时间线编排（timeline）、性能优化（performance） |

## 推荐搭配

- **视频制作全流程**：`video-spec-builder`（分镜规划）→ `video-agency-roles`（链路审查）→ `motion-design`（动效决策）→ `hyperframes`（合成编排）→ `gsap`（动画参考）→ `hyperframes-cli`（预览渲染）
- **带音频的视频**：`hyperframes-media`（TTS/转录）→ `hyperframes`（字幕同步）
- **新手入门**：`hyperframes-cli`（init 脚手架）→ `hyperframes`（写 HTML）→ `gsap`（参考 API）

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill video-spec-builder --skill video-agency-roles --skill motion-design --skill hyperframes --skill hyperframes-cli --skill hyperframes-media --skill gsap
```
