#coin1,3 : 매수 -> 5일선 상승 & 5~10일선 사이 매수, 매도 -> 볼린저갭 2배이상, 5일선-10일선 갭 축소
#coin2 : 볼린저 하단 매수, 상단 매도
 
import time
import pyupbit
import datetime
import openpyxl



def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2) # 전일 데이터까지만 인출
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=100)
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma12'] = df['close'].rolling(12).mean()
    df['ma15'] = df['close'].rolling(15).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    df['ma26'] = df['close'].rolling(26).mean()
    df['ma50'] = df['close'].rolling(50).mean()
    df['stddev'] = df['close'].rolling(20).std()
    df['upper'] = df['ma20'] + (df['stddev']*2)
    df['lower'] = df['ma20'] - (df['stddev']*2)
    df['boll_gap'] = df['upper'] - df['lower']
    return df

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    # print(balances)
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def get_daily_gap(ticker):
#     """하루 가격차의 50% 산출"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=3)
    # prev_low = df['low'].shift(1)
    df['prev_low'] = df['low'].shift(1)
    df['prev_high'] = df['high'].shift(1)
    df['prev_open'] = df['open'].shift(1)
    df['prev_close'] = df['close'].shift(1)

    df['decision_price'] = df['high'] - ((df['high'] - df['low']) * 0.5) 
    return df

wb = openpyxl.Workbook()

def macd(ticker):
    df = pyupbit.get_ohlcv(ticker, count=100)
    # 12일 EMA = EMA12
    if len(df) < 26:
        print("Stock info is short")
    # print(stick, len(df))
    # y = df.Close.values[0]
    # m_list = [y]
    y1 = df.iloc[0]['close']
    y2 = df.iloc[0]['close']
    s1 = df.iloc[0]['close']
    m_list1 = [y1] 
    m_list2 = [y2]
    s_list1 = [s1]
    # 12일 지수이동평균 계산
    for i in range(len(df)):
        if i < 12:
            a12 = 2 / (i+1 + 1)
        else:
            a12 = 2 / (12 + 1)
        y1 = y1*(1-a12) + df.close.values[i]*a12
        m_list1.append(y1)

    # 26일 지수이동평균 계산    
    for k in range(len(df)):
        if k < 26:
            a26 = 2 / (k+1 + 1)
        else:
            a26 = 2 / (26 + 1)
        y2 = y2*(1-a26) + df.close.values[k]*a26
        m_list2.append(y2)
    macd1 = m_list1[-1] - m_list2[-1]
    macd2 = m_list1[-2] - m_list2[-2] 
    # m_signal =m_list1 - m_list2
        # 9일 지수이동평균 계산
    for j in range(len(m_list1)):
        if j < 9:
            a9 = 2 / (j+1 + 1)
        else:
            a9 = 2 / (9 + 1)
        s1 = s1*(1-a9) + (m_list1[j] - m_list2[j])*a9
        s_list1.append(s1)   
    return macd1, macd2, s_list1
tickers = pyupbit.get_tickers(fiat = 'KRW')
print(len(tickers), tickers)
m = 0
for m in range(len(tickers)) :
    macd1, macd2, s_list1=macd(tickers[m]) 
    print(m)
    time.sleep(0.5)
    # df_ma = get_ma(tickers[i])
    if macd1 > 0 and macd2 < 0 :
        print(tickers[m], macd1, 'macd_0')
    elif macd1 > 0 and macd1 > s_list1[-1] and macd2 < s_list1[-2] :
         print(tickers[m], macd1, 'macd_gold')       
