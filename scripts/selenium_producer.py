from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from confluent_kafka import Producer
import time
import socket
import json

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

class Sign:
    def __init__(self):
        self.sign = 0

    def acked(self, err, msg):
        if err is not None:
            self.sign = 0
        else:
            self.sign = 1

conf = {'bootstrap.servers': 'localhost:29092,localhost:29093',
        'client.id': socket.gethostname()}
producer = Producer(conf)
topic_name = 'reviewTopic'

# Set the URL Target
url = "https://play.google.com/store/apps/details?id=com.whatsapp"

# Call the URL and let the browser open the web page
driver.get(url)
driver.implicitly_wait(5)
driver.set_window_size(1936, 1096)

# Find the element where "See all reviews" is exit, then click it
whatsapp_link = driver.find_elements(By.CSS_SELECTOR, "span.VfPpkd-vQzf8d")
whatsapp_link[-1].click()
time.sleep(5)

length = 0
offset = 0

while True:
    popup = driver.find_elements(By.CSS_SELECTOR, "div.RHo1pe")
    action = ActionChains(driver)
    action.move_to_element(to_element=popup[-1]).perform()
    action.scroll_by_amount(0, 2333).perform()

    length = len(popup) - length
    review = {}
    for j in range(offset, offset + length):
        sign_obj = Sign()

        try:
            review["name"] = popup[j].find_element(By.CSS_SELECTOR, "div.X5PpBb").text
            review["date"] = popup[j].find_element(By.CSS_SELECTOR, "span.bp9Aid").text
            review["message"] = popup[j].find_element(By.CSS_SELECTOR, "div.h3YV2d").text
            review["star"] = len(popup[j].find_elements(By.CSS_SELECTOR, "span.Z1Dz7b"))
        except:
            break

        while sign_obj.sign == 0:
            producer.produce(topic_name, value=json.dumps(review).encode(), callback=sign_obj.acked)
            producer.poll(1)
        
        print("Succesfully send:", review)
    
    offset = j+1

    if length > 100000:
        break

popup = driver.find_elements(By.CSS_SELECTOR, "div.RHo1pe")
for j in range(offset, offset + length):
    sign_obj = Sign()

    try:
        review["name"] = popup[j].find_element(By.CSS_SELECTOR, "div.X5PpBb").text
        review["date"] = popup[j].find_element(By.CSS_SELECTOR, "span.bp9Aid").text
        review["message"] = popup[j].find_element(By.CSS_SELECTOR, "div.h3YV2d").text
        review["star"] = len(popup[j].find_elements(By.CSS_SELECTOR, "span.Z1Dz7b"))
    except:
            break

    while sign_obj.sign == 0:
        producer.produce(topic_name, value=json.dumps(review).encode(), callback=sign_obj.acked)
        producer.poll(1)
    
    print("Succesfully send:", review)

driver.quit()
