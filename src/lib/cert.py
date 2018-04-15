#!/user/bin/env python
# -*- coding: utf-8 -*-

from .crypto import b2hex, hex2b, b2int, int2b, b2long, long2b, b2string, string2b, sha256_from_hex
from . import const
from . import transaction
from . import account
from . import crypto
from . import sqlite


import random


def unusedid():
	result = [0]
	while len(result)>0:
		unusedid = "".join([random.choice('0123456789abcdef') for x in range(16)])
		if unusedid == "0000000000000000" or unusedid == "ffffffffffffffff":
			continue
		result = sqlite.search("certs", "id", unusedid)
	return unusedid

def info(certId):
	result = sqlite.search("certs", "id", certId)
	return result
