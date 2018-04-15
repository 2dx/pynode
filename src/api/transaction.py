#!/user/bin/env python
# -*- coding: utf-8 -*-
from bottle import get, post, route, request, HTTPResponse, abort
from api import api
from lib import *

@route('/transaction/<string>', method="OPTIONS")
def index(string):
	return api.responce({"status":"ok"})

@post('/transaction/encode')
def index():
	tx = request.json
	valid, _ = transaction.isValidJson(tx)
	print(tx)
	if not valid: return api.responce({'message':'failed', 'detail':_})
	data = transaction.encode(tx)
	resp = {
		'message':'ok',
		'data':data
	}
	return api.responce(resp)

@post('/transaction/decode') # for debug
def index():
	params = request.json
	tx = transaction.decode(params['data'])
	return api.responce({
		'message':'ok',
		'transactiont':tx
	})

@post('/transaction/sign') # for local only
def index():
	params = request.json
	sig = crypto.sign(params['data'], params['privateKey'])
	resp = {
		'message':'ok',
		'data':params['data'],
		'signature':sig
	}
	return api.responce(resp)

@post('/transaction/verify') # for debug
def index():
	params = request.json
	tx = transaction.decode(params['data'])
	valid = crypto.verify(params['signature'], params['data'], tx['signer'])
	resp = {
		'message':'ok',
		'valid':valid
	}
	return api.responce(resp)

@post('/transaction/announce')
def index():
	txs = sqlite.fetchAll("pool")
	if len(txs)>20:
		return api.responce({'message':'failed', 'detail':'NETWORK_OVER_LOADED'})
	params = request.json
	valid, _ = transaction.isValid(params['data'])
	if not valid: return api.responce({'message':'failed', 'detail':_})
	tx = transaction.decode(params['data'])
	valid = crypto.verify(params['signature'], params['data'], tx['signer'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_SIGNATURE'})

	txs.append([params['data'], params['signature']])
	transactions = []
	for tx_ in txs:
		transactions.append({"data":tx_[0], "signature":tx_[1]})
		if not block.balanceCheck(transactions):
			# バランスが不整合を起こすトランザクションはリジェクト
			return api.responce({'message':'failed', 'detail':'INSUFFICIENT_BALANCE'})

	network.announce(params['data'], params['signature'])
	return api.responce({'message':'ok'})

@post('/transaction/receive-announce')
def index():
	params = request.json
	valid, _ = transaction.isValid(params['data'])
	if not valid: return api.responce({'message':'failed', 'detail':_})
	tx = transaction.decode(params['data'])
	valid = crypto.verify(params['signature'], params['data'], tx['signer'])
	if not valid: return api.responce({'message':'failed', 'detail':'INVALID_SIGNATURE'})
	# TODO: 正当なトランザクションに正当な署名が付いているならpoolに追加する
	sqlite.insert("pool", (params['data'], params['signature'], tx['deadline']))
	return api.responce({'message':'ok'})
