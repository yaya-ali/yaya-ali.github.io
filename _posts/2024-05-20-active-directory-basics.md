---
title: "Introduction to Windows Active Directory for Pentesters"
date: 2024-05-20 10:00:00 +0200
categories: [active-directory]
tags: [ctf, active-directory, windows, kerberos, ldap]
---

## What Is Active Directory?

Active Directory (AD) is Microsoft's directory service used in virtually every enterprise Windows environment. As a pentester, understanding AD is non-negotiable — most internal network engagements start and end with AD exploitation.

---

## Core Concepts

### Domain Controller (DC)
The server that runs AD. All authentication requests go through it. Compromising the DC = game over for the network.

### Organisational Units (OUs)
Containers for organising users, computers, and groups. Permissions can be delegated at the OU level.

### Kerberos Authentication
The default authentication protocol. Key concepts:
- **AS-REQ / AS-REP** — user requests a Ticket Granting Ticket (TGT)
- **TGS-REQ / TGS-REP** — client requests a service ticket
- **Kerberoasting** — requesting service tickets for accounts with SPNs, then cracking the ticket offline

```bash
# Kerberoasting with Impacket
GetUserSPNs.py domain.local/user:password -dc-ip 10.10.x.x -request
hashcat -m 13100 tickets.txt rockyou.txt
```

### LDAP
AD is fundamentally an LDAP directory. Useful for enumeration:

```bash
ldapsearch -H ldap://10.10.x.x -b "DC=domain,DC=local" -x
```

---

## Common Attack Paths

| Attack | What It Does |
|---|---|
| **Pass-the-Hash** | Use NTLM hash without cracking it |
| **Kerberoasting** | Crack service account password offline |
| **AS-REP Roasting** | Attack accounts with pre-auth disabled |
| **BloodHound** | Graph all AD relationships to find attack paths |
| **DCSync** | Replicate all password hashes from the DC |

---

## BloodHound Quick Start

```bash
# Collect data with SharpHound
.\SharpHound.exe -c All

# Or remotely
bloodhound-python -u user -p pass -d domain.local -dc dc.domain.local -c All

# Start Neo4j and BloodHound, import ZIP
# Query: "Find Shortest Paths to Domain Admins"
```

The BloodHound graph will immediately show you if any user has an unintended path to DA — often through misconfigured delegations or group memberships.

---

## Resources

- [HackTricks AD Pentesting](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology)
- [TryHackMe AD Path](https://tryhackme.com/path/outline/activedirectory)
- Impacket, BloodHound, CrackMapExec
