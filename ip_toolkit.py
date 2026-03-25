import socket
import json
import sys
import threading
import datetime
import subprocess
import platform

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

RISK = {
    23:    ("HIGH",   RED),
    445:   ("HIGH",   RED),
    3389:  ("HIGH",   RED),
    6379:  ("HIGH",   RED),
    27017: ("HIGH",   RED),
    21:    ("MEDIUM", YELLOW),
    5900:  ("MEDIUM", YELLOW),
    25:    ("MEDIUM", YELLOW),
}

def section(title):
    print(CYAN + BOLD + f"\n ┌─ {title} {'─' * (45 - len(title))}┐" + RESET)

def section_end():
    print(CYAN + BOLD + f" └{'─' * 48}┘" + RESET)

def clean_date(date_str):
    if date_str:
        return date_str.split("T")[0]
    return "N/A"

def save_log(target, modules):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("ip_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'=' * 55}\n")
        f.write(f"  [{timestamp}]  TARGET: {target}\n")
        f.write(f"{'=' * 55}")
        for section_name, data in modules.items():
            if not data:
                continue
            f.write(f"\n  >> {section_name}\n")
            f.write(f"  {'─' * 40}\n")
            for key, value in data.items():
                f.write(f"     {key:<16}: {value}\n")
    print(YELLOW + "\n  [~] Saved to ip_log.txt" + RESET)

def resolve(target, exit_on_fail=True):
    if target.replace(".", "").isnumeric():
        return target
    try:
        ip = socket.gethostbyname(target)
        print(YELLOW + f"\n [~] {target} → {ip}" + RESET)
        return ip
    except socket.gaierror:
        print(RED + f"\n [!] Could not resolve '{target}'" + RESET)
        if exit_on_fail:
            sys.exit(1)
        return None

def http_get(host, path):
    sock = socket.create_connection((host, 80), timeout=8)
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    sock.sendall(request.encode())
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    sock.close()
    return response.decode(errors="replace").split("\r\n\r\n")[1]

def whois_query(host, query):
    sock = socket.create_connection((host, 43), timeout=8)
    sock.sendall((query + "\r\n").encode())
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    sock.close()
    return response.decode(errors="replace")

def get_info(target):
    ip = resolve(target)
    section("IP INFO")
    body = http_get("ip-api.com", f"/json/{ip}?fields=status,message,query,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting")
    data = json.loads(body)
    if data["status"] != "success":
        print(RED + f"  [!] Error: {data.get('message', 'unknown')}" + RESET)
        return
    print(GREEN + f"  IP Address   : {data['query']}"    + RESET)
    print(GREEN + f"  Country      : {data['country']}"    + RESET)
    print(GREEN + f"  Region       : {data['regionName']}" + RESET)
    print(GREEN + f"  City         : {data['city']}"       + RESET)
    print(GREEN + f"  Coordinates  : {data['lat']}, {data['lon']}" + RESET)
    print(GREEN + f"  Timezone     : {data['timezone']}"   + RESET)
    print(GREEN + f"  ISP          : {data['isp']}"        + RESET)
    print(GREEN + f"  Organisation : {data['org']}"        + RESET)
    print(GREEN + f"  ASN          : {data['as']}"         + RESET)
    print(GREEN + f"  Proxy/VPN    : " + RESET + (RED    + "YES (!)" + RESET if data["proxy"]   else GREEN + "NO" + RESET))
    print(GREEN + f"  Hosting      : " + RESET + (YELLOW + "YES"     + RESET if data["hosting"] else GREEN + "NO" + RESET))
    print(GREEN + f"  Mobile       : " + RESET + (YELLOW + "YES"     + RESET if data["mobile"]  else GREEN + "NO" + RESET))
    section_end()
    return {
        "IP Address": data["query"],
        "Country": data["country"],
        "City": data["city"],
        "Region": data["regionName"],
        "Timezone": data["timezone"],
        "ISP": data["isp"],
        "Organisation": data["org"],
        "ASN": data["as"],
        "Proxy/VPN": "YES" if data["proxy"] else "NO",
        "Hosting": "YES" if data["hosting"] else "NO",
        "Mobile": "YES" if data["mobile"] else "NO",
    }

