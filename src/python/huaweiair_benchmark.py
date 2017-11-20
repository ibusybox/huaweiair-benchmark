# -*- coding: utf-8 -*-
#!/usr/bin/env python

import uuid
import sys
import logging
import time
import argparse
import datetime
import json
import requests
import urllib

logger = logging.getLogger('huaweiair-benchmark')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

STAT_INTERVAL = 100
SRC_MICROSERVICE = {'x-ces-src-microservice': 'gateway'}

def call_query_orders(host, times=None, interval=None, userid="uid0@email.com"):
    url = "%s/orders/huaweiair/v1/orders" % host
    userid = "uid0@email.com" if userid is None else userid
    times = sys.maxint if times is None or int(times) == 0 else int(times)
    interval = 0 if interval is None else float(interval)
    playload = {'userId': userid}
    
    logger.info('start query orders with host: %s, times: %s, interval: %s, userid: %s', host, times, interval, userid)

    cookie = login(host)
    if cookie is None:
        logger.error("login failure")
        return

    headers = {'x-cse-context': json.dumps(SRC_MICROSERVICE), 'Cookie': cookie}
    n = 0
    success = 0
    failure = 0
    while n < times:
        try:
            response = requests.get(url, headers=headers, params=playload)
            if response.status_code == 200:
                success = success + 1
            else:
                failure = failure + 1
            logger.debug(
                "query order by url %s at times %s, got response %s", url, n, response.status_code)
        except requests.exceptions.ConnectionError:
            logger.error('connection refused')
        except Exception as e:
            logger.error(
                'query order by url %s at times %s with exception %s', url, n, e.message)
            failure = failure + 1
        n = n + 1
        if n % STAT_INTERVAL == 0:
            logger.info(
                '[query order stat] total rquests: %s, success: %s, failure %s', n, success, failure)
        if interval != 0:
            time.sleep(interval)


def call_create_order(host, times=None, interval=None, userid="uid0@email.com"):
    url = "%s/orders/huaweiair/v1/orders" % host
    userid = "uid0@email.com" if userid is None else userid
    times = sys.maxint if times is None or int(times) == 0 else int(times)
    interval = 0 if interval is None else float(interval)

    toDate = datetime.datetime.now()
    toArrivalDate = toDate + datetime.timedelta(hours=2)
    retDate = toDate + datetime.timedelta(days=1)
    retArrivalDate = retDate + datetime.timedelta(hours=2)
    playload = {
        "fromAirPortName": u'北京 Beijing',
        "oneWayFlight": False,
        "retFlightClass": 1,
        "retFlightId": "9c0ca371-184e-47e4-b083-e9af4d7e1f17",
        "retFlightPrice": 200,
        "retFlightSegId": "AA482",
        "retScheduledArrivalTime": retDate.strftime("%Y-%m-%d %H:%M:%S"),
        "retScheduledDepartureTime": retArrivalDate.strftime("%Y-%m-%d %H:%M:%S"),
        "toAirPortName": u'上海 Shanghai',
        "toFlightClass": 1,
        "toFlightId": "76f3334e-486c-4be6-8fd6-d4fe9ee1a3c1",
        "toFlightPrice": 200,
        "toFlightSegId": "AA467",
        "toScheduledArrivalTime": toDate.strftime("%Y-%m-%d %H:%M:%S"),
        "toScheduledDepartureTime": toArrivalDate.strftime("%Y-%m-%d %H:%M:%S"),
        "userId": "uid0@email.com"
    }

    logger.info('start create order with host: %s, times: %s, interval: %s, userid: %s',
                host, times, interval, userid)

    cookie = login(host)
    if cookie is None:
        logger.error("login failure")
        return

    n = 0
    success = 0
    failure = 0
    headers = {'Content-Type': 'Application/json', 'x-cse-context': json.dumps(SRC_MICROSERVICE), 'Cookie': cookie}
    while n < times:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(playload))
            if response.status_code == 200:
                success = success + 1
            else:
                failure = failure + 1
            logger.debug(
                "create order by url %s at times %s, got response %s", url, n, response.status_code)
        except requests.exceptions.ConnectionError:
            logger.error('connection refused')
        except Exception as e:
            logger.error(
                'create order by url %s at times %s with exception %s', url, n, e.message)
            failure = failure + 1

        n = n + 1
        if n % STAT_INTERVAL == 0:
            logger.info(
                '[create order stat] total rquests: %s, success: %s, failure %s', n, success, failure)
        if interval != 0:
            time.sleep(interval)