# 로그인
# upbit = pyupbit.Upbit(access, secret)
# print("autotrade start")
# # excel table 생성
# wb = openpyxl.Workbook()
# wb.save('upbit_deal_data.xlsx')
# sheet = wb.active
# # cell name : time, cur_pr, high, low, k, ref_pr, prev_low, sell 
# sheet.append(['time', 'ticker', 'deal_price', 'deal_type', 'buy-sell'])
# wb.save('upbit_deal_data.xlsx')
# coin0_buy_key = 0
# coin1_buy_key = 0
# coin2_buy_key = 0
# coin = ['KRW-ELF', 'KRW-CHZ', 'KRW-META']
# coin1 = ['ELF', 'CHZ', 'META'] 

# # 자동매매 시작
# while True:
#     try:
#         now = datetime.datetime.now()
#         start_time = get_start_time("KRW-BTC") #날짜 바뀌는 것 실시간 업데이트
#         end_time = start_time + datetime.timedelta(days=1)
        
#         krw = get_balance("KRW")
#         print(krw)
#         coin_b0 = get_balance(coin1[0])
#         coin_b1 = get_balance(coin1[1])
#         coin_b2 = get_balance(coin1[2])
#         if coin_b0 == None:
#             coin_b0 = 0
#         if coin_b1 == None:
#             coin_b1 = 0
#         if coin_b2 == None:
#             coin_b2 = 0
        
# #buy
#         if krw > 5000 and coin_b0 < 1 :
#             df = get_daily_gap(coin[0])  # 하루 중 계속 변할 수 있는 값으로 실시간 도출 필요
#             current_price = get_current_price(coin[0])
#             high = df.iloc[-1]['high']
#             low = df.iloc[-1]['low']
#             ref_price = df.iloc[-1]['decision_price'] 
#             prev_low = df.iloc[-1]['prev_low']
#             df_ma = get_ma(coin[0])
#             if df_ma['ma5'].iloc[-1] > df_ma['ma5'].iloc[-2] and df_ma['ma10'].iloc[-1] < current_price < df_ma['ma10'].iloc[-1] + (df_ma['ma5'].iloc[-1] - df_ma['ma10'].iloc[-1]) / 2 :
#                 # 5일선 상승 확인 & 현재가가 10일선 위, 5일선과 10일선 갭의 중간 이하에 위치할 때 매수
#                 if coin_b1 > 1 and coin_b2 > 1:
#                     upbit.buy_market_order(coin[0], krw*0.9)     # 남은 원화의 90% 금액으로 buy
#                     sheet.append([now, coin[0], current_price, 'type1_5~10사이', 'buy'])
#                     wb.save('upbit_deal_data.xlsx')
#                     time.sleep(1)
#                 elif (coin_b1 > 1 and coin_b2 < 1) or (coin_b1 < 1 and coin_b2 > 1):
#                     upbit.buy_market_order(coin[0], krw*0.45)     # 남은 원화의 45% 금액으로 buy
#                     sheet.append([now, coin[0], current_price, 'type1_5~10사이', 'buy'])
#                     wb.save('upbit_deal_data.xlsx')
#                     time.sleep(1)
#                 else :
#                     upbit.buy_market_order(coin[0], krw*0.3)     # 남은 원화의 90% 금액으로 buy
#                     sheet.append([now, coin[0], current_price, 'type1_5~10사이', 'buy'])
#                     wb.save('upbit_deal_data.xlsx')
#                     time.sleep(1)
#             elif df['low'].iloc[-2] > df_ma['lower'].iloc[-2] and current_price < df_ma['lower'].iloc[-1] :# 첫 볼린저 하단 진입시 매수
#                 if coin_b1 > 1 and coin_b2 > 1:
#                     upbit.buy_market_order(coin[0], krw*0.9)     # 남은 원화의 90% 금액으로 buy
#                     sheet.append([now, coin[0], current_price, 'type1_boll_low', 'buy'])
#                     wb.save('upbit_deal_data.xlsx')
#                     time.sleep(1)
#                 elif (coin_b1 > 1 and coin_b2 < 1) or (coin_b1 < 1 and coin_b2 > 1):
#                     upbit.buy_market_order(coin[0], krw*0.45)     # 남은 원화의 45% 금액으로 buy
#                     sheet.append([now, coin[0], current_price, 'type1_boll_low', 'buy'])
#                     wb.save('upbit_deal_data.xlsx')
#                     time.sleep(1)
#                 else :
#                     upbit.buy_market_order(coin[0], krw*0.3)     # 남은 원화의 90% 금액으로 buy
#                     sheet.append([now, coin[0], current_price, 'type1_boll_low', 'buy'])
#                     wb.save('upbit_deal_data.xlsx')
#                     time.sleep(1)
#             else :
#                 pass    
#         else  :
#             pass
#         if krw > 5000 and coin_b1 < 1:
#             df = get_daily_gap(coin[1])  # 하루 중 계속 변할 수 있는 값으로 실시간 도출 필요
#             current_price = get_current_price(coin[1])
#             high = df.iloc[-1]['high']
#             low = df.iloc[-1]['low']
#             ref_price = df.iloc[-1]['decision_price'] 
#             prev_low = df.iloc[-1]['prev_low']
#             df_ma = get_ma(coin[1])
#             if df['low'].iloc[-2] > df_ma['lower'].iloc[-2] and current_price < df_ma['lower'].iloc[-1] :    # 첫 볼린저 하단 진입시 매수
#                 if coin_b0 > 1 and coin_b2 > 1:
#                     upbit.buy_market_order(coin[1], krw*0.9)     # 남은 원화의 90% 금액으로 buy
#                     sheet.append([now, coin[1], current_price, 'type2_boll_low', 'buy'])
#                     wb.save('upbit_deal_data.xlsx')
#                     time.sleep(1)
#                 elif (coin_b0 > 1 and coin_b2 < 1) or (coin_b0 < 1 and coin_b2 > 1):
#                     upbit.buy_market_order(coin[1], krw*0.45)     # 남은 원화의 90% 금액으로 buy
#                     sheet.append([now, coin[1], current_price, 'type2_boll_low', 'buy'])
#                     wb.save('upbit_deal_data.xlsx')
#                     time.sleep(1)
#                 else :
#                     upbit.buy_market_order(coin[1], krw*0.3)     # 남은 원화의 90% 금액으로 buy
#                     sheet.append([now, coin[1], current_price, 'type2_boll_low', 'buy'])
#                     wb.save('upbit_deal_data.xlsx')
#                     time.sleep(1)
#         else  :
#             pass

