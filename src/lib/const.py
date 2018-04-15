#!/user/bin/env python
# -*- coding: utf-8 -*-
import os

class VERSION():
	MAIN = 0x00
	TEST = 0x01

class TRANSACTION_TYPE():
	TRANSFER_TRANSACTION = 0
	AUTHORITY_DELEGATE_TRANSACTION = 1
	AUTHORITY_NAMING_TRANSACTION = 2
	CERTIFICATE_DEFINITION_TRANSACTION = 3

class CONST():
	EPOCH = 1519830000 # 2018/03/01 00:00:00 (Tokyo)

class NODE():
	PRIVATE_KEY = os.getenv("PRIVATE_KEY", "632b075ca9cd853a6174cc98dce6e6d75965884479bd9eb1b5df4ef415af22fd")
	SQLITE_PATH = "/root/blocks/db.sqlite3"
	BLOCK_PATH = "/root/blocks/"
	LOGFILE_PATH = "/root/blocks/debug.log"
	PID_PATH = "/tmp/daemon.pid"
	GENESIS_BLOCK_URL = "https://s3-ap-northeast-1.amazonaws.com/mochicoin/block.0.b"
	NODELIST_URL = "https://s3-ap-northeast-1.amazonaws.com/mochicoin/config.json"
	VERSION = VERSION.MAIN

class PHASE():
	BROADCAST = 0
	PREPREPARE = 1
	PREPARE = 2

# {
#     "privateKey": "05dd63061a33c9f73a889e0bb599948d20d61e13ade6c2145779eaa8ccd7016b",
#     "publicKey": "5922fbbee83af6a7f32a302067b8f999563e214c7461db7bf4cc3ca5a115b965",
#     "address": "NA2C3V2VEH6E4LBQDTSD4PLV2ZPLZNFB4U3DKN3F"
# }
