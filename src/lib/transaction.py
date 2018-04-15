#!/user/bin/env python
# -*- coding: utf-8 -*-

from .crypto import b2hex, hex2b, b2int, int2b, b2long, long2b, b2string, string2b, pk2addr
from . import const
from . import common
from . import block
from . import account
from . import cert

def isValidJson(json):
	try:
		if not isinstance(json['signer'], str):
			return False, "SIGNER_MUST_BE_STRING"
		if not isinstance(json['version'], int):
			return False, "VERSION_MUST_BE_INT"
		if not isinstance(json['timeStamp'], int):
			return False, "TIMESTAMP_MUST_BE_INT"
		if not isinstance(json['deadline'], int):
			return False, "DEADLINE_MUST_BE_INT"
		if not isinstance(json['type'], int):
			return False, "TYPE_MUST_BE_INT"
		if not isinstance(json['fee'], int):
			return False, "FEE_MUST_BE_INT"
		if len(json['signer'])!=64:
			return False, "INVALID_SIGNER_PUBLICKEY_LENGTH"
		if len(json['signer'].strip('0123456789abcdef'))!=0:
			return False, "SIGNER_PUBLICKEY_INCLUDES_ILLEGAL_CHARACTERS"
		if json['version']!=const.NODE.VERSION:
			return False, "INVALID_CHAIN_VERSION"

		if json['type'] == const.TRANSACTION_TYPE.TRANSFER_TRANSACTION:
			if not isinstance(json['recipient'], str):
				return False, "SIGNER_MUST_BE_STRING"
			if not "type" in json['message']:
				return False, "MESSAGE_MUST_CONTAIN_TYPE"
			if not "payload" in json['message']:
				return False, "MESSAGE_MUST_CONTAIN_PAYLOAD"
			if len(json['recipient'])!=40:
				return False, "INVALID_ADDRESS_LENGTH"
			# if not crypto.isValidAddress(json['recipient']):
			# 	return False, "INVALID_ADDRESS_CHECKSUM"
			if not isinstance(json['message']['type'], int):
				return False, "MESSAGE_TYPE_MUST_BE_INT"
			if not isinstance(json['message']['payload'], str):
				return False, "MESSAGE_PAYLOAD_MUST_BE_STRING"
			if not isinstance(json['mosaics'], list):
				return False, "MOSAICS_STRUCTURE_MUST_BE_LIST"
			for m in json['mosaics']:
				if not "id" in m:
					return False, "MOSAIC_STRUCTURE_MUST_CONTAIN_ID"
				if not "quantity" in m:
					return False, "MOSAIC_STRUCTURE_MUST_CONTAIN_QUANTITY"
				if not isinstance(m['id'], str):
					return False, "MOSAIC_ID_MUST_BE_HEXSTRING"
				if not isinstance(m['quantity'], int):
					return False, "MOSAIC_QUANTITY_MUST_BE_INT"
				if not (m['quantity']>0 and m['quantity']<1000000000):
					return False, "MOSAIC_QUANTITY_MUST_BE_0-1000000000"
		elif json['type'] == const.TRANSACTION_TYPE.CERTIFICATE_DEFINITION_TRANSACTION:
			json_ = json['certificateDefinition']
			if not isinstance(json_['id'], str):
				return False, "ID_MUST_BE_HEXSTRING"
			certInfo = cert.info(json_['id'])
			if len(certInfo)>0:
				return False, "DUPLICATED_CERT_ID"
			if len(json_['id'])!=16:
				return False, "INVALID_CERT_ID_LENGTH"
			if len(json_['id'].strip('0123456789abcdef'))!=0:
				return False, "CERT_ID_INCLUDES_ILLEGAL_CHARACTERS"
			if not isinstance(json_['name'], str):
				return False, "NAME_MUST_BE_STRING"
			if not isinstance(json_['description'], str):
				return False, "DESCRIPTION_MUST_BE_STRING"
			if not isinstance(json_['properties'], list):
				return False, "PROPERTIES_STRUCTURE_MUST_BE_LIST"
			for p in json_['properties']:
				if not "name" in p:
					return False, "PROPERTY_STRUCTURE_MUST_CONTAIN_NAME"
				if not "value" in p:
					return False, "PROPERTY_STRUCTURE_MUST_CONTAIN_VALUE"
				if not isinstance(p['name'], str):
					return False, "PROPERTY_NAME_MUST_BE_HEXSTRING"
				if not isinstance(p['value'], str):
					return False, "PROPERTY_VALUE_MUST_BE_INT"
				if not p['name'] in ["supply", "unit"]:
					return False, "PROPERTY_NAME_MUST_BE_UNIT_OR_SUPPLY"
				if p['name'] == "supply" and not isinstance(int(p['value']), int):
					return False, "PROPERTY_SUPPLY_MUST_BE_INTABLE_STRING"
				if p['name'] == "unit" and len(p['value'])>=16:
					return False, "PROPERTY_SUPPLY_LENGTH_MUST_BE_SHORTER_THAN_16"
		return True, True
	except:
		import traceback
		traceback.print_exc()
		return False, "FAILURE_TRANSACTION_INCOMPLETE"

