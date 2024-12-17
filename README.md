This repository contains a docker-compose based environment to simulate a global broker and global cache, and also contains a container which can be used to create test data


MSG_RATE_PER_SECOND=10000 python3 notification-generator.py | mosquitto_pub -h test-broker -p 1883 -u everyone -P everyone -t "cache/a/wis2/ru-aviamettelecom/data/core/weather/surface-based-observations/synop" -l


TEST_ID=test1 python3 notification-generator.py | mosquitto_pub -h test-broker -p 1883 -u everyone -P everyone -t "cache/a/wis2/ru-aviamettelecom/data/core/weather/surface-based-observations/synop" -l


MSG_RATE_PER_SECOND=10000 MAX_MESSAGES=1000000 TEST_ID=test1 python3 notification-generator.py | mosquitto_pub -h test-broker -p 1883 -u everyone -P everyone -t "cache/a/wis2/ru-aviamettelecom/data/core/weather/surface-based-observations/synop" -l