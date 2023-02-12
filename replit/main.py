from flask import Flask, request
from mint_functions import mint_nft, get_status, upload_filecoin_json, upload_filecoin
from threading import Thread
from time import sleep
from datetime import datetime
from pytz import timezone
import json
from twilio.rest import Client 
 
account_sid = 'AC10a3f10544c1369220c21a62b7df06cc'
auth_token = 'b6cc697a27cbf3637b41b6e6ef1e1954'

DM_LIST = ["+917044943188"]

app = Flask(__name__)

DEBUG = False
IMG_PATH = "./kobeni.png"

@app.route("/")
def index():
    return "OK"


@app.route("/mint", methods=["POST"])
def mint():
    data = request.get_json()
    print(data)
    if data is None:
        return "No data provided", 400
    name = data["name"]
    # description = data["description"]
    json_data = json.loads(data["json"])
    address = data["address"]

    # json_url = upload_filecoin_json(json_data)
    image_url = upload_filecoin(IMG_PATH)

    r1 = mint_nft(name, image_url, json.dumps(json_data), address)
    id_ = r1["result"]["id"]
    print(r1)
    r2 = get_status(id_)
    hash = r2["result"]["onChain"]["mintHash"]
    print(r2)
    return hash


def roj_8_baje():
    one_min = 60*60
    while True:
        now = datetime.now(timezone("Asia/Kolkata"))
        # print(now)
        if now.hour == 8 and now.minute == 1:
            print("8 BAJ GAYE")
            for number in DM_LIST:
                message = client.messages.create( 
                                      from_='whatsapp:+14155238886',  
                                      body=str(datetime.now(timezone("Asia/Kolkata")).strftime("%m/%d/%Y, %H:%M:%S")),  
                                      to='whatsapp:'+number 
                                  )
                sleep(1.05)
            sleep(one_min)

def har_ghante():
    one_hr = 60*60
    while True:
        print("EK GHANTA HO GAYA")
        sleep(one_hr)
        

if __name__ == "__main__":
    client = Client(account_sid, auth_token)
    ek_ghanta_wala = Thread(target=har_ghante)
    aath_baje_wala = Thread(target=roj_8_baje)
    ek_ghanta_wala.start()
    aath_baje_wala.start()
    app.run(host="0.0.0.0",port=8080,debug=DEBUG)

