import win32com.client

excel = win32com.client.Dispatch("Excel.Application")                             # excel 실행
excel.Visible = True                                                              # 화면에 띄울지 말지
wb = excel.Workbooks.Open('C:\\98_Git\\KJS_Project\\Trading\\test.xlsx')          # 파일 불러오기
ws = wb.ActiveSheet                                                               # 현재 active된 sheet
# ws = wb.Worksheets('Sheet1')                                                    # Sheet 고르기
ws.Range("C1").Interior.ColorIndex = 10                                           # C1 줄 색깔
print(ws.Cells(1,1).Value)
excel.Quit()                                                                      # 끝내기