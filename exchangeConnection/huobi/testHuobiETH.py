#!/usr/bin/env python
# -*- coding: utf-8 -*-


from utilETH import *
import huobiServiceETH

if __name__ == '__main__':
    print("get current balance")
    print(huobiServiceETH.get_balance())
