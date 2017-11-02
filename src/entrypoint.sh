#!/bin/bash

command=$1

if [ "get-order" = ${command} ] || \
[ "create-order" = ${command} ] || \
[ "pay-order" = ${command} ] || \
[ "delete-order" = ${command} ]; then
    python /home/huaweiair-benchmark/huaweiair_benchmark.py $@
else
    exec $@
fi