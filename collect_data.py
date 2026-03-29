import yfinance as yf
from datetime import datetime
import pytz

# 한국 시간 설정
tz = pytz.timezone('Asia/Seoul')
today = datetime.now(tz).strftime('%Y-%m-%d')

# 수집할 지표 목록
tickers = {
    "나스닥": "^IXIC", "S&P500": "^GSPC", "다우": "^DJI", "러셀2000": "^RUT",
    "필라델피아반도체": "^SOX", "코스피200": "^KS200", 
    "달러인덱스": "DX-Y.NYB", "원달러환율": "KRW=X",
    "미국채10년": "^TNX", "미국채2년": "^2YR", "미국채30년": "^30YR",
    "WTI유": "CL=F", "브렌트유": "BZ=F", "금": "GC=F", "은": "SI=F", "구리": "HG=F",
    "옥수수": "ZC=F", "밀": "ZW=F", "대두": "ZS=F"
}

properties = f"---\ndate: {today}\n"
table_content = f"# 📅 {today} 시장 브리핑\n\n| 지표 | 현재가 | 등락율 |\n| :--- | :--- | :--- |\n"

for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol).history(period="2d")
        if len(data) < 2: continue
        
        current_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2]
        change_pct = ((current_price - prev_price) / prev_price) * 100
        
        properties += f"{name}: {current_price:.2f}\n"
        table_content += f"| **{name}** | {current_price:,.2f} | {change_pct:+.2f}% |\n"
    except:
        pass

# 최종 텍스트 합치기 및 저장
final_content = properties + "---\n\n" + table_content

with open(f"{today}.md", "w", encoding="utf-8") as f:
    f.write(final_content)
