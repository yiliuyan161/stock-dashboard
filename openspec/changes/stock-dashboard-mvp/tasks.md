## 1. 后端 API

- [x] 1.1 创建 backend/requirements.txt（fastapi, uvicorn, tushare）
- [x] 1.2 创建 backend/main.py — FastAPI 应用骨架 + 静态文件挂载
- [x] 1.3 实现 GET /api/stocks — 股票列表搜索（Tushare stock_basic）
- [x] 1.4 实现 GET /api/daily — 日线数据（Tushare daily）
- [x] 1.5 实现 MA 计算（MA5/MA10/MA20）附加到日线响应

## 2. 前端页面

- [x] 2.1 创建 frontend/index.html — 基础布局 + 深色主题 + CDN 引入 lightweight-charts
- [x] 2.2 实现股票搜索框 + 下拉列表（fetch /api/stocks）
- [x] 2.3 实现 K线图 + 成交量柱状图渲染（fetch /api/daily）
- [x] 2.4 实现 MA 均线叠加（MA5/MA10/MA20）
- [x] 2.5 实现股票切换（搜索选择 → 重新加载图表数据）

## 3. Docker 部署

- [x] 3.1 创建 backend/Dockerfile（Python slim + requirements + 源码）
- [x] 3.2 创建 docker-compose.yml（单容器 + 环境变量 + Traefik 网络）
- [x] 3.3 创建 ~/apps/traefik/dynamic/stock-dashboard.yml — Traefik 动态路由
- [x] 3.4 创建 .env.example（TUSHARE_TOKEN 占位）

## 4. 开发态验证

- [x] 4.1 用 dev-serve.sh 启动开发态，验证 tradingview.dev.test.icopy.site 可访问
- [x] 4.2 验证股票搜索功能
- [x] 4.3 验证 K线图渲染 + MA 均线
- [x] 4.4 验证股票切换

## 5. 生产部署

- [x] 5.1 docker compose up -d 构建并启动容器
- [x] 5.2 验证 Traefik 路由 tradingview.test.icopy.site（本地 Traefik 200 OK）
- [x] 5.3 验证 API 和页面功能完整（Playwright 自动化测试通过）
- [x] 5.4 提交并推送到 GitHub
