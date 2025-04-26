from fastapi import FastAPI
from pytrends.request import TrendReq
from googletrans import Translator
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

app = FastAPI()

SECRET_PATH = '/etc/secrets/.env'
if os.path.exists(SECRET_PATH):
    load_dotenv(SECRET_PATH)
else:
    load_dotenv()

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

@app.get("/domains/value")
async def get_domain_value(word: str):
    try:
        client = genai.Client(api_key=genai_api_key)
        prompt = f"""「{word}」
            このキーワードのドメインとしての価値を測定してください。
            下記の3つの要素の答えだけをそれぞれ半角空白を入れて答えてください。

            1.価値の将来性は何点か。
            条件:0~100の間の整数で答えてください。100の方が価値があるとします。単位は必要無いです。

            2.市場価値を日本円で換算した時、何円になるか。
            条件:単位は必要無いです。桁数に応じて「,」を入れてください。

            3.関連するキーワードは何か。
            条件:日本語で答えてください。5つ答えてください。それぞれのキーワードの間に「/」を入れてください。

            回答の例:
            80 100,000 関連A/関連B/関連C/関連D/関連E"""
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

        # レスポンスから結果を抽出
        result = response.text.strip().split('\n')[0]  # 最初の行を取得
        score, value, keywords_str = result.split(' ')
        keywords = keywords_str.split('/')

        return {
            "score": int(score),
            "value": value,
            "keywords": keywords
        }

    except Exception as e:
        # エラーログを出力（オプション）
        print(f"Error fetching trends: {e}")
        return {"score": "", "value": "", "keywords": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)