#         if krw > 5000 and coin_b2 < 1:
#             df = get_daily_gap(coin[2])  # 하루 중 계속 변할 수 있는 값으로 실시간 도출 필요
#             current_price = get_current_price(coin[2])
#             high = df.iloc[-1]['high']
#             low = df.iloc[-1]['low']
#             ref_price = df.iloc[-1]['decision_price'] 
#             prev_low = df.iloc[-1]['prev_low']
#             df_ma = get_ma(coin[2])

#             if start_time < now < end_time - datetime.timedelta(seconds=300):
#                 target_price = get_target_price(coin[2], 0.5)


#                 # if target_price < current_price: 
#                 if target_price < current_price and df_ma['ma5'].iloc[-1] < current_price:
#                     if coin_b0 > 1 and coin_b1 > 1:
#                         upbit.buy_market_order(coin[2], krw*0.9)     # 남은 원화의 90% 금액으로 buy
#                         sheet.append([now, coin[2], current_price, 'type3_daily_target_price', 'buy'])
#                         wb.save('upbit_deal_data.xlsx')
#                         time.sleep(1)
#                     elif (coin_b0 > 1 and coin_b1 < 1) or (coin_b0 < 1 and coin_b1 > 1):
#                         upbit.buy_market_order(coin[2], krw*0.45)     # 남은 원화의 45% 금액으로 buy
#                         sheet.append([now, coin[2], current_price, 'type3_daily_target_price', 'buy'])
#                         wb.save('upbit_deal_data.xlsx')
#                         time.sleep(1)
#                     else :
#                         upbit.buy_market_order(coin[2], krw*0.3)     # 남은 원화의 30% 금액으로 buy
#                         sheet.append([now, coin[2], current_price, 'type3_daily_target_price', 'buy'])
#                         wb.save('upbit_deal_data.xlsx')
#                         time.sleep(1)
#             else:
#                 pass

        
# #sell 
#         if coin_b0 > 1 :
#             df = get_daily_gap(coin[0])  # 하루 중 계속 변할 수 있는 값으로 실시간 도출 필요
#             current_price = get_current_price(coin[0])
#             high = df.iloc[-1]['high']
#             low = df.iloc[-1]['low']
#             ref_price = df.iloc[-1]['decision_price'] 
#             prev_low = df.iloc[-1]['prev_low']
#             df_ma = get_ma(coin[0]) 
               
