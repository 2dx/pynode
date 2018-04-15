# -*- coding: utf-8 -*-

from . import block
from . import crypto
from . import const
from . import sqlite
from . import account
from . import common
from . import transaction
import requests
import shutil
import json

def initNodeEndpoint():
	r = requests.get(const.NODE.NODELIST_URL, headers={"content-type": "application/json"})
	data = r.json()
	for d in data:
		address = crypto.pk2addr(d['publicKey'])
		updated = sqlite.update("nodes", "address", address, {"publicKey":d['publicKey'], "endpoint":d['endpoint'], "lastChecked":common.epoch()})
		if not updated:
			sqlite.insert("nodes", (d['endpoint'], d['publicKey'], address, 0, common.epoch()))
	


def updateDB(height):
	hexdata = block.readBlock(height)
	bl = block.decode(hexdata)
	needToUpdateNodes = []
	for i in range(len(bl['transactions'])):
		tx = transaction.decode(bl['transactions'][i]['data'])
		txid = crypto.pk2addr(tx['signer'])+'_'+str(height)+'_'+str(i)+'_X'
		data = bl['transactions'][i]['data']
		sqlite.insert("transactions", (txid, data))
		if tx['type'] == const.TRANSACTION_TYPE.TRANSFER_TRANSACTION:
			txid = tx['recipient']+'_'+str(height)+'_'+str(i)+'_R'
			data = bl['transactions'][i]['data']
			sqlite.insert("transactions", (txid, data))
			for mosaic in tx['mosaics']:
				if mosaic['id'] == 'ffffffffffffffff':
					needToUpdateNodes.append(tx['recipient'])
		if tx['type'] == const.TRANSACTION_TYPE.CERTIFICATE_DEFINITION_TRANSACTION:
			certId = tx['certificateDefinition']['id']
			data = bl['transactions'][i]['data']
			sqlite.insert("certs", (certId, data))
	for address in needToUpdateNodes:
		updateNodesDB(address)
					
	return 0

def updateNodesDB(nodeAddress):
	balance = account.balance(nodeAddress)
	updated = sqlite.update("nodes", "address", nodeAddress, {"balance":balance["vestedBalance"]['ffffffffffffffff']})
	if not updated:
		sqlite.insert("nodes", ("ENDPOINT_UNKNOWN", "PUBLIC_KEY_UNKNOWN", nodeAddress, balance["vestedBalance"]['ffffffffffffffff'],common.epoch()))
	return 0

def downloadGenesis():
	if block.height() == -1:
		res = requests.get(const.NODE.GENESIS_BLOCK_URL, stream=True)
		with open(const.NODE.BLOCK_PATH+"block.0.b","wb") as fp:
			shutil.copyfileobj(res.raw,fp)
		updateDB(0)