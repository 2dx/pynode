# #!/user/bin/env python
# # -*- coding: utf-8 -*-
# @route('/structure/AccountInfo')
# def api():
# 	data = {
# 		"address": "TALICELCD3XPH4FFI5STGGNSNSWPOTG5E4DS2TOS",
# 		"balance": 124446551689680,
# 		"vestedBalance": 1041345514976241,
# 		"importance": 0.010263666447108395,
# 		"publicKey": "a11a1a6c17a24252e674d151713cdf51991ad101751e4af02a20c61b59f1fe1a",
# 		"label": null,
# 		"harvestedBlocks": 645,
# 		"multisigInfo": {}
# 	}
# 	return api.responce(data)

# @route('/structure/AccountMetaData')
# def api():
# 	data = {
# 		"status": "LOCKED",
# 		"remoteStatus": "ACTIVE",
# 		"cosignatoryOf" : [
# 			"<AccountInfo>",
# 			"<AccountInfo>"
# 		],
# 		"cosignatories" : [
# 			"<AccountInfo>",
# 			"<AccountInfo>"
# 		]
# 	}
# 	return api.responce(data)

# @route('/structure/AccountMetaDataPair')
# def api():
# 	data = {
# 		"account":
# 			"<AccountInfo>",
# 		"meta":
# 			"<AccountMetaData>"
# 	}
# 	return api.responce(data)

# @route('/structure/Block')
# def api():
# 	data = {
# 		"timeStamp": 9022656,
# 		"signature": "256ebcfa4f92e2881963359c51095a390b9f4d1b3fee75ae19f96d5e6bcf055abbcaae3e55bcc17e6214924e4e6a9ebbe77357236b1a235e944950b851bda804",
# 		"prevBlockHash":
# 		{
# 			"data": "0a3d6bea020bb1a503364c37d57392342f368389bb23b05799c54d536d94749b"
# 		},
# 		"type": 1,
# 		"transactions": [
# 			"Transaction1, Transaction2, …, Transaction11"
# 		],
# 		"version": 1744830465,
# 		"signer": "6c66ea288522990db7a0a63c9c20f532cdcb68dc3c9544fb20f7322c92ceadbb",
# 		"height": 39324
# 	}
# 	return api.responce(data)

# @route('/structure/BlockHeight')
# def api():
# 	data = {
# 		"height": 2649
# 	}
# 	return api.responce(data)

# @route('/structure/ExplorerBlockViewModel')
# def api():
# 	data = {
# 		"data":[
# 			{
# 				"txes":[
# 					"<ExplorerTransferViewModel>",
# 					"<ExplorerTransferViewModel>"
# 				],
# 				"block": "<Block>",
# 				"hash":"a6f62c62eedf4fafe6991e5cf31eae440963577c919f4eae86b4db8f8e572dce",
# 				"difficulty": 23456345897
# 			},
# 			{
# 				"txes":[
# 					"<ExplorerTransferViewModel>",
# 					"<ExplorerTransferViewModel>"
# 				],
# 				"block": "<Block>",
# 				"hash":"a6f62c62eedf4fafe6991e5cf31eae440963577c919f4eae86b4db8f8e572dce",
# 				"difficulty": 23456345897
# 			}
# 		]
# 	}
# 	return api.responce(data)


# @route('/structure/BlockHeight')
# def api():
# 	data = {
# 		"tx": "<Transaction>",
# 		"hash": "5cba4614e52af19417fb53c4bdf442a57b9f558aee17ece530a5220da55cf47d",
# 		"innerHash": "ae3b107f1216e1ccf12b6f3c3c555bc1d95311747338ce66f539ea2c18c0aa57"
# 	}
# 	return api.responce(data)


# @route('/structure/KeyPairViewModel')
# def api():
# 	data = {
# 		"privateKey": "0962c6505d02123c40e858ff8ef21e2b7b5466be12c4770e3bf557aae828390f",
# 		"publicKey": "c2e19751291d01140e62ece9ee3923120766c6302e1099b04014fe1009bc89d3",
# 		"address": "NCKMNCU3STBWBR7E3XD2LR7WSIXF5IVJIDBHBZQT"
# 	}
# 	return api.responce(data)


