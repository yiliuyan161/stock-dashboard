# Comet Design Handoff

- Change: stock-dashboard-mvp
- Phase: design
- Mode: compact
- Context hash: badec16afb6f62b22ae33c730ae7c4bcaf8afc524d27625b233bf0fdf750ba4b

Generated-by: comet-handoff.sh

OpenSpec remains the canonical capability spec. This handoff is a deterministic, source-traceable context pack, not an agent-authored summary.

## openspec/changes/stock-dashboard-mvp/proposal.md

- Source: openspec/changes/stock-dashboard-mvp/proposal.md
- Lines: 1-31
- SHA256: 26f25a836578f61de671e6645ea4c6214a13ec0951cb1c4815aa081cb87b419e

```md
## Why

需要一个公网可访问的 A股日线看盘工具，用于快速查看任意 A股的日线 K线图和成交量。现有工具（同花顺/东方财富）需要客户端，且无法自定义展示。基于 TradingView Lightweight Charts + Tushare SDK 可以快速构建一个轻量级 Web 看盘应用。

## What Changes

- 新建 Python FastAPI 后端，提供日线数据 API（Tushare SDK 数据源）
- 新建单页 HTML 前端，使用 TradingView Lightweight Charts 渲染 K线图
- 支持股票搜索（Tushare stock_basic 接口获取 A股列表）
- 日K线展示：OHLC 蜡烛图 + 成交量柱状图 + MA 均线叠加
- 深色主题，响应式布局
- Docker Compose 部署 + Traefik 动态路由到 tradingview.test.icopy.site
- 开发态 fast-loop：tradingview.dev.test.icopy.site

## Capabilities

### New Capabilities
- `daily-data-api`: FastAPI 后端，提供日线数据和股票列表 JSON API
- `chart-frontend`: 单页 HTML 前端，TradingView Lightweight Charts 渲染 K线图
- `docker-deploy`: Docker Compose + Traefik 部署配置

### Modified Capabilities
<!-- 无现有 capability 需要修改 -->

## Impact

- 新建项目：~/repos/stock-dashboard/
- 依赖：FastAPI + uvicorn（Python）、TradingView Lightweight Charts（CDN）、Tushare SDK（已安装）
- 部署：新增 ~/apps/stock-dashboard/ Docker Compose 配置 + Traefik 动态路由
- 环境变量：TUSHARE_TOKEN（已存在于 hermes/.env）
- 公网访问：tradingview.test.icopy.site
```

## openspec/changes/stock-dashboard-mvp/design.md

- Source: openspec/changes/stock-dashboard-mvp/design.md
- Lines: 1-84
- SHA256: 6100166bb91d6dab6e49b9383f634f5ba4404d931e1e36690307d04e21ebb34e

[TRUNCATED]

```md
---
comet_change: stock-dashboard-mvp
role: technical-design
canonical_spec: openspec
---

## Context

全新项目，从零构建 A股日线看盘 Web 应用。现有基础设施：Traefik 反向代理 + frp 内网穿透 + Docker，域名 `*.test.icopy.site` 已配置。Tushare SDK v1.4.29 已安装，token 已存在于环境变量中。TradingView Lightweight Charts 通过 CDN 引入，无需 npm 依赖。

## Goals / Non-Goals

**Goals:**
- 公网可访问的日线 K线图看盘工具
- 支持任意 A股搜索和切换
- OHLC 蜡烛图 + 成交量 + MA 均线
- 深色主题，响应式布局
- 开发态 fast-loop + 生产态 Docker 部署

**Non-Goals:**
- 实时行情（日线 = 收盘后 Tushare 数据）
- 分钟级/Tick 数据
- 交易功能
- 用户认证
- 复杂指标库（第一版只 MA5/MA10/MA20）
- 本地数据缓存（第一版直接调 Tushare API）

## Decisions

### 1. 后端：FastAPI + uvicorn

**选择：** FastAPI
**理由：** 轻量、自带 OpenAPI 文档、异步支持好、与 Tushare SDK（同步）兼容
**替代方案：** Flask（无自带文档）、纯静态 JSON 文件（无法动态查询）

### 2. 前端：单页 HTML + CDN 引入 Lightweight Charts

**选择：** 单个 index.html，CDN 引入 lightweight-charts
**理由：** 零构建步骤，改代码刷新即生效，符合 fast-loop 哲学
**替代方案：** Vue/React SPA（过度工程，看盘工具不需要框架）

### 3. 数据源：Tushare SDK 直接调用

**选择：** 每次请求直接调 `tushare.pro_api()`，不做本地缓存
**理由：** 日线数据量小（单只股票 ~5000 条），Tushare 响应快（<1s），简单优先
**替代方案：** SQLite 缓存 + 定时刷新（第一版不需要，后续可加）

### 4. API 设计

```
GET /api/stocks?q=<keyword>          → 股票列表（搜索）
GET /api/daily?ts_code=000001.SZ     → 日线数据 [{date,open,high,low,close,vol}, ...]
```

**理由：** 两个端点覆盖全部需求，RESTful 风格，前端 fetch 即可

### 5. 部署：Docker Compose + Traefik 动态路由

**选择：** 单容器（FastAPI + 静态文件），Traefik file provider 路由
**理由：** 复用现有 Traefik 基础设施，无需额外反向代理
**配置：** `~/apps/stock-dashboard/docker-compose.yml` + `~/apps/traefik/dynamic/stock-dashboard.yml`

### 6. 项目结构

```
stock-dashboard/
├── backend/
│   ├── main.py          # FastAPI 应用
│   ├── requirements.txt # fastapi, uvicorn, tushare
│   └── Dockerfile
├── frontend/
│   └── index.html       # 单页应用
├── docker-compose.yml   # 容器编排
└── openspec/            # 规划工件
```

**理由：** 前后端分离目录但同容器部署，简单且部署方便

## Risks / Trade-offs

```

