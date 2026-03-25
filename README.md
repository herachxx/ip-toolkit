
```
           ██╗██████╗     ████████╗ ██████╗  ██████╗ ██╗      ██╗  ██╗██╗████████╗
           ██║██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║      ██║ ██╔╝██║╚══██╔══╝
           ██║██████╔╝       ██║   ██║   ██║██║   ██║██║      █████╔╝ ██║   ██║
           ██║██╔═══╝        ██║   ██║   ██║██║   ██║██║      ██╔═██╗ ██║   ██║
           ██║██║            ██║   ╚██████╔╝╚██████╔╝███████╗ ██║  ██╗██║   ██║
           ╚═╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝ ╚═╝  ╚═╝╚═╝   ╚═╝
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-00ff41?style=for-the-badge&logo=python&logoColor=00ff41&labelColor=0d0d0d)
![Modules](https://img.shields.io/badge/Modules-6-00ff41?style=for-the-badge&logoColor=00ff41&labelColor=0d0d0d)
![Dependencies](https://img.shields.io/badge/Dependencies-ZERO-00ff41?style=for-the-badge&labelColor=0d0d0d)
![License](https://img.shields.io/badge/License-MIT-00ff41?style=for-the-badge&labelColor=0d0d0d)
![Status](https://img.shields.io/badge/Status-ACTIVE-00ff41?style=for-the-badge&labelColor=0d0d0d)

**A modular command-line OSINT toolkit for analysing IP addresses and domains.**  
*Geolocation. Port scanning. Reputation. WHOIS. Traceroute. Reverse DNS. All in one tool.*  

</div>

---

> (!) **LEGAL NOTICE:** This tool is for educational purposes only. Only use it against systems and networks you own or have permission to test. Unauthorized scanning is illegal in most jurisdictions. The author takes no responsibility for misuse.

---

## `> OVERVIEW`

**IP Toolkit** is a modular command-line OSINT tool built entirely in python with zero third-party dependencies. It combines six modules into one unified interface - giving you geolocation data, open port detection, blocklist reputation checks, WHOIS registration data, network path tracing, and hostname discovery from a single script.  

It supports two modes: an **interactive menu** (just run the script with no arguments) and a **CLI mode** (pass the command and target directly from the terminal).

---

## `> FEATURES`

```
[+] IP geolocation        - country, city, region, coordinates, timezone
[+] ISP, organisation, and ASN identification
[+] VPN / proxy / hosting / mobile detection
[+] WHOIS lookup          - works for both domains and raw IP addresses
[+] Multi-threaded port scanner with risk ratings (HIGH / MEDIUM / LOW)
[+] DNS blocklist check across 5 major blocklists
[+] Traceroute            - network path with configurable hop limit
[+] Reverse DNS           - discover hostnames behind an IP
[+] Structured log file   - timestamped, auto-saved on every full scan
[+] Interactive menu      - back button, quit anywhere, hop count input
[+] CLI mode              - pass commands directly from the terminal
[+] Automatic domain → IP resolution
[+] Zero third-party dependencies - pure Python standard library
[+] Colour-coded terminal output
```

---

## `> DEMO`

```
  Enter target (IP/domain) or 'q' to quit: 185.220.101.1

  [1] IP Info       [5] Traceroute
  [2] WHOIS         [6] Reverse DNS
  [3] Port Scan     [a] All
  [4] Reputation    [b] Change target   [q] Quit

  Pick a command: a
  Max hops (default 20): 10

 ┌─ IP INFO ──────────────────────────────────────┐
  IP Address   : 185.220.101.1
  Country      : Germany
  Region       : Brandenburg
  City         : Brandenburg
  Coordinates  : 52.6171, 13.1207
  Timezone     : Europe/Berlin
  ISP          : Stiftung Erneuerbare Freiheit
  Organisation : Artikel10 e.V
  ASN          : AS60729 Stiftung Erneuerbare Freiheit
  Proxy/VPN    : YES (!)
  Hosting      : NO
  Mobile       : NO
 └────────────────────────────────────────────────┘

 ┌─ WHOIS ────────────────────────────────────────┐
  NetRange      : 185.220.100.0 - 185.220.103.255
  CIDR          : 185.220.100.0/22
  NetName       : FREIHEIT
  Organisation  : Stiftung Erneuerbare Freiheit
  Country       : DE
 └────────────────────────────────────────────────┘

 ┌─ PORT SCAN ────────────────────────────────────┐
  Scanning 185.220.101.1 - 16 ports...

  PORT     SERVICE      RISK
  80       HTTP         LOW
  443      HTTPS        LOW
 └────────────────────────────────────────────────┘

 ┌─ REPUTATION ───────────────────────────────────┐
  Checking 185.220.101.1 against 5 blocklists...

  [LISTED]  Spamhaus ZEN
  [CLEAN]   SpamCop
  [CLEAN]   SORBS
  [LISTED]  Spamhaus XBL
  [CLEAN]   Barracuda

  Result: IP is listed on one or more blocklists!
 └────────────────────────────────────────────────┘

 ┌─ TRACEROUTE ───────────────────────────────────┐
  Tracing route to 185.220.101.1 (max 10 hops)...

    1     3 ms     2 ms     2 ms  192.168.0.1
    2    11 ms     5 ms     4 ms  77.74.65.227
    ...
 └────────────────────────────────────────────────┘

 ┌─ REVERSE DNS ──────────────────────────────────┐
  IP Address   : 185.220.101.1
  Hostname     : berlin01.tor-exit.artikel10.org
 └────────────────────────────────────────────────┘

  [~] Saved to ip_log.txt
