import yfinance as yf
from datetime import datetime
import pytz

# 한국 시간 기준 오늘 날짜 가져오기
tz = pytz.timezone('Asia/Seoul')
today = datetime.now(tz).strftime('%Y-%m-%d')

# 수집할 지표들 (이미지 속 모든 항목)
tickers = {
    "나스닥": "^IXIC", "S&P500": "^GSPC", "다우": "^DJI", "러셀2000": "^RUT",
    "코스피200야간선물": "KRW=X", # Yfinance에서 지원하는 가장 유사한 지표
    "미국채10년": "^TNX", "미국채2년": "^2YR", "미국채30년": "^30YR",
    "WTI유": "CL=F", "금": "GC=F", "은": "SI=F", "구리": "HG=F",
    "달러인덱스": "DX-Y.NYB"
}

content = f"## 📅 {today} 시장 브리핑\n\n"
content += "| 지표 | 종가 | 등락폭 | 등락률(%)\n"
content += "| :--- | :--- | :--- | :--- |\n"

for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol).history(period="1d")
        if data.empty: continue # 데이터가 없으면 건너뜀
        
        price = data['Close'].iloc[-1]
        change = price - data['Open'].iloc[-1]
        pct = (change / data['Open'].iloc[-1]) * 100
        content += f"| **{name}** | {price:,.2f} | {change:+,.2f} | {pct:+.2f}% |\n"
    except:
        pass

# 파일 저장하기 (옵시디언 호환 마크다운 파일)
with open(f"{today}.md", "w", encoding="utf-8") as f:
    f.write(content)
