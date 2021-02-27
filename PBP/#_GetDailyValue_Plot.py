import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt

# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(df, name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False)

    # 위와같이 code명을 가져오면 앞에 공백이 붙어있는 상황이 발생하여 앞뒤로 sript() 하여 공백 제거
    code = code.strip()
    return code

# excel 파일을 다운로드하는거와 동시에 pandas에 load하기
code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

# data frame정리 (회사명이랑 종목코드만 남김)
code_df = code_df[['회사명', '종목코드']]

# data frame title 변경 '회사명' = name, 종목코드 = 'code'
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

# 종목코드는 6자리로 구분되기때문에 0을 채워 6자리로 변경
code_df.code = code_df.code.map('{:06d}'.format)

# ex) 삼성전자 코드로 데이터 받아오기
# yahoo의 주식 데이터 종목은 코스피는 .KS, 코스닥은 .KQ 써줘야댐
code = get_code(code_df, '삼성전자')
code = code + '.KS'
df = web.DataReader(code, "yahoo", "2020-02-20", "2021-02-20")

# 공휴일 데이터 빼기 Volume = 거래량이 0인 애들
df = df[df['Volume']!=0]

# Moving Average Filter 걸어서 보기 pandas dataframe에서 제공하는 rolling이라는 기능 사용
ma5 = df['Adj Close'].rolling(window=5).mean()
ma20 = df['Adj Close'].rolling(window=20).mean()

df.insert(len(df.columns), "MA5", ma5)
df.insert(len(df.columns), "MA20", ma20)

plt.plot(df.index, df['Adj Close'], label='Adj Close')
plt.plot(df.index, df['MA5'], label='MA5')
plt.plot(df.index, df['MA20'], label='MA20')

plt.legend(loc='best')
plt.grid()
plt.show()