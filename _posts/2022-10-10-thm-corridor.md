---
title: "TryHackMe: Corridor — Writeup"
date: 2022-10-10 10:00:00 +0800
categories: [TryHackMe]
tags: [ctf, web, idor, md5, hash]
---

## Overview

**Corridor** is an easy TryHackMe room that teaches Insecure Direct Object Reference (IDOR) via MD5-hashed room parameters. If you can predict or enumerate the hash, you can access objects you shouldn't.

---

## Recon

Web app — a corridor image with clickable doors. Each door links to a URL like:

```
http://10.10.x.x/c4ca4238a0b923820dcc509a6f75849b
```

That hash looked familiar — MD5 of `1`:

```bash
echo -n "1" | md5sum
# c4ca4238a0b923820dcc509a6f75849b
```

The doors are numbered 1–13 with their MD5 hashes as the path.

---

## IDOR — Hash `0`

Tried the MD5 of `0`:

```bash
echo -n "0" | md5sum
# cfcd208495d565ef66e7dff9f98764da
```

```
http://10.10.x.x/cfcd208495d565ef66e7dff9f98764da
```

Flag returned directly — room 0 was hidden from the UI but accessible via the hash.

```
FLAG{— IDOR via hash enumeration}
```

---

## Key Takeaway

Hashing an ID doesn't make it secret — if the hash function is predictable and the space is small (e.g. integers 0–100), it's trivially brute-forced. Authorization checks must happen server-side, not rely on obscurity.
