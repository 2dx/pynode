#!/user/bin/env python
# -*- coding: utf-8 -*-

from . import crypto
from . import const
from . import sqlite
from . import transaction
from . import common

import requests

def balance(address, withUnconfirmed=False):
	res = sqlite.accountSearch(address) #[[XXXXXXXX_X_X","XXXXXXXXX"]]
	if withUnconfirmed:
		ptxs = sqlite.fetchAll("pool")
		for ptxdata in ptxs:
			ptx = transaction.decode(ptxdata[0])
			if crypto.pk2addr(ptx['signer']) == address:
				# もしpoolに残高計算対象のアドレスが送信元となっているトランザクションがあれば追加する。
				res.append([address+"_X_X_X",ptxdata[0]])
			if tx['type'] == const.TRANSACTION_TYPE.TRANSFER_TRANSACTION:
				if ptx['recipient'] == address:
					# もしpoolに残高計算対象のアドレスが受取人となっているトランザクションがあれば追加する。
					res.append([address+"_X_X_R",ptxdata[0]])

	balance = {'0000000000000000':0}
	vestedBalance = {'0000000000000000':0}
	for r in res:
		txtype = r[0].split('_')[3] # R or X
		tx = transaction.decode(r[1])
		vr = (1-0.9**((common.epoch()-tx['timeStamp'])/3600/24)) #24時間につき、未既得バランスの10%が加算される
		if txtype == "X":
			balance['0000000000000000'] -= tx['fee']
			vestedBalance['0000000000000000'] -= tx['fee']*vr
		if tx['type'] == const.TRANSACTION_TYPE.TRANSFER_TRANSACTION:
			for mosaic in tx['mosaics']:
				if not mosaic['id'] in balance:
					balance[mosaic['id']] = 0
				if txtype=="R":
					balance[mosaic['id']] += mosaic['quantity']
				else:
					balance[mosaic['id']] -= mosaic['quantity']
				if mosaic['id'] == '0000000000000000' or mosaic['id'] == 'ffffffffffffffff': # base.xmc / base.xa
					if not mosaic['id'] in vestedBalance:
						vestedBalance[mosaic['id']] = 0
					if txtype=="R":
						vestedBalance[mosaic['id']] += mosaic['quantity']*vr
					else:
						vestedBalance[mosaic['id']] -= mosaic['quantity']*vr
		if tx['type'] == const.TRANSACTION_TYPE.CERTIFICATE_DEFINITION_TRANSACTION:
			if crypto.pk2addr(tx['signer']) == address:
				supply = [x['value'] for x in tx['certificateDefinition']['properties'] if x['name'] == 'supply'][0]
				balance[tx['certificateDefinition']['id']] = int(supply)

	# slimBalance = {} # 残高0の証明書は含めない
	# for key in balance.keys():
	# 	if balance[key] > 0:
	# 		slimBalance.update({key: balance[key]})
	# balance = slimBalance

	return {"balance":balance, "vestedBalance":vestedBalance}

def tx(address, io="all", unconfirmed=False):
	data = []
	if not unconfirmed:
		res = sqlite.accountSearch(address) #[[XXXXXXXX_X_X_X","XXXXXXXXX"]]
	else:
		res = []
		ptxs = sqlite.fetchAll("pool")
		for ptxdata in ptxs:
			ptx = transaction.decode(ptxdata[0])
			if crypto.pk2addr(ptx['signer']) == address:
				# もしpoolに残高計算対象のアドレスが送信元となっているトランザクションがあれば追加する。
				res.append([address+"_X_X_X",ptxdata[0]])
			if ptx['recipient'] == address:
				# もしpoolに残高計算対象のアドレスが受取人となっているトランザクションがあれば追加する。
				res.append([address+"_X_X_R",ptxdata[0]])

	for r in res:
		tx = transaction.decode(r[1])
		if tx['type'] == const.TRANSACTION_TYPE.TRANSFER_TRANSACTION:
			if io == "incoming":
				if tx['recipient'] != address:
					continue
			if io == "outgoing":
				if crypto.pk2addr(tx['signer']) != address:
					continue

			if r[0].split('_')[3]=="R":
				txtype = "incoming"
			else:
				txtype = "outgoing"

			meta = {
				"height":r[0].split('_')[1],
				"index":r[0].split('_')[2],
				"type":txtype
			}
			data.append({"meta":meta, "transaction":tx})
	return data
