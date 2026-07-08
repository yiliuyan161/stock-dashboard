## ADDED Requirements

### Requirement: Docker Compose 部署
应用 SHALL 通过 Docker Compose 部署，复用现有 Traefik 基础设施。

#### Scenario: 启动服务
- **WHEN** docker compose up -d
- **THEN** 容器启动，FastAPI 监听 8000 端口，Traefik 路由 tradingview.test.icopy.site → 容器:8000

#### Scenario: 停止服务
- **WHEN** docker compose down
- **THEN** 容器停止，Traefik 路由移除

### Requirement: Traefik 动态路由
SHALL 通过 Traefik file provider 配置动态路由，无需重启 Traefik。

#### Scenario: 添加路由
- **WHEN** 在 ~/apps/traefik/dynamic/ 创建 stock-dashboard.yml
- **THEN** Traefik 自动检测并路由 tradingview.test.icopy.site → host.docker.internal:8000

### Requirement: 开发态 fast-loop
开发态 SHALL 使用 dev-serve.sh 启动本地服务。

#### Scenario: 开发态启动
- **WHEN** dev-serve.sh stock-dashboard 8000 "uvicorn backend.main:app --host 0.0.0.0 --port 8000"
- **THEN** tradingview.dev.test.icopy.site 可访问，代码修改后刷新即生效

### Requirement: 环境变量管理
Tushare token SHALL 通过环境变量注入，不硬编码。

#### Scenario: 生产环境
- **WHEN** docker compose up
- **THEN** TUSHARE_TOKEN 从 .env 文件注入容器环境变量
