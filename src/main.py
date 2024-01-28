from fastapi import FastAPI, Query
from pytrends.request import TrendReq
from googletrans import Translator
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
 return {"Success!!"}

class TrendItem(BaseModel):
    rank: int
    content: dict

@app.get("/trends")
async def get_trends():
    # PyTrendsオブジェクトを作成
    pytrends = TrendReq(hl='en-US', tz=360)

    # 日本のトレンド検索キーワードを取得
    trends = pytrends.trending_searches(pn='japan')

    # トレンドアイテムのリストを作成
    trend_items = []
    for key, value in trends[0].items():
        rank = int(key)
        content = {"ja": value, "en": Translator().translate(value, dest='en').text}
        trend_item = TrendItem(rank=rank, content=content)
        trend_items.append(trend_item)

    return {"trends": trend_items}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)