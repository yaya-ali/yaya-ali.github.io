---
title: "IIUM CTF 2022 — Forensics Challenges Writeup"
date: 2022-05-14 11:00:00 +0800
categories: [sig22ctf-IIUM]
tags: [ctf, forensics, steganography, pcap]
---

> We placed **1st** at IIUM CTF 2022. This post covers the Forensics category.

---

## Challenge 1 — "What's in the Image?"

**Points:** 100 | **Category:** Forensics — Steganography

Given a JPEG file. Ran basic checks:

```bash
file challenge.jpg
strings challenge.jpg | grep FLAG
exiftool challenge.jpg
```

`exiftool` revealed a comment field:

```
Comment: FLAG{m3tad4ta_t0ld_m3}
```

---

## Challenge 2 — "Hidden in Plain Sight"

**Points:** 200 | **Category:** Forensics — Steganography

PNG file with no obvious hints. Tried `steghide` — asked for passphrase. Tried empty string:

```bash
steghide extract -sf challenge.png -p ""
```

Extracted `secret.txt` with the flag:

```
FLAG{st3gh1d3_n0_p4ss}
```

---

## Challenge 3 — "Network Secrets"

**Points:** 300 | **Category:** Forensics — PCAP

Given a `.pcap` file. Opened in Wireshark and filtered HTTP:

```
http
```

Spotted a POST request to `/login` — form data visible in plaintext:

```
username=admin&password=s3cr3tP4ss&flag=FLAG{pcap_c4ptur3d}
```

> Lesson: HTTP sends credentials in cleartext. Always use HTTPS.
