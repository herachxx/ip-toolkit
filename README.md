
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
![Modules](https://img.shields.io/badge/Modules-4-00ff41?style=for-the-badge&logoColor=00ff41&labelColor=0d0d0d)
![Dependencies](https://img.shields.io/badge/Dependencies-MINIMAL-00ff41?style=for-the-badge&labelColor=0d0d0d)
![License](https://img.shields.io/badge/License-MIT-00ff41?style=for-the-badge&labelColor=0d0d0d)
![Status](https://img.shields.io/badge/Status-ACTIVE-00ff41?style=for-the-badge&labelColor=0d0d0d)

**A modular command-line OSINT toolkit for investigating IP addresses and domains.**   
*Geolocation. Port scanning. Reputation checks. WHOIS. All in one tool.*

</div>

---

> **(!) LEGAL NOTICE:** This tool is for educational purposes and authorized security testing only.   
Unauthorized scanning is illegal in most jurisdictions. The author takes no responsibility for misuse.   

---

## `> OVERVIEW`

**IP Toolkit** is a modular, command-line OSINT and network reconnaissance tool built in Python. It combines four independent investigation modules into a single unified interface giving you geolocation data, open port detection, blocklist reputation checks, and WHOIS registration data with a single command.   

Each module can be run individually or all at once for a full snapshot of any IP address or domain.   

---

## `> MODULES`

```
[+] info       - Geolocation, ISP, ASN, timezone, VPN/proxy/mobile detection
[+] scan       - Multi-threaded TCP port scanner with risk ratings and banner grabbing
[+] reputation - DNS blocklist checks across 5 major blocklists + AbuseIPDB integration
[+] whois      - WHOIS registration data for IP blocks and domain names
[+] all        - Runs all four modules in sequence for a full recon snapshot
```

---

## `> DEMO`

```bash
$ python ip_toolkit.py all 185.220.101.1

  ┌────────────────────────────────────────────────────────────┐
  │  IP GEOLOCATION & INFO                                     │
  └────────────────────────────────────────────────────────────┘   
  Query IP         185.220.101.1
  Country          Germany
  Region           Brandenburg
  City             Brandenburg an der Havel
  Coordinates      52.4075, 12.5251
  Timezone         Europe/Berlin
  ISP              Stiftung Erneuerbare Freiheit
  AS               AS60729
  Flags            PROXY  TOR EXIT NODE

  ┌────────────────────────────────────────────────────────────┐
  │  PORT SCANNER  (Top 20 common ports)                       │
  └────────────────────────────────────────────────────────────┘   
  PORT     SERVICE        RISK       BANNER / NOTE
  ──────── ────────────── ────────── ──────────────────────────
  22       SSH            LOW
  80       HTTP           LOW
  443      HTTPS          LOW

  ┌────────────────────────────────────────────────────────────┐
  │  IP REPUTATION CHECK                                       │
  └────────────────────────────────────────────────────────────┘   
  Checking 185.220.101.1 against 5 DNS blocklists...

  [LISTED]  Spamhaus XBL (exploits/botnets)
  [LISTED]  SORBS

  AbuseIPDB Report
  Abuse Score      97%
  Total Reports    482
  Last Reported    2024-03-23T18:42:00+00:00
  Tor Exit Node    YES
```

---

## `> INSTALLATION`

**Requirements:**
- Python 3.10+
- Internet connection
- Terminal with ANSI colour support (CMD, PowerShell, VS Code, Linux/Mac)

```bash
# Clone the repository
git clone https://github.com/yourusername/ip-toolkit.git

# Navigate into the folder
cd ip-toolkit

# Install optional dependency (recommended)
pip install -r requirements.txt
```

> `python-whois` is the only third-party dependency and is optional. All other modules run on Python's standard library.

---

## `> USAGE`

### Basic syntax
```
python ip_toolkit.py <module> <target> [options]
```

### Examples
```bash
# Geolocate an IP address
python ip_toolkit.py info 8.8.8.8

# Geolocate a domain name
python ip_toolkit.py info google.com

# Scan the top 20 most common ports
python ip_toolkit.py scan 192.168.1.1

# Scan specific ports only
python ip_toolkit.py scan example.com -p 22,80,443,8080

# Check if an IP is blacklisted
python ip_toolkit.py reputation 185.220.101.1

# WHOIS lookup on a domain
python ip_toolkit.py whois google.com

# Run all modules at once
python ip_toolkit.py all 8.8.8.8

# Full recon with custom scan settings
python ip_toolkit.py all 8.8.8.8 --timeout 1.0 --threads 100
```

---

## `> MODULE REFERENCE`

### `info` - Geolocation & ISP
```bash
python ip_toolkit.py info <IP or domain>
```

Queries the [ip-api.com](https://ip-api.com) free endpoint. No API key required.

**Returns:**
```
[+] Query IP       - the resolved IP address
[+] Country        - registered country
[+] Region / City  - approximate physical location
[+] Coordinates    - latitude and longitude
[+] Timezone       - local timezone
[+] ISP            - Internet Service Provider
[+] Organisation   - network owner
[+] ASN            - Autonomous System Number
[+] Flags          - PROXY / VPN / HOSTING / MOBILE detection
```

---

### `scan` - Port Scanner
```bash
python ip_toolkit.py scan <IP or domain> [options]

  -p, --ports     Comma-separated ports  e.g. 22,80,443   (default: top 20)
  -t, --timeout   Socket timeout in seconds                (default: 0.5)
  --threads       Number of concurrent worker threads      (default: 50)
```

Uses multi-threaded TCP connections to probe ports concurrently. Attempts banner grabbing on open ports. All open ports are risk-rated:

| Risk | Colour | Examples |
|------|--------|---------|
| `HIGH` | 🔴 Red | Telnet (23), SMB (445), RDP (3389), Redis (6379), MongoDB (27017) |
| `MEDIUM` | 🟡 Yellow | FTP (21), VNC (5900) |
| `LOW` | 🟢 Green | SSH (22), HTTP (80), HTTPS (443) |

**Top 20 ports scanned by default:**

```
21 · 22 · 23 · 25 · 53 · 80 · 110 · 135 · 139 · 143
443 · 445 · 3306 · 3389 · 5432 · 5900 · 6379 · 8080 · 8443 · 27017
```

---

### `reputation` - Blocklist & Abuse Check
```bash
python ip_toolkit.py reputation <IP>
```

**DNS Blocklists checked (no API key required):**
```
[+] Spamhaus ZEN        - combined spam/exploit blocklist
[+] Spamhaus XBL        - exploits and botnet IPs
[+] SpamCop             - spam source blocklist
[+] SORBS               - spam and open relay blocklist
[+] Barracuda           - reputation-based blocklist
```

**Enhanced mode - AbuseIPDB integration (optional):**

Get a free API key at [abuseipdb.com](https://www.abuseipdb.com), then:

```bash
# Linux / Mac
export ABUSEIPDB_API_KEY="your_key_here"

# Windows CMD
set ABUSEIPDB_API_KEY=your_key_here

# Windows PowerShell
$env:ABUSEIPDB_API_KEY="your_key_here"
```

With the key set, the tool will also report:
```
[+] Abuse confidence score (0–100%)
[+] Total number of abuse reports
[+] Date of last report
[+] Whether the IP is a Tor exit node
```

---

### `whois` - WHOIS Lookup
```bash
python ip_toolkit.py whois <IP or domain>
```

Uses `python-whois` if installed, with a raw socket fallback so it works even without the library.

**Returns:**
```
[+] Organisation   - who owns this IP block or domain
[+] CIDR / Netblock
[+] Country
[+] Abuse contact email
[+] Registrar
[+] Registration / expiry dates
[+] Name servers
```

---

### `all` - Full Recon
```bash
python ip_toolkit.py all <IP or domain> [--timeout SECONDS] [--threads N]
```

Runs all four modules in sequence:
```
info  →  whois  →  scan  →  reputation
```

Useful for a complete picture of any target in a single command.

---

## `> PROJECT STRUCTURE`

```
ip-toolkit/
│
├── ip_toolkit.py          ← CLI entry point & argument parser
├── requirements.txt       ← python-whois (optional)
│
├── core/
│   ├── info.py            ← IP geolocation via ip-api.com
│   ├── scanner.py         ← multi-threaded TCP port scanner
│   ├── reputation.py      ← DNSBL checks + AbuseIPDB integration
│   └── whois_lookup.py    ← WHOIS via python-whois / raw socket fallback
│
└── utils/
    ├── display.py         ← ANSI colours, ASCII banner, section headers
    └── helpers.py         ← IP validation, DNS resolution
```

---

## `> IP ADDRESS FUNDAMENTALS`

### What is an IP address?
An IP address is a unique numerical label assigned to every device on a network. It serves two purposes: identifying the host and providing its location on the network.

### Public vs. Private

| Type | Assigned By | Visible To | Example Range |
|------|-------------|------------|---------------|
| Public | Your ISP | The entire internet | Any routable address |
| Private | Your router | Local network only | `192.168.x.x` · `10.x.x.x` · `172.16–31.x.x` |

```bash
# Find your public IP
curl ifconfig.me

# Find your private IP (Windows)
ipconfig

# Find your private IP (Linux / Mac)
ip addr show
```

### Static vs. Dynamic

| Type | Changes? | Typical Use |
|------|----------|-------------|
| Static | Never | Servers, websites, DNS resolvers |
| Dynamic | On reconnect | Home users, mobile devices |

### Resolve a domain to IP
```bash
ping google.com
nslookup google.com
dig google.com
```

---

## `> CYBERSECURITY CONCEPTS`

### Risky Open Ports

| Port | Service | Risk | Why |
|------|---------|------|-----|
| 21 | FTP | MEDIUM | Plaintext credentials, anonymous login |
| 23 | Telnet | HIGH | Fully plaintext - never expose to internet |
| 135 | MS-RPC | HIGH | Common Windows attack vector |
| 139 | NetBIOS | HIGH | Information disclosure, legacy Windows |
| 445 | SMB | HIGH | EternalBlue, WannaCry ransomware vector |
| 3389 | RDP | HIGH | Brute-force attacks, BlueKeep CVE |
| 5900 | VNC | MEDIUM | Weak auth by default in many setups |
| 6379 | Redis | HIGH | No authentication by default |
| 27017 | MongoDB | HIGH | Often exposed without authentication |

### DNS Blocklists (DNSBL)

Blocklists are databases of IPs known to send spam, host malware, or run botnets. Checking an IP against a blocklist requires no API - just a reverse DNS query:

```
# Format:
<reversed-IP>.<blocklist-host>

# Example: check 1.2.3.4 against Spamhaus ZEN
4.3.2.1.zen.spamhaus.org

# If the query resolves → IP is LISTED
# If it throws NXDOMAIN → IP is CLEAN
```

### WHOIS Protocol

WHOIS (RFC 3912) is a query/response protocol for looking up registration data on IP blocks and domain names. A raw WHOIS query is just plain text sent over a TCP connection to port 43:

```
→  Connect to whois.iana.org:43
→  Send: "8.8.8.8\r\n"
←  Receive: organisation, netblock, country, abuse contact...
```

### ASN — Autonomous System Number

An ASN identifies a network under a single administrative control (like Google, Cloudflare, or your ISP). Every public IP block is owned by an ASN. Example: `AS15169` is Google LLC.

---

## `> APIs USED`

| API | Used For | Auth | Rate Limit | Cost |
|-----|----------|------|------------|------|
| [ip-api.com](http://ip-api.com) | Geolocation, ISP, flags | None | 45 req/min | Free |
| [AbuseIPDB](https://www.abuseipdb.com) | Abuse score, reports | API key | 1000 req/day | Free tier |

---

## `> LIMITATIONS`

```
[-] Geolocation is approximate - city-level accuracy varies
[-] ip-api.com free tier limited to 45 requests per minute
[-] AbuseIPDB requires a free API key for enhanced reports
[-] IPv4 only - IPv6 not yet supported
[-] Port scanner uses TCP only - UDP ports not detected
[-] ANSI colours may not display in older Windows CMD versions
```

---

## `> ROADMAP`

```
[ ] IPv6 support
[ ] UDP port scanning
[ ] CVE lookup for detected service versions
[ ] Shodan API integration
[ ] Traceroute module
[ ] Batch mode — scan multiple targets from a file
[ ] Export results to JSON / CSV
[ ] Config file for API keys and default settings
```

---

## `> CONTRIBUTING`

Pull requests are welcome. If you have an idea for a new module or improvement, open an issue first to discuss it.

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "add: your feature description"
git push origin feature/your-feature-name
# → open a Pull Request
```

---

## `> LICENSE`

```
MIT License - do whatever you want with this.
See LICENSE for full terms.
```

---

<div align="center">

*Built for learning. Use responsibly.*

</div>
