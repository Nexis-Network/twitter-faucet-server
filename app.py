from flask import Flask,jsonify
from ntscraper import Nitter
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
scraper = Nitter()


# variables
rpc_url = os.getenv('RPC_URL')
chain_id = int(os.getenv('CHAIN_ID'))
airdrop_amount = float(os.getenv('AIRDROP_AMOUNT'))
sender_address = os.getenv('SENDER_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')

web3 = Web3(Web3.HTTPProvider(rpc_url))

if web3.is_connected():
    print("Connected to Nexis Network")
else:
    print("Connection failed")

def send_transaction(address):
    nonce = web3.eth.get_transaction_count(sender_address)
    amount = web3.to_wei(airdrop_amount, 'ether')
    gas_price = web3.eth.gas_price
    gas_limit = 21000

    transaction = {
        'nonce': nonce,
        'to': address,
        'value': amount,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId':chain_id
    }

    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        print(f"Transaction hash: {web3.to_hex(tx_hash)}")
        
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction receipt: {tx_receipt}")
        return True
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


@app.route('/faucet')
def hello_world():
    return 'Nexis Twitter Faucet v1'

@app.route('/search/<value>')
def search(value):
    tweets = scraper.get_tweets(str(value),mode='user',number=5)

    word = "@Nexis_Network"

    for tweet in tweets["tweets"]:
        if word in tweet["text"]:
            words_split = word.split(":")
            if len(words_split)>0:
                address = words_split[1].strip()
                tx_response = send_transaction(address)
                if tx_response:
                    return jsonify({
                        'sent':True,
                        'message':f"successfully sent"
                    })
                else: 
                    return jsonify({
                        'sent':False,
                        'message':f"user did not tweet"
                    })

    return jsonify({
        'sent':False,
        'message':f"user did not tweet"
    })



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5001)