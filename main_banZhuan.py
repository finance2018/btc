#!/usr/bin/env python
# -*- coding: utf-8 -*-

from banZhuan.banZhuanStrategy import *
from utils.helper import *

if __name__ == "__main__":
    ################################################################################
    # trade for BTC 
    ################################################################################

    strat =BanZhuanStrategy(datetime.datetime.now(), 0.8, 1, 0.1, 60, helper.COIN_TYPE_BTC_CNY)

    start_strat(strat)