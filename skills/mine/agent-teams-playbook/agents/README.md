# Agents 专业智能体库

> 本目录中的 `.md` 文件是子代理 prompt 参考库，不是任何平台自动加载或直接执行的原生 agent 配置。使用时先通过本 README 匹配角色，再只读取对应角色文件，将相关行为说明注入子代理创建调用的 prompt。

本目录包含专业智能体的行为模式参考文件，用于多代理协作编排中的角色匹配（SKILL.md 阶段2）。

## 快速查找表

### 按任务类型查找

> SKILL.md 要求：第一列为"智能体名称"，根据任务类型快速定位

| 智能体名称 | 适用任务类型 | 配置文件 |
|-----------|-------------|---------|
| backend-architect | 后端系统设计、API开发、数据库架构、后端安全 | backend-architect.md |
| frontend-architect | UI组件开发、前端架构、无障碍访问(WCAG)、响应式设计 | frontend-architect.md |
| devops-architect | CI/CD管道、基础设施自动化、监控日志、可观测性 | devops-architect.md |
| system-architect | 系统架构设计、可扩展性、技术选型、依赖管理 | system-architect.md |
| planner | 实现计划制定、复杂功能分解、技术实施规划、依赖分析 | planner.md |
| python-expert | Python开发、SOLID原则、类型提示、异步编程、clean architecture | python-expert.md |
| performance-engineer | 性能优化、瓶颈分析、前端性能、后端性能 | performance-engineer.md |
| quality-engineer | 测试策略、测试框架、边界情况检测、QA、覆盖率检查 | quality-engineer.md |
| tdd-guide | 测试驱动开发、测试先行、红绿重构循环、TDD强制 | tdd-guide.md |
| e2e-runner | E2E测试、端到端测试、Playwright/Agent Browser、flaky test管理 | e2e-runner.md |
| refactoring-expert | 代码重构、技术债务减少、SOLID应用、代码质量提升 | refactoring-expert.md |
| security-engineer | 安全漏洞评估、威胁建模、安全合规、OWASP | security-engineer.md |
| build-error-resolver | 构建错误修复、TypeScript类型错误、编译问题快速修复 | build-error-resolver.md |
| go-build-resolver | Go构建错误修复、go vet问题、linter警告修复 | go-build-resolver.md |
| requirements-analyst | 需求分析、PRD撰写、用户故事、验收标准 | requirements-analyst.md |
| root-cause-analyst | 问题调查、Bug分析、根本原因定位、日志分析 | root-cause-analyst.md |
| database-reviewer | 数据库审查、PostgreSQL优化、查询性能、schema设计、RLS安全 | database-reviewer.md |
| repo-index | 代码库研究、上下文压缩、仓库索引 | repo-index.md |
| deep-research-agent | 复杂问题深度调研、跨领域信息综合、证据链分析、多跳推理任务 | deep-research-agent.md |
| deep-research | 快速信息查询、外部资料收集、简单事实核实、轻量调研 | deep-research.md |
| technical-writer | 技术文档编写、API文档、教程、用户指南 | technical-writer.md |
| learning-guide | 编程概念讲解、代码原理说明、教程文档编写、学习路径设计 | learning-guide.md |
| socratic-mentor | Clean Code原则探索、设计模式发现、苏格拉底式提问引导、自主思考培养 | socratic-mentor.md |
| self-review | 实施后验证、质量把关、验收检查、反思总结 | self-review.md |
| python-reviewer | Python代码审查、PEP 8合规、Pythonic模式、类型提示审查 | python-reviewer.md |
| go-reviewer | Go代码审查、Go惯用模式、并发模式、错误处理审查 | go-reviewer.md |
| business-panel-experts | 商业战略分析、市场分析、竞争策略 | business-panel-experts.md |
| pm-agent | 知识库管理、PDCA循环、文档维护、经验教训 | pm-agent.md |
| code-reviewer | 代码审查专家、安全审查、React/Node.js模式、技术审查清单 | code-reviewer.md |
| refactor-cleaner | 死代码清理、重复代码消除、依赖清理、knip、depcheck | refactor-cleaner.md |

### 按关键词快速匹配

> SKILL.md 要求：第一列为"智能体名称"，根据关键词快速定位