def get_whois(target):
    section("WHOIS")
    try:
        is_ip = target.replace(".", "").isnumeric()
        if is_ip:
            raw = whois_query("whois.arin.net", f"+ {target}")
            result = {}
            print()
            for line in raw.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("%"):
                    continue
                for prefix in ("NetName:", "Organization:", "OrgName:", "Country:", "CIDR:", "NetRange:"):
                    if line.startswith(prefix):
                        key, val = line.split(":", 1)
                        print(GREEN + f"  {key:<14}: {val.strip()}" + RESET)
                        result[key] = val.strip()
                        break
            section_end()
            return result
        else:
            raw = whois_query("whois.iana.org", target)
            refer = None
            for line in raw.splitlines():
                if line.lower().startswith("refer:"):
                    refer = line.split(":", 1)[1].strip()
                    break
            if refer:
                raw = whois_query(refer, target)
            fields = {
                "Domain Name":          None,
                "Registrar":            None,
                "Creation Date":        None,
                "Updated Date":         None,
                "Registry Expiry Date": None,
                "Name Server":          [],
                "DNSSEC":               None,
            }
            for line in raw.splitlines():
                line = line.strip()
                for key in fields:
                    if line.lower().startswith(key.lower() + ":"):
                        value = line.split(":", 1)[1].strip()
                        if key == "Name Server":
                            fields[key].append(value)
                        elif fields[key] is None:
                            fields[key] = value
            print(GREEN + f"  Domain       : {fields['Domain Name']}"                      + RESET)
            print(GREEN + f"  Registrar    : {fields['Registrar']}"                        + RESET)
            print(GREEN + f"  Created      : {clean_date(fields['Creation Date'])}"        + RESET)
            print(GREEN + f"  Updated      : {clean_date(fields['Updated Date'])}"         + RESET)
            print(GREEN + f"  Expires      : {clean_date(fields['Registry Expiry Date'])}" + RESET)
            print(GREEN + f"  DNSSEC       : {fields['DNSSEC']}"                           + RESET)
            print(GREEN + f"  Name Servers : {', '.join(fields['Name Server'][:4])}"       + RESET)
            section_end()
            return {
                "Domain":    fields.get("Domain Name", "N/A"),
                "Registrar": fields.get("Registrar", "N/A"),
                "Created":   clean_date(fields.get("Creation Date")),
                "Expires":   clean_date(fields.get("Registry Expiry Date")),
                "DNSSEC":    fields.get("DNSSEC", "N/A"),
            }
    except Exception as e:
        print(RED + f"  [!] WHOIS failed: {e}" + RESET)
        section_end()
        return {}

def scan_ports(target):
    ip = resolve(target)
    section("PORT SCAN")
    ports = {
        21: "FTP",      22: "SSH",       23: "Telnet",
        25: "SMTP",     53: "DNS",       80: "HTTP",
        110: "POP3",    143: "IMAP",     443: "HTTPS",
        445: "SMB",     3306: "MySQL",   3389: "RDP",
        5900: "VNC",    6379: "Redis",   8080: "HTTP-Alt",
        27017: "MongoDB",
    }
    print(YELLOW + f"  Scanning {ip} - {len(ports)} ports..." + RESET)
    open_ports = []
    lock = threading.Lock()
    def probe(port, service):
        try:
            sock = socket.create_connection((ip, port), timeout=0.5)
            sock.close()
            with lock:
                open_ports.append((port, service))
        except:
            pass
    threads = []
    for port, service in ports.items():
        t = threading.Thread(target=probe, args=(port, service))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    open_ports.sort()
    if not open_ports:
        print(YELLOW + "  No open ports found." + RESET)
    else:
        print(GREEN + f"\n  {'PORT':<8} {'SERVICE':<12} RISK" + RESET)
        for port, service in open_ports:
            risk, color = RISK.get(port, ("LOW", GREEN))
            print(color + f"  {port:<8} {service:<12} {risk}" + RESET)
    section_end()
    return {
        "Open Ports": ", ".join(f"{p}({s})" for p, s in open_ports) or "None",
    }

def check_reputation(target):
    ip = resolve(target)
    section("REPUTATION")
    blocklists = [
        ("zen.spamhaus.org",      "Spamhaus ZEN"),
        ("bl.spamcop.net",        "SpamCop"),
        ("dnsbl.sorbs.net",       "SORBS"),
        ("xbl.spamhaus.org",      "Spamhaus XBL"),
        ("b.barracudacentral.org","Barracuda"),
    ]
    reversed_ip = ".".join(reversed(ip.split(".")))
    print(YELLOW + f"  Checking {ip} against {len(blocklists)} blocklists...\n" + RESET)
    found = False
    for bl_host, bl_name in blocklists:
        query = f"{reversed_ip}.{bl_host}"
        try:
            socket.getaddrinfo(query, None)
            print(RED + f"  [LISTED]  {bl_name}" + RESET)
            found = True
        except socket.gaierror:
            print(GREEN + f"  [CLEAN]   {bl_name}" + RESET)
    if not found:
        print(YELLOW + f"\n  Result: IP appears clean across all blocklists." + RESET)
    else:
        print(YELLOW + f"\n  Result: IP is listed on one or more blocklists!" + RESET)
    section_end()
    return {
        "Result": "LISTED on one or more blocklists" if found else "CLEAN",
    }

