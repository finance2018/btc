#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exchangeConnection.okcoin.httpMD5Util import buildMySign, httpGet, httpPost
from utils.helper import *


class OKCoinSpot:
    def __init__(self, url, apikey, secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey


    def ticker(self, symbol=''):
        TICKER_RESOURCE = "/api/v1/ticker.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return httpGet(self.__url, TICKER_RESOURCE, params)


    def depth(self, symbol='', size=1):
        DEPTH_RESOURCE = "/api/v1/depth.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s&size=%(size)d' % {'symbol': symbol, 'size': size}
        return httpGet(self.__url, DEPTH_RESOURCE, params)

		
    def trades(self, symbol=''):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return httpGet(self.__url, TRADES_RESOURCE, params)


    def userInfo(self):
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params = {}
        params['api_key'] = self.__apikey
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, USERINFO_RESOURCE, params)


    def trade(self, symbol, tradeType, price='', amount=''):
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'type': tradeType
        }
        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount

        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, TRADE_RESOURCE, params)


    def batchTrade(self, symbol, tradeType, orders_data):
        BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'type': tradeType,
            'orders_data': orders_data
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, BATCH_TRADE_RESOURCE, params)


    def cancelOrder(self, symbol, orderId):
        CANCEL_ORDER_RESOURCE = "/api/v1/cancel_order.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, CANCEL_ORDER_RESOURCE, params)


    def orderInfo(self, symbol, orderId):
        ORDER_INFO_RESOURCE = "/api/v1/order_info.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDER_INFO_RESOURCE, params)


    def ordersInfo(self, symbol, orderId, tradeType):
        ORDERS_INFO_RESOURCE = "/api/v1/orders_info.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'order_id': orderId,
            'type': tradeType
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDERS_INFO_RESOURCE, params)


    def orderHistory(self, symbol, status, currentPage, pageLength):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'status': status,
            'current_page': currentPage,
            'page_length': pageLength
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDER_HISTORY_RESOURCE, params)


    def getMinimumOrderQty(self, symbol):
        if symbol == COIN_TYPE_BTC_CNY:
            return 0.01 * 1
        else:
            return 0.1 * 1