# @route('/structure/ImportanceTransferTransaction')
# def api():
# 	data = {
# 		"timeStamp": 9111526,
# 		"signature": "651a19ccd09c1e0f8b25f6a0aac5825b0a20f158ca4e0d78f2abd904a3966b6e3599a47b9ff199a3a6e1152231116fa4639fec684a56909c22cbf6db66613901",
# 		"fee": 150000,
# 		"mode": 1,
# 		"remoteAccount": "cc6c9485d15b992501e57fe3799487e99de272f79c5442de94eeb998b45e0144",
# 		"type": 2049,
# 		"deadline": 9154726,
# 		"version": 1744830465,
# 		"signer": "a1aaca6c17a24252e674d155713cdf55996ad00175be4af02a20c67b59f9fe8a"
# 	}
# 	return api.responce(data)


# @route('/structure/MosaicDefinitionCreationTransaction')
# def api():
# 	data = {
# 		"timeStamp": 9111526,
# 		"signature": "651a19ccd09c1e0f8b25f6a0aac5825b0a20f158ca4e0d78f2abd904a3966b6e3599a47b9ff199a3a6e1152231116fa4639fec684a56909c22cbf6db66613901",
# 		"fee": 150000,
# 		"type": 16385,
# 		"deadline": 9154726,
# 		"version": -1744830463,
# 		"signer": "cbda3edb771d42801a5c6ce0725f9374efade19a8933d6ac22ccfa50c777d0f9",
# 		"creationFee": 10000000,
# 		"creationFeeSink": "53e140b5947f104cabc2d6fe8baedbc30ef9a0609c717d9613de593ec2a266d3",
# 		"mosaicDefinition": {
# 			"creator": "cbda3edb771d42801a5c6ce0725f9374efade19a8933d6ac22ccfa50c777d0f9",
# 			"description": "precious vouchers",
# 			"name": "apple_B",
# 			"properties": [{
# 					"name": "divisibility",
# 					"value": "3"
# 				},{
# 					"name": "supply",
# 					"value": "1000"
# 				}
# 			]
# 		}
# 	}
# 	return api.responce(data)

# @route('/structure/MultisigAggregateModificationTransaction')
# def api():
# 	data = {
# 		"timeStamp": 9111526,
# 		"signature": "651a19ccd09c1e0f8b25f6a0aac5825b0a20f158ca4e0d78f2abd904a3966b6e3599a47b9ff199a3a6e1152231116fa4639fec684a56909c22cbf6db66613901",
# 		"fee": 500000,
# 		"type": 257,
# 		"deadline": 9154726,
# 		"version": 1744830466,
# 		"signer": "a1aaca6c17a24252e674d155713cdf55996ad00175be4af02a20c67b59f9fe8a",
# 		"modifications": [
# 			"<MultisigCosignatoryModification>",
# 			"<MultisigCosignatoryModification>"
# 		],
# 		"minCosignatories" : {
# 			"relativeChange" : 2
# 		}
# 	}
# 	return api.responce(data)

# @route('/structure/MultisigCosignatoryModification')
# def api():
# 	data = {
# 	"modificationType": 1,
# 	"cosignatoryAccount": "213150649f51d6e9113316cbec5bf752ef7968c1e823a28f19821e91daf848be"
# }
# 	return api.responce(data)

# @route('/structure/MultisigSignatureTransaction')
# def api():
# 	data = {
# 	"timeStamp": 9111526,
# 	"signature": "651a19ccd09c1e0f8b25f6a0aac5825b0a20f158ca4e0d78f2abd904a3966b6e3599a47b9ff199a3a6e1152231116fa4639fec684a56909c22cbf6db66613901",
# 	"fee": 150000,
# 	"type": 257,
# 	"deadline": 9154726,
# 	"version": -1744830463,
# 	"signer": "a1aaca6c17a24252e674d155713cdf55996ad00175be4af02a20c67b59f9fe8a",
# 	"otherHash": {
# 		"data": "44e4968e5aa35fe182d4def5958e23cf941c4bf809364afb4431ebbf6a18c039"
# 	},
# 	"otherAccount": "TDGIMREMR5NSRFUOMPI5OOHLDATCABNPC5ID2SVA"
# }

# 	return api.responce(data)

# @route('/structure/MultisigTransaction')
# def api():
# 	data = {
# 		"timeStamp": 9111526,
# 		"signature": "651a19ccd09c1e0f8b25f6a0aac5825b0a20f158ca4e0d78f2abd904a3966b6e3599a47b9ff199a3a6e1152231116fa4639fec684a56909c22cbf6db66613901",
# 		"fee": 150000,
# 		"type": 257,
# 		"deadline": 9154726,
# 		"version": -1744830463,
# 		"signer": "a1aaca6c17a24252e674d155713cdf55996ad00175be4af02a20c67b59f9fe8a",
# 		"otherTrans": "<inner transaction>",
# 		"signatures":[
# 			"<MultisigSignatureTransaction>",
# 			"<MultisigSignatureTransaction>"
# 		]
# 	}
# 	return api.responce(data)

