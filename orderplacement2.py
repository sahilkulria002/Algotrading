from fyers_api.Websocket import ws
from fyers_api import fyersModel
import numpy as np

print("file is getting exhicuted")
client_id = '5ISLSS90GN-100'
secret_key = '7XYC33VXZ1'
ltplist = []



log_path = "F:\common\python\AlgoTrading\logs"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2NTM4ODc3OTIsImV4cCI6MTY1Mzk1NzAzMiwibmJmIjoxNjUzODg3NzkyLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCaWxGTXd0UWw1UGRXMmlIRHhvRHRZX3VtTm03ZFVEaFJWckUzXzVYWHB0dER6b0hvNXBZRUVzVEp2djAzd0pQOVZzd3pMMVNONm1CREhDaktkNDdPTFA1MmM5Smg1TWIwX2xFYTFQYUNYa2M5a29uTT0iLCJkaXNwbGF5X25hbWUiOiJBQkhJU0hFSyBLVU1BUiIsImZ5X2lkIjoiWEEzNDA4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.Q2uX5qInFwXTyKmxEd29WNHK7ZyS3dfB7_OC1Jvv9Mo"
fyers = fyersModel.FyersModel(client_id=client_id,token= token,log_path=log_path)
fyers.token = token
pr = fyers.get_profile()
# ob = fyers.orderbook()
print(pr)

########## variables for order
isorder = False
quantity = int(2)
symbol = ["NSE:NAUKRI-EQ"]
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
tim = np.array(range(20))
n = 19
n2 = 5
def custom_message(ticks) :
	fle = open('temp.txt','a')
	sc = ticks[0]['symbol']
	ltp = ticks[0]['ltp']
	print(sc,ltp)
	fle.writelines(str(ltp))
	ltplist.append(ltp)
	if i[0] >=n :
		m,c = np.polyfit(tim,ltplist,1)
		m5,c5 = np.polyfit(tim,ltplist,1)
		ltplist.pop(0)
		print(order[0])
		
		if m5>0.2 and m>0.25 and not order[0] :
			fle.writelines('\n placed a buy order at ' + str(ltp) + '\n')
			print('placed a buy order ')
			# placeorder(1)
			order[0] = True
		elif order[0] :
			print('already ordered')
		else :
			print('not ordered yet')
		
		if  m5<0 and m < 0.1 and order[0] :
			fle.writelines('\n placed a sell order at ' + str(ltp) + '\n')
			print('placing a sell order')
			# placeorder(-1)
			order[0] = False
	fle.close()
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