```

---

## `> INSTALLATION`

**Requirements:**
- Python 3.10+
- Internet connection
- Terminal with ANSI colour support (CMD, PowerShell, VS Code, Linux/Mac)

**No pip install needed.** Zero dependencies.

```bash
# Clone the repository
git clone https://github.com/herachxx/ip-toolkit.git

# Navigate into the folder
cd ip-toolkit

# Run it
python ip_toolkit.py
```

---

## `> USAGE`

### Interactive mode
Run the script with no arguments. You'll get the ASCII banner, a target prompt, and a module menu:

```bash
python ip_toolkit.py
```

### CLI mode
Pass the command and target directly:

```bash
python ip_toolkit.py <command> <target>
```

### Commands

| Command | Description |
|---------|-------------|
| `info` | Geolocation, ISP, ASN, VPN/proxy detection |
| `whois` | WHOIS registration data |
| `scan` | Multi-threaded port scanner |
| `reputation` | DNS blocklist checks |
| `traceroute` | Network path tracing |
| `reverse` | Reverse DNS hostname lookup |
| `all` | Runs all modules + saves to log |

### Examples

```bash
# Geolocate an IP
python ip_toolkit.py info 8.8.8.8

# Geolocate a domain
python ip_toolkit.py info google.com

# WHOIS lookup
python ip_toolkit.py whois google.com

# Port scan
python ip_toolkit.py scan 8.8.8.8

# Reputation check
python ip_toolkit.py reputation 185.220.101.1

# Traceroute
python ip_toolkit.py traceroute google.com

# Reverse DNS
python ip_toolkit.py reverse 185.220.101.1

