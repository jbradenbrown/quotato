# 🎯 Prompt Experiments — Quotato

A living document of prompts used across the system. Keep track of what works, what's worth tweaking, and what's brittle.

---

## ✉️ Quote Email Prompt

**Purpose:** Generate a polite email requesting a service quote.

**Prompt Template:**

## Vendor Json Generator
**Purpose**

**Prompt Template:**
I’m in {CITY}.

    Find custom glass tabletop fabricators (minimum 5, maximum 8) that serve this city.

    For each company return a single JSON object with exactly these keys (all strings except services, which is an array of short strings):

{
  "name": "",
  "phone": "",
  "address": "",
  "website": "",
  "contact_form_url": "",
  "services": [],
  "support_notes": ""
}

    Combine them into a JSON array—no extra text before or after.

    Immediately beneath the JSON, list your web citations in plain text.

    Use web browsing to verify phone numbers and contact‑/quote‑form URLs and to ensure they actually cut tabletops (not just windows).

    Prefer companies within 30 miles of downtown {CITY}; if you must include one farther away, note the distance in support_notes.

    Be concise—limit support_notes to one sentence.

    If you can’t find at least five valid entries, say “FEWER THAN 5 RESULTS” instead of the JSON.”

## Vendor Prompts Used

**Prompt List** 
can you find local glass companies in seattle that can create custom glass tabletop? I would a list of them with their contact information, extra information, and any differences in their support? 

can you give me this information in a json? Also find any scheduling or contact forms? 