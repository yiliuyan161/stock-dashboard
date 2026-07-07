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
