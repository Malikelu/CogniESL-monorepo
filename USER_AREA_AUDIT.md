# CogniESL: User Area Audit
**Last updated:** 2026-05-24

---

## Fixed Since Last Audit

| Item | Status |
|------|--------|
| Usage counter — now shows monthly generations, not total stored | ✅ Fixed |
| FREE_TIER_LIMIT was 10, now fetched from API (correct value: 5) | ✅ Fixed |
| Stripe billing — checkout, webhook, founding counter | ✅ Built (untested) |
| Account settings page (/settings) | ✅ Built |
| Password reset flow | ✅ Built |
| Account deletion / GDPR | ✅ Built |
| Privacy Policy + Terms pages | ✅ Built |

---

## Remaining Bugs

### Bug 1: Chat does not send auth token ← HIGH PRIORITY
The chat (`ChatInterface.tsx`) does not include the `Authorization: Bearer {token}` header. This means:
- The server doesn't know who is generating → materials are not saved to accounts
- The generation counter doesn't increment for the right user
- Free tier enforcement works only when user is identified

**Fix:** In `ChatInterface.tsx`, when building fetch headers, add:
```javascript
const token = localStorage.getItem("cogniesl_token");
// Add to headers:
...(token ? { Authorization: `Bearer ${token}` } : {}),
```

### Bug 2: Regenerate link passes no context
The "↩ Regenerate" link opens `/?regenerate=present_simple&l1=Spanish` but the homepage doesn't read these params. Teacher has to re-type everything from scratch.

**Fix:** In `page.tsx`, read URL params on mount and inject a pre-fill message into chat context.

### Bug 3: Materials table missing `level` column
Materials cards don't show the proficiency level (A1, B1, etc.) and the Regenerate link can't reconstruct the full request without it.

**Fix:** Already done in `auth/db.py` (ALTER TABLE migration). The agent needs to pass `level` when saving the material after generation.

### Bug 4: Download links break on every redeploy
Railway uses ephemeral disk. Every `railway up` wipes `/app/mnt/`. Every download link in My Materials becomes a 404 until Railway Volume is attached (Phase F0).

**Workaround:** Add a "Regenerate" CTA when files are missing. Long-term fix: Railway Volume (Phase F0).

---

## Missing Features

| Feature | Priority | Phase |
|---------|----------|-------|
| Fix auth token in chat (Bug 1 above) | CRITICAL | Now |
| Railway Volume — persistent file storage | HIGH | F0 (before launch) |
| Stripe price IDs corrected in Railway | HIGH | B |
| Pending jobs visible in My Materials | MEDIUM | Post-launch |
| Email verification at registration | MEDIUM | Post-launch |
| Slide thumbnail preview on material cards | LOW | Post-launch |
| Bulk download ZIP | LOW | Post-launch |
| "Edit this deck" shortcut from My Materials | LOW | Post-launch |

---

## What's Working

- Register, login, JWT auth
- My Materials library with filters, delete, download buttons
- Usage meter (monthly, correct limits per tier)
- Settings page (account info, subscription, danger zone)
- Password reset end-to-end
- Privacy Policy + Terms of Service pages
- Pricing page with tier cards and founding member counter
- Stripe checkout + webhook (code complete, needs price ID fix to test)
- Founder dashboard at /admin
