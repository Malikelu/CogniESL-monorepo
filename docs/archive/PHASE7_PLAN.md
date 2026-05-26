# Phase 7 — UI/Brand Identity
**Status:** Planned — start after Phase 6 (User Accounts) is stable  
**Estimated effort:** 1–2 weeks  
**Goal:** CogniESL looks and feels like a real product. Logo exists. Product and website share the same visual identity. Ready for public launch.

---

## Why This Phase Exists

Right now:
- The **product** (the chat UI) has no logo, no brand colors, no identity
- The **website** has a thoughtful design system (teal #0D7377, coral #FF6B6B, gold #F4A261) but no logo
- The **email** has a header that just says "CogniESL" in plain text
- There is **zero visual consistency** between the product, the website, and the email

A teacher who discovers CogniESL on the website, uses the product, and gets a delivery email should feel like they're in the same world at every step. Right now they're in three different ones.

This phase fixes that.

---

## 7A — Logo Design

### What's needed
1. **Primary logo**: wordmark or logomark + wordmark — "CogniESL" in a typeface that feels smart but warm, not corporate
2. **Favicon**: 32×32 and 16×16 versions for browser tabs
3. **Email header version**: 200px wide, works on white and dark backgrounds
4. **App version**: fits in a 64px-tall navbar

### Design direction (from existing design system)
- **Colors**: Primary teal #0D7377, accent coral #FF6B6B or gold #F4A261
- **Feeling**: Intelligent but approachable. Not edtech-generic (no graduation caps, no apples). Think brain + language, or a subtle "C" mark.
- **Font**: The website uses Inter (heading) + Nunito (accent). The logo could use either, or a complementary display font.

### How to get a logo (options)
1. **Figma + AI generation**: Use Midjourney or Adobe Firefly to generate logomark concepts, then refine in Figma. Cost: ~$0–20.
2. **Looka or Brandmark**: AI logo tools. Generate 10+ concepts in minutes. Best ones: Looka ($65 for files), Brandmark ($25). Fast.
3. **Fiverr designer**: $50–150 for a human designer with 2–3 revision rounds. Better quality, 3–5 day turnaround.
4. **Claude + SVG**: I can generate SVG logo concepts directly — not production-quality, but useful for testing directions before committing to a designer.

**Recommendation**: Use Brandmark or Looka first (30 minutes, $25–65) to find a direction you like, then either use that or take it to a Fiverr designer for polish.

---

## 7B — Apply Logo Everywhere

### Product chat UI (`webui/`)
- Add logo to the top-left of the chat navbar
- Replace any plain "CogniESL" text with the logo image
- Apply the teal/coral palette to the chat UI buttons and header if not already present

### Website (`CogniESL Website/`)
- Add logo to `Navbar.tsx` (replace text "CogniESL")
- Add logo to `Footer.tsx`
- Add Open Graph image using the logo (for link previews on Twitter/LinkedIn/Slack)
- Add `apple-touch-icon` and favicon files to `public/`

### Email template (`agent/email_sender.py`)
- Replace the plain text "CogniESL" header with an `<img>` tag pointing to the logo hosted on the website
- Logo URL: `https://cogniesl.com/logo.png` (or similar)
- Add a fallback text version for email clients that block images

### Branded email example (target state):
```
[CogniESL logo — teal, 200px wide]
──────────────────────────────────
Your Present Perfect materials are ready! 🎉

[📊 Download Slides (PowerPoint)]    ← teal button
[📝 Download Worksheet]              ← teal button
[🎮 Download Activity Guide]         ← teal button
──────────────────────────────────
Need to change something? Go back to your chat.
CogniESL · cogniesl.com
```

---

## 7C — Product UI Color Alignment

The chat UI (Next.js `webui/`) was built before the design system was defined. It likely uses default blues or grays. This step aligns it with the website's palette.

### What to check
1. Does the chat UI use the teal #0D7377 primary color or something else?
2. Are buttons, links, and accents consistent with the website?
3. Is the font Inter (matching the website)?

### Steps
1. Audit `webui/` CSS/Tailwind config
2. Update primary color tokens to match: `#0D7377` (teal), `#FF6B6B` (coral), `#F4A261` (gold)
3. Update Navbar background, CTA buttons, and any accent elements
4. No full redesign — just color token updates and the logo addition

---

## 7D — Website Final Polish

The website is functionally complete but needs these before public launch:

### Real testimonials (highest priority)
- Current state: no testimonials (the "Trusted by" section was changed to "Built for" as a stopgap)
- Get 3–5 real quotes from beta users or colleagues who've seen the product
- Even one genuine quote from one teacher is infinitely more valuable than placeholder text
- Format: name, title (e.g., "ESL teacher, Austin TX"), 1–2 sentence quote

### Real screenshots in Samples page
- Current state: Samples page describes what's inside each format, but no actual images
- Add 2–3 real slide screenshots from the generated decks (present_simple_spanish, third_conditional test)
- One worksheet screenshot
- These are the most powerful conversion tool — teachers want to see the output before trusting it

### Open Graph image
- When someone shares cogniesl.com on Twitter/LinkedIn, it shows a link preview with an image
- Current: no OG image defined (or a placeholder)
- Create a 1200×630px branded image: logo + tagline + one slide screenshot

### Fix the `BlogPreview` section copy
- Currently imports from `BlogPreview` component on the homepage — verify the 3 blog posts display correctly and the "Read more" links work

---

## 7E — Domain & Deployment Prep

These aren't strictly brand, but they're pre-launch infrastructure:

### Domain
- cogniesl.com → Vercel (website)
- api.cogniesl.com or cogniesl.com/app → the FastAPI product server (Railway or similar)

### Analytics
- Add Plausible or Umami to the website (privacy-friendly, FERPA-safe)
- Track: page views, waitlist signups, which blog posts get traffic
- Don't use Google Analytics (FERPA implications with student data context)

### Waitlist → email list
- When teachers join the waitlist, their email should go somewhere you can actually reach them
- Check: does `/api/waitlist` in the website actually store emails anywhere? If not, wire it to Resend or a simple SQLite store
- Launch email: "We're live — here's how to get started" to everyone who waitlisted

---

## Implementation Order

```
7A: Commission/generate logo           → 1–3 days (depends on approach)
7B: Apply logo everywhere              → 2–3 hours
7C: Product UI color alignment         → 2–4 hours
7D: Website final polish               → depends on testimonials/screenshots
7E: Domain + analytics + waitlist fix  → 2–4 hours
```

**Total**: 1–2 weeks if done sequentially, faster if logo comes quickly.

---

## Success Criteria

- [ ] Logo exists as SVG/PNG in at least 3 sizes (full, nav, favicon)
- [ ] Logo appears in: website navbar, website footer, email header, product navbar
- [ ] Product chat UI uses teal #0D7377 as primary color
- [ ] At least 1 real teacher testimonial on the website
- [ ] At least 1 real screenshot of generated slides on the Samples page
- [ ] cogniesl.com resolves to the website
- [ ] Waitlist emails are actually being stored/received
- [ ] Plausible analytics installed

---

## Open Questions

1. **Who designs the logo?** You (with AI tools), a Fiverr designer, or me (SVG concept)?
2. **What's the product URL at launch?** Same domain as website (cogniesl.com/app), a subdomain (app.cogniesl.com), or a separate URL?
3. **Do you have Railway or another hosting set up for the product server?** If not, that's part of 7E.
4. **Do you have any teacher contacts who could give a real testimonial**, even informally? Even a screenshot of a WhatsApp message saying "this is great" works.
