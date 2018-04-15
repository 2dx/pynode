#!/user/bin/env python
# -*- coding: utf-8 -*-

from . import const
from datetime import datetime, timezone, timedelta
import time
from . import crypto

def epoch(delta=0):
    now = time.time()
    utc = datetime.fromtimestamp(now, timezone.utc)
    return int(utc.timestamp()+delta-const.CONST.EPOCH)

def concat(phase,pk,sig,data):
	if not len(pk)==(32*2): #32bytes
		print("invalid pk",flush=True)
	if not len(sig)==(64*2): #64bytes
		print("invalid sig",flush=True)
	concatData = crypto.int2hex(phase)+pk+sig+data
	return concatData