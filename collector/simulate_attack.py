from datetime import datetime

ip = "192.168.1.50"
username = "admin"

file = open("../sample_logs/auth.log", "a")

for attempt in range(1, 11):
    time = datetime.now().strftime("%b %d %H:%M:%S")

    log = (
        f"{time} server sshd[{attempt}]: "
        f"Failed password for user {username} "
        f"from {ip} port {42000 + attempt} ssh2"
    )

    file.write(log + "\n")
    print(log)

file.close()

print("\nAttack simulation completed.")