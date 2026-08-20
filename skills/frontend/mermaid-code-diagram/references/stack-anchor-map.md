# Stack Anchor Map — 按技术栈的代码分析锚点

分析陌生项目时先识别栈,再按下表定位锚点。配合 SKILL.md 的 Analysis Strategy 使用。

## 1. 技术栈识别(读依赖清单,不猜)

| 信号文件 | 生态 | 框架线索(在依赖里 grep) |
|---|---|---|
| `pyproject.toml` / `requirements.txt` | Python | `fastapi`→FastAPI;`django`→Django;`flask`;`sqlalchemy` / `tortoise-orm` / `peewee`(ORM) |
| `package.json` | Node | `express` / `fastify`;`@nestjs/core`→NestJS;`next`→Next.js;`prisma` / `typeorm` / `drizzle-orm` / `mongoose`(ORM) |
| `pom.xml` / `build.gradle` | Java | `spring-boot-starter-web`→Spring Boot;`spring-cloud-gateway`;`mybatis` / `spring-boot-starter-data-jpa`(ORM) |
| `go.mod` | Go | `gin` / `echo` / `fiber`;`gorm` / `sqlx` / `sqlc` |
| `Cargo.toml` | Rust | `axum` / `actix-web`;`sqlx` / `sea-orm` / `diesel` |
| `*.csproj` / `*.sln` | .NET | `Microsoft.AspNetCore.*`;`EntityFrameworkCore` / `Npgsql.EntityFrameworkCore` |
| `composer.json` | PHP | `laravel/framework` / `symfony/*`;`doctrine/orm` |
| `Gemfile` | Ruby | `rails`;`activerecord` |
| `mix.exs` | Elixir | `phoenix`;`ecto` |

## 2. 锚点表(识别栈后按行读)

| Stack | 入口 | 路由(Routes) | 数据模型(Data models) | 服务层(Service) | 异步/事件 | 配置 |
|---|---|---|---|---|---|---|
| Python·FastAPI | `main.py` / `app.py` | `grep '@(app\|router)\.(get\|post\|put\|delete\|api_route)'` | `models.py`、`models/`;SQLAlchemy: `grep 'class.*\(Base\)'`;Tortoise: `grep 'class.*\(Model\)'` | `services/`、`use_cases/` | Celery: `tasks.py`、`grep '@(celery_app\|shared_task)'`;grep `kafka\|aio-pika\|pika` | `.env`、`settings.py`、`config.py` |
| Python·Django | `manage.py` + `settings.py` 的 `INSTALLED_APPS`(app 清单) | 各 app `urls.py` | 各 app `models.py` | `views.py`、`services.py` | `celery.py`;Channels: `consumers.py` | `settings.py` |
| Node·NestJS | `src/main.ts` | `grep '@Controller'`、`controllers/` | Prisma: `prisma/schema.prisma`;TypeORM: `*.entity.ts`;Drizzle: `src/db/schema.ts`;Mongoose: `*.schema.ts` | `grep '@Injectable'`、`services/` | `grep '@Processor'`(Bull);grep `kafkajs\|amqplib` | `.env`、`app.module.ts` |
| Node·Express | `server.*` / `index.*` | `routes/`;`grep '\.use(\|\.get(\|\.post('` | 同上 ORM 信号 | `services/`、`lib/` | `cron`、Bull 队列 | `.env` |
| Node·Next.js | `package.json` scripts + `app/`(或 `pages/`)目录树即路由 | 文件树:`app/**/page.tsx`、`route.ts`(API) | 同上 + server actions | `app/api/**`、`lib/` | — | `next.config.*`、`.env` |
| Java·Spring | `*Application.java` | `grep '@RestController\|@RequestMapping'` | JPA: `grep '@Entity'` + `*Repository.java`;MyBatis: `mapper/*.xml` | `grep '@Service'` | `grep '@KafkaListener\|@RabbitListener\|@Scheduled'` | `application.yml` / `application.properties` |
| Go | `cmd/*/main.go`、`main.go` | `grep '(gin\|echo\|fiber)\.(GET\|POST\|PUT\|DELETE)'` 或 `http.HandleFunc` | GORM: struct tag `gorm:"..."`;sqlc: `db/queries/` | `internal/service/`、`internal/` | grep `segmentio/kafka\|rabbitmq\|nsq`;goroutine+channel 模式 | `config.yaml`、env |
| Rust | `src/main.rs` | `grep '#\[get\|post\|route'`(axum/actix 宏) | sqlx: `migrations/` + `grep 'FromRow'`;sea-orm: `entity/` | `src/services/` 或 use-case 模块 | grep `lapin\|rdkafka` | `.env`、`config.toml` |
| .NET | `Program.cs` / `Startup.cs` | `Controllers/*.cs`(`[ApiController]`、`[Route]`) | EF Core: `Models/*.cs` + DbContext 的 `DbSet<>`;migrations: `Migrations/` | `Services/` | `BackgroundService` / `IHostedService`;MassTransit | `appsettings.json` |

