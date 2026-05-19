---
title: "PicoCTF 2023 — Selected Writeups (Top 20%)"
date: 2023-06-15 10:00:00 +0200
categories: [PicoCTF]
tags: [ctf, web, forensics, crypto, linux, binary]
---

## Overview

Competed in PicoCTF 2023 and finished in the **top 20% globally**. Here are writeups for the challenges I found most interesting.

---

## Web — "findme"

**Points:** 150

Clicking "login" performs multiple redirects. Intercepted with Burp:

```
HTTP/1.1 302 Found
Location: /next-page/id=cGljb0NURntwcjB4eV9...
```

Each redirect contained a Base64-encoded piece of the flag. Decoded all parts and concatenated:

```bash
echo "cGljb0NURntwcjB4eV9..." | base64 -d
```

```
picoCTF{pr0xy_j1ggl1ng_...}
```

---

## Forensics — "hideme"

**Points:** 100

PNG file. Checked for hidden data after the IEND chunk:

```bash
binwalk challenge.png
```

`binwalk` found a ZIP archive appended to the PNG. Extracted:

```bash
binwalk -e challenge.png
cd _challenge.png.extracted
unzip *.zip
cat flag
```

```
picoCTF{h1dd3n_1n_pl41n_s1ght}
```

---

## Crypto — "rotation"

**Points:** 100

Ciphertext using a rotational cipher with an unknown shift. Wrote a quick brute-force:

```python
ciphertext = "xqkwKBN{z0bib1wv_p2bkbxb0_i521bab0}"
for shift in range(26):
    result = ""
    for c in ciphertext:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr((ord(c) - base - shift) % 26 + base)
        else:
            result += c
    if "picoCTF" in result:
        print(f"Shift {shift}: {result}")
```

Shift 18 gave the flag.

---

## Binary Exploitation — "two-sum"

**Points:** 100

Integer overflow challenge in C. The program checks if `a + b > MAX_INT`. Since C integers wrap on overflow, passing two large positive numbers causes the sum to wrap to a negative value, bypassing the check:

```bash
python3 -c "print(2147483647); print(2147483647)"  | nc mercury.picoctf.net PORT
```

```
picoCTF{tw0_s4m_a8f3dc9b}
```
