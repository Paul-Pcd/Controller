#!/usr/bin/env python
# coding: utf-8

import load
import cpu
import memory


# 获取网卡带宽状态
def get_network_status():
    return load.monitor()


# 获取CPU状态
def get_cpu_status():
    return cpu.monitor()


# 获取内存状态
def get_memory_status():
    return memory.monitor()