| 智能体名称 | 匹配关键词 | 配置文件 |
|-----------|-----------|---------|
| backend-architect | API、后端API、服务器、REST API、GraphQL | backend-architect.md |
| frontend-architect | 前端框架、组件库、用户界面、组件、响应式、WCAG、无障碍、React、Vue | frontend-architect.md |
| devops-architect | CI/CD、部署、监控、日志、Kubernetes、Docker、可观测性 | devops-architect.md |
| system-architect | 系统架构、微服务、可扩展性、技术选型、依赖 | system-architect.md |
| planner | 规划、实施计划、任务分解、依赖、风险、技术方案 | planner.md |
| python-expert | Python、SOLID、类型提示、异步、clean architecture、Pythonic | python-expert.md |
| performance-engineer | 系统性能、响应时间、性能优化、加载时间、瓶颈、Core Web Vitals | performance-engineer.md |
| quality-engineer | QA、测试策略、边界情况、覆盖率检查、自动化测试 | quality-engineer.md |
| tdd-guide | TDD、测试驱动、测试先行、红绿重构、单元测试、测试强制 | tdd-guide.md |
| e2e-runner | E2E、端到端测试、Playwright、Agent Browser、flaky、artifacts | e2e-runner.md |
| refactoring-expert | 代码重构、SOLID、技术债务、代码质量、复杂度、可维护性 | refactoring-expert.md |
| security-engineer | 代码安全、漏洞检测、OWASP、威胁、加密、合规 | security-engineer.md |
| build-error-resolver | 构建、TypeScript、类型错误、编译、快速修复 | build-error-resolver.md |
| go-build-resolver | Go构建、go vet、staticcheck、编译、模块、依赖 | go-build-resolver.md |
| requirements-analyst | PRD、用户需求、用户故事、验收标准、利益相关者 | requirements-analyst.md |
| root-cause-analyst | Bug、调试、根因分析、日志、调查、证据 | root-cause-analyst.md |
| database-reviewer | PostgreSQL、SQL、查询、索引、RLS、schema、查询性能 | database-reviewer.md |
| repo-index | 仓库索引、索引、上下文、压缩、结构分析 | repo-index.md |
| deep-research-agent | 综合研究、多跳推理、自适应策略、深度调查、复杂分析、证据链 | deep-research-agent.md |
| deep-research | 信息查询、信息收集、资料查找、外部知识、轻量调研 | deep-research.md |
| technical-writer | 技术文档、说明、API文档、用户指南、技术写作 | technical-writer.md |
| learning-guide | 编程教学、概念讲解、教程编写、示例演示、渐进学习、直接指导 | learning-guide.md |
| socratic-mentor | 苏格拉底式、提问引导、发现学习、Clean Code、设计模式探索、原则发现 | socratic-mentor.md |
| self-review | 验收、验证、质量把关、实施后检查、反思 | self-review.md |
| python-reviewer | Python、审查、PEP 8、Pythonic、类型提示、mypy、ruff | python-reviewer.md |
| go-reviewer | Go、审查、惯用、并发、错误、golangci-lint、staticcheck | go-reviewer.md |
| business-panel-experts | 商业模式、商业战略、市场、竞争、分析 | business-panel-experts.md |
| pm-agent | PDCA、知识管理、文档管理、经验教训 | pm-agent.md |
| code-reviewer | 代码审查、XSS、SQL注入、React、Next.js、Node.js、技术审查清单 | code-reviewer.md |
| refactor-cleaner | 死代码、重复代码、knip、depcheck、依赖清理、ts-prune | refactor-cleaner.md |

## 智能体分类

> SKILL.md 要求：包含"职责描述"列，用于兜底机制。添加"配置文件"列保持结构一致性。

### 工程类 (Engineering)

| 智能体名称 | 职责描述 | 配置文件 |
|-----------|---------|---------|
| backend-architect | 设计可靠的后端系统,专注API设计、数据库架构、安全性和容错性 | backend-architect.md |
| frontend-architect | 创建可访问、高性能的用户界面,专注用户体验和现代框架 | frontend-architect.md |
| devops-architect | 自动化基础设施和部署流程,专注可靠性和可观测性 | devops-architect.md |
| system-architect | 设计可扩展的系统架构,专注可维护性和长期技术决策 | system-architect.md |

### 分析类 (Analysis)

| 智能体名称 | 职责描述 | 配置文件 |
|-----------|---------|---------|
| deep-research-agent | 自适应深度调研专家,通过多跳推理和证据链分析进行复杂信息综合 | deep-research-agent.md |
| deep-research | 快速信息收集代理,提供外部资料查询和轻量化调研支持 | deep-research.md |
| requirements-analyst | 将模糊的项目想法转化为具体规格说明 | requirements-analyst.md |
| root-cause-analyst | 系统性调查复杂问题,通过证据分析和假设测试定位根本原因 | root-cause-analyst.md |
| repo-index | 仓库索引和代码库简报助手,压缩上下文以提高token效率 | repo-index.md |

