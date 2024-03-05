from Crypto.PublicKey import RSA
from Crypto.IO import PEM
from Crypto.Cipher import PKCS1_OAEP

import json
import base64
from uvicorn import run
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from sys import argv
from magarmach import magarmach

HOST = "127.0.0.1"
PORT = int(argv[1])
KEY = "magarmachgang"

peer = argv[2]

instance = magarmach(peer)
instance.NewNode(f'{HOST}:{PORT}')

app = FastAPI()

@app.get("/")
def home():
    instance.NodeUpdate()
    instance.Consensus()
    return instance.chain

@app.get("/current_chain")
def current_chain():
    return instance.chain

@app.get("/createwallet")
def createwallet(data:str):
    try:
        json_data = json.loads(data)
        if "username" in json_data and "name" in json_data and "phone" in json_data and "sign" in json_data:

            RSAKEY = RSA.generate(2048)
            EnRSAKEY = PKCS1_OAEP.new(RSAKEY)

            cdata = EnRSAKEY.encrypt(data.encode())
            cdata = base64.b64encode(cdata)
            cdata = cdata.decode()

            return {
                    "publickey": RSAKEY.public_key().export_key().decode().replace("+","%2B"),
                    "privatekey": RSAKEY.export_key().decode().replace("+","%2B"),
                    "data": cdata.replace("+","%2B")
                    }
    except:
        return { "status": False }

@app.get("/lookup")
def verifysign(tx:str):
    for i in instance.chain:
        if i['hash'] == tx:
            return i
        else:
            return { status: False }

@app.get("/sign")
def sign(data:str):
    try:
        json_data = json.loads(data)
        if "publickey" in json_data and "privatekey" in json_data and "data" in json_data and "receiver" in data:
            pks = json_data["privatekey"]
            PKRSAKEY = RSA.importKey(pks)
            EnRSAKEY = PKCS1_OAEP.new(PKRSAKEY)


            ddata = EnRSAKEY.decrypt(base64.b64decode((json_data['data'].replace(" ","+").encode())))
            ddata = json.loads(ddata)
            
            raw_sender = json_data["publickey"]
            sender = raw_sender[0:26] + raw_sender[26:-24].replace(" ","+") + raw_sender[-24:]

            instance.Mine({"sender": sender, "receiver": json_data["receiver"], "senderinfo": { "name": ddata["name"], "sign": ddata["sign"] } })
        else:
            return { "status": False } 
    except:
        return { "status": 'd' }

@app.get("/nodes")
def nodes():
    return instance.nodes

@app.get("/addnode")
def addnode(peer:str):
    instance.AddNode(peer)
    return { "status" : 200 }

if __name__ == "__main__":
    run("api:app", host=HOST, port=PORT, reload=True)
