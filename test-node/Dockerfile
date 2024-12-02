FROM ubuntu:latest

RUN apt-get update && apt-get install -y mosquitto-clients curl python3 python3-pip python3-requests iputils-ping

COPY ./* /app/

WORKDIR /app

RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]

CMD ["/bin/bash","publoop.sh"]