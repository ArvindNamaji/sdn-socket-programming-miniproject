#!/usr/bin/env python3
import subprocess
import time

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

def clear_all_flows():
    for sw in ["s1", "s2", "s3", "s4"]:
        run_cmd(f"sudo ovs-ofctl -O OpenFlow13 del-flows {sw}")

def install_primary_path():
    print("\n" + "="*65)
    print(">>> [SDN CONTROLLER] Installing PRIMARY Path (s1 <-> s2 <-> s4) <<<")
    print("="*65)

    clear_all_flows()

    # Switch 1: Port 1 (h1) <-> Port 2 (s2)
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s1 'priority=100,in_port=1,actions=output:2'")
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s1 'priority=100,in_port=2,actions=output:1'")

    # Switch 2: Port 1 (s1) <-> Port 2 (s4)
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s2 'priority=100,in_port=1,actions=output:2'")
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s2 'priority=100,in_port=2,actions=output:1'")

    # Switch 4: Port 2 (s2) <-> Port 1 (h2)
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s4 'priority=100,in_port=2,actions=output:1'")
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s4 'priority=100,in_port=1,actions=output:2'")

    print("[+] Primary path active via s2.\n")

def install_backup_path():
    print("\n" + "!"*65)
    print("🚨 >>> [SDN DYNAMIC RECOVERY] Rerouting to BACKUP (s1 <-> s3 <-> s4) <<< 🚨")
    print("!"*65)

    clear_all_flows()

    # Switch 1: Port 1 (h1) <-> Port 3 (s3)
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s1 'priority=200,in_port=1,actions=output:3'")
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s1 'priority=200,in_port=3,actions=output:1'")

    # Switch 3: Port 1 (s1) <-> Port 2 (s4)
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s3 'priority=200,in_port=1,actions=output:2'")
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s3 'priority=200,in_port=2,actions=output:1'")

    # Switch 4: Port 3 (s3) <-> Port 1 (h2)
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s4 'priority=200,in_port=3,actions=output:1'")
    run_cmd("sudo ovs-ofctl -O OpenFlow13 add-flow s4 'priority=200,in_port=1,actions=output:3'")

    print("[+] Backup path active via s3.\n")

def is_primary_link_up():
    """Checks OpenFlow port status directly from switch s1."""
    out = run_cmd("sudo ovs-ofctl -O OpenFlow13 dump-ports-desc s1")
    lines = out.splitlines()
    for i, line in enumerate(lines):
        if "s1-eth2" in line:
            # Check if this port or following config lines mention state=LINK_DOWN or config=PORT_DOWN
            block = " ".join(lines[i:i+3])
            if "LINK_DOWN" in block or "PORT_DOWN" in block:
                return False
            return True
    return False

def monitor_network():
    print("[*] SDN Controller Started. Managing OpenFlow tables...")
    install_primary_path()
    current_path = "primary"

    try:
        while True:
            primary_up = is_primary_link_up()

            if not primary_up and current_path == "primary":
                print("\n[ALERT] Failure detected on Primary Link (s1 <-> s2)!")
                install_backup_path()
                current_path = "backup"
            elif primary_up and current_path == "backup":
                print("\n[INFO] Primary Link (s1 <-> s2) restored! Reverting to primary path.")
                install_primary_path()
                current_path = "primary"

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[*] Stopping controller.")

if __name__ == "__main__":
    monitor_network()
