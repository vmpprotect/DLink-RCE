# D-Link DVG-N5402GF – Authenticated RCE

Credits to [me](https://github.com/vmpprotect) ( finding rce ) and [nitrix](https://github.com/prodbyskid) ( showing me router and helping out when i was stumped )

## Summary

An authenticated command injection vulnerability exists in the **DVG-N5402GF** router.  
The Ping diagnostic page fails to sanitize user input, allowing arbitrary command execution as `root`.

---

## Affected Device

- Vendor: D-Link  
- Model: DVG-N5402GF  
- Component: Login -> Maintenance -> Diagnostics -> Ping Test
- Fofa Query: `"D-Link VoIP Wireless Router"`
---

## Vulnerability

The **Ping Destination** parameter is passed directly to a shell command with little filtering.
The filtering can just be wiped with using anything with letters, example localhost.

Example payload:

```
localhost;echo hi
```

This will execute `echo  hi` ( duh ) with full superuser priviliges.

---

<p align="center">
  <img src="https://i.imgur.com/oV6VgUb.png" alt="RCE Proof">
</p>
