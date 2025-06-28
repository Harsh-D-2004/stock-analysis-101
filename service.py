import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def get_stock(stock_name):

    end = datetime.today()

    start = end - timedelta(days=365 * 8)
    df = yf.download(stock_name, start=start, end=end)
    df = df.dropna()
    df["Daily Return"] = df["Close"].pct_change()
    df["Positive Day"] = df["Daily Return"] > 0
    df["Weekday"] = df.index.day_name()
    return df

def analyze_day_bias(df, label, years=None, months=None):

    end = datetime.today()
    
    if years:
        from_date = end - timedelta(days=365 * years)
    elif months:
        from_date = end - timedelta(days=30 * months)
    else:
        return None

    df_filtered = df[df.index >= from_date]

    total_days = df_filtered.groupby("Weekday").size()
    pos_days = df_filtered[df_filtered["Positive Day"]].groupby("Weekday").size()

    summary = pd.DataFrame({
        f"{label}_Positive_Days": pos_days,
        f"{label}_Total_Days": total_days
    }).fillna(0)

    summary[f"{label}_Bias%"] = (summary[f"{label}_Positive_Days"] / summary[f"{label}_Total_Days"]) * 100
    summary[f"{label}_Total%"] = (summary[f"{label}_Total_Days"] / summary[f"{label}_Total_Days"].sum()) * 100
    summary = summary.round(2)

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    summary = summary.reindex(weekdays)

    total_trading_days = df_filtered.shape[0]
    total_positive_days = df_filtered["Positive Day"].sum()
    overall_bias = round((total_positive_days / total_trading_days) * 100, 2)

    return summary, total_trading_days, total_positive_days, overall_bias

def get_stock_analysis(stock_name):

    df = get_stock(stock_name)

    periods = [
    ("8yr", {"years": 8}),
    ("5yr", {"years": 5}),
    ("3yr", {"years": 3}),
    ("2yr", {"years": 2}),
    ("1yr", {"years": 1}),
    ("6mo", {"months": 6})
    ]

    all_summaries = []

    for label, params in periods:
        summary, total_days, pos_days, bias_pct = analyze_day_bias(df, label, **params)
        all_summaries.append(summary)
    
    final_df = pd.concat(all_summaries, axis=1)
    final_df = final_df.to_string()
    return final_df

def get_current_stock_details(stock_name):

    ticker = yf.Ticker(stock_name)
    data = ticker.history(period="1d")  # Gets today's data

    if data.empty:
        return {"error": "No data available for this ticker."}

    current_info = {
        "symbol": stock_name,
        "open": round(data["Open"].iloc[0], 2),
        "high": round(data["High"].iloc[0], 2),
        "low": round(data["Low"].iloc[0], 2),
        "close": round(data["Close"].iloc[0], 2),
        "volume": int(data["Volume"].iloc[0])
    }

    return current_info