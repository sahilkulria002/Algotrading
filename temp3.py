from fyers_api.Websocket import ws
from fyers_api import fyersModel
import numpy as np
from datetime import datetime

print("file is getting exhicuted")
client_id = '5ISLSS90GN-100'
secret_key = '7XYC33VXZ1'
ltplist = []



log_path = "F:\common\python\AlgoTrading\logs"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2NTQ2NzEwMzgsImV4cCI6MTY1NDczNDYzOCwibmJmIjoxNjU0NjcxMDM4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCaW9FYS1STzVzWFZZb183SHQ4Z3V2UmNKQlJYYm9sTHJIamhrMkNvbTF6QVk1OFROUUtCX3FPVk50dnJrRldpaVpnMlRTZUZTRGJhVUhxMkVHbGQ0Q1YxaW1rTjR6Wk45Q01ZajlVUXNBZlFtbzNZOD0iLCJkaXNwbGF5X25hbWUiOiJBQkhJU0hFSyBLVU1BUiIsImZ5X2lkIjoiWEEzNDA4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.0jteJTD9Rw6GnLWpeJT-JmDMtDNPNNDc4TaZMrGt2GI"
fyers = fyersModel.FyersModel(client_id=client_id,token= token,log_path=log_path)
fyers.token = token
pr = fyers.get_profile()
ob = fyers.orderbook()
fd = fyers.funds()
print(pr)

########## variables for order
isorder = False
quantity = int(10)
symbol = ["NSE:ONGC-EQ"]
type = 2 #2 for market order
side = 1  # 1 for BUY order and -1 for SELL order
productType = "INTRADAY" 
# target_price = int(ltp*0.02)
# stoploss_price = int(ltp*0.01)
##########

########### To get the data
acess_token = client_id+":"+token
data_type = "symbolData"
#######

def placeorder(side):
	order1 = fyers.place_order({"symbol":symbol[0],"qty":quantity,"type":type,
			"side":side,"productType":productType,"limitPrice":"0","stopPrice":"0",
			"disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":0,
			"takeProfit":0})
	print(order1)

order = [False,True]
i = [0]
bp = [0]
tim = []
n = 59
n2 = 20
n3 = 300
def custom_message(ticks) :
	# fle = open('temp.txt','a')
	sc = ticks[0]['symbol']
	ltp = ticks[0]['ltp']
	print(sc,ltp)
	# fle.writelines(str(ltp) + ' ')
	tim.append(i[0]*0.2)
	ltplist.append(ltp)
	if i[0] >=n :
		m,c = np.polyfit(tim[-1:-n-1:-1],ltplist[-1:-n-1:-1],1)
		m5,c5 = np.polyfit(tim[-1:-n2-1:-1],ltplist[-1:-n2-1:-1],1)
		m5m,c = np.polyfit(tim,ltplist,1)
		if i[0] >= n3 :
			ltplist.pop(0)
			tim.pop(0)
		# print('m5m is : ', m5m)
		if i[0] > 130 :
			print(order[0],'  m is : ',m,'  m5 is : ', m5, '  m5m is : ', m5m)
			bolbuy = ((0.01<m and 0.04<m5 and m5m > 0.0015) or (m>m5m>0.003 and m5>0.01) )and not order[0]
			if bolbuy and 162 < ltp < 166 :
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
			bolsell = ((m5m < 0 and m5<0 and m < 0) or m5<-0.3 or m<-0.018)  and order[0]
			if  bolsell and ltp > (bp[0]+0.5) :
				ttm = datetime.now().strftime("%H:%M:%S")
				fle = open('temp.txt','a')
				fle.writelines('\n placed a sell order at ' + str(ltp)  + ' m,m5 and m5m are : ' + str(m) + str(m5) + str(m5m) + ' at ' + ttm + '\n')
				print('placing a sell order')
				# placeorder(-1)
				order[0] = False
				fle.close()
	# fle.close()
	i[0] += 1
        
        

	##########  modify these conditions to place an order
	
		

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

