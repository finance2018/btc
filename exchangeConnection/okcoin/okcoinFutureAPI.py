#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exchangeConnection.okcoin.httpMD5Util import buildMySign, httpGet, httpPost


class OKCoinFuture:
    def __init__(self, url, apikey, secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey

    def future_ticker(self, symbol, contractType):
        FUTURE_TICKER_RESOURCE = "/api/v1/future_ticker.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        return httpGet(self.__url, FUTURE_TICKER_RESOURCE, params)


    def future_depth(self, symbol, contractType, size):
        FUTURE_DEPTH_RESOURCE = "/api/v1/future_depth.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        if size:
            params += '&size=' + size if params else 'size=' + size
        return httpGet(self.__url, FUTURE_DEPTH_RESOURCE, params)


    def future_trades(self, symbol, contractType):
        FUTURE_TRADES_RESOURCE = "/api/v1/future_trades.do"
        params = ''
        if symbol:
            params += '&symbol=' + symbol if params else 'symbol=' + symbol
        if contractType:
            params += '&contract_type=' + contractType if params else 'contract_type=' + symbol
        return httpGet(self.__url, FUTURE_TRADES_RESOURCE, params)


    def future_index(self, symbol):
        FUTURE_INDEX = "/api/v1/future_index.do"
        params = ''
        if symbol:
            params = 'symbol=' + symbol
        return httpGet(self.__url, FUTURE_INDEX, params)


    def exchange_rate(self):
        EXCHANGE_RATE = "/api/v1/exchange_rate.do"
        return httpGet(self.__url, EXCHANGE_RATE, '')


    def future_estimated_price(self, symbol):
        FUTURE_ESTIMATED_PRICE = "/api/v1/future_estimated_price.do"
        params = ''
        if symbol:
            params = 'symbol=' + symbol
        return httpGet(self.__url, FUTURE_ESTIMATED_PRICE, params)


    def future_userinfo(self):
        FUTURE_USERINFO = "/api/v1/future_userinfo.do?"
        params = {}
        params['api_key'] = self.__apikey
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_USERINFO, params)


    def future_position(self, symbol, contractType):
        FUTURE_POSITION = "/api/v1/future_position.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_POSITION, params)


    def future_trade(self, symbol, contractType, price='', amount='', tradeType='', matchPrice='', leverRate=''):
        FUTURE_TRADE = "/api/v1/future_trade.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'amount': amount,
            'type': tradeType,
            'match_price': matchPrice,
            'lever_rate': leverRate
        }
        if price:
            params['price'] = price
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_TRADE, params)


    def future_batchTrade(self, symbol, contractType, orders_data, leverRate):
        FUTURE_BATCH_TRADE = "/api/v1/future_batch_trade.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'orders_data': orders_data,
            'lever_rate': leverRate
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_BATCH_TRADE, params)


    def future_cancel(self, symbol, contractType, orderId):
        FUTURE_CANCEL = "/api/v1/future_cancel.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_CANCEL, params)


    def future_orderinfo(self, symbol, contractType, orderId, status, currentPage, pageLength):
        FUTURE_ORDERINFO = "/api/v1/future_order_info.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'order_id': orderId,
            'status': status,
            'current_page': currentPage,
            'page_length': pageLength
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_ORDERINFO, params)


    def future_userinfo_4fix(self):
        FUTURE_INFO_4FIX = "/api/v1/future_userinfo_4fix.do?"
        params = {'api_key': self.__apikey}
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_INFO_4FIX, params)


    def future_position_4fix(self, symbol, contractType, type1):
        FUTURE_POSITION_4FIX = "/api/v1/future_position_4fix.do?"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'contract_type': contractType,
            'type': type1
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, FUTURE_POSITION_4FIX, params)
