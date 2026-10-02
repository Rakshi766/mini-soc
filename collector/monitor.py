import time
import sys
import json
from datetime import datetime

sys.path.append("../detection")

from detector import process_login_event

file_path = "../sample_logs/auth.log"

file = open(file_path, "r")

failed_attempts = {}

for line in file:

    if "Failed password" in line:

        words = line.split()
        ip = words[11]

        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

file.seek(0, 2)

print("================================")
print("       MINI SOC MONITOR")
print("================================")
print("Monitoring auth.log...")
print("Waiting for new security events...\n")


while True:

    line = file.readline()

    if line:

        print("New Log Event:")
        print(line.strip())

        process_login_event(line, failed_attempts)

    else:

        time.sleep(1)