Full source: openspec/changes/stock-dashboard-mvp/design.md

## openspec/changes/stock-dashboard-mvp/tasks.md

- Source: openspec/changes/stock-dashboard-mvp/tasks.md
- Lines: 1-36
- SHA256: 643032f87c458da02a4e7748c251d28bb6589b10a8275d9ffdd631fc58ba182d

```md
## 1. 后端 API

- [ ] 1.1 创建 backend/requirements.txt（fastapi, uvicorn, tushare）
- [ ] 1.2 创建 backend/main.py — FastAPI 应用骨架 + 静态文件挂载
- [ ] 1.3 实现 GET /api/stocks — 股票列表搜索（Tushare stock_basic）
- [ ] 1.4 实现 GET /api/daily — 日线数据（Tushare daily）
- [ ] 1.5 实现 MA 计算（MA5/MA10/MA20）附加到日线响应

## 2. 前端页面

- [ ] 2.1 创建 frontend/index.html — 基础布局 + 深色主题 + CDN 引入 lightweight-charts
- [ ] 2.2 实现股票搜索框 + 下拉列表（fetch /api/stocks）
- [ ] 2.3 实现 K线图 + 成交量柱状图渲染（fetch /api/daily）
- [ ] 2.4 实现 MA 均线叠加（MA5/MA10/MA20）
- [ ] 2.5 实现股票切换（搜索选择 → 重新加载图表数据）

## 3. Docker 部署

- [ ] 3.1 创建 backend/Dockerfile（Python slim + requirements + 源码）
- [ ] 3.2 创建 docker-compose.yml（单容器 + 环境变量 + Traefik 网络）
- [ ] 3.3 创建 ~/apps/traefik/dynamic/stock-dashboard.yml — Traefik 动态路由
- [ ] 3.4 创建 .env.example（TUSHARE_TOKEN 占位）

## 4. 开发态验证

- [ ] 4.1 用 dev-serve.sh 启动开发态，验证 tradingview.dev.test.icopy.site 可访问
- [ ] 4.2 验证股票搜索功能
- [ ] 4.3 验证 K线图渲染 + MA 均线
- [ ] 4.4 验证股票切换

## 5. 生产部署

- [ ] 5.1 docker compose up -d 构建并启动容器
- [ ] 5.2 验证 tradingview.test.icopy.site 公网可访问
- [ ] 5.3 验证 API 和页面功能完整
- [ ] 5.4 提交并推送到 GitHub
```

## openspec/changes/stock-dashboard-mvp/specs/chart-frontend/spec.md

- Source: openspec/changes/stock-dashboard-mvp/specs/chart-frontend/spec.md
- Lines: 1-37
- SHA256: d75b1fa1965fa4374cecbae1ad7dc2dff71dc7c3a1098fcb0c768baa1a9c277f