def traceroute(target, hops=20):
    section("TRACEROUTE")
    if platform.system() == "Windows":
        command = ["tracert", "-d", "-h", str(hops), target]
    else:
        command = ["traceroute", "-n", "-m", str(hops), target]
    print(YELLOW + f"  Tracing route to {target} (max {hops} hops)...\n" + RESET)
    hop_lines = []
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in process.stdout:
            line = line.decode(errors="replace").rstrip()
            if not line.strip():
                continue
            print(GREEN + f"  {line}" + RESET)
            hop_lines.append(line.strip())
        process.wait()
    except Exception as e:
        print(RED + f"  [!] Traceroute failed: {e}" + RESET)
    section_end()
    return {"Hops": str(len(hop_lines) - 2), "Route": " → ".join(
        line.split()[-1] for line in hop_lines
        if line and line[0].isdigit() and line.split()[-1] != "out."
    )}

# get_info("google.com")
# get_whois("google.com")
# scan_ports("google.com")
# check_reputation("8.8.8.8")
# check_reputation("185.220.101.1")
# traceroute("google.com")

def print_banner():
    print(CYAN + BOLD + """
  ██╗██████╗     ████████╗ ██████╗  ██████╗ ██╗      ██╗  ██╗██╗████████╗
  ██║██╔══██╗       ██╔══╝██╔═══██╗██╔═══██╗██║      ██║ ██╔╝██║╚══██╔══╝
  ██║██████╔╝       ██║   ██║   ██║██║   ██║██║      █████╔╝ ██║   ██║   
  ██║██╔═══╝        ██║   ██║   ██║██║   ██║██║      ██╔═██╗ ██║   ██║   
  ██║██║            ██║   ╚██████╔╝╚██████╔╝███████╗ ██║  ██╗██║   ██║   
  ╚═╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝ ╚═╝  ╚═╝╚═╝   ╚═╝  
    """ + RESET)

def ask_hops():
    hops = input(GREEN + "  Max hops (default 20): " + YELLOW).strip()
    sys.stdout.write(RESET)
    if hops.isdigit() and int(hops) >= 1:
        return int(hops)
    return 20

def interactive_menu():
    print_banner()
    while True:
        print(CYAN + "  ─" * 25 + RESET)
        target = input(GREEN + "\n  Enter target (IP/domain) or 'q' to quit: " + YELLOW).strip()
        sys.stdout.write(RESET)
        if not target or target.lower() == "q":
            print(RED + "\n  [~] Goodbye!\n" + RESET)
            break
        print(CYAN + """
  [1] IP Info
  [2] WHOIS
  [3] Port Scan
  [4] Reputation
  [5] Traceroute
  [a] All
  [b] Change target
  [q] Quit
        """ + RESET)
        choice = input(GREEN + "  Pick a command: " + YELLOW).strip().lower()
        sys.stdout.write(RESET)
        if choice == "q":
            print(RED + "\n  [~] Goodbye!\n" + RESET)
            break
        elif choice == "b":
            print(YELLOW + "\n  [~] Going back...\n" + RESET)
            continue
        elif choice == "a":
            ip = resolve(target, exit_on_fail=False)
            if not ip:
                continue
            hops = ask_hops()
            modules = {}
            modules["IP INFO"]    = get_info(ip)          or {}
            modules["WHOIS"]      = get_whois(target)     or {}
            modules["PORT SCAN"]  = scan_ports(ip)        or {}
            modules["REPUTATION"] = check_reputation(ip)  or {}
            modules["TRACEROUTE"] = traceroute(ip, hops)  or {}
            save_log(target, modules)
        elif choice == "1": get_info(target)
        elif choice == "2": get_whois(target)
        elif choice == "3": scan_ports(target)
        elif choice == "4": check_reputation(target)
        elif choice == "5":
            hops = ask_hops()
            traceroute(target, hops)
        else:
            print(RED + "\n  [!] Invalid choice.\n" + RESET)

if len(sys.argv) == 1:
    interactive_menu()
elif len(sys.argv) < 3:
    print(YELLOW + "\n  Usage: python ip_toolkit.py <command> <target>" + RESET)
    print(YELLOW +   "  Commands: info | whois | scan | reputation | traceroute | all\n" + RESET)
    sys.exit(0)
else:
    command = sys.argv[1].lower()
    target  = sys.argv[2]
    if command == "info":           get_info(target)
    elif command == "whois":        get_whois(target)
    elif command == "scan":         scan_ports(target)
    elif command == "reputation":   check_reputation(target)
    elif command == "traceroute":   traceroute(target)
    elif command == "all":
        modules = {}
        modules["IP INFO"] = get_info(target) or {}
        modules["WHOIS"] = get_whois(target) or {}
        modules["PORT SCAN"] = scan_ports(target) or {}
        modules["REPUTATION"] = check_reputation(target) or {}
        modules["TRACEROUTE"] = traceroute(target) or {}
        save_log(target, modules)
    else:
        print(RED + f"\n  [!] Unknown command: '{command}'" + RESET)
        print(YELLOW + "  Commands: info | whois | scan | reputation | all\n" + RESET)
