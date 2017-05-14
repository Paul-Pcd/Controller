#!/usr/bin/env python
# coding:utf-8

import commands


def monitor():
    shell_command = "free -m | egrep '(Mem|Swap)'"
    status, result = commands.getstatusoutput(shell_command)
    if status != 0:     # cmd exec error
        value_dic = {'status': status}
    else:
        result = result.split()
        mem_total, mem_use = float(result[1]), float(result[2])
        swap_total, swap_use = float(result[8]), float(result[9])
        mem_usage = mem_use * 100 / mem_total
        swap_usage = swap_use * 100 / swap_total
        value_dic = {
            'mem_total': mem_total,
            'mem_use': mem_use,
            'swap_total': swap_total,
            'swap_use': swap_use,
            'mem_usage': mem_usage,
            'swap_usage': swap_usage,
            'status': status,
        }
    return value_dic