## 3. 数据流向图的四锚点扫描(专用于 data flow)

数据流向图按数据的生命周期收集节点,四个锚点都有典型落点:

| 锚点 | 找什么 | 典型信号 |
|---|---|---|
| **入口** | 数据从哪进来 | 路由(锚点表 Routes 列)、MQ consumer、`@Scheduled`/cron 任务、文件导入接口 |
| **变换** | 谁在处理 | Service 层(锚点表 Service 列)、`grep 'transform\|process\|aggregate\|clean'` |
| **沉淀** | 落到哪里 | ORM 模型 + 迁移目录(`alembic/versions`、`prisma/migrations`、`db/migration` Flyway、`Migrations/`)、Redis 读写(`grep 'redis\|cache'`)、对象存储/ES |
| **出口** | 流向哪里 | 第三方 SDK 调用(`requests\|httpx` / `axios\|fetch` / `okhttp\|RestTemplate` / `Wire`),推送/导出/回调 `grep 'webhook\|export\|notify\|push'` |

箭头语义:入口→变换→沉淀为主干;沉淀→变换(回读)、变换→出口(旁路)用虚线;缓存读写标双向。

## 4. Monorepo 处理

- 信号:`pnpm-workspace.yaml` / `package.json` 的 `workspaces` / `turbo.json` / `nx.json`(JS);`settings.gradle` + 多 `build.gradle`(Java);多 `go.mod`(Go)
- 策略:**先画 app 间依赖图**(`apps/*/` 互相 import / Maven module 依赖),再对目标 app 深入;不要一上来平铺所有包
- 共享包(`packages/shared`、`common/`)在图中作为独立节点,标明被哪些 app 引用

## 5. 分析时排除(噪音目录与文件)

**依赖与构建产物**:`node_modules/` `bower_components/` `vendor/`(Go/PHP) `venv/` `.venv/` `env/` `target/`(Java/Rust) `build/` `dist/` `out/` `.next/` `.nuxt/` `.turbo/` `.gradle/` `*.egg-info/`

**缓存**:`__pycache__/` `.mypy_cache/` `.pytest_cache/` `.tox/` `coverage/` `.cache/`

**IDE / 系统 / VCS**:`.git/` `.idea/` `.vscode/` `.DS_Store`

**生成文件**:`*.min.*` `*.lock`(lock 文件只在识别依赖版本时按需查,不全读)

**操作提示**:glob 源码时按扩展名收窄(`**/*.py`、`**/*.ts`)已天然排除二进制;跨文件 grep 时用 `--exclude-dir=node_modules --exclude-dir=venv --exclude-dir=target --exclude-dir=dist --exclude-dir=__pycache__` 或先 `git ls-files`(只看受版本管理的文件,一步排除所有忽略项)。

`git ls-files` 是最省事的排除法——依赖、构建产物、缓存默认都不在版本管理里。

## 6. 按图类型的定向读(与锚点表配合)

| 图类型 | 读什么 |
|---|---|
| 架构图 | Routes 列 + Service 列 + 配置 → 服务边界与分层 |
| ER 图 | Data models 列 + 迁移目录(迁移比模型更能反映真实表结构) |
| 时序图 | 选一个 endpoint,追 handler → service → repository → 外部调用的完整链 |
| 数据流向 | §3 四锚点扫描 |
| 依赖图 | import / use 语句 + 构建文件的 module 依赖 |
