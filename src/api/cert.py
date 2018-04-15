#!/user/bin/env python
# -*- coding: utf-8 -*-
from bottle import get, post, route, request, HTTPResponse, abort
from api import api
from lib import *

@route('/cert/<string>', method="OPTIONS")
def index(string):
	return api.responce({"status":"ok"})

@get('/cert/info')
def index():
	certId=request.query.id or "0000000000000000"
	if certId == "0000000000000000":
		resp = {
		    "signer": "f60e73c1904c679e08d6614faf8b68b5e5b32134b3e38abeaba59350efb1cc42",
		    "version": 0,
		    "timeStamp": 0,
		    "certificateDefinition": {
		        "id": certId,
		        "name": "base.xct",
		        "description": "",
		        "properties": [{
					"name": "supply",
					"value": "1000000000"
				},{
					"name": "unit",
					"value": "XCT"
				}]
		    }
		}
	elif certId == "ffffffffffffffff":
		resp = {
		    "signer": "f60e73c1904c679e08d6614faf8b68b5e5b32134b3e38abeaba59350efb1cc42",
		    "version": 0,
		    "timeStamp": 0,
		    "certificateDefinition": {
		        "id": certId,
		        "name": "base.xa",
		        "description": "",
		        "properties": [{
					"name": "supply",
					"value": "1000000000"
				},{
					"name": "unit",
					"value": "XA"
				}]
		    }
		}
	else:
		certInfo = cert.info(certId)
		if len(certInfo)==0:
			return api.responce({"message":"failed", "detail":"NOT_FOUND"})
		resp = transaction.decode(certInfo[0][1])
		resp['certificateDefinition']['name'] = "cert."+resp['certificateDefinition']['name'] # cert.をプレフィックスとして付加

	return api.responce({"message":"ok", "cert":resp})

@get('/cert/newid')
def index():
	unusedid = cert.unusedid()
	# TODO: 未使用か否かのチェック
	return api.responce({"message":"ok", "id":unusedid})