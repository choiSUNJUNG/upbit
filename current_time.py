import time
import pyupbit
import datetime



def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_daily_gap(ticker):
#     """하루 가격차"""
    df = pyupbit.get_ohlcv(ticker)
    df['prev_low'] = df['low'].shift(1)
    df['decision_price'] = df['high'] - ((df['high'] - df['low']) * 0.5) 
    return df

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df1 = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    df1['target_price'] = df1.iloc[0]['close'] + (df1.iloc[0]['high'] - df1.iloc[0]['low']) * k
    return df1
    # target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    # return target_price

now = datetime.datetime.now()
print("현재시간 : ", now)
start_time = get_start_time("KRW-DOGE")
print("시작시간 : ", start_time)
end_time = start_time + datetime.timedelta(days=1)
print("종료 시간 : ", end_time)

current_price = get_current_price("KRW-DOGE")

df = get_daily_gap("KRW-DOGE")
high = df.iloc[-1]['high']
low = df.iloc[-1]['low']
ref_price = df.iloc[-1]['decision_price']
daily_gap = (high - ref_price) / ref_price

print("현재가 : ", current_price)
df1 = get_target_price("KRW-DOGE", 0.5)
# target_price = get_target_price("KRW-DOGE", 0.5)
if start_time < now < end_time - datetime.timedelta(seconds=82000):
    print("매수 가능 시간")
elif current_price > df.iloc[-1]['decision_price'] and current_price > df.iloc[-1]['prev_low']:
    print("no sell 조건1")
elif daily_gap < 0.103:
    print("당일 변동 비율 : ", daily_gap)
    print("no sell 조건2")
else:
    print("매도")

ma15 = get_ma15("KRW-DOGE")
print("ma15일선 : ", ma15)
print("매수기준가 : ", df1.iloc[-1]['target_price'])
print("매도기준가 : ", df.iloc[-1]['decision_price'])
print("전일저가 : ", df.iloc[-1]['prev_low'])
print(df)
df.to_excel("dd10.xlsx")


# if current < decision_price:
#     print("현재가 : ", current_price)

# hilow = get_daily_gap("DOGE")
# print(high)
# print(low)
# df = pyupbit.get_ohlcv("KRW-DOGE")
# print(df)
# df1 = pyupbit.get_ohlcv("KRW-DOGE", interval="day", count=1)
# print(df1)

        