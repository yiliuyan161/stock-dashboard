# daily-data-api Specification

## Purpose
TBD - created by archiving change stock-dashboard-mvp. Update Purpose after archive.
## Requirements
### Requirement: 日线数据 API
后端 SHALL 提供 REST API 返回指定股票的日线数据。

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
后端 SHALL 提供股票列表搜索接口。

#### Scenario: 搜索股票
- **WHEN** GET /api/stocks?q=平安
- **THEN** 返回 JSON 数组，每条含 ts_code/name 字段，匹配名称或代码

#### Scenario: 无搜索关键词
- **WHEN** GET /api/stocks
- **THEN** 返回全量 A股列表（ts_code + name）

### Requirement: 静态文件服务
后端 SHALL 同时提供前端静态文件服务。

#### Scenario: 访问首页
- **WHEN** GET /
- **THEN** 返回 index.html

#### Scenario: 访问不存在的路径
- **WHEN** GET /nonexistent
- **THEN** 返回 404

