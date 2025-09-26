# 🤖 Sales Email Agent (with Hugging Face + Gmail)

This project is a simple **agentic workflow** for sending automated outreach emails.  
It uses:

- **Hugging Face Inference API** (via OpenAI-compatible client) → to generate professional emails.
- **Gmail SMTP API** → to send the generated emails.
- **.env file** → to manage secrets safely.

---

## ⚡ Features
- Generates personalized email text using the `Qwen2-7B-Instruct` model.
- Sends emails automatically via Gmail.
- Modular agent design:
  - `ResearchAgent` → finds prospects (demo data here).
  - `ComposerAgent` → writes the email with AI.
  - `OutreachAgent` → sends the email.

---

## 📦 Requirements

- Python 3.10+
- Install dependencies:
  ```bash
  pip install openai python-dotenv
