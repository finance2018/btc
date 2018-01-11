#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exchangeConnection.bitvc.bitvcService import *
from utils.helper import *

a = BitVC()
print(a.assets())
print(a.list_orders(HUOBI_COIN_TYPE_BTC))  

b = BitVCFuture()
balance = b.balance(HUOBI_COIN_TYPE_BTC)  
dynamicRights = balance["dynamicRights"]
priceStruct = b.get_current_bitvc_future_deal_price()
dynamicRightsInRMB = float(priceStruct["last"]) * dynamicRights
print(dynamicRightsInRMB)

print(float(5.009))

print("%s" % float(5.009))
