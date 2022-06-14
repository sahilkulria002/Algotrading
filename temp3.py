from fyers_api.Websocket import ws
from fyers_api import fyersModel
import numpy as np
from datetime import datetime
import historicalDataRetriving as hst


############ variables to change
quantity = int(10)
symbol = ["NSE:BANKNIFTY2261634500PE"]
type = 2 #2 for market order
side = 1  # 1 for BUY order and -1 for SELL order
productType = "INTRADAY"

n = 59
n2 = 20
n3 = 300
prlmt = 20 ########## minimum profit range in rupees 
devider = int(input('give the diveder for ltp ( an intiger ) : '))   ### the devider of ltp for slope
###########



print("file is getting exhicuted")
client_id = '5ISLSS90GN-100'
secret_key = '7XYC33VXZ1'


log_path = "F:\common\python\AlgoTrading\logs"
tokenfile = open('F:/common/python/AlgoTrading/acessToken.txt', 'r')
token = tokenfile.readline()

fyers = fyersModel.FyersModel(client_id=client_id,token= token,log_path=log_path)
fyers.token = token
pr = fyers.get_profile()
ob = fyers.orderbook()
fd = fyers.funds()
print(pr)

openpr = hst.openprice(fyers,symbol[0])
acess_token = client_id+":"+token
data_type = "symbolData"
order = [False,True]
i = [0]
bp = [0]
tim = []
ltplist = []
m5tim = []
m5ltp = []



def placeorder(side):
	order1 = fyers.place_order({"symbol":symbol[0],"qty":quantity,"type":type,
			"side":side,"productType":productType,"limitPrice":"0","stopPrice":"0",
			"disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":0,
			"takeProfit":0})
	print(order1)



def custom_message(ticks) :
	sc = ticks[0]['symbol']
	ltp = ticks[0]['ltp']
	print(sc,ltp)
############## dont forgate to set this multiplication value to i[0] or ltp
	if i[0] % 5 == 0 :
		m5tim.append(i[0]*2)
		m5ltp.append(ltp)
		print(len(m5tim),len(m5ltp),len(tim),len(ltplist))
	tim.append(i[0])
	ltplist.append(round(ltp/devider,3))
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
			bolbuy = ((0.025<m and 0.03<m5 and m5m > 0.0015) or (m>m5m>0.005 and m5>0.01) )and not order[0]
			if bolbuy and ltp < openpr-20 :
				ttm = datetime.now().strftime("%H:%M:%S")
				fle = open('temp.txt','a')
				fle.writelines('\n placed a buy order at ' + str(ltp) + ' m,m5 and m5m are : ' + str(m) + str(m5) + str(m5m)  + ' at ' + ttm + '\n')
				print('placed a buy order ')
				bp[0] = ltp
				# placeorder(1)
				order[0] = True
				fle.close()
			elif order[0] :
				print('already ordered')
			else :
				print('not ordered yet')
			########### set the slope values if necessary
			bolsell = ((m5m < 0 and m5<0 and m < 0) or m5<m<-0.020)  and order[0]
			if  bolsell and ltp > (bp[0]+prlmt) :
				ttm = datetime.now().strftime("%H:%M:%S")
				fle = open('temp.txt','a')
				fle.writelines('\n placed a sell order at ' + str(ltp)  + ' m,m5 and m5m are : ' + str(m) + str(m5) + str(m5m) + ' at ' + ttm + '\n')
				print('placing a sell order')
				# placeorder(-1)
				order[0] = False
				fle.close()

		

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

