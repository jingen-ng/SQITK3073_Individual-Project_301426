import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#Question1
stocks={
    "Maybank":"1155.KL",
    "Nestle":"4707.KL",
    "TNB":"5347.KL",
    "Petronas Dagangan":"5681.KL",
    "Panasonic":"3719.KL"
}

stock_list = list(stocks.values())
end_date = datetime.today()
start_date = end_date - timedelta(days=30)

data=yf.download(stock_list, start=start_date, end=end_date, auto_adjust=True)

def analyse_stock(ticker):
    close_prices = data["Close"][ticker].dropna()
    
    yesterday_price = float(close_prices.iloc[-2])
    today_price = float(close_prices.iloc[-1])
    daily_return = today_price - yesterday_price
    shares = 1000 // yesterday_price
    estimated_return = daily_return * shares
    return_percentage = (estimated_return / 1000) * 100

    return [
        ticker,
        round(yesterday_price, 2),
        round(today_price, 2),
        round(daily_return, 2),
        int(shares),
        round(estimated_return, 2),
        round(return_percentage, 2)
    ]

results=[]

for ticker in stock_list:
    results.append(analyse_stock(ticker))

columns=[
    "Ticker", 
    "Yesterday Closing Price",
    "Today Closing Price",
    "Daily Return",
    "Shares Purchaseable",
    "Estimated Total Return",
    "Return Percentage"
]

df=pd.DataFrame(results, columns=columns)
print(df)


#Question2
col_summary = ['Ticker','Yesterday Closing Price','Today Closing Price','Estimated Total Return','Return Percentage']

portfolio_summary=df.loc[:,col_summary]
print(portfolio_summary)

def classify_performance(return_pct):
    if return_pct < 0:
        return "Negative Return"
    elif return_pct <= 2:
        return "Moderate Return"
    else:
        return "High Return"
  
df['Performance Category'] = df['Return Percentage'].apply(classify_performance)
grouped = df.groupby('Performance Category')['Estimated Total Return'].mean()
print(df[['Ticker', 'Return Percentage', 'Performance Category']])
print(grouped)


#Question3
colors=['#ffd700', '#63513d', '#ffa500', '#48d1cc', '#4169e1']
stock_names=list(stocks.keys())

plt.figure(figsize=(12,6))
for i,ticker in enumerate(stock_list):
    close=data['Close'][ticker].dropna()
    plt.plot(close.index,close, label=ticker+" ("+stock_names[i]+")", color=colors[i])

plt.title('Closing Price Trend')
plt.xlabel('Date')
plt.ylabel('Closing Price (RM)')
plt.legend()
plt.show()

plt.figure(figsize=(10,6))
bars = plt.bar(df['Ticker'], df['Return Percentage'], color=colors)
plt.legend(bars, stock_names, title="Stocks", fontsize=8,title_fontsize=9)
plt.title('Return Percentage Comparison')
plt.xlabel('Stocks')
plt.ylabel('Return Percentage (%)')
plt.axhline(y=0,color='black', linewidth=0.8, linestyle='--',label='_nolegend_')
plt.tight_layout()
plt.show()