def isValid(targetTxData):
	# 過去に同じdataを持つトランザクションが無いかを確認（timeStamp以降、かつ、現在までに生成されたブロックをすべて調べる）
	t = common.epoch()+3600
	height = block.height()
	try:
		targetTx = decode(targetTxData)
		valid, _ = isValidJson(targetTx)
		if not valid:
			return False, _
	except:
		import traceback
		traceback.print_exc()
		return False, "INVALID_DATA_STRUCTURE"
	while t > targetTx['timeStamp']:
		data = block.readBlock(height)
		bl = block.decode(data)
		t = bl['timeStamp']; height -= 1
		for tx in bl['transactions']:
			# ここで、過去のブロックに同じものがないかを確認する
			if tx['data'] == targetTxData:
				return False, "FAILURE_DUPURICATED_TRANSACTION"
	# 時刻の確認
	if targetTx['timeStamp'] > common.epoch():
		return False, "FAILURE_FUTURE_TIMESTAMP"
	if targetTx['deadline'] < common.epoch():
		return False, "FAILURE_PAST_DEADLINE"
	return True, ""

def encode(tx):
	b = b''
	b += hex2b(tx['signer'])
	b += int2b(tx['version'])
	b += int2b(tx['timeStamp'])
	b += int2b(tx['deadline'])
	b += int2b(tx['type'])
	b += long2b(tx['fee'])
	if tx['type'] == const.TRANSACTION_TYPE.TRANSFER_TRANSACTION:
		b += encode_TRANSFER_TRANSACTION(tx['recipient'], tx['message'], tx['mosaics'])
	elif tx['type'] == const.TRANSACTION_TYPE.CERTIFICATE_DEFINITION_TRANSACTION:
		b += encode_CERTIFICATE_DEFINITION_TRANSACTION(tx['certificateDefinition'])

	return b2hex(b)

def decode(hex):
	b = hex2b(hex)
	tx = {}
	c = 0
	tx['signer'] = b2hex(b[c:c+32]); c+=32
	tx['version'] = b2int(b[c:c+4]); c+=4
	tx['timeStamp'] = b2int(b[c:c+4]); c+=4
	tx['deadline'] = b2int(b[c:c+4]); c+=4
	tx['type'] = b2int(b[c:c+4]); c+=4
	tx['fee'] = b2long(b[c:c+8]); c+=8
	if tx['type'] == const.TRANSACTION_TYPE.TRANSFER_TRANSACTION:
		tx.update(decode_TRANSFER_TRANSACTION(b[c:]))
	if tx['type'] == const.TRANSACTION_TYPE.CERTIFICATE_DEFINITION_TRANSACTION:
		tx.update(decode_CERTIFICATE_DEFINITION_TRANSACTION(b[c:]))
	return tx

