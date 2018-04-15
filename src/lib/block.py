#!/user/bin/env python
# -*- coding: utf-8 -*-

from .crypto import b2hex, hex2b, b2int, int2b, b2long, long2b, b2string, string2b, sha256_from_hex
from . import const
from . import transaction
from . import account
from . import crypto


def readBlock(height):
	fin = open(const.NODE.BLOCK_PATH+'block.'+str(height)+'.b', 'rb')
	bdata = fin.read()
	fin.close()
	return b2hex(bdata)

def writeBlock(height, data):
	fout = open(const.NODE.BLOCK_PATH+'block.'+str(height)+'.b', 'wb')
	fout.write(hex2b(data))
	fout.close()
	return 0

def encode(bl):
	b = b''
	b += hex2b(bl['signer'])
	b += int2b(bl['version'])
	b += int2b(bl['height'])
	b += int2b(bl['timeStamp'])
	b += hex2b(bl['prevHash'])
	b += int2b(len(bl['transactions']))
	for tx in bl['transactions']:
		txStructure = hex2b(tx['data']+tx['signature'])
		b += int2b(len(txStructure))
		b += txStructure
	return b2hex(b)

def decode(hex):
	b = hex2b(hex)
	bl = {}
	c = 0
	bl['signer'] = b2hex(b[c:c+32]); c+=32
	bl['version'] = b2int(b[c:c+4]); c+=4
	bl['height'] = b2int(b[c:c+4]); c+=4
	bl['timeStamp'] = b2int(b[c:c+4]); c+=4
	bl['prevHash'] = b2hex(b[c:c+32]); c+=32
	txnum = b2int(b[c:c+4]); c+=4
	transactions = []
	for i in range(txnum):
		txStructureLength = b2int(b[c:c+4]); c+=4
		txStructure = b2hex(b[c:c+txStructureLength]); c+=txStructureLength
		transactions.append({"data": txStructure[:-128], "signature":txStructure[-128:]}) # 64byte = 128 hex chars
	bl['transactions'] = transactions
	return bl

def height():
	import glob
	count = -1
	files = glob.glob(const.NODE.BLOCK_PATH+"block.*.b")
	for i in range(len(files)):
		if const.NODE.BLOCK_PATH+"block."+str(i)+".b" in files:
			count += 1
		else:
			return count
	return count

def blockHash(height):
	datahex = readBlock(height)
	blockdatahash = sha256_from_hex(datahex)
	return blockdatahash

def balanceCheck(transactions):
	# まず、setを使ってブロック中のトランザクションの送信元を重複なくリストアップする
	# 次にsetをイテレート(address)して、そのループの中で更にトランザクションをイテレート(tx)する
	# address == txの送信者アドレス　なら、addressの残高を更新する
	# マイナスになった時点でエラーを返す
	addresses = set()
	for tx_ in transactions:
		tx = transaction.decode(tx_['data'])
		address = crypto.pk2addr(tx['signer'])
		addresses.add(address)
	for address in addresses:
		balance = account.balance(address)['balance']
		for tx_ in transactions:
			tx = transaction.decode(tx_['data'])
			senderAddress = crypto.pk2addr(tx['signer'])
			if address == senderAddress:
				# 残高の更新
				balance['0000000000000000'] -= tx['fee']
				if tx['type'] == const.TRANSACTION_TYPE.TRANSFER_TRANSACTION:
					for mosaic in tx['mosaics']:
						if not mosaic['id'] in balance:
							balance[mosaic['id']] = 0
						balance[mosaic['id']] -= mosaic['quantity']
		for mosaicName in balance.keys():
			if balance[mosaicName] < 0:
				print("BALANCE_ERROR", mosaicName)
				return False
	return True
