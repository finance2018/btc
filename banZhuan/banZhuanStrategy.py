#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import logging

from common.Errors import StartRunningTimeEmptyError
from exchangeConnection.huobi import huobiService
from exchangeConnection.huobi.util import *
from exchangeConnection.okcoin.util import getOkcoinSpot
from utils import helper


class BanZhuanStrategy(object):
    def __init__(self, startRunningTime, orderRatio, timeInterval, orderWaitingTime, dataLogFixedTimeWindow,
                 coinMarketType,
                 dailyExitTime=None):
        self.startRunningTime = startRunningTime
        self.orderRatio = orderRatio  
        self.timeInterval = timeInterval  
        self.orderWaitingTime = orderWaitingTime  
        self.dataLogFixedTimeWindow = dataLogFixedTimeWindow  # in seconds
        self.coinMarketType = coinMarketType
        self.dailyExitTime = dailyExitTime
        self.TimeFormatForFileName = "%Y%m%d%H%M%S%f"
        self.TimeFormatForLog = "%Y-%m-%d %H:%M:%S.%f"
        self.okcoinService = getOkcoinSpot()
        self.huobiService = huobiService
        self.huobi_min_quantity = self.huobiService.getMinimumOrderQty(
            helper.coinTypeStructure[self.coinMarketType]["huobi"]["coin_type"])
        self.huobi_min_cash_amount = self.huobiService.getMinimumOrderCashAmount()
        self.okcoin_min_quantity = self.okcoinService.getMinimumOrderQty(
            helper.coinTypeStructure[self.coinMarketType]["okcoin"]["coin_type"])
        self.last_data_log_time = None

        # setup timeLogger
        self.timeLogger = logging.getLogger('timeLog')
        self.timeLogger.setLevel(logging.DEBUG)
        self.timeLogHandler = logging.FileHandler(self.getTimeLogFileName())
        self.timeLogHandler.setLevel(logging.DEBUG)
        self.consoleLogHandler = logging.StreamHandler()
        self.consoleLogHandler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.timeLogHandler.setFormatter(formatter)
        self.consoleLogHandler.setFormatter(formatter)

        self.timeLogger.addHandler(self.timeLogHandler)
        self.timeLogger.addHandler(self.consoleLogHandler)

        # setup dataLogger
        self.dataLogger = logging.getLogger('dataLog')
        self.dataLogger.setLevel(logging.DEBUG)
        self.dataLogHandler = logging.FileHandler(self.getDataLogFileName())
        self.dataLogHandler.setLevel(logging.DEBUG)
        self.dataLogger.addHandler(self.dataLogHandler)

    def getStartRunningTime(self):
        if self.startRunningTime == None:
            raise StartRunningTimeEmptyError("startRunningTime is not set yet!")
        return self.startRunningTime

    def getTimeLogFileName(self):
        return "log/%s_log_%s.txt" % (
            self.__class__.__name__, self.getStartRunningTime().strftime(self.TimeFormatForFileName))

    def getDataLogFileName(self):
        return "data/%s_data_%s.data" % (
            self.__class__.__name__, self.getStartRunningTime().strftime(self.TimeFormatForFileName))

    def timeLog(self, content):
        self.timeLogger.info(content)

    def getAccuntInfo(self):
        huobiAcct = self.huobiService.getAccountInfo(helper.coinTypeStructure[self.coinMarketType]["huobi"]["market"],
                                                     ACCOUNT_INFO)
        huobi_cny_cash = float(huobiAcct[u'available_cny_display'])
        huobi_cny_btc = float(huobiAcct[u'available_btc_display'])
        huobi_cny_ltc = float(huobiAcct[u'available_ltc_display'])
        huobi_cny_cash_loan = float(huobiAcct[u'loan_cny_display'])
        huobi_cny_btc_loan = float(huobiAcct[u'loan_btc_display'])
        huobi_cny_ltc_loan = float(huobiAcct[u'loan_ltc_display'])
        huobi_cny_cash_frozen = float(huobiAcct[u'frozen_cny_display'])
        huobi_cny_btc_frozen = float(huobiAcct[u'frozen_btc_display'])
        huobi_cny_ltc_frozen = float(huobiAcct[u'frozen_ltc_display'])
        huobi_cny_total = float(huobiAcct[u'total'])
        huobi_cny_net = float(huobiAcct[u'net_asset'])

        okcoinAcct = self.okcoinService.userinfo()
        okcoin_cny_cash = float(okcoinAcct["info"]["funds"]["free"]["cny"])
        okcoin_cny_btc = float(okcoinAcct["info"]["funds"]["free"]["btc"])
        okcoin_cny_ltc = float(okcoinAcct["info"]["funds"]["free"]["ltc"])
        okcoin_cny_cash_frozen = float(okcoinAcct["info"]["funds"]["freezed"]["cny"])
        okcoin_cny_btc_frozen = float(okcoinAcct["info"]["funds"]["freezed"]["btc"])
        okcoin_cny_ltc_frozen = float(okcoinAcct["info"]["funds"]["freezed"]["ltc"])
        okcoin_cny_total = float(okcoinAcct["info"]["funds"]["asset"]["total"])
        okcoin_cny_net = float(okcoinAcct["info"]["funds"]["asset"]["net"])
        total_net = huobi_cny_net + okcoin_cny_net
        return {
            "huobi_cny_cash": huobi_cny_cash,
            "huobi_cny_btc": huobi_cny_btc,
            "huobi_cny_ltc": huobi_cny_ltc,
            "huobi_cny_cash_loan": huobi_cny_cash_loan,
            "huobi_cny_btc_loan": huobi_cny_btc_loan,
            "huobi_cny_ltc_loan": huobi_cny_ltc_loan,
            "huobi_cny_cash_frozen": huobi_cny_cash_frozen,
            "huobi_cny_btc_frozen": huobi_cny_btc_frozen,
            "huobi_cny_ltc_frozen": huobi_cny_ltc_frozen,
            "huobi_cny_total": huobi_cny_total,
            "huobi_cny_net": huobi_cny_net,

            "okcoin_cny_cash": okcoin_cny_cash,
            "okcoin_cny_btc": okcoin_cny_btc,
            "okcoin_cny_ltc": okcoin_cny_ltc,
            "okcoin_cny_cash_frozen": okcoin_cny_cash_frozen,
            "okcoin_cny_btc_frozen": okcoin_cny_btc_frozen,
            "okcoin_cny_ltc_frozen": okcoin_cny_ltc_frozen,
            "okcoin_cny_total": okcoin_cny_total,
            "okcoin_cny_net": okcoin_cny_net,

            "total_net": total_net,
        }

    def dataLog(self, content=None):
        if content is None:
            accountInfo = self.getAccuntInfo()
            t = datetime.datetime.now()
            content = "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % \
                      (t.strftime(self.TimeFormatForLog),
                       accountInfo["huobi_cny_cash"],
                       accountInfo["huobi_cny_btc"],
                       accountInfo["huobi_cny_ltc"],
                       accountInfo["huobi_cny_cash_loan"],
                       accountInfo["huobi_cny_btc_loan"],
                       accountInfo["huobi_cny_ltc_loan"],
                       accountInfo["huobi_cny_cash_frozen"],
                       accountInfo["huobi_cny_btc_frozen"],
                       accountInfo["huobi_cny_ltc_frozen"],
                       accountInfo["huobi_cny_total"],
                       accountInfo["huobi_cny_net"],
                       accountInfo["okcoin_cny_cash"],
                       accountInfo["okcoin_cny_btc"],
                       accountInfo["okcoin_cny_ltc"],
                       accountInfo["okcoin_cny_cash_frozen"],
                       accountInfo["okcoin_cny_btc_frozen"],
                       accountInfo["okcoin_cny_ltc_frozen"],
                       accountInfo["okcoin_cny_total"],
                       accountInfo["okcoin_cny_net"],
                       accountInfo["total_net"])
            self.last_data_log_time = t
        self.dataLogger.info("%s" % str(content))

    def sell(self, security, quantity, exchange="huobi"):  # quantity is a string value
        if exchange == "huobi":
            self.timeLog("sell order of huobi...")
            self.timeLog("keep quantity 4 number of decimals...")
            self.timeLog("orient quantity:%s" % quantity)
            tmp = float(quantity)
            tmp = helper.downRound(tmp, 4)
            quantity = str(tmp)
            self.timeLog("quantity:%s" % quantity)
            if float(quantity) < self.huobi_min_quantity:
                self.timeLog(
                    "quantity:%s too samll to trade(huobi min:%f),ignore the signal" % (quantity, self.huobi_min_quantity))
                return None

            coin_type = helper.coinTypeStructure[self.coinMarketType]["huobi"]["coin_type"]
            res = self.huobiService.sellMarket(coin_type, quantity, None, None,
                                               helper.coinTypeStructure[self.coinMarketType]["huobi"]["market"],
                                               SELL_MARKET)
            if u"result" not in res or res[u"result"] != u'success':
                self.timeLog("huobi sell order failed（quantity：%s）!" % quantity)
                return None
            order_id = res[u"id"]
            # query order
            order_info = self.huobiService.getOrderInfo(coin_type, order_id,
                                                        helper.coinTypeStructure[self.coinMarketType]["huobi"][
                                                            "market"], ORDER_INFO)
            self.timeLog("huobi sell order, quantity：%s" % quantity)
            self.timeLog(str(order_info))
            if order_info["status"] != 2:
                self.timeLog("waiting %fs until finished" % self.orderWaitingTime)
                time.sleep(self.orderWaitingTime)
                order_info = self.huobiService.getOrderInfo(coin_type, order_id,
                                                            helper.coinTypeStructure[self.coinMarketType]["huobi"][
                                                                "market"], ORDER_INFO)
                self.timeLog(str(order_info))
            executed_qty = float(order_info["processed_amount"])
            self.timeLog(
                "huobi sell order, quantity：%f，cash：%.2f" % (executed_qty, executed_qty * float(order_info["processed_price"])))
            self.dataLog()
            return executed_qty
        elif exchange == "okcoin":
            self.timeLog("OK coin sell order...")
            self.timeLog("keep quantity 2 number of decimals...")
            self.timeLog("orient quantity:%s" % quantity)
            tmp = float(quantity)
            tmp = helper.downRound(tmp, 2)
            quantity = str(tmp)
            self.timeLog("quantity:%s" % quantity)
            if float(quantity) < self.okcoin_min_quantity:
                self.timeLog(
                    "quantity:%s too small to trade(huobi quantity:%f),ignore the signal" % (quantity, self.okcoin_min_quantity))
                return None
            res = self.okcoinService.trade(helper.coinTypeStructure[self.coinMarketType]["okcoin"]["coin_type"],
                                           "sell_market", amount=quantity)
            if "result" not in res or res["result"] != True:
                self.timeLog("okcoin sell order（quantity：%s）failed" % quantity)
                return None
            order_id = res["order_id"]
            # query order
            order_info = self.okcoinService.orderinfo(
                helper.coinTypeStructure[self.coinMarketType]["okcoin"]["coin_type"], str(order_id))
            self.timeLog("OKcoin sell order, quantity：%s" % quantity)
            self.timeLog(str(order_info))
            if order_info["orders"][0]["status"] != 2:
                self.timeLog("wait%.1fs until order finished" % self.orderWaitingTime)
                time.sleep(self.orderWaitingTime)
                order_info = self.okcoinService.orderinfo(
                    helper.coinTypeStructure[self.coinMarketType]["okcoin"]["coin_type"], str(order_id))
                self.timeLog(str(order_info))
            executed_qty = order_info["orders"][0]["deal_amount"]
            self.timeLog("okcoin sell order excuted，quantity：%f，cash：%.2f" % (
                executed_qty, executed_qty * order_info["orders"][0]["avg_price"]))
            self.dataLog()
            return executed_qty

    def buy(self, security, cash_amount, exchange="huobi", sell_1_price=None):  # cash_amount is a string value
        if exchange == "huobi":
            self.timeLog("start huobi buy order...")
            self.timeLog("keep quantity 2 number of decimals...")
            self.timeLog("orient cash:%s" % cash_amount)
            tmp = float(cash_amount)
            tmp = helper.downRound(tmp, 2)
            cash_amount = str(tmp)
            self.timeLog("cash:%s" % cash_amount)

            if float(cash_amount) < self.huobi_min_cash_amount:
                self.timeLog("cash:%s too samll to trade(huobi min:1Yuan),ignore the signal" % (cash_amount, self.huobi_min_cash_amount))
                return None

            coin_type = helper.coinTypeStructure[self.coinMarketType]["huobi"]["coin_type"]
            res = self.huobiService.buyMarket(coin_type, cash_amount, None, None,
                                              helper.coinTypeStructure[self.coinMarketType]["huobi"]["market"],
                                              BUY_MARKET)
            if u"result" not in res or res[u"result"] != u'success':
                self.timeLog("huobi buy order failed（cash：%s）failed！" % cash_amount)
                return None
            order_id = res[u"id"]
            # query order
            order_info = self.huobiService.getOrderInfo(coin_type, order_id,
                                                        helper.coinTypeStructure[self.coinMarketType]["huobi"][
                                                            "market"], ORDER_INFO)
            self.timeLog("huobi buy order, cash：%s" % cash_amount)
            self.timeLog(str(order_info))
            if order_info["status"] != 2:
                self.timeLog("waiting%fs until order finished" % self.orderWaitingTime)
                time.sleep(self.orderWaitingTime)
                order_info = self.huobiService.getOrderInfo(coin_type, order_id,
                                                            helper.coinTypeStructure[self.coinMarketType]["huobi"][
                                                                "market"], ORDER_INFO)
                self.timeLog(str(order_info))
            executed_qty = float(order_info["processed_amount"]) / float(order_info["processed_price"])
            self.timeLog("huobi buy order excuted, quantity：%f，cash：%.2f" % (executed_qty, float(order_info["processed_amount"])))
            self.dataLog()
            return executed_qty
        elif exchange == "okcoin":
            if sell_1_price is None:
                raise ValueError("need okcoin sell1, pls check sell_1_price!")
            self.timeLog("start okcoin buy order...")
            self.timeLog("keep quantity 2 number of decimals...")
            self.timeLog("orient cash:%s" % cash_amount)
            tmp = float(cash_amount)
            tmp = helper.downRound(tmp, 2)
            cash_amount = str(tmp)
            self.timeLog("cash:%s" % cash_amount)

            if float(cash_amount) < self.okcoin_min_quantity * sell_1_price:
                self.timeLog(
                    "cash:%s too small to trade(okcoin min:%f，sell1:%.2f,mincash：%.2f),ignore the signal" % (
                        cash_amount, self.okcoin_min_quantity, sell_1_price, self.okcoin_min_quantity * sell_1_price))
                return None
            res = self.okcoinService.trade(helper.coinTypeStructure[self.coinMarketType]["okcoin"]["coin_type"],
                                           "buy_market", price=cash_amount)

            if "result" not in res or res["result"] != True:
                self.timeLog("okcoin buy order（cash：%s）failed" % cash_amount)
                return None
            order_id = res["order_id"]
            # query order
            order_info = self.okcoinService.orderinfo(
                helper.coinTypeStructure[self.coinMarketType]["okcoin"]["coin_type"], str(order_id))
            self.timeLog("okcoin buy order cash：%s" % cash_amount)
            self.timeLog(str(order_info))
            if order_info["orders"][0]["status"] != 2:
                self.timeLog("wait%.1fs until order finished" % self.orderWaitingTime)
                time.sleep(self.orderWaitingTime)
                order_info = self.okcoinService.orderinfo(
                    helper.coinTypeStructure[self.coinMarketType]["okcoin"]["coin_type"], str(order_id))
                self.timeLog(str(order_info))
            executed_qty = order_info["orders"][0]["deal_amount"]
            self.timeLog("okcoin buy order excuted quantity：%f，cash：%.2f" % (
                executed_qty, executed_qty * order_info["orders"][0]["avg_price"]))
            self.dataLog()
            return executed_qty

    def go(self):
        self.timeLog("log start at: %s" % self.getStartRunningTime().strftime(self.TimeFormatForLog))
        self.dataLog(
            content="time|huobi_cny_cash|huobi_cny_btc|huobi_cny_ltc|huobi_cny_cash_loan|huobi_cny_btc_loan|huobi_cny_ltc_loan|huobi_cny_cash_frozen|huobi_cny_btc_frozen|huobi_cny_ltc_frozen|huobi_cny_total|huobi_cny_net|okcoin_cny_cash|okcoin_cny_btc|okcoin_cny_ltc|okcoin_cny_cash_frozen|okcoin_cny_btc_frozen|okcoin_cny_ltc_frozen|okcoin_cny_total|okcoin_cny_net|total_net")
        self.dataLog()

        while (True):
            # check whether current time is after the dailyExitTime, if yes, exit
            if self.dailyExitTime is not None and datetime.datetime.now() > datetime.datetime.strptime(
                                    datetime.date.today().strftime("%Y-%m-%d") + " " + self.dailyExitTime,
                    "%Y-%m-%d %H:%M:%S"):
                self.timeLog("end time：%s, now exiting..." % self.dailyExitTime)
                break

            self.timeLog("waiting %d s for next loop..." % self.timeInterval)
            time.sleep(self.timeInterval)

            # calculate the net asset at a fixed time window
            time_diff = datetime.datetime.now() - self.last_data_log_time
            if time_diff.seconds > self.dataLogFixedTimeWindow:
                self.dataLog()


            accountInfo = self.getAccuntInfo()


            huobiDepth = self.huobiService.getDepth(helper.coinTypeStructure[self.coinMarketType]["huobi"]["coin_type"],
                                                    helper.coinTypeStructure[self.coinMarketType]["huobi"]["market"],
                                                    depth_size=1)

            okcoinDepth = self.okcoinService.depth(helper.coinTypeStructure[self.coinMarketType]["okcoin"]["coin_type"])

            huobi_sell_1_price = huobiDepth["asks"][0][0]
            huobi_sell_1_qty = huobiDepth["asks"][0][1]
            huobi_buy_1_price = huobiDepth["bids"][0][0]
            huobi_buy_1_qty = huobiDepth["bids"][0][1]

            okcoin_sell_1_price = okcoinDepth["asks"][0][0]
            okcoin_sell_1_qty = okcoinDepth["asks"][0][1]
            okcoin_buy_1_price = okcoinDepth["bids"][0][0]
            okcoin_buy_1_qty = okcoinDepth["bids"][0][1]

            if huobi_buy_1_price > okcoin_sell_1_price:  
                self.timeLog("find the signal")
                self.timeLog("depth of huobi:%s" % str(huobiDepth))
                self.timeLog("depth of okcoin:%s" % str(okcoinDepth))


                Qty = helper.downRound(min(huobi_buy_1_qty, okcoin_sell_1_qty) * self.orderRatio, 4)
                # check security and cash
                Qty = min(Qty, accountInfo[helper.coinTypeStructure[self.coinMarketType]["huobi"]["coin_str"]],
                          helper.downRound(accountInfo[helper.coinTypeStructure[self.coinMarketType]["okcoin"][
                              "market_str"]] / okcoin_sell_1_price, 4))
                Qty = helper.downRound(Qty, 4)
                Qty = helper.getRoundedQuantity(Qty, self.coinMarketType)

                if Qty < self.huobi_min_quantity or Qty < self.okcoin_min_quantity:
                    self.timeLog(
                        "quantity:%f too small to trade(huobi:%f, okcoin:%f),ignore the signal" % (
                            Qty, self.huobi_min_quantity, self.okcoin_min_quantity))
                    continue
                else:
                    # step1: sell
                    executed_qty = self.sell(self.coinMarketType, str(Qty), exchange="huobi")
                    if executed_qty is not None:
                        # step2: buy
                        Qty2 = min(executed_qty, Qty)
                        Qty2 = max(helper.getRoundedQuantity(Qty2, self.coinMarketType), self.okcoin_min_quantity)

                    if Qty2 < self.okcoin_min_quantity * 1.05:
                        self.buy(self.coinMarketType, str(Qty2 * okcoin_sell_1_price * 1.05), exchange="okcoin",
                                 sell_1_price=okcoin_sell_1_price)
                    else:
                        self.buy(self.coinMarketType, str(Qty2 * okcoin_sell_1_price), exchange="okcoin",
                                 sell_1_price=okcoin_sell_1_price)

            elif okcoin_buy_1_price > huobi_sell_1_price: 
                self.timeLog("find signal")
                self.timeLog("depth of huobi:%s" % str(huobiDepth))
                self.timeLog("depth of okcoin:%s" % str(okcoinDepth))


                Qty = helper.downRound(min(huobi_sell_1_qty, okcoin_buy_1_qty) * self.orderRatio, 4)

                Qty = min(Qty, accountInfo[helper.coinTypeStructure[self.coinMarketType]["okcoin"]["coin_str"]],
                          helper.downRound(accountInfo[helper.coinTypeStructure[self.coinMarketType]["huobi"][
                              "market_str"]] / huobi_sell_1_price), 4)
                Qty = helper.getRoundedQuantity(Qty, self.coinMarketType)

                if Qty < self.huobi_min_quantity or Qty < self.okcoin_min_quantity:
                    self.timeLog("quantity:%f too small to trade(huobi:%f, okcoin:%f),ignore the signal" % (
                        Qty, self.huobi_min_quantity, self.okcoin_min_quantity))
                    continue
                else:
                    executed_qty = self.sell(self.coinMarketType, str(Qty), exchange="okcoin")
                    if executed_qty is not None:
                        Qty2 = min(executed_qty, Qty)
                        self.buy(self.coinMarketType, str(Qty2 * huobi_sell_1_price), exchange="huobi")
