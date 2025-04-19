# 🥔 Quotato

**Quotato** is an AI-powered agent that finds and compares service quotes (like plumbers, glass repair, contractors, and more). It autonomously searches for local vendors, gathers pricing information through emails or calls, and organizes the results into a clean report — so you don’t have to.

This is a proof-of-concept built to explore autonomous AI workflows for real-world service discovery and comparison.

---

## 🚀 Features

- 🔍 Autonomous local vendor discovery
- 📬 Quote collection via email (calls coming soon!)
- 📊 Clean report generation with organized pricing
- 💾 Stores and logs all findings for transparency and debugging
- 🧠 Optional human-in-the-loop confirmations for safer testing

---

## 📦 Tech Stack

- Python + LangChain (or another agent framework)
- Email automation (SMTP / IMAP or service APIs)
- Call integration via Twilio (planned)
- Local data sources via Google Search / Yelp / custom scrapers
- SQLite or Postgres for logging results
- FastAPI or CLI for triggering quote hunts

---

## 🔧 Setup

```bash
git clone https://github.com/yourname/quotato.git
cd quotato
pip install -r requirements.txt
cp .env.example .env  # Fill in API keys and config

```

___

## Issues Found

- chat gpt is not able to easily navigate the website forms, they are often nested and have drop downs
- 