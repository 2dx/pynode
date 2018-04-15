from gevent import monkey; monkey.patch_all()
from bottle import route, hook, run, HTTPResponse
from api import *
from lib import *

print("server started!", flush=True)


schedule.downloadGenesis()
schedule.initNodeEndpoint()

currentHeight = block.height()
for i in range(currentHeight+1):
	schedule.updateDB(i)

# hexdata = block.readBlock(0)
# print(hexdata)
# block = block.decode(hexdata)
# print(block)
# tx0 = transaction.decode(block['transactions'][0]['data'])
# print(tx0)

import threading
import requests
import time
def f():
	while True:
		try:
			time.sleep(10) # 10秒は最低でも待つ。
			r = requests.get('http://localhost:8080/trigger')
			# print(r.json(), flush=True)
		except:
			pass
th = threading.Thread(target=f,name="th",args=())
# スレッドthの作成　targetで行いたいメソッド,nameでスレッドの名前,argsで引数を指定する
th.setDaemon(True)
# thをデーモンに設定する。メインスレッドが終了すると、デーモンスレッドは一緒に終了する
th.start()
#スレッドの開始

@route('/trigger')
def index():
	print("CRON JOB TRIGGERED", flush=True)
	currentHeight = block.height()

	# 全てのトランザクションの投入 #TODO スパムへの対策.トランザクションがなければステータスチェックもしない。
	txs = sqlite.fetchAll("pool")
	if len(txs) == 0:
		print("zero transactions so block didn't generated", flush=True)
		return api.responce({'message': 'ok'})
	transactions = []
	for tx in txs[:10]:
		transactions.append({"data":tx[0], "signature":tx[1]})
		if not block.balanceCheck(transactions):
			# バランスが不整合を起こすトランザクションはブロックに含めず、poolDBからも削除する
			transactions.pop()
			sqlite.delete("pool", "data", tx[0])
			print("transaction discarded!")
	if len(transactions) == 0:
		print("zero transactions of valid balance so block didn't generated", flush=True)
		return api.responce({'message': 'ok'})



	network.statusCheck()

	# 最後の生存確認が4分以内で、かつ、成功しているノードは有効
	rnl = network.rnl()
	firstNode = network.firstNode(rnl)
	if not firstNode == False:
		if firstNode['publicKey'] == crypto.sk2pk(const.NODE.PRIVATE_KEY):
			print("I am the leader.", flush=True)

			# ブロックの生成
			blockdatahash = block.blockHash(currentHeight)

			bl = {
				"timeStamp": common.epoch(),
				"prevHash": blockdatahash,
				"transactions": transactions,
				"version": const.NODE.VERSION,
				"signer": crypto.sk2pk(const.NODE.PRIVATE_KEY),
				"height": currentHeight+1
			}
			data = block.encode(bl)

			# if 自分の作ったブロックが現在承認作業中ならパス。
			# 1.sqliteからpreprepareを読む
			# 2.自分のノードのdateを読んで、同一のdataをすでにpreprepareで発していたらパス。
			data_ = sqlite.search("preprepare", "nodePublicKey", crypto.sk2pk(const.NODE.PRIVATE_KEY))
			if len(data_)>0:
				if data == data_[0][1]:
					print("my block is in progress", flush=True)
					return api.responce({'message': 'ok'})

			sig = crypto.sign(data, const.NODE.PRIVATE_KEY)
			network.broadcast(data, sig)
			print("broadcasted!!", flush=True)
		else:
			print("I am not the leader. The leader is "+firstNode['endpoint'], flush=True)
	return api.responce({'message': 'ok'})

@route('/status')
def index():
	return api.responce({'message': 'ok', 'height': block.height()})

# run(host='0.0.0.0', port=8080)
run(host='0.0.0.0', port=8080, reloader=False, server='gevent')
