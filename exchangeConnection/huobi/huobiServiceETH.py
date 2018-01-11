#!/usr/bin/env python
# -*- coding: utf-8 -*-


from utilETH import *

'''
Market data API
'''



def get_kline(symbol, period, long_polling=None):
    """
    :param symbol: optional：{ ethcny }
    :param period: optional:{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param long_polling: optional： { true, false }
    :return:
    """
    params = {'symbol': symbol,
              'period': period}

    if long_polling:
        params['long-polling'] = long_polling
    url = MARKET_URL + '/market/kline'
    return http_get_request(url, params)


	
def get_depth(symbol, type, long_polling=None):
    """
    :param symbol: optional:{ ethcny }
    :param type: optional:{ percent10, step0, step1, step2, step3, step4, step5 }
    :param long_polling: optional: { true, false }
    :return:
    """
    params = {'symbol': symbol,
              'type': type}

    if long_polling:
        params['long-polling'] = long_polling
    url = MARKET_URL + '/market/depth'
    return http_get_request(url, params)



def get_trade(symbol, long_polling=None):
    """
    :param symbol: optional:{ ethcny }
    :param long_polling: optional: { true, false }
    :return:
    """
    params = {'symbol': symbol}
    if long_polling:
        params['long-polling'] = long_polling
    url = MARKET_URL + '/market/trade'
    return http_get_request(url, params)



def get_detail(symbol, long_polling=None):
    """
    :param symbol: optional:{ ethcny }
    :param long_polling: optional: { true, false }
    :return:
    """
    params = {'symbol': symbol}
    if long_polling:
        params['long-polling'] = long_polling
    url = MARKET_URL + '/market/detail'
    return http_get_request(url, params)

'''
Trade/Account API
'''


def get_accounts():
    """
    :return: 
    """
    path = "/v1/account/accounts"
    params = {}
    return api_key_get(params, path)



def get_balance(acct_id=None):
    """
    :param acct_id
    :return:
    """

    if not acct_id:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id'];

    url = "/v1/account/accounts/{0}/balance".format(acct_id)
    params = {"account-id": acct_id}
    return api_key_get(params, url)



def orders(amount, source, symbol, _type, price=0):
    """
    
    :param amount: 
    :param source: 
    :param symbol: 
    :param _type: option {buy-market：, sell-market, buy-limit, sell-limit}
    :param price: 
    :return: 
    """
    accounts = get_accounts()
    acct_id = accounts['data'][0]['id'];

    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": source}
    if price:
        params["price"] = price

    url = "/v1/order/orders"
    return api_key_post(params, url)



def place_order(order_id):
    """
    
    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}/place".format(order_id)
    return api_key_post(params, url)



def cancel_order(order_id):
    """
    
    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}/submitcancel".format(order_id)
    return api_key_post(params, url)


	
def order_info(order_id):
    """
    
    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}".format(order_id)
    return api_key_get(params, url)


	
def order_matchresults(order_id):
    """
    
    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}/matchresults".format(order_id)
    return api_key_get(params, url)



def orders_list(symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    
    :param symbol: 
    :param states: optional: {pre-submitted , submitted, partial-filled , partial-canceled , filled , canceled }
    :param types: optional: {buy-market, sell-market, buy-limit, sell-limit}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: option: {prev, next }
    :param size: 
    :return: 
    """
    params = {'symbol': symbol,
              'states': states}

    if types:
        params[types] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/orders'
    return api_key_get(params, url)


def orders_matchresults(symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    
    :param symbol: 
    :param types: option: {buy-market, sell-market, buy-limit, sell-limit}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: option: {prev, next}
    :param size: 
    :return: 
    """
    params = {'symbol': symbol}

    if types:
        params[types] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    url = '/v1/order/matchresults'
    return api_key_get(params, url)



def get_withdraw_address(currency):
    """
    
    :param currency: 
    :return: 
    """
    params = {'currency': currency}
    url = '/v1/dw/withdraw-virtual/addresses'
    return api_key_get(params, url)



def withdraw(address_id, amount):
    """
    
    :param address_id: 
    :param amount: 
    :return: 
    """
    params = {'address-id': address_id,
              'amount': amount}
    url = '/v1/dw/withdraw-virtual/create'
    return api_key_post(params, url)



def place_withdraw(address_id):
    """
    
    :param address_id: 
    :return: 
    """
    params = {}
    url = '/v1/dw/withdraw-virtual/{0}/place'.format(address_id)
    return api_key_post(params, url)



def cancel_withdraw(address_id):
    """
    
    :param address_id: 
    :return: 
    """
    params = {}
    url = '/v1/dw/withdraw-virtual/{0}/cancel'.format(address_id)
    return api_key_post(params, url)
