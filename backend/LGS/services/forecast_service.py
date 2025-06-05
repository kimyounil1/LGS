from datetime import datetime
import yfinance as yf
import feedparser
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from LGS.schemas.forecast import ForecastResponse, PricePoint
import nltk

nltk.download("vader_lexicon")

def compute_rsi(s, period=14):
    delta = s.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def forecast_stock_logic(ticker: str = "TSLA") -> ForecastResponse:
    # 주가 수집
    finance = yf.Ticker(ticker).history(period="6mo", interval="1d")
    df_price = finance[["Close"]].rename(columns={"Close": "price"}).reset_index()
    df_price["date"] = pd.to_datetime(df_price["Date"]).dt.date

    # 뉴스 수집 및 감성 분석
    rss_url = f"https://news.google.com/rss/search?q={ticker}+when:7d&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    entries = [{"title": e.title, "published": datetime(*e.published_parsed[:6])} for e in feed.entries]
    news_df = pd.DataFrame(entries)
    news_df["date"] = pd.to_datetime(news_df["published"]).dt.date
    sia = SentimentIntensityAnalyzer()
    news_df["compound"] = news_df["title"].apply(lambda x: sia.polarity_scores(x)["compound"])
    sentiment_df = news_df.groupby("date")["compound"].mean().reset_index()
    sentiment_df.columns = ["date", "sentiment"]

    # 병합 및 지표 추가
    df = pd.merge(df_price, sentiment_df, on="date", how="left").fillna(0)
    df["ma_3"] = df["price"].rolling(3).mean()
    df["ma_7"] = df["price"].rolling(7).mean()
    df["sentiment_ma"] = df["sentiment"].rolling(3).mean().fillna(0)
    df["rsi"] = compute_rsi(df["price"])
    df = df.fillna(method="bfill").set_index("date")

    # 스케일링 및 입력 구성
    features = ["price", "sentiment_ma", "ma_3", "ma_7", "rsi"]
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[features])
    SEQ_LEN = 7
    X = np.array([scaled[i - SEQ_LEN:i] for i in range(SEQ_LEN, len(scaled))])
    y = np.array([scaled[i, 0] for i in range(SEQ_LEN, len(scaled))])

    # 모델 정의 및 학습
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(SEQ_LEN, X.shape[2])),
        Dropout(0.2),
        LSTM(32),
        Dropout(0.2),
        Dense(1, activation="linear")
    ])
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=10, batch_size=16, verbose=0)

    # 예측
    last_7 = scaled[-SEQ_LEN:].copy()
    future_scaled = []
    for _ in range(3):
        pred = model.predict(last_7.reshape(1, SEQ_LEN, X.shape[2]), verbose=0)[0][0]
        new_input = np.array([[pred, *last_7[-1, 1:]]])
        future_scaled.append(pred)
        last_7 = np.concatenate((last_7[1:], new_input), axis=0)

    # 결과 처리
    pred_prices = (np.array(future_scaled) - scaler.min_[0]) / scaler.scale_[0]
    today_price = df["price"].iloc[-1]
    forecast_dates = pd.date_range(start=pd.to_datetime(df.index[-1]) + pd.Timedelta(days=1), periods=3)
    signal = "BUY" if pred_prices[-1] > today_price * 1.01 else ("SELL" if pred_prices[-1] < today_price * 0.99 else "HOLD")
    summary = f"Sentiment-adjusted forecast suggests a {signal} signal."

    # 응답 포맷
    historical = [
        PricePoint(date=str(d), price=round(p, 2))
        for d, p in zip(df.index[-SEQ_LEN:], df["price"].values[-SEQ_LEN:])
    ]
    forecast = [
        PricePoint(date=d.strftime("%Y-%m-%d"), price=round(p, 2))
        for d, p in zip(forecast_dates, pred_prices)
    ]

    return ForecastResponse(
        ticker=ticker,
        today=round(today_price, 2),
        historical=historical,
        forecast=forecast,
        signal=signal,
        summary=summary
    )
