---
title: Quick Start
description: Make your first request to ScamShield.
---

# Quick Start

## Base URL

```text
https://api.scamshield.click
```

---

## Email Analysis

```bash
curl -X POST https://api.scamshield.click/email \
-H "Content-Type: application/json" \
-d '{
  "body":"Congratulations! You have won $10,000."
}'
```

---

## Audio Analysis

```bash
curl -X POST https://api.scamshield.click/audio \
-F "file=@sample.mp3"
```

---

## WebSocket

```
wss://api.scamshield.click/ws
```
