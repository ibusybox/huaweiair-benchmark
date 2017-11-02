#!/usr/bin/env python

# -*- coding: utf-8 -*-

import uuid
import sys
import logging
import time
import argparse
import requests

logger = logging.getLogger('huaweiair-benchmark')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def call_query_orders(host, times=None, interval=None, userid=None):
    url = "%s/huaweiair/v1/orders" % host
    userid = uuid.uuid4().hex if userid is None else userid
    times = sys.maxint if times is None else int(times)
    interval = 0.1 if interval is None else float(interval)
    playload = {'userId': userid}
    
    logger.info('start query orders with host: %s, times: %s, interval: %s, userid: %s', host, times, interval, userid)
    n = 0
    while n < times:
        try:
            response = requests.get(url, params=playload)
            logger.debug("query orders by url %s at times %s, got response %s", url, n, response.status_code)
        except Exception as e:
            logger.error('query orders by url %s at times %s with exception %s', url, n, e.message)
        time.sleep(interval)
        n = n + 1

def query_orders(args):
    parser = argparse.ArgumentParser(prog="huaweiair-benchmark")
    parser.add_argument('-s', '--host', dest='host',
                        help='host address, e.g: http://ip:port')
    parser.add_argument('-t', '--times', dest='times',
                        help='call times, 0 means infinity')
    parser.add_argument('-i', '--interval', dest='interval',
                        help='call intervals, 1 means 1s, 0.1 means 100 ms')
    parser.add_argument('-u', '--userid', dest='userid', help='user id')
    know_args = parser.parse_args(args)
    if know_args.host is None:
        parser.print_help()
        return

    call_query_orders(know_args.host, know_args.times, know_args.interval, know_args.userid)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logger.error('Usage: %s get-order|pay-order|create-order|delete-order [options]', sys.argv[0])
        sys.exit(1)
    command = sys.argv[1]
    args = sys.argv[2:]
    if command == "get-order":
        query_orders(args)
    else:
        logger.error('unknow command: %s', command)
