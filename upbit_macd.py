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

# def get_daily_gap(ticker):
# #     """하루 가격차의 50% 산출"""
#     df = pyupbit.get_ohlcv(ticker, interval="day", count=3)
#     # prev_low = df['low'].shift(1)
#     return df
def macd(stick):
    df = pyupbit.get_ohlcv(stick, interval="day", count=100)

    # 12일 EMA = EMA12
    # if len(df.close) < 26:
    #     print("Stock info is short")

    # y = df.Close.values[0]
    # m_list = [y]
    y1 = df.iloc[0]['close']
    y2 = df.iloc[0]['close']
    s1 = df.iloc[0]['close']
    m_list1 = [y1] 
    m_list2 = [y2]
    signal = [s1]
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
    # macd1 = m_list1[-1] - m_list2[-1]
    # macd2 = m_list1[-2] - m_list2[-2] 
    # m_signal =m_list1 - m_list2
        # 9일 지수이동평균 계산
    for j in range(len(m_list1)):
        if j < 9:
            a9 = 2 / (j+1 + 1)
        else:
            a9 = 2 / (9 + 1)
        s1 = s1*(1-a9) + (m_list1[j] - m_list2[j])*a9
        signal.append(s1)   
    # macd 계산
    # print(m_list1)
    # print(m_list2)
    
    
        # print(macd)
    return m_list1, m_list2, signal

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# excel table 생성
wb = openpyxl.Workbook()
wb.save('upbit_deal_data.xlsx')
sheet = wb.active
# cell name : time, cur_pr, high, low, k, ref_pr, prev_low, sell 
sheet.append(['time', 'ticker', 'deal_price', 'deal_type', 'buy-sell'])
wb.save('upbit_deal_data.xlsx')
tickers = pyupbit.get_tickers(fiat = 'KRW')
# coin = ['KRW-CHZ', 'KRW-IQ', 'KRW-ELF', 'KRW-META', 'KRW-POLY', 'KRW-DOGE', 'KRW-IOTA', 'KRW-HIVE', 'KRW-BORA', 'KRW-HUM', 'KRW-SAND', \
#     'KRW-XRP', 'KRW-MANA', 'KRW-XLM', 'KRW-AERGO', 'KRW-BTT']
# coin =    ['KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-ARK', 'KRW-STORJ', 
# 'KRW-GRS', 'KRW-REP', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-MBL', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-HUNT', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-STRAX', 'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', 
# 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-DAWN', 'KRW-AXS', 'KRW-STX', 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-NU', 'KRW-AAVE', 'KRW-1INCH', 'KRW-ALGO']
    # coin1 = ['CHZ', 'ELF', 'META'] KRW-CHZ   

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") #날짜 바뀌는 것 실시간 업데이트
        end_time = start_time + datetime.timedelta(days=1)
        krw = get_balance("KRW")
        total_amount = krw
        
        for m in range(len(tickers)) :
            
            # print(m, tickers[m])
            current_coin = get_balance(tickers[m].split('-')[1])
            if current_coin == None:
                current_coin = 0
            # current_price = get_current_price(tickers[m])
            df_ma = get_ma(tickers[m])
            current_price = df_ma['close'].iloc[-1]
            amount = int(current_coin * current_price)
            total_amount += amount 
        order_limit = total_amount * 0.2 #1회 총자산의 20%까지 매수 가능
        if krw < order_limit :
            order_krw = krw * 0.9
        else :
            order_krw = order_limit * 0.9 
        for m in range(len(tickers)) :
            if order_krw > 5000:
                current_coin = get_balance(tickers[m].split('-')[1])
                if current_coin == None or current_coin < 1 :
                    # current_price = get_current_price(tickers[m])
                    df_ma = get_ma(tickers[m])
                    current_price = df_ma['close'].iloc[-1]
                    if current_price < 20000 :
                        # df_ma = get_ma(tickers[m])
                        m_list1, m_list2, signal=macd(tickers[m]) 
                        macd1 = m_list1[-1] - m_list2[-1]
                        macd2 = m_list1[-2] - m_list2[-2] 
                        macd3 = m_list1[-3] - m_list2[-3]
                        if macd1 > 0 and macd2 >= 0 and macd3 < 0 : # macd가 골든크로스후 다음날도 +인 경우
                            upbit.buy_market_order(tickers[m], order_krw)     
                            sheet.append([now, tickers[m], current_price, 'buy_macd_0line_gold', 'buy'])
                            wb.save('upbit_deal_data.xlsx')
                            time.sleep(0.5)
                        elif macd1 > 0 and macd3 <= signal[-3] and macd2 >= signal[-2] and macd1 > signal[-1] : # macd가 0선 위에 있고 signal선 기준 -, +, +일 경우
                            upbit.buy_market_order(tickers[m], order_krw)     
                            sheet.append([now, tickers[m], current_price, 'buy_macd_gold_w_over_macd0', 'buy'])
                            wb.save('upbit_deal_data.xlsx')
                            time.sleep(0.5) 
                        
                        # elif 0 <macd1 < 0.5 and macd1 >= macd2 and macd1 > signal[-1]: # 당일 macd가 0선 위에서 상승중이고 0.5보다 작으며 signam선보다 위에 있을 경우 매수
                        #     upbit.buy_market_order(tickers[m], order_krw)     
                        #     sheet.append([now, tickers[m], current_price, 'buy_macd_gold_w_over_macd0', 'buy'])
                        #     wb.save('upbit_deal_data.xlsx')
                        #     time.sleep(1)  
                        # elif df['close'].iloc[-2] > df_ma['lower'].iloc[-2] and current_price < df_ma['lower'].iloc[-1] :# 첫 볼린저 하단 진입시 매수
                        #     upbit.buy_market_order(coin[0], order_krw)    
                        #     sheet.append([now, coin[i], current_price, 'buy_boll_low', 'buy'])
                        #     wb.save('upbit_deal_data.xlsx')
                        #     time.sleep(1)
                        
                else :
                    pass    
            else  :
                pass
   
