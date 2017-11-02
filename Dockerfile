from python:2

RUN pip install requests
RUN mkdir -p /home/huaweiair-benchmark
COPY src/entrypoint.sh /
COPY src/python/huaweiair_benchmark.py /home/huaweiair-benchmark
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "get-order", "-s", "http://localhost:8080", "-t", "2"]