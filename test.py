import requests
from src.lib import const, common
import random

transaction = {
	"timeStamp": common.epoch(),
	"fee": 15,
	"recipient": "MQPLQQXOD735AN7R7QBW37URN4TWNY7NPGTDOPE4",
	"type": const.TRANSACTION_TYPE.TRANSFER_TRANSACTION,
	"deadline": common.epoch()+3600,
	"message":
	{
		"payload": "benchmark test",
		"type": 1
	},
	"version": const.NODE.VERSION,
	"signer": "80f251095087d52a809bc772eb678db9c4458e44019b815fd19e684c8b38575d",
	"mosaics":[
		{
			"id": "bd6e317f15b36c70",
			"quantity": 100
		}
	]
}

# endpoint = 'http://localhost:4000'
endpoint = 'http://nis.imagic.me:4000'
submitData = []
n = 80
for i in range(n):
	transaction['message']['payload'] = "benchmark test"+str(i)
	transaction['mosaics'][0]['quantity'] = i+1#random.randrange(100,200)
	r = requests.post(endpoint+'/transaction/encode', json=transaction)
	print(r)
	try:
		print(r.json())
	except:
		pass

	r = requests.post(endpoint+'/transaction/sign', json={"data":r.json()["data"], "privateKey":"632b075ca9cd853a6174cc98dce6e6d75965884479bd9eb1b5df4ef415af22fd"})
	print(r)
	try:
		print(i, r.json())
	except:
		pass

	submitData.append({"data":r.json()["data"], "signature":r.json()["signature"]})

for i in range(n):
	r = requests.post(endpoint+'/transaction/announce', json=submitData[i])
	print("try of ",i,r)
	try:
		print(r.json())
	except:
		pass
