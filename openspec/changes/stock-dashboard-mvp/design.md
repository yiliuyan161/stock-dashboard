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

- **[Tushare API 限频]** → Tushare 免费版每分钟有限频，单用户看盘场景不会触发
- **[无缓存导致重复请求]** → 日线数据不变，可后续加 ETag/Last-Modified 头优化
- **[CDN 依赖]** → lightweight-charts CDN 不可用时页面空白，可后续下载到本地
- **[Tushare token 暴露]** → token 只在后端环境变量，不暴露给前端
