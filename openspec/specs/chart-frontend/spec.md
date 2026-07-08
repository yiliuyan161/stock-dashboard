# chart-frontend Specification

## Purpose
TBD - created by archiving change stock-dashboard-mvp. Update Purpose after archive.
## Requirements
### Requirement: K线图展示
前端 SHALL 使用 TradingView Lightweight Charts 渲染日线 K线图。

#### Scenario: 加载股票日线
- **WHEN** 用户选择一只股票
- **THEN** 页面显示 OHLC 蜡烛图 + 成交量柱状图（pane 2），深色主题

#### Scenario: 切换股票
- **WHEN** 用户搜索并选择另一只股票
- **THEN** 图表数据更新，无需刷新页面

### Requirement: MA 均线叠加
K线图上 SHALL 叠加移动平均线。

#### Scenario: 显示 MA 均线
- **WHEN** 日线图加载完成
- **THEN** 图表上显示 MA5（黄色）、MA10（紫色）、MA20（蓝色）三条均线

### Requirement: 股票搜索
前端 SHALL 提供股票搜索功能。

#### Scenario: 搜索股票
- **WHEN** 用户在搜索框输入关键词
- **THEN** 显示匹配的股票列表（代码 + 名称），点击后加载该股票日线

### Requirement: 响应式布局
页面 SHALL 适配不同屏幕尺寸。

#### Scenario: 桌面端
- **WHEN** 浏览器宽度 > 768px
- **THEN** 图表占满屏幕，搜索框在顶部

#### Scenario: 移动端
- **WHEN** 浏览器宽度 <= 768px
- **THEN** 图表自适应宽度，搜索框可折叠