#sell 
        for m in range(len(tickers)) :
            current_coin = get_balance(tickers[m].split('-')[1])
            if current_coin == None:
                current_coin = 0
            if current_coin > 1 :
                # current_price = get_current_price(tickers[m])
                df_ma = get_ma(tickers[m])
                current_price = df_ma['close'].iloc[-1]
                macd1, macd2, signal=macd(tickers[m]) 
                macd1 = m_list1[-1] - m_list2[-1]
                macd2 = m_list1[-2] - m_list2[-2] 
                macd3 = m_list1[-3] - m_list2[-3]   
                # if current_price > df_ma['close'].iloc[-2] + df_ma['boll_gap'].iloc[-2] * 3 : #현재가가 전일종가 + 전일 볼랜드갭의 3배 이상 가격일 때 매도
                if current_price > df_ma['upper'].iloc[-1] + df_ma['boll_gap'].iloc[-1] * 2 : #현재가가 당일 볼린저 상단 + 당일 볼랜드갭의 2배 이상 일 때 매도
                    upbit.sell_market_order(tickers[m], current_coin*0.9995)
                    sheet.append([now, tickers[m], current_price, 'sell_bigjump', 'sell'])
                    wb.save('upbit_deal_data.xlsx')
                elif df_ma['close'].iloc[-3] > df_ma['upper'].iloc[-3] and df_ma['close'].iloc[-2] > df_ma['upper'].iloc[-2] and current_price > df_ma['upper'].iloc[-1]:  #3일 연속 볼린저 상단 돌파시 매도
                    upbit.sell_market_order(tickers[m], current_coin*0.9995)
                    sheet.append([now, tickers[m], current_price, 'sell_2days_bol_high', 'sell'])
                    wb.save('upbit_deal_data.xlsx')
                elif macd1>0 and macd3 >= signal[-3] and macd2 <= signal[-2] and macd1 < signal[-1] : #macd가 0선 위에 있고 signal선과 데드크로스 발생이후 다음날 매도
                    upbit.sell_market_order(tickers[m], current_coin)
                    sheet.append([now, tickers[m], current_price, 'sell_macd_dead', 'sell'])
                    wb.save('upbit_deal_data.xlsx')
                elif macd3 >= 0 and macd2 <= 0 and macd1 < 0 : #macd가 0선과 dead cross 이후 다음날 매도
                    upbit.sell_market_order(tickers[m], current_coin)
                    sheet.append([now, tickers[m], current_price, 'sell_macd_0line_dead', 'sell'])
                    wb.save('upbit_deal_data.xlsx')
                elif macd3 < signal[-3] and macd2 < signal[-2] and macd1 < signal[-1] : # macd가 3일 연속 signal선 이하에 있을 경우
                    upbit.sell_market_order(tickers[m], current_coin)
                    sheet.append([now, tickers[m], current_price, 'sell_macd_3days_under', 'sell'])
                    wb.save('upbit_deal_data.xlsx')
        
            else  :
                pass
        

    except Exception as e:
        print(e)
        # time.sleep(1)