# Run everything at once
python ip_toolkit.py all 8.8.8.8
```

> Domains and full URLs are automatically resolved to their IP address before scanning.

---

## `> MODULE REFERENCE`

### `info` - Geolocation & ISP
Queries the free [ip-api.com](http://ip-api.com) endpoint. No API key required.

```
[+] IP Address    - resolved IP
[+] Country       - registered country
[+] Region        - state or region
[+] City          - approximate city
[+] Coordinates   - latitude and longitude
[+] Timezone      - local timezone
[+] ISP           - Internet Service Provider
[+] Organisation  - network owner
[+] ASN           - Autonomous System Number
[+] Proxy/VPN     - YES / NO
[+] Hosting       - YES / NO  (datacenter / cloud provider)
[+] Mobile        - YES / NO  (cellular network)
```

---

### `whois` - WHOIS Lookup
Sends raw WHOIS queries over TCP port 43. Works for both domains and raw IPs. For domains it automatically follows IANA referrals to find the correct WHOIS server.

**For domains:**
```
[+] Domain name, registrar, creation / expiry dates, DNSSEC, name servers
```

**For IP addresses:**
```
[+] Net range, CIDR block, network name, organisation, country
```

---

### `scan` - Port Scanner
Uses Python's `threading` module to probe all ports simultaneously. Only open ports are shown with risk ratings.

**Ports scanned:**
```
21 FTP · 22 SSH · 23 Telnet · 25 SMTP · 53 DNS · 80 HTTP
110 POP3 · 143 IMAP · 443 HTTPS · 445 SMB · 3306 MySQL
3389 RDP · 5900 VNC · 6379 Redis · 8080 HTTP-Alt · 27017 MongoDB
```

**Risk ratings:**

| Risk | Colour | Ports |
|------|--------|-------|
| `HIGH` | Red | Telnet (23), SMB (445), RDP (3389), Redis (6379), MongoDB (27017) |
| `MEDIUM` | Yellow | FTP (21), VNC (5900), SMTP (25) |
| `LOW` | Green | SSH (22), DNS (53), HTTP (80), HTTPS (443), etc. |

---

### `reputation` - Blocklist Check
Checks the IP against 5 DNS-based blocklists. No API key required - uses reverse DNS queries.

```
[+] Spamhaus ZEN    - combined spam and exploit blocklist
[+] SpamCop         - spam source blocklist
[+] SORBS           - spam and open relay blocklist
[+] Spamhaus XBL    - exploits and botnet IPs
[+] Barracuda       - reputation-based blocklist
```

How it works:
```
IP 1.2.3.4  →  reversed: 4.3.2.1
Query: 4.3.2.1.zen.spamhaus.org

resolves   →  LISTED
NXDOMAIN   →  CLEAN
```

---

### `traceroute` - Network Path
Calls the system's built-in `tracert` (Windows) or `traceroute` (Linux/Mac) and displays each hop. In interactive mode you can set a custom max hop limit before running.

```
[+] Each router hop between you and the target
[+] Round-trip time for each hop (3 measurements)
[+] Configurable max hops (default: 20)
```

---

### `reverse` - Reverse DNS
Given an IP address, finds what hostname (domain) is associated with it using a reverse DNS lookup.

```
185.220.101.1  →  berlin01.tor-exit.artikel10.org
```

Useful for identifying hidden infrastructure, Tor exit nodes, and the real identity behind an IP.

---

### `all` - Full Recon
Runs all six modules in sequence and saves the complete results to `ip_log.txt`.

---

## `> LOG FILE`

Every full scan (`all` command) is automatically saved to `ip_log.txt` in the project folder.

```
=======================================================
  [2026-03-25 22:18]  TARGET: 185.220.101.1
=======================================================
  >> IP INFO
  ────────────────────────────────────────
     IP Address      : 185.220.101.1
     Country         : Germany
     City            : Brandenburg
     ...

  >> WHOIS
  ────────────────────────────────────────
     NetRange        : 185.220.100.0 - 185.220.103.255
     ...

  >> PORT SCAN
  ────────────────────────────────────────
     Open Ports      : 80(HTTP), 443(HTTPS)

  >> REPUTATION
  ────────────────────────────────────────
     Result          : LISTED on one or more blocklists

  >> TRACEROUTE
  ────────────────────────────────────────
     Hops            : 10
     Route           : 192.168.0.1 → 77.74.65.227 → ...

  >> REVERSE DNS
  ────────────────────────────────────────
     IP              : 185.220.101.1
     Hostname        : berlin01.tor-exit.artikel10.org
```

Results are never overwritten - every scan appends to the existing file.

---

## `> PROJECT STRUCTURE`

```
ip-toolkit/
│
├── ip_toolkit.py    ← entire tool - all modules in one file
├── ip_log.txt       ← auto-generated log (created on first full scan)
└── README.md        ← you are here
```

---

## `> IP ADDRESS FUNDAMENTALS`

### What is an IP address?
A unique numerical label assigned to every device on a network. It identifies the host and provides its location on the network.

### Public vs. Private

| Type | Assigned By | Visible To | Example Range |
|------|-------------|------------|---------------|
| Public | Your ISP | The entire internet | Any routable address |
| Private | Your router | Local network only | `192.168.x.x` · `10.x.x.x` · `172.16–31.x.x` |

```bash
# Find your public IP - just press Enter with no input when running the tool

