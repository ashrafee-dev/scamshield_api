---
title: Rate Limits
description: API usage limits.
---

# Rate Limits

ScamShield applies IP-based rate limiting to protect the API.

When the limit is exceeded, the API returns:

```json
{
  "error":"Reached your limit, wait 60 seconds before requesting again"
}
```

Wait 60 seconds before sending another request.
