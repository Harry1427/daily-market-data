import yfinance as yf
from datetime import datetime
import pytz

# 한국 시간 설정
tz = pytz.timezone('Asia/Seoul')
today = datetime.now(tz).strftime('%Y-%m-%d')

# 수집할 지표 목록 (이미지 속 모든 항목)
tickers = {
    "나스닥": "^IXIC", "S&P500": "^GSPC", "다우": "^DJI", "러셀2000": "^RUT",
    "필라델피아반도체": "^SOX", "코스피200": "^KS200", 
    "달러인덱스": "DX-Y.NYB", "원달러환율": "KRW=X",
    "미국채10년": "^TNX", "미국채2년": "^2YR", "미국채30년": "^30YR",
    "WTI유": "CL=F", "브렌트유": "BZ=F", "금": "GC=F", "은": "SI=F", "구리": "HG=F",
    "옥수수": "ZC=F", "밀": "ZW=F", "대두": "ZS=F"
}

content = f"---\ndate: {today}\n---\n# 📅 {today} 시장 브리핑\n\n"
content += "| 지표 | 현재가 | 등락율 |\n| :--- | :--- | :--- |\n"

for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol).history(period="2d")
        if len(data) < 2: continue
        
        current_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2]
        change_pct = ((current_price - prev_price) / prev_price) * 100
        
        # 옵시디언에서 인식할 수 있게 메타데이터(속성)로도 저장
        content += f"| {name} | {current_price:,.2f} | {change_pct:+.2f}% |\n"
        # 개별 속성 저장 (그래프용)
        content = content.replace("---", f"---\n{name}: {current_price:.2f}\ndate: {today}", 1)
    except:
        pass

with open(f"{today}.md", "w", encoding="utf-8") as f:
    f.write(content)
