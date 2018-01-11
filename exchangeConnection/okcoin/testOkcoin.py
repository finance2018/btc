#!/usr/bin/env python
# -*- coding: utf-8 -*-


from exchangeConnection.okcoin.util import *


okcoinSpot = getOkcoinSpot()


okcoinFuture = getOkcoinFuture()

print(u' ticker ')
print(okcoinSpot.ticker('btc_cny'))

print(u' depth ')
print(okcoinSpot.depth('btc_cny'))

print(u' user info ')
print(okcoinSpot.userInfo())


print(u' user info ')
print(okcoinSpot.userInfo())

print(u' order query ')
print(type(okcoinSpot.orderInfo('btc_cny', '6122509921')))
print(okcoinSpot.orderInfo('btc_cny', '6122509921'))

print(u' order trade ')
# print (okcoinSpot.trade('btc_cny','buy_market','50'))

print(u' user info ')
print(type(okcoinSpot.userInfo()))
print(okcoinSpot.userInfo())