def call_pay_order(host, times=None, interval=None, userid="uid0@email.com"):
    url = "%s/orders/huaweiair/v1/orders/%s" % (host, uuid.uuid4().hex)
    userid = "uid0@email.com" if userid is None else userid
    times = sys.maxint if times is None or int(times) == 0 else int(times)
    interval = 0 if interval is None else float(interval)

    playload = {'action': 1}
    logger.info('start pay order with host: %s, times: %s, interval: %s, userid: %s',
                host, times, interval, userid)

    cookie = login(host)
    if cookie is None:
        logger.error("login failure")
        return

    n = 0
    success = 0
    failure = 0
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'x-cse-context': json.dumps(SRC_MICROSERVICE), 'Cookie': cookie}
    while n < times:
        try:
            response = requests.put(
                url, headers=headers, data=playload)
            if response.status_code == 200:
                success = success + 1
            else:
                failure = failure + 1
            logger.debug(
                "pay order by url %s at times %s, got response %s", url, n, response.status_code)
        except requests.exceptions.ConnectionError:
            logger.error('connection refused')
        except Exception as e:
            logger.error(
                'pay order by url %s at times %s with exception %s', url, n, e.message)
            failure = failure + 1
        n = n + 1
        if n % STAT_INTERVAL == 0:
            logger.info(
                '[pay order stat] total rquests: %s, success: %s, failure %s', n, success, failure)
        if interval != 0:
            time.sleep(interval)


def call_delete_order(host, times=None, interval=None, userid="uid0@email.com"):
    url = "%s/orders/huaweiair/v1/orders/%s" % (host, uuid.uuid4().hex)
    userid = "uid0@email.com" if userid is None else userid
    times = sys.maxint if times is None or int(times) == 0 else int(times)
    interval = 0 if interval is None else float(interval)
    
    logger.info('start delete order with host: %s, times: %s, interval: %s, userid: %s',
                host, times, interval, userid)
    cookie = login(host)
    if cookie is None:
        logger.error("login failure")
        return

    headers = {'x-cse-context': json.dumps(SRC_MICROSERVICE), 'Cookie': cookie}
    n = 0
    success = 0
    failure = 0
    while n < times:
        try:
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                success = success + 1
            else:
                failure = failure + 1
            logger.debug(
                "delete order by url %s at times %s, got response %s", url, n, response.status_code)
        except requests.exceptions.ConnectionError:
            logger.error('connection refused')
        except Exception as e:
            logger.error(
                'delete order by url %s at times %s with exception %s', url, n, e.message)
            failure = failure + 1
        n = n + 1
        if n % STAT_INTERVAL == 0:
            logger.info(
                '[delete order stat] total rquests: %s, success: %s, failure %s', n, success, failure)
        if interval != 0:
            time.sleep(interval)

def create_arg_parser():
    parser = argparse.ArgumentParser(prog="huaweiair-benchmark")
    parser.add_argument('-s', '--host', dest='host',
                        help='host address, e.g: http://ip:port')
    parser.add_argument('-t', '--times', dest='times',
                        help='call times, 0 means infinity')
    parser.add_argument('-i', '--interval', dest='interval',
                        help='call intervals, 1 means 1s, 0.1 means 100 ms')
    parser.add_argument('-u', '--userid', dest='userid', help='user id')
    return parser


def login(host, userid="uid0@email.com", password="password"):
    url = "%s/customers/rest/api/login" % (host)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'login': userid, 'password': password}
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        # sessionid=53156a18-5a21-49d9-b844-009e1c2be227;path=/
        set_cookie = response.headers.get('Set-Cookie')
        logger.info('Set-Cookie in headers: %s', set_cookie)
        sessiondid = set_cookie.split(';')[0].split('=')[1]
        # sessionid=4aaa8aa2-19bf-4041-8169-6ef361661067; loggedinuser=uid0%40email.com
        cookie = "sessionid=%s; loggedinuser=%s" % (sessiondid, urllib.quote(userid))
        logger.info("cookie in headers: %s", cookie)
        return cookie
    else:
        logger.error('login failure with user: %s, password: %s', userid, password)
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logger.error('Usage: %s get-order|pay-order|create-order|delete-order [options]', sys.argv[0])
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    parser = create_arg_parser()
    know_args = parser.parse_args(args)

    if know_args.host is None:
        parser.print_help()
        sys.exit(1)

    if command == "get-order":
        call_query_orders(know_args.host, know_args.times,
                        know_args.interval, know_args.userid)
    elif command == "create-order":
        call_create_order(know_args.host, know_args.times,
                      know_args.interval, know_args.userid)
    elif command == "pay-order":
        call_pay_order(know_args.host, know_args.times,
                          know_args.interval, know_args.userid)
    elif command == "delete-order":
        call_delete_order(know_args.host, know_args.times,
                          know_args.interval, know_args.userid)
    else:
        logger.error('unknow command: %s', command)
