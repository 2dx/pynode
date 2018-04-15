#!/user/bin/env python
# -*- coding: utf-8 -*-
from bottle import get, post, route, request, HTTPResponse, abort
from api import api
from lib import *

@route('/account/<string>', method="OPTIONS")
def index(string):
	return api.responce({"status":"ok"})

@get('/account/generate') # only for local
def index():
	sk = crypto.sk()
	pk = crypto.sk2pk(sk)
	addr = crypto.pk2addr(pk)
	resp = {
		"privateKey": sk,
		"publicKey": pk,
		"address": addr
	}
	return api.responce(resp)

@get('/account/get')
def index():
	addr=request.query.address or ""
	balance = account.balance(addr)
	resp = {
		"address": addr,
		"balance": balance['balance'],
		"vestedBalance": balance['vestedBalance'],
		"importance": 0.010263666447108395,
		"publicKey": "a11a1a6c17a24252e674d151713cdf51991ad101751e4af02a20c61b59f1fe1a",
		"harvestedBlocks": 645,
		"multisigInfo": {},
		"MOCK":True
	}
	return api.responce(resp)

@get('/account/get/from-publicKey')
def index():
	publicKey=request.query.publicKey or ""
	addr=crypto.pk2addr(publicKey)
	balance = account.balance(addr)
	resp = {
		"address": addr,
		"balance": balance['balance'],
		"vestedBalance": balance['vestedBalance'],
		"importance": 0.010263666447108395,
		"publicKey": "a11a1a6c17a24252e674d151713cdf51991ad101751e4af02a20c61b59f1fe1a",
		"harvestedBlocks": 645,
		"multisigInfo": {},
		"MOCK":True
	}
	return api.responce(resp)

@get('/account/transfers/<io>')
def index(io):
	if io != "incoming" and io != "outgoing" and io != "all":
		abort(404, "Not found: '/account/transflers/"+io+"'")
	addr = request.query.address
	txStructures = account.tx(addr, io=io)
	resp = {
		"data": txStructures
	}
	return api.responce(resp)

@get('/account/unconfirmed-transfers/<io>')
def index(io):
	if io != "incoming" and io != "outgoing" and io != "all":
		abort(404, "Not found: '/account/transflers/"+io+"'")
	addr = request.query.address
	txStructures = account.tx(addr, io=io, unconfirmed=True)
	resp = {
		"data": txStructures
	}
	return api.responce(resp)