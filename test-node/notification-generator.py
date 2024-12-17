import json
import time
import random
import copy
import datetime
import os
import base64, hashlib

import logging

# log_level = os.getenv("LOG_LEVEL", "INFO")
# level = logging.getLevelName(log_level)

# logger = logging.getLogger(__name__)
# logger.setLevel(level)


notification_template = json.load(open("notification-template.json"))


content_integrated_rate = float(os.environ.get("CONTENT_INTEGRATED_RATE"))  # % of messages should have the content included
integrity_checksum_rate = float(os.environ.get("INTEGRITY_CHECKSUM_RATE")) # % of messates should have wrong checksum
integrity_length_content_rate = float(os.environ.get("INTEGRITY_LENGTH_CONTENT_RATE")) # % of messages should have wrong lenght in content
integrity_length_link_rate = float(os.environ.get("INTEGRITY_LENGTH_LINK_RATE")) # % of messages should have wrong lenght in content
integrity_schema_rate = float(os.environ.get("INTEGRITY_SCHEMA_RATE")) # % of messages with incorrect schema
integrity_pubdate_rate = float(os.environ.get("INTEGRITY_PUBDATE_RATE")) # % of messages with non ISO pubdate
integrity_no_dataid_rate = float(os.environ.get("INTEGRITY_NO_DATAID_RATE")) # % of messages with no data_id
nr_duplicates_max = int(os.environ.get("NR_DUPLICATES_MAX"))
nr_duplicates_min = int(os.environ.get("NR_DUPLICATES_MIN"))
duplicate_max_delay_ms = int(os.environ.get("DUPLICATE_MAX_DELAY_MS"))
nr_caches = int(os.environ.get("NR_CACHES"))
cache_host = os.environ.get("CACHE_HOST")
cache_domain = os.environ.get("CACHE_DOMAIN")
cache_root_dir = os.environ.get("CACHE_ROOTDIR","")
msg_rate = int(os.environ.get("MSG_RATE_PER_SECOND"))
max_messages = int(os.environ.get("MAX_MESSAGES","0"))

test_id = os.environ.get("TEST_ID")

data_dir = os.environ.get("DATA_DIR")

# print("""Starting notification generator with the following parameters: 
#             content_integrated_rate {:.0%}, 
#             integrity_checksum_rate {:.0%}, 
#             integrity_length_content_rate {:.0%}, 
#             integrity_length_link_rate {:.0%},
#             integrity_schema_rate {:.0%}, 
#             integrity_pubdate_rate {:.0%},
#             integrity_no_dataid_rate {:.0%},
#             nr_duplicates_max {},
#             nr_duplicates_min {},
#             duplicate_max_delay_ms {},
#             nr_caches {},
#             msg_rate {}
#             """.format(content_integrated_rate,integrity_checksum_rate,integrity_length_content_rate,integrity_length_link_rate,integrity_schema_rate,integrity_pubdate_rate,integrity_no_dataid_rate,nr_duplicates_max,nr_duplicates_min,duplicate_max_delay_ms,nr_caches,msg_rate) )



def process_file(file_name,counter):
    
    file_path = os.path.join(data_dir, file_name)

    wsi = file_name.split("_")[1]
    observation_time = file_name.split("_")[2].replace(".bufr","")

    data = open(file_path, "rb").read()

    n = copy.deepcopy(notification_template)

    n["properties"]["data_id"] = n["properties"]["data_id"]+ "-"+test_id+"-" + wsi + "-" + observation_time
    n["properties"]["wigos_station_identifier"] = wsi
    n["id"] = n["id"] + "-" + str(counter)

    if random.random() < content_integrated_rate:
        n["properties"].pop("content")
    else:
        n["properties"]["content"] = {
            "encoding": "base64",
            "value":  base64.b64encode(data).decode("utf-8"),
            "size": len(data) + (10 if random.random() < integrity_length_content_rate else 0)
        }

    
    b64_sha512_hash = base64.b64encode(hashlib.sha512(data).digest()).decode("utf-8")
    n["properties"]["integrity"]["value"] = b64_sha512_hash + ("xx" if random.random() < integrity_checksum_rate else "")

    n["links"][0]["length"] = len(data) + (10 if random.random() < integrity_length_link_rate else 0)

    if random.random() < integrity_schema_rate:
        n["findme"] = "I am not supposed to be here"

    if random.random() < integrity_pubdate_rate:
        n["properties"]["pubtime"] = "the day before yesterday"

    if random.random() < integrity_no_dataid_rate:
        n["properties"].pop("data_id")

    for i in range(1,random.randint(nr_duplicates_min,nr_duplicates_max)+1):
        n_new = copy.deepcopy(n)

        n_new["id"] = n_new["id"] + "-" + str(i)

        rel_filename = file_name.split("/")[-2] + "/" + file_name.split("/")[-1]

        if nr_caches>1:
            cache = "{host}-{nr}.{domain}/{cache_root_dir}/{rel_filename}".format(host=cache_host,nr=random.randint(1,nr_caches),domain=cache_domain,cache_root_dir=cache_root_dir, rel_filename=rel_filename)
        else:
            cache = "{host}.{domain}/{cache_root_dir}/{rel_filename}".format(host=cache_host,domain=cache_domain,cache_root_dir=cache_root_dir,rel_filename=rel_filename)


        n_new["links"][0]["href"] = cache 
        n_new["links"][0]["href"].replace("http://test-cache/",cache).replace("WIGOS_0-20000-0-20674_20240618T120000",rel_filename)

        return n_new




counter = 0
files = []
for root, dirs, file_names in os.walk(data_dir):
    for file_name in file_names:
        if file_name.endswith(".bufr4"):
            file_path = os.path.relpath(os.path.join(root, file_name), data_dir)
            notification = process_file(file_path,counter)
            print( json.dumps(notification,indent=None))

            if msg_rate > 0:
                time.sleep(  1/msg_rate )
            counter = counter + 1

            if max_messages > 0 and counter >= max_messages:
                break