```md
## ADDED Requirements

### Requirement: K线图展示
前端使用 TradingView Lightweight Charts 渲染日线 K线图。

#### Scenario: 加载股票日线
- **WHEN** 用户选择一只股票
- **THEN** 页面显示 OHLC 蜡烛图 + 成交量柱状图（pane 2），深色主题

#### Scenario: 切换股票
- **WHEN** 用户搜索并选择另一只股票
- **THEN** 图表数据更新，无需刷新页面

### Requirement: MA 均线叠加
K线图上叠加移动平均线。

#### Scenario: 显示 MA 均线
- **WHEN** 日线图加载完成
- **THEN** 图表上显示 MA5（黄色）、MA10（紫色）、MA20（蓝色）三条均线

### Requirement: 股票搜索
前端提供股票搜索功能。

#### Scenario: 搜索股票
- **WHEN** 用户在搜索框输入关键词
- **THEN** 显示匹配的股票列表（代码 + 名称），点击后加载该股票日线

### Requirement: 响应式布局
页面适配不同屏幕尺寸。

#### Scenario: 桌面端
- **WHEN** 浏览器宽度 > 768px
- **THEN** 图表占满屏幕，搜索框在顶部

#### Scenario: 移动端
- **WHEN** 浏览器宽度 <= 768px
- **THEN** 图表自适应宽度，搜索框可折叠
```

## openspec/changes/stock-dashboard-mvp/specs/daily-data-api/spec.md

- Source: openspec/changes/stock-dashboard-mvp/specs/daily-data-api/spec.md
- Lines: 1-38
- SHA256: ede8a670861232d8eadea98114002090c0f7b6b18ac681c14a6290ad380971e8

```md
## ADDED Requirements

### Requirement: 日线数据 API
后端提供 REST API 返回指定股票的日线数据。

#### Scenario: 获取日线数据
- **WHEN** GET /api/daily?ts_code=000001.SZ
- **THEN** 返回 JSON 数组，每条含 date/open/high/low/close/vol 字段，按日期升序排列

#### Scenario: 无效股票代码
- **WHEN** GET /api/daily?ts_code=INVALID
- **THEN** 返回 404，JSON body 含 error 字段

#### Scenario: 缺少 ts_code 参数
- **WHEN** GET /api/daily
- **THEN** 返回 422，提示缺少必填参数

### Requirement: 股票搜索 API
后端提供股票列表搜索接口。

#### Scenario: 搜索股票
- **WHEN** GET /api/stocks?q=平安
- **THEN** 返回 JSON 数组，每条含 ts_code/name 字段，匹配名称或代码

#### Scenario: 无搜索关键词
- **WHEN** GET /api/stocks
- **THEN** 返回全量 A股列表（ts_code + name）

### Requirement: 静态文件服务
后端同时提供前端静态文件服务。

#### Scenario: 访问首页
- **WHEN** GET /
- **THEN** 返回 index.html

#### Scenario: 访问不存在的路径
- **WHEN** GET /nonexistent
- **THEN** 返回 404
```

## openspec/changes/stock-dashboard-mvp/specs/docker-deploy/spec.md

- Source: openspec/changes/stock-dashboard-mvp/specs/docker-deploy/spec.md
- Lines: 1-33
- SHA256: 19693c8c20eb4108f126a67ba1c9666c3d438dc1ebb9ca7431eebb746ee67f22

```md
## ADDED Requirements

### Requirement: Docker Compose 部署
应用通过 Docker Compose 部署，复用现有 Traefik 基础设施。

#### Scenario: 启动服务
- **WHEN** docker compose up -d
- **THEN** 容器启动，FastAPI 监听 8000 端口，Traefik 路由 tradingview.test.icopy.site → 容器:8000

#### Scenario: 停止服务
- **WHEN** docker compose down
- **THEN** 容器停止，Traefik 路由移除

### Requirement: Traefik 动态路由
通过 Traefik file provider 配置动态路由，无需重启 Traefik。

#### Scenario: 添加路由
- **WHEN** 在 ~/apps/traefik/dynamic/ 创建 stock-dashboard.yml
- **THEN** Traefik 自动检测并路由 tradingview.test.icopy.site → host.docker.internal:8000

### Requirement: 开发态 fast-loop
开发态使用 dev-serve.sh 启动本地服务。

#### Scenario: 开发态启动
- **WHEN** dev-serve.sh stock-dashboard 8000 "uvicorn backend.main:app --host 0.0.0.0 --port 8000"
- **THEN** tradingview.dev.test.icopy.site 可访问，代码修改后刷新即生效

### Requirement: 环境变量管理
Tushare token 通过环境变量注入，不硬编码。

#### Scenario: 生产环境
- **WHEN** docker compose up
- **THEN** TUSHARE_TOKEN 从 .env 文件注入容器环境变量
```

