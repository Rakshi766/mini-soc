
import json
from datetime import datetime

incidents = []
blocked_ips = []


def process_login_event(line, failed_attempts):

    if "Failed password" in line:

        words = line.split()
        ip = words[11]
        user = words[9]

        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

        if failed_attempts[ip] >= 5:

            print("\nAttack: SSH Brute Force")
            print("Severity: HIGH")
            print("MITRE ATT&CK: T1110")
            print("Status: ALERT")

            incident = {
                "attack": "SSH Brute Force",
                "source_ip": ip,
                "target_user": user,
                "failed_attempts": failed_attempts[ip],
                "severity": "HIGH",
                "mitre_attack": "T1110",
                "status": "ALERT",
                "timestamp": datetime.now().isoformat()
            }

            save_realtime_incident(incident, ip)

    elif "Accepted password" in line:

        words = line.split()
        ip = words[11]
        user = words[9]

        attempts = failed_attempts.get(ip, 0)

        if attempts >= 5:

            print("\nAttack: Suspicious Login After Failed Attempts")
            print("Severity: CRITICAL")
            print("MITRE ATT&CK: T1078")
            print("Status: ALERT")

            incident = {
                "attack": "Suspicious Login After Failed Attempts",
                "source_ip": ip,
                "target_user": user,
                "failed_attempts": attempts,
                "severity": "CRITICAL",
                "mitre_attack": "T1078",
                "status": "ALERT",
                "timestamp": datetime.now().isoformat()
            }

            save_realtime_incident(incident, ip)


def save_realtime_incident(incident, ip):

    try:
        with open("../reports/incidents.json", "r") as file:
            existing_incidents = json.load(file)
    except:
        existing_incidents = []

    existing_incidents.append(incident)

    with open("../reports/incidents.json", "w") as file:
        json.dump(existing_incidents, file, indent=4)

    try:
        with open("../reports/blocked_ips.json", "r") as file:
            existing_blocked = json.load(file)
    except:
        existing_blocked = []

    if ip not in existing_blocked:
        existing_blocked.append(ip)

    with open("../reports/blocked_ips.json", "w") as file:
        json.dump(existing_blocked, file, indent=4)

    print("\nAutomated Response")
    print("------------------")
    print("Blocked IP:", ip)
    print("Response status: SIMULATED")


def detect_login_attacks():

    file = open("../sample_logs/auth.log", "r")

    failed_attempts = {}
    users = {}

    for line in file:

        words = line.split()

        if "Failed password" in line:

            user = words[9]
            ip = words[11]

            users[ip] = user
            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

        elif "Accepted password" in line:

            user = words[9]
            ip = words[11]

            attempts = failed_attempts.get(ip, 0)

            if attempts >= 5:

                incidents.append({
                    "attack": "Suspicious Login After Failed Attempts",
                    "source_ip": ip,
                    "target_user": user,
                    "failed_attempts": attempts,
                    "severity": "CRITICAL",
                    "mitre_attack": "T1078",
                    "status": "ALERT",
                    "timestamp": datetime.now().isoformat()
                })

    file.close()

    for ip in failed_attempts:

        if failed_attempts[ip] >= 5:

            incidents.append({
                "attack": "SSH Brute Force",
                "source_ip": ip,
                "target_user": users[ip],
                "failed_attempts": failed_attempts[ip],
                "severity": "HIGH",
                "mitre_attack": "T1110",
                "status": "ALERT",
                "timestamp": datetime.now().isoformat()
            })


def detect_port_scan():

    file = open("../sample_logs/network.log", "r")

    scanned_ports = {}

    for line in file:

        if "Connection from" in line:

            words = line.split()

            ip = words[6]
            port = words[9]

            scanned_ports.setdefault(ip, []).append(port)

    file.close()

    for ip in scanned_ports:

        ports = scanned_ports[ip]

        if len(ports) >= 5:

            incidents.append({
                "attack": "Possible Port Scan",
                "source_ip": ip,
                "ports_contacted": len(ports),
                "severity": "HIGH",
                "mitre_attack": "T1046",
                "status": "ALERT",
                "timestamp": datetime.now().isoformat()
            })


def respond_to_incidents():

    for incident in incidents:

        if incident["severity"] in ["HIGH", "CRITICAL"]:

            ip = incident["source_ip"]

            if ip not in blocked_ips:
                blocked_ips.append(ip)


def save_reports():

    with open("../reports/incidents.json", "w") as file:
        json.dump(incidents, file, indent=4)

    with open("../reports/blocked_ips.json", "w") as file:
        json.dump(blocked_ips, file, indent=4)


def run_detection():

    print("================================")
    print("     MINI SOC DETECTION ENGINE")
    print("================================")

    detect_login_attacks()
    detect_port_scan()
    respond_to_incidents()
    save_reports()

    print("\nDetection Summary")
    print("-----------------")

    for incident in incidents:

        print(
            incident["attack"],
            "|",
            incident["severity"],
            "|",
            incident["mitre_attack"]
        )

    print("\nBlocked IPs:", blocked_ips)
    print("Reports saved.")


if __name__ == "__main__":
    run_detection()
