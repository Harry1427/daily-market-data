import yfinance as yf
from datetime import datetime
import pytz

# 한국 시간 기준 오늘 날짜 가져오기
tz = pytz.timezone('Asia/Seoul')
today = datetime.now(tz).strftime('%Y-%m-%d')

# 수집할 지표들
tickers = {
    "나스닥": "^IXIC", "S&P500": "^GSPC", "다우": "^DJI",
    "국채10년": "^TNX", "WTI유": "CL=F", "금": "GC=F"
}

content = f"## 📅 {today} 시장 브리핑\n\n"
for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol).history(period="1d")
        price = data['Close'].iloc[-1]
        change = data['Close'].iloc[-1] - data['Open'].iloc[-1]
        pct = (change / data['Open'].iloc[-1]) * 100
        content += f"- **{name}**: {price:,.2f} ({pct:+.2f}%)\n"
    except:
        pass

# 파일 저장하기
with open(f"{today}.md", "w", encoding="utf-8") as f:
    f.write(content)
