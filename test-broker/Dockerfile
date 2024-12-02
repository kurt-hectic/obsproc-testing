FROM eclipse-mosquitto

COPY ./mosquitto.conf /mosquitto/config/mosquitto.conf
COPY ./passwd /etc/mosquitto/passwd

RUN chmod 0700 /etc/mosquitto/passwd
RUN chown mosquitto:mosquitto /etc/mosquitto/passwd

#EXPOSE 1883