#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exchangeConnection.huobi.util import *
from utils.helper import *


def getAccountInfo(market, method):
    params = {"method": method}
    extra = {}
    extra['market'] = market
    res = send2api(params, extra)
    return res


def getOrders(coinType, market, method):
    params = {"method": method}
    params['coin_type'] = coinType
    extra = {}
    extra['market'] = market
    res = send2api(params, extra)
    return res



def getOrderInfo(coinType, id, market, method):
    params = {"method": method}
    params['coin_type'] = coinType
    params['id'] = id
    extra = {}
    extra['market'] = market
    res = send2api(params, extra)
    return res





def buy(coinType, price, amount, tradePassword, tradeid, market, method):
    params = {"method": method}
    params['coin_type'] = coinType
    params['price'] = price
    params['amount'] = amount
    extra = {}
    extra['trade_password'] = tradePassword
    extra['trade_id'] = tradeid
    extra['market'] = market
    res = send2api(params, extra)
    return res




def sell(coinType, price, amount, tradePassword, tradeid, market, method):
    params = {"method": method}
    params['coin_type'] = coinType
    params['price'] = price
    params['amount'] = amount
    extra = {}
    extra['trade_password'] = tradePassword
    extra['trade_id'] = tradeid
    extra['market'] = market
    res = send2api(params, extra)
    return res





def buyMarket(coinType, amount, tradePassword, tradeid, market, method):
    params = {"method": method}
    params['coin_type'] = coinType
    params['amount'] = amount
    extra = {}
    extra['trade_password'] = tradePassword
    extra['trade_id'] = tradeid
    extra['market'] = market
    res = send2api(params, extra)
    return res





def sellMarket(coinType, amount, tradePassword, tradeid, market, method):
    params = {"method": method}
    params['coin_type'] = coinType
    params['amount'] = amount
    extra = {}
    extra['trade_password'] = tradePassword
    extra['trade_id'] = tradeid
    extra['market'] = market
    res = send2api(params, extra)
    return res




def getNewDealOrders(coinType, market, method):
    params = {"method": method}
    params['coin_type'] = coinType
    extra = {}
    extra['market'] = market
    res = send2api(params, extra)
    return res




def getOrderIdByTradeId(coinType, tradeid, market, method):
    params = {"method": method}
    params['coin_type'] = coinType
    params['trade_id'] = tradeid
    extra = {}
    extra['market'] = market
    res = send2api(params, extra)
    return res





def cancelOrder(coinType, id, market, method):
    params = {"method": method}
    params['coin_type'] = coinType
    params['id'] = id
    extra = {}
    extra['market'] = market
    res = send2api(params, extra)
    return res




def getTicker(coinType, market):
    if market == COIN_TYPE_CNY:
        if coinType == HUOBI_COIN_TYPE_BTC:
            url = "http://api.huobi.com/staticmarket/ticker_btc_json.js"
        else:
            url = "http://api.huobi.com/staticmarket/ticker_ltc_json.js"
    elif market == COIN_TYPE_USD:
        if coinType == HUOBI_COIN_TYPE_BTC:
            url = "http://api.huobi.com/usdmarket/ticker_btc_json.js"
        else:
            raise ValueError("invalid coinType %d for market %s" % (coinType, market))
    else:
        raise ValueError("invalid market %s" % market)
    return httpRequest(url, {})




def getDepth(coinType, market, depth_size=5):
    if market == COIN_TYPE_CNY:
        if coinType == HUOBI_COIN_TYPE_BTC:
            url = "http://api.huobi.com/staticmarket/depth_btc_" + str(depth_size) + ".js"
        else:
            url = "http://api.huobi.com/staticmarket/depth_ltc_" + str(depth_size) + ".js"
    elif market == COIN_TYPE_USD:
        if coinType == HUOBI_COIN_TYPE_BTC:
            url = "http://api.huobi.com/usdmarket/depth_btc_" + str(depth_size) + ".js"
        else:
            raise ValueError("invalid coinType %d for market %s" % (coinType, market))
    else:
        raise ValueError("invalid market %s" % market)
    return httpRequest(url, {})




def getMinimumOrderQty(coinType):
    if coinType == HUOBI_COIN_TYPE_BTC:
        return 0.001
    else:
        return 0.01




def getMinimumOrderCashAmount():
    return 1
