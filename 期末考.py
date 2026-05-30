from datetime import datetime
import os
import pandas as pd
import yfinance as yf

# 設定要抓取的科技股代號
tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

# 設定抓取的時間（從今天算起往前抓一整年）
end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)

print("--- [1/3] 開始下載四大科技巨頭最新股價 ---")

company_list = []
company_name = ["APPLE", "GOOGLE", "MICROSOFT", "AMAZON"]

for stock, com_name in zip(tech_list, company_name):
    # 確保抓下來的資料格式乾淨，直接拉取單一 Ticker
    df_stock = yf.download(stock, start=start, end=end)

    if not df_stock.empty:
        # 🔥 核心修正：把多重索引扁平化，防止欄位變成 NaN 錯位
        if isinstance(df_stock.columns, pd.MultiIndex):
            df_stock.columns = df_stock.columns.get_level_values(0)

        df_stock = df_stock.reset_index()
        df_stock["company_name"] = com_name
        company_list.append(df_stock)
        print(f"-> {com_name} ({stock}) 下載成功，共 {len(df_stock)} 筆交易資料")
    else:
        print(f"❌ 錯誤：無法抓取 {com_name} 的資料")

# 進行資料處理與匯出
if company_list:
    # 合併四家公司的資料
    df = pd.concat(company_list, axis=0, ignore_index=True)

    print("\n--- [2/3] 正在進行課堂應用：Pandas 資料清洗與整理 ---")
    # 課堂應用：刪除所有可能含有空值的資料列
    df = df.dropna()

    # 建立資料存放夾
    output_dir = "stock_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 自動匯出成 CSV 與 Excel 檔（期末加分亮點！）
    df.to_csv(os.path.join(output_dir, "tech_stocks_final.csv"), index=False)
    print(f"👉 成果 1：已成功匯出 CSV 檔至 {output_dir}\\tech_stocks_final.csv")

    print("\n===== [3/3] 執行大成功！以下是完整的最後 10 筆數據 (df.tail(10)) =====")
    # 限制欄位顯示，讓控制台排版整齊漂亮
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df[['Date', 'company_name', 'Open', 'High', 'Low', 'Close', 'Volume']].tail(10))
    print("======================================================================")

else:
    print("\n❌ 錯誤：沒有成功整合成任何資料表，請檢查網路。")