# Find your private IP on Windows
ipconfig

# Find your private IP on Linux / Mac
ip addr show
```

### Static vs. Dynamic

| Type | Changes? | Typical Use |
|------|----------|-------------|
| Static | Never | Servers, websites, DNS resolvers |
| Dynamic | On reconnect | Home users, mobile devices |

---

## `> CYBERSECURITY CONCEPTS`

### Risky Open Ports

| Port | Service | Risk | Why |
|------|---------|------|-----|
| 21 | FTP | MEDIUM | Plaintext credentials, anonymous login possible |
| 23 | Telnet | HIGH | Fully plaintext - never expose to the internet |
| 445 | SMB | HIGH | EternalBlue, WannaCry ransomware vector |
| 3389 | RDP | HIGH | Brute-force attacks, BlueKeep CVE |
| 6379 | Redis | HIGH | No authentication by default |
| 27017 | MongoDB | HIGH | Often exposed without authentication |

### What is an ASN?
An Autonomous System Number identifies a network under single administrative control - like Google (`AS15169`), Cloudflare (`AS13335`), or your ISP. Every public IP block belongs to an ASN.

### What is WHOIS?
WHOIS (RFC 3912) is a protocol for querying domain and IP registration data. A raw query is just plain text sent over TCP to port 43:
```
→  Connect to whois.iana.org:43
→  Send: "google.com\r\n"
←  Receive: registrar, dates, name servers...
```

### What is a DNS Blocklist?
A database of IPs known for spam, malware, or botnet activity. Checking an IP requires no API - just a reverse DNS lookup. If the address resolves, the IP is listed. If it returns NXDOMAIN, it's clean.

### What is Reverse DNS?
Normal DNS goes forward - domain to IP. Reverse DNS goes backward - IP to domain. It's used to find what hostname is registered against an IP address. Useful for identifying Tor exit nodes, mail servers, and hidden infrastructure.

### What is Traceroute?
Traceroute exploits the TTL (Time To Live) field in network packets. By sending packets with incrementing TTL values (1, 2, 3...), each router along the path reveals itself when it drops the packet. This maps the full network path between you and the target.

---

## `> API USED`

| API | Used For | Auth | Rate Limit | Cost |
|-----|----------|------|------------|------|
| [ip-api.com](http://ip-api.com) | Geolocation, ISP, flags | None | 45 req/min | Free |

---

## `> LIMITATIONS`

```
[-] Geolocation is approximate - city-level accuracy varies
[-] ip-api.com free tier limited to 45 requests per minute
[-] IPv4 only - IPv6 not yet supported
[-] Port scanner uses TCP only - UDP ports not detected
[-] Traceroute relies on system tracert/traceroute command
[-] Some routers don't respond to traceroute (shown as * * *)
[-] Reverse DNS has no record for many IPs - returns N/A
[-] ANSI colours may not display in some older terminals
```

---

## `> ROADMAP`

```
[ ] URL support
[ ] IPv6 support
[ ] Custom port selection from CLI
[ ] AbuseIPDB integration for detailed abuse score and reports
[ ] UDP port scanning
[ ] Banner grabbing on open ports
[ ] Batch mode - scan multiple targets from a file
[ ] Export log as CSV for Excel / Sheets
[ ] Search and filter through the log file from CLI
```

---

## `> WHAT I LEARNED BUILDING THIS`

- How HTTP works at the raw socket level - no libraries
- What DNS resolution is and how domains map to IP addresses
- How the WHOIS protocol works over TCP port 43
- How IANA referrals chain WHOIS queries to the correct server
- How DNS blocklists work using reverse IP queries
- How reverse DNS works and what it reveals about an IP
- How traceroute exploits the TTL field to map network paths
- How threading works in Python and why it matters for network scanning
- How `sys.argv` enables CLI argument parsing without any library
- How to handle real network errors gracefully with try/except
- How to write structured log files that append without data loss

---

## `> LICENSE`

```
MIT License - do (almost) whatever you want with this.
```

---

<div align="center">

*Built from scratch. No shortcuts. No magic.*

</div>
