#!/user/bin/env python
# -*- coding: utf-8 -*-
from bottle import get, post, route, request, HTTPResponse, abort
from api import api
from lib import *

@route('/block/<string>', method="OPTIONS")
def index(string):
	return api.responce({"status":"ok"})

@get('/block/genesis') # only for genesis block
def index():
	# block = request.json
	genesisSigner = {
		"privateKey": "991564b0fdafc8cf2af9ab076f3cf6f5205e19924d63e7058138e71ba813565a",
		"publicKey": "f60e73c1904c679e08d6614faf8b68b5e5b32134b3e38abeaba59350efb1cc42"
	}

	allocAddress = [
	"MR32CIQG3E3LWRPENK4I3VUT5NBJ2RJXENQJUXOD",
	"MRQFUFCXPEVCNGNWJNOQBOCACGSW4PLOX4OGG5F2",
	"MQPLQQXOD735AN7R7QBW37URN4TWNY7NPGTDOPE4",
	"MQEJCPXF4KB54DU3OXTZT6X6RUOPCA44TXUCYO4S",
	"MQONHGHSQB5HPBWGLBC4NLWM744TDLBBPUCJV6M7",
	"MQ47VJUDTUGQ7MNR54HUQSQF6E3U3A7G5US57QVV",
	"MSGH6SHYTUK32PBKNN73HF2CK6OP4ON5WF6ZK2V3",
	"MTDULSHJYGDBXK4BNZGZCYHIINT47TJMFK3BUBW4"
	]

	transactions = []
	for addr in allocAddress:
		tx = {
			"timeStamp": 0,
			"fee": 0,
			"recipient": addr,
			"type": const.TRANSACTION_TYPE.TRANSFER_TRANSACTION,
			"deadline": 3600,
			"message":
			{
				"payload": "initial allocation",
				"type": 0
			},
			"version": const.NODE.VERSION,
			"signer": genesisSigner['publicKey'],
			"mosaics":[
				{
					"id": "0000000000000000",
					"quantity": 100000000
				},
				{
					"id": "ffffffffffffffff",
					"quantity": 100000000
				}
			]
		}
		data = transaction.encode(tx)
		sig = crypto.sign(data, genesisSigner['privateKey'])
		transactions.append({"data":data, "signature":sig})

	bl = {
		"timeStamp": 0,
		"prevHash": "0000000000000000000000000000000000000000000000000000000000000000",
		"transactions": transactions,
		"version": const.NODE.VERSION,
		"signer": genesisSigner['publicKey'],
		"height": 0
	}
	data = block.encode(bl)
	sig = crypto.sign(data, genesisSigner['privateKey'])
	res = HTTPResponse(status=200, body=crypto.hex2b(data+sig))
	res.set_header('Content-Type', 'application/octet-stream')
	res.set_header('Content-Disposition', 'attachment; filename=block.0.b')
	return res

