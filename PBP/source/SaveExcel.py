import win32com.client

excel = win32com.client.Dispatch("Excel.Application")       # excel 실행
excel.Visible = True                                        # 화면에 띄울지 말지
wb = excel.Workbooks.Add()                                  # Workbook 추가
ws = wb.Worksheets("Sheet1")                                # Sheet 추가
ws.Cells(1, 1).Value = "hello world"                        # cell 정하기
wb.SaveAs('C:\\98_Git\\KJS_Project\\Trading\\test.xlsx')    # 저장 파일
excel.Quit()                                                # 끝내기