---
title: "IIUM CTF 2022 — Misc & Networking Writeup"
date: 2022-05-14 12:00:00 +0800
categories: [sig22ctf-IIUM]
tags: [ctf, misc, networking, osint, crypto]
---

> We placed **1st** at IIUM CTF 2022. This post covers Misc, Networking, OSINT, and Crypto.

---

## Misc — "Encoded Mess"

**Points:** 100

Given string:
```
RkxBR3tiNHMzXzY0X2VuYzBkM2R9
```

Looks like Base64:

```bash
echo "RkxBR3tiNHMzXzY0X2VuYzBkM2R9" | base64 -d
```

```
FLAG{b4s3_64_enc0d3d}
```

---

## Networking — "Find the Service"

**Points:** 200

Given an IP. Ran aggressive nmap scan:

```bash
nmap -A -p- 10.x.x.x
```

Found a service on a non-standard port (31337) responding with a banner:

```
Welcome. Send the magic word.
```

```bash
nc 10.x.x.x 31337
# typed: magic
FLAG{b4nn3r_gr4bb1ng_w0rks}
```

---

## OSINT — "Who Is This?"

**Points:** 150

Given a username: `ctf_player_iium`. Task: find their email.

Searched GitHub → found profile with email in public commit:

```bash
curl https://api.github.com/users/ctf_player_iium/events/public \
  | grep email
```

```
FLAG{0s1nt_g1t_3ma1l_l34k}
```

---

## Crypto — "Classic Cipher"

**Points:** 150

Given ciphertext:
```
SYNT{ebg13_vf_rnfl}
```

ROT13 decode:

```bash
echo "SYNT{ebg13_vf_rnfl}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

```
FLAG{rot13_is_easy}
```
