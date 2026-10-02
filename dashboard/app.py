import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="Mini SOC",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Mini SOC")
st.caption("Automated Threat Detection & Incident Response")

with open("../reports/incidents.json", "r") as file:
    incidents = json.load(file)

with open("../reports/blocked_ips.json", "r") as file:
    blocked_ips = json.load(file)


critical = 0
high = 0
medium = 0
low = 0

attack_counts = {}

for incident in incidents:

    attack = incident["attack"]

    attack_counts[attack] = attack_counts.get(attack, 0) + 1

    if incident["severity"] == "CRITICAL":
        critical += 1

    elif incident["severity"] == "HIGH":
        high += 1

    elif incident["severity"] == "MEDIUM":
        medium += 1

    elif incident["severity"] == "LOW":
        low += 1


# Metrics

col1, col2, col3, col4 = st.columns(4)

col1.metric("🚨 Total Alerts", len(incidents))
col2.metric("🔴 Critical", critical)
col3.metric("🟠 High", high)
col4.metric("🛑 Blocked IPs", len(blocked_ips))


st.divider()


# Security Analytics

st.header("📊 Security Analytics")

chart1, chart2 = st.columns(2)

with chart1:

    st.subheader("Attack Distribution")

    attack_data = pd.DataFrame(
        {
            "Attack": list(attack_counts.keys()),
            "Count": list(attack_counts.values())
        }
    )

    st.bar_chart(
        attack_data,
        x="Attack",
        y="Count"
    )


with chart2:

    st.subheader("Severity Distribution")

    severity_data = pd.DataFrame(
        {
            "Severity": [
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "LOW"
            ],
            "Count": [
                critical,
                high,
                medium,
                low
            ]
        }
    )

    st.bar_chart(
        severity_data,
        x="Severity",
        y="Count"
    )


st.divider()


# Security Incidents

st.header("🚨 Security Incidents")

for incident in incidents:

    severity = incident["severity"]

    if severity == "CRITICAL":

        st.error(
            f"""
### 🔴 CRITICAL ALERT

**Attack:** {incident["attack"]}

**Source IP:** `{incident["source_ip"]}`

**Target User:** `{incident["target_user"]}`

**Failed Attempts:** `{incident["failed_attempts"]}`

**MITRE ATT&CK:** `{incident["mitre_attack"]}`

**Status:** `{incident["status"]}`

**Timestamp:** `{incident["timestamp"]}`
"""
        )

    elif severity == "HIGH":

        st.warning(
            f"""
### 🟠 HIGH ALERT

**Attack:** {incident["attack"]}

**Source IP:** `{incident["source_ip"]}`

**MITRE ATT&CK:** `{incident["mitre_attack"]}`

**Status:** `{incident["status"]}`

**Timestamp:** `{incident["timestamp"]}`
"""
        )

        if "target_user" in incident:

            st.write(
                "**Target User:**",
                incident["target_user"]
            )

            st.write(
                "**Failed Attempts:**",
                incident["failed_attempts"]
            )

        if "ports_contacted" in incident:

            st.write(
                "**Ports Contacted:**",
                incident["ports_contacted"]
            )


st.divider()


# Automated Response

st.header("🛑 Automated Response")

if blocked_ips:

    st.success(
        "Automated response is active. "
        "The following IP addresses were simulated as blocked."
    )

    for ip in blocked_ips:
        st.write("🔒", ip)

else:

    st.info("No IP addresses have been blocked.")


st.divider()


# Detected Attack Types

st.header("🛡️ Detected Attack Types")

for attack in attack_counts:

    st.write("•", attack)
