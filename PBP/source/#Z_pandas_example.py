from pandas import *

''' 
# pandas 사용 이유[1], Series 기능
kakao2 = Series([92600, 92400, 92100, 94300, 92300], index=['2016-02-19',
                                                            '2016-02-18',
                                                            '2016-02-17',
                                                            '2016-02-16',
                                                            '2016-02-15'])
print(kakao2)       # Series가 python list와 다른점
print(kakao2['2016-02-19']) # index를 지정할 수 있고 지정했던 인덱스 사용가능

for date in kakao2.index:   # .index로 접근 가능
    print(date)

for ending_price in kakao2.values:  # .values 로 접근 가능
    print(ending_price)
'''


''' 
# pandas 사용 이유[2], 서로 다른 indexing끼리의 합 가능
mine   = Series([10, 20, 30, 100], index=['naver', 'sk', 'kt', 'hmc'])
friend = Series([10, 30, 20], index=['kt', 'naver', 'sk'])
merge = mine + friend
print(merge) 
'''


''' 
# pandas 사용 이유[3], 2차원 자료 만들기가 쉬움
daeshin = {'open':  [11650, 11100, 11200, 11100, 11000],
           'high':  [12100, 11800, 11200, 11100, 11150],
           'low' :  [11600, 11050, 10900, 10950, 10900],
           'close': [11900, 11600, 11000, 11100, 11050]}

# column, index(=row) 지 맘대로임
daeshin_day = DataFrame(daeshin) 
print(daeshin_day)

# column, index 내 맘대로 조절
date = ['16.02.29', '16.02.26', '16.02.25', '16.02.24', '16.02.23']
daeshin_day = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'], index=date)
print(daeshin_day) 

# dataframe 접근법
print(daeshin_day['open']) # 이름으로 column접근
print(daeshin_day.open) # 이름으로 column접근 방법2
print(daeshin_day.loc['16.02.26']) # index(=row) 접근
print(daeshin_day.loc['16.02.26','open']) # 딱 특정 위치에 있는 data 접근
'''