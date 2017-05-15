#!/usr/bin/env python
# coding:utf-8

import commands


def monitor():
    shell_command = 'sar -n DEV 1 3| egrep "^Average:.*(eth0|ens33)"'    # 默认只监控eth0/ens33网卡

    status, result = commands.getstatusoutput(shell_command)
    if status != 0:     # cmd exec error
        value_dic = {'status': status}
    else:
        # value_dic = {}
        IFACE, rxpcks, txpcks, rxKBs, txKBs, rxcmps, txcmps, rxmcsts, ifutil = result.split()[1:]
        value_dic= {
            'IFACE': IFACE,
            'in': rxpcks,       # 每秒接收包数量
            'out': txpcks,      # 每秒发送包数量
            'rxKBs': rxKBs,
            'txKBs': txKBs,
            'rxcmps': rxcmps,
            'txcmps': txcmps,
            'rxmcsts': rxmcsts,
            'ifutil': ifutil,
            'status': status
        }
    return value_dic

'''
    sar -n DEV 1 3| grep "^Average:.*eth0"
                 IFACE  rxpck/s  txpck/s  rxKB/s  txKB/s  rxcmp/s txcmp/s txcmp/s rxmcst/s
    ['Average:', 'eth0', '0.67', '0.67', '0.04', '0.05', '0.00', '0.00', '0.00', '0.00']


'''