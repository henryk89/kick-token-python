import json
from selenium import webdriver
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from seleniumrequests import Chrome


def get_token(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    primaryDriver = uc.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    token_provider_url = "https://kick.com/kick-token-provider"

    primaryDriver.get(token_provider_url)

    token_provider_response = primaryDriver.execute_script(
        "return document.body.innerText")
    token_provider = json.loads(token_provider_response)

    login_payload = {
        "isMobileRequest": True,
        "email": username,
        "password": password,
        token_provider["nameFieldName"]: "",
        token_provider["validFromFieldName"]: token_provider["encryptedValidFrom"]
    }

    options = ChromeOptions()
    options.add_argument("--headless=new")

    new_driver = Chrome(options=options)
    response = new_driver.request(
        'POST', 'https://kick.com/mobile/login', data=login_payload)

    if response.status_code == 200:
        token = response.json()['token']
        return token
    else:
        return None


token = get_token('myusername', 'mypassword')
print(token)
