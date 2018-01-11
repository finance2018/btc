#!/usr/bin/env python
# -*- coding: utf-8 -*-



import exchangeConnection.huobi.huobiService as HuobiService
from exchangeConnection.huobi.util import *
from utils.helper import *

if __name__ == "__main__":
    print("get account info")
    print(HuobiService.getAccountInfo("cny", ACCOUNT_INFO))

    print(HuobiService.getAccountInfo("usd", ACCOUNT_INFO))

    print("real time market")
    t = HuobiService.getTicker(HUOBI_COIN_TYPE_BTC, "cny")
    print(t)


    print("get depth")
    print(HuobiService.getDepth(HUOBI_COIN_TYPE_BTC, "cny", depth_size=1))

    print('order execution status')
    print(HuobiService.getOrderInfo(HUOBI_COIN_TYPE_LTC, 326711967, "cny", ORDER_INFO))


