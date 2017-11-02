from python:2

RUN mkdir -p /home/huaweiair-benchmark
COPY src/python/huaweiair-benchmark.py /home/huaweiair-benchmark

ENTRYPOINT [ "python /home/huaweiair-behchmark/huaweiair-benchmark.py" ]
CMD [ "get-order", "-s", "http://localhost:8080" ]