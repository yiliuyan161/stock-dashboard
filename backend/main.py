"""Stock Dashboard API — A股日线看盘后端"""
import os
from pathlib import Path

import tushare as ts
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Stock Dashboard API", version="1.0.0")

# Tushare 初始化
TUSHARE_TOKEN = os.environ.get("TUSHARE_TOKEN", "")
if TUSHARE_TOKEN:
    ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api() if TUSHARE_TOKEN else None

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


def calc_ma(closes: list[float], period: int) -> list[float | None]:
    """计算移动平均线，前 period-1 个返回 None"""
    result = []
    for i in range(len(closes)):
        if i < period - 1:
            result.append(None)
        else:
            result.append(round(sum(closes[i - period + 1 : i + 1]) / period, 2))
    return result


@app.get("/api/stocks")
async def get_stocks(q: str = Query(default="", description="搜索关键词")):
    """股票列表搜索 — Tushare stock_basic"""
    if not pro:
        return JSONResponse(status_code=503, content={"error": "TUSHARE_TOKEN not configured"})
    try:
        df = pro.stock_basic(exchange="", list_status="L", fields="ts_code,symbol,name,area,industry")
        if q:
            mask = df["name"].str.contains(q, case=False, na=False) | df["ts_code"].str.contains(
                q.upper(), case=False, na=False
            )
            df = df[mask]
        rows = df.head(50).to_dict("records")
        return [{"ts_code": r["ts_code"], "name": r["name"]} for r in rows]
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/daily")
async def get_daily(ts_code: str = Query(..., description="股票代码，如 000001.SZ")):
    """日线数据 — Tushare daily，含 MA5/MA10/MA20"""
    if not pro:
        return JSONResponse(status_code=503, content={"error": "TUSHARE_TOKEN not configured"})
    try:
        df = pro.daily(ts_code=ts_code, start_date="20200101")
        if df.empty:
            return JSONResponse(status_code=404, content={"error": f"No data for {ts_code}"})
        df = df.sort_values("trade_date")
        closes = df["close"].tolist()
        ma5 = calc_ma(closes, 5)
        ma10 = calc_ma(closes, 10)
        ma20 = calc_ma(closes, 20)
        result = []
        for i, row in df.iterrows():
            result.append(
                {
                    "date": row["trade_date"],
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "vol": float(row["vol"]),
                    "ma5": ma5[list(df.index).index(i)],
                    "ma10": ma10[list(df.index).index(i)],
                    "ma20": ma20[list(df.index).index(i)],
                }
            )
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/", response_class=HTMLResponse)
async def index():
    """返回前端首页"""
    html_file = FRONTEND_DIR / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Frontend not found</h1>", status_code=404)


# 静态文件（如果需要额外的 JS/CSS）
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
