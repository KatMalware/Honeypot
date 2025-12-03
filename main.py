import os
import json
import asyncio

from core.listener import ServiceListener
from core.scanner import scan_ports


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config', 'ports.json')


async def main():
    print("\n=== Honeypot Starting ===\n")

    # -----------------------
    # Load config
    # -----------------------

    if not os.path.exists(CONFIG_PATH):
        print(f"[!] config file not found: {CONFIG_PATH}")
        return

    with open(CONFIG_PATH, 'r') as f:
        cfg = json.load(f)

    bind = cfg.get("bind", "0.0.0.0")
    services = cfg.get("services", {})

    if not services:
        print("[!] No services defined in config/ports.json")
        return

    ports = [int(p) for p in services.keys()]

    # -----------------------
    # Pre-scan ports
    # -----------------------

    print(f"[*] Scanning {len(ports)} ports on {bind}...\n")

    scan_result = await scan_ports(bind, ports)

    for port, st in scan_result.items():
        status = "OPEN" if st else "CLOSED"
        print(f"PORT {port:<5} : {status}")

    print("\n---------------------------------------------")
    print("        Starting Honeypot Listeners")
    print("---------------------------------------------\n")

    # -----------------------
    # Start listeners
    # -----------------------

    tasks = []

    for port_str, svc in services.items():
        port = int(port_str)

        sl = ServiceListener(bind=bind, port=port, service_name=svc)

        tasks.append(asyncio.create_task(sl.start()))

        print(f"[+] {svc.upper()} listening on {bind}:{port}")

    # -----------------------
    # Run all async tasks
    # -----------------------

    if tasks:
        print("\n[*] Honeypot running...\n")
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            print("\n[!] Honeypot stopped")

    else:
        print("[!] No tasks to run")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Stopped by user")