@post('/block/receive-broadcast')
def index():
	print("receive broadcast!!", flush=True)
	params = request.json
	# broadcastData = {
	# 	'data':data,
	# 	'signature':sig,
	# 	'phase':const.PHASE.BROADCAST,
	# 	'nodePublicKey':const.NODE.PUBLICK_KEY,
	# 	'messageSignature':concatDataSig
	# }

	# 1位のノードからの送信かを確認
	rnl = network.rnl()
	firstNode = network.firstNode(rnl)
	print(params['nodePublicKey'],firstNode['publicKey'])
	if params['nodePublicKey'] != firstNode['publicKey']:
		return api.responce({'message':'failed', 'detail':'INVELID_RANKED_NODE'})

	# メッセージ署名検証
	concatData = common.concat(const.PHASE.BROADCAST, params['nodePublicKey'], params['signature'], params['data'])
	valid = crypto.verify(params['messageSignature'], concatData, params['nodePublicKey'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_MESSAGE_SIGNATURE'})

	# ブロック署名検証
	bl = block.decode(params['data'])
	valid = crypto.verify(params['signature'], params['data'], bl['signer'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_BLOCK_SIGNATURE'})

	# ブロック高検証
	currentHeight = block.height()
	if bl['height'] != (currentHeight+1): return api.responce({'message':'failed', 'detail':'INVALID_BLOCK_HEIGHT'})

	# 確定済みのブロックと検証するブロック内のトランザクションの結果によって残高が負にならないかをチェック
	valid = block.balanceCheck(bl['transactions'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_BALANCE_RESULT'})


	# トランザクション検証
	for tx in bl['transactions']:
		valid, _ = transaction.isValid(tx['data'])
		if not valid: return api.responce({'message':'failed', 'detail':_})

	# 正当なトランザクションに正当な署名が付いており、正当なノードの署名付きであれば/transaction/preprepareへブロードキャストする
	network.preprepare(params['data'], params['signature'])
	return api.responce({'message':'ok'})

@post('/block/receive-preprepare')
def index():
	params = request.json
	print("receive preprepare!!", flush=True)
	# preprepareData = {
	# 	'data':data,
	# 	'signature':sig,
	# 	'phase':const.PHASE.PREPREPARE,
	# 	'nodePublicKey':const.NODE.PUBLICK_KEY,
	# 	'messageSignature':concatDataSig
	# }

	# 1位のノードからでなくて良い

	# メッセージ署名検証
	concatData = common.concat(const.PHASE.PREPREPARE, params['nodePublicKey'], params['signature'], params['data'])
	valid = crypto.verify(params['messageSignature'], concatData, params['nodePublicKey'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_MESSAGE_SIGNATURE'})

	# ブロック署名検証
	bl = block.decode(params['data'])
	valid = crypto.verify(params['signature'], params['data'], bl['signer'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_BLOCK_SIGNATURE'})

	# ブロック高検証
	currentHeight = block.height()
	if bl['height'] != (currentHeight+1): return api.responce({'message':'failed', 'detail':'INVALID_BLOCK_HEIGHT'})

	# トランザクション検証
	for tx in bl['transactions']:
		valid, _ = transaction.isValid(tx['data'])
		if not valid: return api.responce({'message':'failed', 'detail':_})

	# 確定済みのブロックと検証するブロック内のトランザクションの結果によって残高が負にならないかをチェック
	valid = block.balanceCheck(bl['transactions'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_BALANCE_RESULT'})

	# 正当なトランザクションに正当な署名が付いており、正当なノードの署名付きであれば、受信回数をインクリメントする
	# TODO increment
	updated = sqlite.update("preprepare", "nodePublicKey", params['nodePublicKey'], {"data":params['data'], "created":common.epoch()})
	if not updated:
		sqlite.insert("preprepare", (params['nodePublicKey'], params['data'], common.epoch()))
	li = sqlite.dataSearch("preprepare", params['data'])
	print("preprepare", len(li), flush=True)
	if len(li)>6: #受信回数が規定値を超えたら/transaction/prepareへブロードキャストする
		ret = network.prepare(params['data'], params['signature'])
	return api.responce({'message':'ok'})

@post('/block/receive-prepare')
def index():
	params = request.json
	print("receive prepare!!", flush=True)
	# prepareData = {
	# 	'data':data,
	# 	'signature':sig,
	# 	'phase':const.PHASE.PREPARE,
	# 	'nodePublicKey':const.NODE.PUBLICK_KEY,
	# 	'messageSignature':concatDataSig
	# }

	# 1位のノードからでなくて良い
		
	# メッセージ署名検証
	concatData = common.concat(const.PHASE.PREPARE, params['nodePublicKey'], params['signature'], params['data'])
	valid = crypto.verify(params['messageSignature'], concatData, params['nodePublicKey'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_MESSAGE_SIGNATURE'})

	# ブロック署名検証
	bl = block.decode(params['data'])
	valid = crypto.verify(params['signature'], params['data'], bl['signer'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_BLOCK_SIGNATURE'})

	# ブロック高検証
	currentHeight = block.height()
	if bl['height'] != (currentHeight+1): return api.responce({'message':'failed', 'detail':'INVALID_BLOCK_HEIGHT'})

	# トランザクション検証
	for tx in bl['transactions']:
		valid, _ = transaction.isValid(tx['data'])
		if not valid: return api.responce({'message':'failed', 'detail':_})

	# 確定済みのブロックと検証するブロック内のトランザクションの結果によって残高が負にならないかをチェック
	valid = block.balanceCheck(bl['transactions'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_BALANCE_RESULT'})

	# 正当なトランザクションに正当な署名が付いており、正当なノードの署名付きであれば、受信回数をインクリメントする
	# TODO increment
	updated = sqlite.update("prepare", "nodePublicKey", params['nodePublicKey'], {"data":params['data'], "created":common.epoch()})
	if not updated:
		sqlite.insert("prepare", (params['nodePublicKey'], params['data'], common.epoch()))
	li = sqlite.dataSearch("prepare", params['data'])
	print("prepare", len(li), flush=True)
	if len(li)>6: #受信回数が規定値を超えたらブロックを保存する
		print("save block", flush=True)
		block.writeBlock(bl['height'], params['data'])
		currentHeight = block.height()
		schedule.updateDB(currentHeight)
		# ブロックに含まれるトランザクションをpoolから削除する
		for tx in bl['transactions']:
			sqlite.delete("pool", "data", tx['data'])
	return api.responce({'message':'ok'})