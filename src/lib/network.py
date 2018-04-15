#!/user/bin/env python
# -*- coding: utf-8 -*-

from . import crypto
from . import const
from . import sqlite
from . import block
from . import common
from . import schedule


import requests

def myEndpoint():
	n = sqlite.search("nodes", "publicKey", crypto.sk2pk(const.NODE.PRIVATE_KEY))[0]
	return n[0]

def nodes():
	nodes = sqlite.fetchAll("nodes")
	li = []
	for d in nodes:
		li.append({"endpoint":d[0], "publicKey":d[1], "address":d[2], "balance":d[3], "lastChecked":d[4]})
	nl = sorted(li, key=lambda x: x['publicKey'])
	return nl

def firstNode(rnl):
	firstNode = False
	for n in rnl:
		if common.epoch()-n['lastChecked']<300:
			firstNode = n
			break
	return firstNode

def rnl():
	# DBからノードリストを取得し、publicKeyでソートする
	# 最終ブロックのハッシュを用いて、ルーレット方式で順位を決める
	# ソートしたリストを返す
	# 生存確認はここでは行わない
	data = sqlite.fetchAll("nodes")
	for node in data:
		schedule.updateNodesDB(node[2]) # address
	nl = nodes()

	currentHeight = block.height()
	blockdatahash = block.blockHash(currentHeight)

	rnl = []
	t = common.epoch()//600
	while len(nl)>0:
		rouletteSum = 0
		roulette = []
		for i in range(len(nl)):
			pie = int(nl[i]['balance']/1000000)
			rouletteSum += pie
			roulette.extend([i]*pie)
		hit = crypto.b2long(crypto.sha256_from_byte(blockdatahash+crypto.int2b(0)+crypto.int2b(t))[0:8])%rouletteSum
		hitNode = nl[roulette[hit]]
		rnl.append(hitNode)
		nl.pop(roulette[hit])
	return rnl

def statusCheck():
	nl = nodes()
	for n in nl:
		# 3分おきに確認 3分以下ならチェックしない
		if common.epoch() - n["lastChecked"] < 180:
			continue
		try:
			r = requests.get(n['endpoint']+'/status')
			data = r.json()
			if block.height() == data['height']:
				sqlite.update("nodes", "address", n['address'], {"lastChecked":common.epoch()})
		except:
			sqlite.update("nodes", "address", n['address'], {"lastChecked":-1})

def announce(data, sig):
	print("announce start!!", flush=True)
	nl = nodes()

	c = 0 #送信成功回数

	for node in nl:
		if node['lastChecked'] < 0:
			print("skip", flush=True)
			continue
		# try:
		r = requests.post(node['endpoint']+'/transaction/receive-announce', json={"data":data, "signature":sig})
		print(r.json(), flush=True)
		c += 1
		# except Exception as e:
		# 	print(e)
	return c

def broadcast(data, sig):
	print("broadcast start!!", flush=True)
	publicKey = crypto.sk2pk(const.NODE.PRIVATE_KEY)
	nl = nodes()
	concatData = common.concat(const.PHASE.BROADCAST, publicKey, sig, data)
	concatDataSig = crypto.sign(concatData, const.NODE.PRIVATE_KEY)

	broadcastData = {
		'data':data,
		'signature':sig,
		'phase':const.PHASE.BROADCAST,
		'nodePublicKey':publicKey,
		'messageSignature':concatDataSig
	}

	c = 0 #送信成功回数

	for node in nl:
		if node['lastChecked'] < 0:
			print("skip", flush=True)
			continue
		# try:
		r = requests.post(node['endpoint']+'/block/receive-broadcast', json=broadcastData)
		if r:
			print(r.json(), flush=True)
		else:
			print(r)
		c += 1
		# except Exception as e:
		# 	print(e)
	return c

def preprepare(data, sig):
	print("preprepare start!!", flush=True)
	publicKey = crypto.sk2pk(const.NODE.PRIVATE_KEY)
	nl = nodes()

	concatData = common.concat(const.PHASE.PREPREPARE, publicKey, sig, data)
	concatDataSig = crypto.sign(concatData, const.NODE.PRIVATE_KEY)
	preprepareData = {
		'data':data,
		'signature':sig,
		'phase':const.PHASE.PREPREPARE,
		'nodePublicKey':publicKey,
		'messageSignature':concatDataSig
	}
	c = 0 #送信成功回数
	for node in nl:
		if node['lastChecked'] < 0:
			print("skip", flush=True)
			continue
		try:
			r = requests.post(node['endpoint']+'/block/receive-preprepare', json=preprepareData)
			print(r.json(), flush=True)
			c += 1
		except Exception as e:
			print(e)
	return c

def prepare(data, sig):
	print("prepare start!!", flush=True)
	publicKey = crypto.sk2pk(const.NODE.PRIVATE_KEY)
	nl = nodes()
	concatData = common.concat(const.PHASE.PREPARE, publicKey, sig, data)
	concatDataSig = crypto.sign(concatData, const.NODE.PRIVATE_KEY)
	prepareData = {
		'data':data,
		'signature':sig,
		'phase':const.PHASE.PREPARE,
		'nodePublicKey':publicKey,
		'messageSignature':concatDataSig
	}
	c = 0 #送信成功回数
	for node in nl:
		if node['lastChecked'] < 0:
			print("skip", flush=True)
			continue
		try:
			r = requests.post(node['endpoint']+'/block/receive-prepare', json=prepareData)
			print(r.json(), flush=True)
			c += 1
		except Exception as e:
			print(e)
	return c
