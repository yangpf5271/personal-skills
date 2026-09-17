# Creative Video Skills（创意视频制作）

基于 HyperFrames（HTML + GSAP）的创意视频制作套件，与上游 [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) marketplace 版同步（2026-09-18）。核心技能构成路由图：`hyperframes` 是强制总入口，按任务路由到专项技能；工作流技能（pr-to-video 等）内部以相对路径引用核心技能，**建议整组安装**。

## Skills

### 核心（路由图主干）

| Skill | 用途 |
|---|---|
| [hyperframes](./hyperframes/) | 视频合成总入口：任何视频/动画/动效请求先读这个，按任务路由到专项技能 |
| [hyperframes-core](./hyperframes-core/) | 合成契约：项目结构、`data-*` 时序属性、clip/tracks/子合成、确定性渲染规则与校验 |
| [hyperframes-cli](./hyperframes-cli/) | 视频命令行工具：init/add/catalog/capture/lint/check/snapshot/compare/render/cloud/lambda 全流程 |
| [hyperframes-animation](./hyperframes-animation/) | 动画知识库：原子运动规则、多阶段场景蓝图、转场，7 种运行时适配器（GSAP/Lottie/Three.js/Anime.js/CSS/WAAPI/FLIP） |
| [hyperframes-creative](./hyperframes-creative/) | 创意导演：设计规范（frame.md/design.md）、调色板、排版、旁白、节拍规划、品牌风格 |
| [hyperframes-keyframes](./hyperframes-keyframes/) | 关键帧运镜：punch-in/out、缩放重构图、Ken Burns、镜头交接等 seek-safe 2D/3D 关键帧 |
| [hyperframes-audio](./hyperframes-audio/) | 音频混音：淡入淡出、交叉淡化、增益自动化、闪避（voiceover carve）、EQ/压缩/限制器 |

### 媒体与字幕

| Skill | 用途 |
|---|---|
| [media-use](./media-use/) | 媒体素材中枢：BGM/SFX/图片/图标/logo/配音/调色 LUT 一站式解析与生成（TTS/音乐/去除背景） |
| [embedded-captions](./embedded-captions/) | 视频字幕：给口播视频加字幕/内嵌/特效字幕，35 风格目录，不动原始画面 |
| [hyperframes-registry](./hyperframes-registry/) | 注册表组件：搜索并接线 CRT 扫描线/故障/色差等现成视觉效果块，避免手搓 |

### 专项工作流

| Skill | 用途 |
|---|---|
| [general-video](./general-video/) | 通用视频合成：无专项工作流可用时的自定义合成编写/编辑（多场景、品牌片、蒙太奇、循环） |
| [faceless-explainer](./faceless-explainer/) | 无人出镜讲解视频：文章/主题 → 逐场景生成视觉的讲解片 |
| [motion-graphics](./motion-graphics/) | 动态图形：动态字体、数字滚动、数据可视化、logo 定版、字幕条、动画地图 |
| [product-launch-video](./product-launch-video/) | 产品发布视频：产品/营销 URL 或 brief → 发布/促销/演示片 |
| [pr-to-video](./pr-to-video/) | PR 讲解视频：GitHub PR diff → 代码变更讲解片（changelog/功能揭示/修复走查） |
| [music-to-video](./music-to-video/) | 音乐驱动视频：音轨 → 卡点视频（歌词视频/幻灯片/动感促销），音乐驱动全部节奏 |
| [talking-head-recut](./talking-head-recut/) | 口播视频包装：访谈/播客视频加动态图形叠卡（标题/字幕条/数据卡），16:9/9:16/4:5 |
| [slideshow](./slideshow/) | 幻灯片与演示：演示文稿/_pitch deck_/交互式 deck，分片显示、分支跳转、演讲者模式 |
| [remotion-to-hyperframes](./remotion-to-hyperframes/) | Remotion 迁移：把现有 Remotion (React) 合成单向移植为 HyperFrames HTML |
| [figma](./figma/) | Figma 导入：渲染资产/品牌 token/组件/分镜段落导入合成，帧读作状态而非幻灯片 |

> ⚠️ 本组全部 skill 均未注册在 plugin.json，安装时在 "Other" 中可选。整组安装约 19MB。

## 推荐搭配

- **视频制作全流程**：`hyperframes`（总入口路由）→ `hyperframes-core`（合成契约）→ `hyperframes-creative`（创意/节拍）→ `hyperframes-animation`（动效）→ `media-use`（素材/配音）→ `hyperframes-cli`（预览渲染）
- **带口播的宣传片**：`product-launch-video` → `media-use`（TTS）→ `embedded-captions`（字幕）
- **讲解/知识类**：`faceless-explainer` 或 `motion-graphics` → `hyperframes-audio`（混音）
- **每周更新**：`pr-to-video`（changelog 片）或 `music-to-video`（卡点片）

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill hyperframes --skill hyperframes-core --skill hyperframes-cli --skill hyperframes-animation --skill hyperframes-creative --skill hyperframes-keyframes --skill hyperframes-audio --skill media-use --skill embedded-captions --skill hyperframes-registry --skill general-video --skill faceless-explainer --skill motion-graphics --skill product-launch-video --skill pr-to-video --skill music-to-video --skill talking-head-recut --skill slideshow --skill remotion-to-hyperframes --skill figma
```
