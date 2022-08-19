from fyers_api.Websocket import ws
from fyers_api import fyersModel
import numpy as np
from datetime import datetime
import historicalDataRetriving as hst


######################
### dont forgate to set this multiplication value to i[0] or ltp
### set order quantity and company name
### make sure to comment or uncomment the "placeorder()" function calling line according to your need


############ variables to change
quantity = int(1)
symbol = ["NSE:BANKNIFTY2281839000CE"]
type = 2 #2 for market order
side = 1  # 1 for BUY order and -1 for SELL order
productType = "INTRADAY"
issellst = False      # is sell stratagy

n = 59
n2 = 20
n3 = 300
trlmt = 100 ###### ruppes above averge to which we can buy, depends on the stock price and fluatuation
prlmt = 20 ########## minimum profit range in rupees
###########



print("file is getting exhicuted")
client_id = ''
secret_key = ''


log_path = "F:\common\python\AlgoTrading\logs"
tokenfile = open('F:/common/python/AlgoTrading/acessToken.txt', 'r')
token = tokenfile.readline()

fyers = fyersModel.FyersModel(client_id=client_id,token= token,log_path=log_path)
fyers.token = token
pr = fyers.get_profile()
ob = fyers.orderbook()
fd = fyers.funds()
print(pr)

# avpr = hst.averprice(fyers,symbol[0])
avpr = 460
acess_token = client_id+":"+token
data_type = "symbolData"
order = [False,False]
i = [0]
bp = [0]
tim = []
ltplist = []
m5tim = []
m5ltp = []

# set 
# 1. divider of ltp
# 2. avprice
# 3. trlmt
# 4. prlmt
# 5. symbol
# 6. comment/uncomment placeorder(1)

def placeorder(side):
	order1 = fyers.place_order({"symbol":symbol[0],"qty":quantity,"type":type,
			"side":side,"productType":productType,"limitPrice":"0","stopPrice":"0",
			"disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":0,
			"takeProfit":0})
	print(order1)


####### buy stratagy
def buyst(m,m5,m5m,ltp):
	bolbuy = ((0.01<m and 0.04<m5 and m5m > 0.0015) or (m>m5m>0.003 and m5>0.01) )and not order[0]
	if bolbuy and avpr-trlmt < ltp < avpr+trlmt :
		ttm = datetime.now().strftime("%H:%M:%S")
		fle = open('temp3.txt','a')
		fle.writelines('\n placed a buy order at ' + str(ltp) + ' m,m5 and m5m are : ' + str(m) + str(m5) + str(m5m)  + ' at ' + ttm + '\n')
		print('placed a buy order ')
		bp[0] = ltp
		#placeorder(1)
		order[0] = True
		fle.close()
	elif order[0] :
		print('already ordered')
	else :
		print('not ordered yet')
	########### set the slope values if necessary
	bolsell = ((m5m < 0 and m5<0 and m < 0) or m5<-0.3 or m<-0.018)  and order[0]
	if  bolsell and (ltp > (bp[0]+prlmt)  or (ltp < bp[0]-15)   ):
		ttm = datetime.now().strftime("%H:%M:%S")
		fle = open('temp3.txt','a')
		fle.writelines('\n placed a sell order at ' + str(ltp)  + ' m,m5 and m5m are : ' + str(m) + str(m5) + str(m5m) + ' at ' + ttm + '\n')
		print('placing a sell order')
		#placeorder(-1)
		order[0] = False
		fle.close()


############# sell stratagy 
def sellst(m,m5,m5m,ltp):
	bolsell = (m < -0.01 and m5 < -0.04 and m5m < -0.0015) or (m<m5m<-0.003 and m5<-0.01)  and not order[1]
	bolsell = ((m5m < 0 and m5<0 and m < 0) or m5<-0.3 or m<-0.018)  and not order[1]
	if  bolsell and avpr-trlmt < ltp < avpr+trlmt :
		ttm = datetime.now().strftime("%H:%M:%S")
		fle = open('temp.txt','a')
		fle.writelines('\n placed a pre-sell order at ' + str(ltp)  + ' m,m5 and m5m are : ' + str(m) + str(m5) + str(m5m) + ' at ' + ttm + '\n')
		print('placing a pre-sell order')
		#placeorder(-1)
		order[0] = False
		fle.close()
	elif order[1] :
		print('already placed a pre-sell order')
	else :
		print('not ordered yet')

	bolbuy = ((m5m>0 and m5>0 and m > 0) or m5>0.3 or m >0.018) and order[1]
	if bolbuy and ltp < (bp[0]-prlmt) :
		ttm = datetime.now().strftime("%H:%M:%S")
		fle = open('temp.txt','a')
		fle.writelines('\n placed a post-buy order at ' + str(ltp) + ' m,m5 and m5m are : ' + str(m) + str(m5) + str(m5m)  + ' at ' + ttm + '\n')
		print('placed a post-buy order ')
		bp[0] = ltp
		#placeorder(1)
		order[0] = True
		fle.close()
	
	########### set the slope values if necessary
	




def custom_message(ticks) :
	# fle = open('temp3.txt','a')
	sc = ticks[0]['symbol']
	ltp = ticks[0]['ltp']
	print(sc,ltp)
	# fle.writelines(str(ltp) + ' ')
	# fle.close()
############## dont forgate to set this multiplication value to i[0] or ltp
	if i[0] % 5 == 0 :
		m5tim.append(i[0]*2)
		m5ltp.append(ltp//10)
		print(len(m5tim),len(m5ltp),len(tim),len(ltplist),i[0])
	tim.append(i[0])
	ltplist.append(ltp/10)
	i[0] += 1
	if i[0] > n3 and i[0]%5==0 :
		m5tim.pop(0)
		m5ltp.pop(0)
	if i[0] >=n :
		m,c = np.polyfit(tim,ltplist,1)
		m5,c5 = np.polyfit(tim[-1:-n2-1:-1],ltplist[-1:-n2-1:-1],1)
		m5m,c = np.polyfit(m5tim,m5ltp,1)
		ltplist.pop(0)
		tim.pop(0)

		if i[0] > 130 :
			print(order[0],'  m is : ',m,'  m5 is : ', m5, '  m5m is : ', m5m)
			######## set the slope values if necessary
			if issellst :
				sellst(m,m5,m5m,ltp)
			else :
				buyst(m,m5,m5m,ltp)
			
		

######### connecting to fyers socket for live data

if pr['code'] == 200 :
	fs = ws.FyersSocket(access_token=acess_token,run_background=False,log_path=log_path)
	print("calling custom_message")
	fs.websocket_data = custom_message
	print('after custom message')
	fs.subscribe(symbol=symbol,data_type=data_type)
	print('custom message 2')
	#fs.keep_running()
else :
	print('error found')

