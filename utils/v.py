import os
import datetime
import win32com.client as win32


def open_excel():
    
    file1 = r'C:\Frank\原始数据\店小秘+TP+订单+盘点\新TP订单下载 order_report.csv'
    file2 = r'C:\Frank\原始数据\店小秘+TP+订单+盘点\老TP订单下载 order_report.csv'
    xlsx_path = r'C:\Frank\2.1_易仓管理.xlsx'

    today = datetime.date.today()

    def is_modified_today(path: str) -> bool:
        return os.path.isfile(path) and datetime.date.fromtimestamp(os.path.getmtime(path)) == today

    if is_modified_today(file1) and is_modified_today(file2):
        try:
            print("✅ Both order files are updated. Opening Excel file...")

            excel = win32.Dispatch("Excel.Application")  # late binding，避开 gen_py
            excel.Visible = True
            wb = excel.Workbooks.Open(xlsx_path)

            print("✅ Excel file opened. Please refresh or process manually.")
        except Exception as e:
            print(f"❌ Operation failed: {e}")
    else:
        print("📌 One or both files were not updated today. Skipping Excel launch.")

'''
if __name__ == "__main__":
    open_excel()
'''