#             if current_price > df['close'].iloc[-2] + df_ma['boll_gap'].iloc[-2] * 3 : #현재가가 전일종가 + 전일 볼랜드갭의 3배 이상 가격일 때 매도
#                 upbit.sell_market_order(coin[0], coin_b0*0.9995)
#                 sheet.append([now, coin[0], current_price, 'type1_bigjump', 'sell'])
#                 wb.save('upbit_deal_data.xlsx')
#             elif df['close'].iloc[-2] > df_ma['upper'].iloc[-2] and current_price > df_ma['upper'].iloc[-1]:  #2일 연속 볼린저 상단 돌파시 매도
#                 upbit.sell_market_order(coin[0], coin_b0*0.9995)
#                 sheet.append([now, coin[0], current_price, 'type1_2days_bol_high', 'sell'])
#                 wb.save('upbit_deal_data.xlsx')
#             elif df_ma['ma5'].iloc[-1] - df_ma['ma10'].iloc[-1] > 0 and df_ma['ma5'].iloc[-1] - df_ma['ma10'].iloc[-1] < (df_ma['ma5'].iloc[-2] - df_ma['ma10'].iloc[-2]) * 0.9 : 
#                 # 5일선이 10일선 위에 있고 당일 5일선 - 10일선 갭이 전일 5일선 - 10일선 갭의 90% 이하일때 매도       
#                 upbit.sell_market_order(coin[0], coin_b0*0.9995)
#                 sheet.append([now, coin[0], current_price, 'type1_5&10gap_down', 'sell'])
#                 wb.save('upbit_deal_data.xlsx')
#             elif df['low'].iloc[-2] < df_ma['lower'].iloc[-2] and current_price < df['low'].iloc[-2] * 0.95 : #2일 연속 볼린저 하단 하락 & 전일 최저가의 5% 이상 하락시 매도
#                 upbit.sell_market_order(coin[0], coin_b0*0.9995)
#                 sheet.append([now, coin[0], current_price, 'type1_2days_bol_under', 'sell'])
#                 wb.save('upbit_deal_data.xlsx')
#             elif df['low'].iloc[-3] < df_ma['lower'].iloc[-3] and df['low'].iloc[-2] < df_ma['lower'].iloc[-2] : #3거래일 연속 볼린저 하단 이하 하락 
#                 if current_price < df_ma['lower'].iloc[-1] and df_ma['lower'].iloc[-2] > df_ma['lower'].iloc[-1] :
#                     upbit.sell_market_order(coin[0], coin_b0*0.9995)
#                     sheet.append([now, coin[0], current_price, 'type1_3days_bol_under', 'sell'])
#                     wb.save('upbit_deal_data.xlsx')
#             # elif df_ma['ma5'].iloc[-1] - df_ma['ma5'].iloc[-2] < 0 and current_price < df_ma['ma10'].iloc[-1] : #5일선이 꺾이고 현재가가 10일선 이하일 때 매도
#             #     upbit.sell_market_order(coin[0], coin_b0*0.9995)
#             #     sheet.append([now, coin[0], current_price, 'type1_5linedown&under_10line', 'sell'])
#             #     wb.save('upbit_deal_data.xlsx')
#         else  :
#             pass
#         if coin_b1 > 1 :
#             df = get_daily_gap(coin[1])  # 하루 중 계속 변할 수 있는 값으로 실시간 도출 필요
#             current_price = get_current_price(coin[1])
#             high = df.iloc[-1]['high']
#             low = df.iloc[-1]['low']
#             ref_price = df.iloc[-1]['decision_price'] 
#             prev_low = df.iloc[-1]['prev_low']
#             df_ma = get_ma(coin[1])
            