def encode_TRANSFER_TRANSACTION(recipient, message, mosaics):
	b = b''
	b += string2b(recipient)
	b += int2b(message['type'])
	tmp = string2b(message['payload'])
	b += int2b(len(tmp))+tmp
	b += int2b(len(mosaics))
	for mosaic in mosaics:
		b += hex2b(mosaic['id']) # 8bytes = 16 hex chars
		b += long2b(mosaic['quantity'])
	return b

def decode_TRANSFER_TRANSACTION(b):
	tx = {}
	c = 0
	tx['recipient'] = b2string(b[c:c+40]); c+=40
	tx['message'] = {}
	tx['message']['type'] = b2int(b[c:c+4]); c+=4
	messageLength = b2int(b[c:c+4]); c+=4
	tx['message']['payload'] = b2string(b[c:c+messageLength]); c+=messageLength
	mosaicNum = b2int(b[c:c+4]); c+=4
	mosaics = []
	for i in range(mosaicNum):
		mosaic = {}
		mosaic['id'] = b2hex(b[c:c+8]); c+=8
		mosaic['quantity'] = b2long(b[c:c+8]); c+=8
		mosaics.append(mosaic)
	tx['mosaics'] = mosaics
	return tx

def encode_CERTIFICATE_DEFINITION_TRANSACTION(certificateDefinition):
	b = b''
	b += hex2b(certificateDefinition['id'])
	tmp = string2b(certificateDefinition['name'])
	b += int2b(len(tmp))+tmp
	tmp = string2b(certificateDefinition['description'])
	b += int2b(len(tmp))+tmp
	b += int2b(len(certificateDefinition['properties']))
	for p in certificateDefinition['properties']:
		tmp = string2b(p['name'])
		b += int2b(len(tmp))+tmp
		tmp = string2b(p['value'])
		b += int2b(len(tmp))+tmp
	return b

def decode_CERTIFICATE_DEFINITION_TRANSACTION(b):
	tx = {}
	c = 0
	certificateDefinition = {}
	certificateDefinition['id'] = b2hex(b[c:c+8]); c+=8
	nameLength =  b2int(b[c:c+4]); c+=4
	certificateDefinition['name'] = b2string(b[c:c+nameLength]); c+=nameLength
	descriptionLength =  b2int(b[c:c+4]); c+=4
	certificateDefinition['description'] = b2string(b[c:c+descriptionLength]); c+=descriptionLength
	propertiesNum =  b2int(b[c:c+4]); c+=4
	properties = []
	for i in range(propertiesNum):
		prop = {}
		nameLength = b2int(b[c:c+4]); c+=4
		prop['name'] = b2string(b[c:c+nameLength]); c+=nameLength
		valueLength = b2int(b[c:c+4]); c+=4
		prop['value'] = b2string(b[c:c+valueLength]); c+=valueLength
		properties.append(prop)
	tx['certificateDefinition'] = certificateDefinition
	tx['certificateDefinition']['properties'] = properties
	return tx

# {
# 	"timeStamp": 892734924,
# 	"fee": 15,
# 	"type": Enum.TRANSACTION_TYPE.CERTIFICATE_DEFINITION_TRANSACTION,
# 	"deadline": 892738524,
# 	"version": Enum.VERSION.TESTNET,
# 	"signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
# 	"certificateDefinition": {
# 		"description": "this is apple (rank B) cerificate.",
# 		"name": "Apple_B.20170908"
# 		"properties": [{
# 				"name": "divisibility",
# 				"value": "3"
# 			},{
# 				"name": "supply",
# 				"value": "130"
# 			},{
# 				"name": "unit",
# 				"value": "kg"
# 			}
# 		]
# 	}
# }