### 质量类 (Quality)

| 智能体名称 | 职责描述 | 配置文件 |
|-----------|---------|---------|
| performance-engineer | 通过测量驱动分析和瓶颈消除来优化系统性能 | performance-engineer.md |
| quality-engineer | 通过全面的测试策略和系统的边界情况检测确保软件质量 | quality-engineer.md |
| refactoring-expert | 通过系统性重构和清洁代码原则提高代码质量并减少技术债务 | refactoring-expert.md |
| refactor-cleaner | 死代码清理和整合专家,识别并移除死代码、重复代码和未使用的导出,运行分析工具(knip, depcheck, ts-prune)安全清理 | refactor-cleaner.md |
| security-engineer | 识别安全漏洞并确保符合安全标准和最佳实践 | security-engineer.md |
| self-review | 实施后验证和反思伙伴,确认生产就绪并捕获经验教训 | self-review.md |
| code-reviewer | 专家级代码审查专家,主动审查代码质量、安全性和可维护性,包含详细的安全、React/Next.js、Node.js检查清单 | code-reviewer.md |

### 沟通/教育类 (Communication)

| 智能体名称 | 职责描述 | 配置文件 |
|-----------|---------|---------|
| learning-guide | 直接指导式教学专家,通过概念解释和代码示例帮助理解编程原理 | learning-guide.md |
| socratic-mentor | 引导发现式导师,通过苏格拉底提问和原则探索培养自主思考能力 | socratic-mentor.md |
| technical-writer | 创建清晰、全面的技术文档,针对特定受众优化可用性和可访问性 | technical-writer.md |

### 业务类 (Business)

| 智能体名称 | 职责描述 | 配置文件 |
|-----------|---------|---------|
| business-panel-experts | 多专家商业战略小组,整合9位商业大师(Christensen、Porter、Drucker等)的思维框架 | business-panel-experts.md |

### 专业类 (Specialized)

| 智能体名称 | 职责描述 | 配置文件 |
|-----------|---------|---------|
| python-expert | 提供遵循SOLID原则和现代最佳实践的生产级、安全、高性能Python代码 | python-expert.md |
| python-reviewer | Python代码审查专家,专注于PEP 8合规、Pythonic惯用模式、类型提示和安全审查 | python-reviewer.md |
| go-reviewer | Go代码审查专家,专注于Go惯用模式、并发模式、错误处理和性能审查 | go-reviewer.md |
| database-reviewer | PostgreSQL数据库专家,专注于查询优化、schema设计、安全和性能,集成Supabase最佳实践 | database-reviewer.md |

### 工具类 (Tools)

| 智能体名称 | 职责描述 | 配置文件 |
|-----------|---------|---------|
| tdd-guide | 测试驱动开发专家,强制测试先行工作流,确保80%+测试覆盖率 | tdd-guide.md |
| build-error-resolver | 构建和TypeScript错误修复专家,快速修复构建/类型错误,最小化改动 | build-error-resolver.md |
| go-build-resolver | Go构建和编译错误修复专家,修复go vet、staticcheck和linter警告 | go-build-resolver.md |
| e2e-runner | 端到端测试专家,使用Agent Browser(优先)和Playwright,管理测试旅程和flaky tests | e2e-runner.md |

### 规划类 (Planning)

| 智能体名称 | 职责描述 | 配置文件 |
|-----------|---------|---------|
| planner | 实现规划专家,创建详细的技术实施计划,分解复杂功能,识别依赖和风险 | planner.md |

### 元类 (Meta)

| 智能体名称 | 职责描述 | 配置文件 |
|-----------|---------|---------|
| pm-agent | 项目管理代理,执行PDCA循环,维护知识库,记录成功模式和错误教训 | pm-agent.md |

## 更新速查表的规则 

### 添加新智能体

当新增智能体配置文件（`.md`文件）时，需同步更新以下表格：

**步骤1：更新"按任务类型查找"表**
```markdown
| 智能体名称 | 适用任务类型 | 配置文件 |
| new-agent | 任务类型1、任务类型2 | new-agent.md |
```

**步骤2：更新"按关键词快速匹配"表**
```markdown
| 智能体名称 | 匹配关键词 | 配置文件 |
| new-agent | 关键词1、关键词2、关键词3 | new-agent.md |
```

**步骤3：更新"智能体分类"表**
```markdown
| 智能体名称 | 职责描述 | 配置文件 |
| new-agent | 简洁的职责描述 | new-agent.md |
```
## 📝 版本信息

- **版本**: 与 SKILL.md v7.0 同步
- **更新日期**: 2026-06-13
- **智能体总数**: 30个