#             if current_price >= df_ma['upper'].iloc[-1]:    # 볼린저 상단 매도
#                 upbit.sell_market_order(coin[1], coin_b1*0.9995)
#                 sheet.append([now, coin[1], current_price, 'type2_boll_high', 'sell'])
#                 wb.save('upbit_deal_data.xlsx')
#             elif df['low'].iloc[-2] < df_ma['lower'].iloc[-2] and current_price < df['low'].iloc[-2] * 0.95 : #2일 연속 볼린저 하단 하락 & 전일 최저가의 5% 이상 하락시 매도
#                 upbit.sell_market_order(coin[1], coin_b1*0.9995)
#                 sheet.append([now, coin[1], current_price, 'type2_2days_bol_under', 'sell'])
#                 wb.save('upbit_deal_data.xlsx')
#             # elif df_ma['ma5'].iloc[-1] - df_ma['ma10'].iloc[-1] > 0 and df_ma['ma5'].iloc[-1] - df_ma['ma10'].iloc[-1] < df_ma['ma5'].iloc[-2] - df_ma['ma10'].iloc[-2] * 0.9 :        
#             #     upbit.sell_market_order(coin[1], coin_b1*0.9995)
#             #     sheet.append([now, coin[1], current_price, 'type2_5&10gap_down', 'sell'])
#             #     wb.save('upbit_deal_data.xlsx')
#             elif df['low'].iloc[-3] < df_ma['lower'].iloc[-3] and df['low'].iloc[-2] < df_ma['lower'].iloc[-2] : #3거래일 연속 볼린저 하단 이하 하락 
#                 if current_price < df_ma['lower'].iloc[-1] and df_ma['lower'].iloc[-2] > df_ma['lower'].iloc[-1] :
#                 #3일 연속 볼린저 하단 발생 및 볼린저 하단가 하락시 매도
#                     upbit.sell_market_order(coin[1], coin_b1*0.9995)
#                     sheet.append([now, coin[1], current_price, 'type2__5linedown&under_10line', 'sell'])
#                     wb.save('upbit_deal_data.xlsx')
#         else  :
#             pass

#         if coin_b2 > 1 :
#             df = get_daily_gap(coin[2])  # 하루 중 계속 변할 수 있는 값으로 실시간 도출 필요
#             current_price = get_current_price(coin[2])
#             high = df.iloc[-1]['high']
#             low = df.iloc[-1]['low']
#             ref_price = df.iloc[-1]['decision_price'] 
#             prev_low = df.iloc[-1]['prev_low']
#             df_ma = get_ma(coin[2])    
            
#             if end_time - datetime.timedelta(seconds=300) < now < end_time and current_price < df['close'].iloc[-2] - (df['prev_high'].iloc[-2] - df['prev_low'].iloc[-2])/2 :
#                 upbit.sell_market_order(coin[2], coin_b2*0.9995)
#                 sheet.append([now, coin[2], current_price, 'type3_daily_sell_price', 'sell'])
#                 wb.save('upbit_deal_data.xlsx')
#                 # log 남기기(현재가, 기준가, 전일저가, sell 기록 남기기)
#             else :
#                 pass
#         else  :
#             pass    

#     except Exception as e:
#         print(e)
#         time.sleep(1)







