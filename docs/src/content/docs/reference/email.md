---
title: Email Endpoint
description: Analyze email text.
---

# POST /email

Analyze an email for scam indicators.

## Request

```json
{
  "body":"Congratulations! You have won $10,000."
}
```

## Response

```json
{
  "label":"Scam",
  "score":0.98,
  "certainty":"High",
  "reason":"Urgent prize scam language."
}
```
