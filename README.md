# IP Toolkit - All-in-One IP Recon & Analysis

A command-line cybersecurity tool for investigating IP addresses and domains. Built for security enthusiasts, penetration testers, and network administrators.

> ⚠️ **Legal Notice:** Only use this tool against systems and networks you own or have explicit written permission to test. Unauthorized scanning may be illegal in your jurisdiction.

---

A raw HTTP request looks like this:
``` bash
GET /json/8.8.8.8 HTTP/1.1
Host: ip-api.com
```
It says "Hey ip-api.com, GET me the page at /json/8.8.8.8".



## Background: IP Address Fundamentals

### What Is an IP Address?
An **IP address** (Internet Protocol address) is a unique numerical label assigned to every device connected to a computer network. It serves two functions: *host identification* and *location addressing*.

### Public vs. Private IP Addresses

| Type    | Assigned By | Scope        | Example Range         |
|---------|-------------|--------------|----------------------|
| Public  | Your ISP    | Global       | Any routable address |
| Private | Your router | Local network| 192.168.x.x, 10.x.x.x, 172.16–31.x.x |

Find your own IPs:
```bash
# Private IP (Windows)
ipconfig

# Private IP (Linux/Mac)
ifconfig    # or: ip addr show
```

### Static vs. Dynamic IP Addresses

| Type    | Changes?  | Typical Use Case              |
|---------|-----------|-------------------------------|
| Static  | Never     | Servers, websites, DNS        |
| Dynamic | On reconnect | Home users, mobile devices |

### How to Find a Domain's IP Address
```bash
ping google.com
# or for full DNS detail:
nslookup google.com
dig google.com
```

---

## Features

| Module      | Description                                          |
|-------------|------------------------------------------------------|
| `info`      | Geolocation, ISP, timezone, ASN, proxy/VPN detection |
| `scan`      | Multi-threaded TCP port scanner with risk ratings    |
| `reputation`| DNS blocklist checks + AbuseIPDB report              |
| `whois`     | WHOIS registration data for IPs and domains          |
| `all`       | Runs all four modules in sequence                    |

---

## Quick Start

### Requirements
- Python 3.10+
- No external dependencies for core features

### Installation
```bash
git clone https://github.com/yourusername/ip-toolkit.git
cd ip-toolkit
pip install -r requirements.txt   # installs python-whois (optional but recommended)
```

### Basic Usage
```bash
# Geolocate an IP
python ip_toolkit.py info 8.8.8.8

# Scan common ports on a domain
python ip_toolkit.py scan example.com

# Check if an IP is blacklisted
python ip_toolkit.py reputation 185.220.101.1

# WHOIS lookup
python ip_toolkit.py whois google.com

# Run everything at once
python ip_toolkit.py all 8.8.8.8
```

---

## 🔧 Module Reference

### `info` - Geolocation & ISP
```bash
python ip_toolkit.py info <IP or domain>
```
Queries the [ip-api.com](https://ip-api.com) free endpoint. Returns country, city, coordinates, ISP, organisation, ASN, and flags for proxy/VPN/hosting/mobile.

---

### `scan` - Port Scanner
```bash
python ip_toolkit.py scan <IP or domain> [options]

Options:
  -p, --ports     Comma-separated ports: 22,80,443  (default: top 20)
  -t, --timeout   Socket timeout in seconds         (default: 0.5)
  --threads        Number of worker threads          (default: 50)
```

**Risk-rated output** - open ports are colour-coded:
- 🔴 `HIGH` - Telnet, SMB, RDP, Redis, MongoDB (critical exposure)
- 🟡 `MEDIUM` - FTP, VNC (verify auth)
- 🟢 `LOW` - HTTP, HTTPS, SSH (standard services)

---

### `reputation` - Blocklist & Abuse Check
```bash
python ip_toolkit.py reputation <IP>
```

Checks against 5 DNS-based blocklists (no API key required):
- Spamhaus ZEN & XBL
- SpamCop
- SORBS
- Barracuda Reputation

**Enhanced mode with AbuseIPDB** (optional, free API key):
```bash
export ABUSEIPDB_API_KEY="your_key_here"
python ip_toolkit.py reputation <IP>
```
Get a free key at [abuseipdb.com](https://www.abuseipdb.com).

---

### `whois` - WHOIS Lookup
```bash
python ip_toolkit.py whois <IP or domain>
```
Returns organisation, netblock/CIDR, country, abuse email, registrar, expiry date, and name servers.

---

### `all` - Full Recon
```bash
python ip_toolkit.py all <IP or domain> [--timeout 1.0] [--threads 100]
```
Runs `info → whois → scan → reputation` in sequence. Useful for a quick, comprehensive snapshot.

---

## 📁 Project Structure

```
ip-toolkit/
├── ip_toolkit.py          # CLI entry point & argument parser
├── requirements.txt
├── core/
│   ├── info.py            # IP geolocation (ip-api.com)
│   ├── scanner.py         # Multi-threaded port scanner
│   ├── reputation.py      # DNSBL + AbuseIPDB checks
│   └── whois_lookup.py    # WHOIS via python-whois / raw socket
└── utils/
    ├── display.py         # ANSI colours, banner, section headers
    └── helpers.py         # IP validation, DNS resolution
```

---

## Key Cybersecurity Concepts

### Common Risky Open Ports
| Port  | Service     | Risk                                         |
|-------|-------------|----------------------------------------------|
| 21    | FTP         | Anonymous login, plaintext credentials       |
| 23    | Telnet      | Plaintext - never expose to internet         |
| 445   | SMB         | Ransomware vector (EternalBlue, WannaCry)    |
| 3389  | RDP         | Brute-force & BlueKeep vulnerability         |
| 6379  | Redis       | Unauthenticated by default in many configs   |
| 27017 | MongoDB     | Often exposed without authentication         |

### DNS Blocklists (DNSBL)
Blocklists are maintained databases of IPs known to send spam, host malware, or participate in botnets. Checking them requires no API - just a reverse DNS query in the format:
```
<reversed-IP>.<blocklist-hostname>
# e.g. for 1.2.3.4 against zen.spamhaus.org:
4.3.2.1.zen.spamhaus.org
```

### WHOIS
WHOIS is a query/response protocol (RFC 3912) used to look up registration information for IP blocks and domain names. It tells you who owns a network range, when a domain expires, and who to contact for abuse.

---

## 🤝 Contributing

Pull requests are welcome! Ideas for extension:
- [ ] IPv6 support
- [ ] Export results to JSON / CSV
- [ ] CVE lookup for detected services
- [ ] Shodan API integration
- [ ] Traceroute module

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.
