import requests
import time
from bs4 import BeautifulSoup
import time
from timeloop import Timeloop
from datetime import timedelta
from sys import exit as sys_exit
import paho.mqtt.client as paho
broker="192.168.2.50"
port=1883
client= paho.Client("myBMW")
client.connect(broker,port)

tl = Timeloop()

@tl.job(interval=timedelta(seconds=300))
def get_bmw(which='2 Serie'):
    url = 'https://www.leaseplandirect.nl/lease-auto/bmw/?staat=occasion&sorteren=naam&richting=asc'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.find_all('div', class_='image-container')
    print ("300s job current time : {}".format(time.ctime()))
    found_my_car = False  # NOTE: SAD
    for info in text:
        content = info.contents
        value = content[1].attrs.get('data-carcloudaccess-model')
        if which in value:
            found_my_car = True
            print(value)
    if found_my_car:
        client.publish(topic='admin/message/slack', payload="WHOOP BMW!")
        time.sleep(5)
        sys_exit(0)
    else: 
        print("Don't worry, let me try again")

if __name__ == '__main__':
    tl.start(block=True)