# @route('/structure/TransferTransaction')
# def api():
# 	data = {
# 		"timeStamp": 9111526,
# 		"signature": "fad7ea2b5df5f7846f45fd9983a75ad8d333af3660f4f0d355864420f4482605d675e89d97177385338b226097342b4222add52c5397423f9eaf6b01fe3ef70c",
# 		"fee": 100000,
# 		"recipient": "TBEH27FNRS43FNH3PXE4XN3H7HXA37H77APSZW46",
# 		"type": 257,
# 		"deadline": 9154726,
# 		"message":
# 		{
# 			"payload": "74657374207472616e73616374696f6e",
# 			"type": 1
# 		},
# 		"version": -1744830462,
# 		"signer": "cb4ef3709d25ccd0c022b2d53e4ce31478ebc4bf177b1b54482afb8e55692521",
# 		"mosaics":[{
# 			"name": "name0",
# 			"quantity": 10
# 		},{
# 			"name": "name1",
# 			"quantity": 20
# 		}]
# 	}
# 	return api.responce(data)

# @route('/structure/Mosaic')
# def api():
# 	data = {
# 		"name": "orange juice",
# 		"quantity": 123000
# 	}
# 	return api.responce(data)

# @route('/structure/MosaicDefinition')
# def api():
# 	data = {
# 		"creator": "10cfe522fe23c015b8ab24ef6a0c32c5de78eb55b2152ed07b6a092121187100",
# 		"name": "orange juice",
# 		"description": "A healthy drink with lots of vitamins",
# 		"properties": [{
# 			"name": "divisibility",
# 			"value": "3"
# 		},{
# 			"name": "supply",
# 			"value": "1000"
# 		}]
# 	}
# 	return api.responce(data)

# @route('/structure/MosaicProperties')
# def api():
# 	data = {
# 		[{
# 			"name": "divisibility",
# 			"value": "3"
# 		},{
# 			"name": "supply",
# 			"value": "1000"
# 		}]
# 	}
# 	return api.responce(data)

# @route('/structure/AnnounceResult')
# def api():
# 	data = {
# 		"type": 4,
# 		"code": 6,
# 		"message": "status",
# 		"transactionHash": {
# 			"data":"c1786437336da077cd572a27710c40c378610e8d33880bcb7bdb0a42e3d35586"
# 		},
# 		"innerTransactionHash": {
# 			"data": "44e4968e5aa35fe182d4def5958e23cf941c4bf809364afb4431ebbf6a18c039"
# 		}
# 	}
# 	return api.responce(data)

# @route('/structure/RequestAnnounce')
# def api():
# 	data = {
# 		"data": "010100000100000000000000200000002b76078fa709bbe675\
# 2222b215abc7ec0152ffe831fb4f9aed3e7749a425900a0009\
# 3d0000000000000000002800000054444e46555946584f5353\
# 334e4e4c4f35465a5348535a49354c33374b4e514945485055\
# 4d584c54c0d45407000000000b00000001000000030000000c\
# 3215",
# 		"signature": "db2473513c7f0ce9f8de6345f0fbe773\
# dc687eb571123d08eab4d98f96849eae\
# b63fa8756fb6c59d9b9d0e551537c1cd\
# ad4a564747ff9291db4a88b65c97c10d"
# 	}
# 	return api.responce(data)

# @route('/structure/RequestPrepareAnnounce')
# def api():
# 	data = { 
# 	   "transaction": 
# 	   { 
# 			"timeStamp": 9111526, 
# 			"amount": 1000000000, 
# 			"fee": 50000,
# 			"recipient": "TDGIMREMR5NSRFUOMPI5OOHLDATCABNPC5ID2SVA", 
# 			"type": 257, 
# 			"deadline": 9154726, 
# 			"message": 
# 			{ 
# 				"payload": "74657374207472616e73616374696f6e", 
# 				"type": 1 
# 			}, 
# 			"version": -1744830463,
# 			"signer": "a1aaca6c17a24252e674d155713cdf55996ad00175be4af02a20c67b59f9fe8a" 
# 	   }, 
# 	   "privateKey": "68e4f79f886927de698df4f857de2aada41ccca6617e56bb0d61623b35b08cc0"
# 	}
# 	return api.responce(data)





















