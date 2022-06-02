
from fyers_api.Websocket import ws
from fyers_api import fyersModel
from fyers_api import accessToken
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

s=Service("F:\common\python\AlgoTrading\chromedriver_win32\chromedriver.exe")
# driver = webdriver.Chrome(service=s)

# log_path = document_file.log_path
client_id = '5ISLSS90GN-100'
secret_key = '7XYC33VXZ1'
redirect_url = 'https://www.google.com/'
response_type = 'code'
grant_type = "authorization_code"
username = "XA34086"
password = 'Abhideep@451'
pin1 = "4"
pin2 = "5"
pin3 = "1"
pin4 = "3"

def generate_auth_code():
	url = f"https://api.fyers.in/api/v2/generate-authcode?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&state=state&scope=&nonce="
	driver = webdriver.Chrome(service=s)
	driver.get(url)
    
	time.sleep(3)
	driver.execute_script(f"document.querySelector('[id=fy_client_id]').value = '{username}'")
	driver.execute_script("document.querySelector('[id=clientIdSubmit]').click()")
	time.sleep(3)
	driver.execute_script(f"document.querySelector('[id=fy_client_pwd]').value = '{password}'")
	driver.execute_script("document.querySelector('[id=loginSubmit]').click()")
	time.sleep(3)


	driver.find_element(by=By.ID, value="verify-pin-page").find_element(by=By.ID, value="first").send_keys(pin1)
	driver.find_element(by=By.ID, value="verify-pin-page").find_element(by=By.ID, value="second").send_keys(pin2)
	driver.find_element(by=By.ID, value="verify-pin-page").find_element(by=By.ID, value="third").send_keys(pin3)
	driver.find_element(by=By.ID, value="verify-pin-page").find_element(by=By.ID, value="fourth").send_keys(pin4)
	driver.execute_script("document.querySelector('[id=verifyPinSubmit]').click()")
	time.sleep(8)
	newurl = driver.current_url
	auth_code = newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
	driver.quit()
	return auth_code

def generate_access_token(auth_code, appId, secret_key):
	appSession = accessToken.SessionModel(client_id=appId, secret_key=secret_key,grant_type="authorization_code")
	appSession.set_token(auth_code)
	response = appSession.generate_token()["access_token"]
	return response


def main() :
    auth_code = generate_auth_code()
    token = generate_access_token(auth_code,client_id,secret_key)
    print(token)
    return token

if __name__ == "__main__" :
    main()
