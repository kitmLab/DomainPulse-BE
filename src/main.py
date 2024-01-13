from fastapi import FastAPI, Query
from pytrends.request import TrendReq
from googletrans import Translator

app = FastAPI()

@app.get("/")
async def root():
 return {"Success!!"}

@app.get("/trends")
async def get_trends(lang: str = Query(default="jp", description="Language: jp or en")):
    # PyTrendsオブジェクトを作成
    pytrends = TrendReq(hl='en-US', tz=360)

    # 日本のトレンド検索キーワードを取得
    trends = pytrends.trending_searches(pn='japan')

    # クエリパラメータで指定された言語に応じて処理を行う
    if lang == "jp":
        return trends
    elif lang == "en":
        # Googletransを使用して日本語から英語に翻訳
        translator = Translator()
        english_trends = {str(i): {str(j): translator.translate(keyword, dest='en').text for j, keyword in trends.items()} for i, trends in trends.items()}
        return english_trends
    else:
        return {"error": "Invalid language. Please use 'jp' or 'en'."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)