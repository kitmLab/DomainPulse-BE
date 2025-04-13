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
    try:
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

    except Exception as e:
        # エラーログを出力（オプション）
        print(f"Error fetching trends: {e}")

        # 代替としてのダミーデータを返す
        dummy_trends = [
            TrendItem(
                rank=1,
                content={
                    "ja": "生成AI",
                    "en": "Generative AI"
                }
            ),
            TrendItem(
                rank=2,
                content={
                    "ja": "量子コンピューティング",
                    "en": "Quantum Computing"
                }
            ),
            TrendItem(
                rank=3,
                content={
                    "ja": "持続可能な都市開発",
                    "en": "Sustainable Urban Development"
                }
            ),
            TrendItem(
                rank=4,
                content={
                    "ja": "パーソナライズド医療",
                    "en": "Personalized Medicine"
                }
            ),
            TrendItem(
                rank=5,
                content={
                    "ja": "脱炭素社会",
                    "en": "Decarbonized Society"
                }
            ),
            TrendItem(
                rank=6,
                content={
                    "ja": "高齢者テクノロジー",
                    "en": "Elderly Care Technology"
                }
            ),
            TrendItem(
                rank=7,
                content={
                    "ja": "宇宙産業",
                    "en": "Space Industry"
                }
            ),
            TrendItem(
                rank=8,
                content={
                    "ja": "デジタルヘルスケア",
                    "en": "Digital Healthcare"
                }
            ),
            TrendItem(
                rank=9,
                content={
                    "ja": "再生可能エネルギー",
                    "en": "Renewable Energy"
                }
            ),
            TrendItem(
                rank=10,
                content={
                    "ja": "自律型モビリティ",
                    "en": "Autonomous Mobility"
                }
            )
        ]

        return {"trends": dummy_trends}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)