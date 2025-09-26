import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
from dotenv import load_dotenv

# ==============================================================================
# Hugging Face Inference API (Using OpenAI-Compatible Endpoint)
#
# Instructions:
# 1. Get your API Key with 'write' permissions from https://huggingface.co/settings/tokens
# 2. Set it as an environment variable named 'HF_TOKEN'.
#    - For Linux/macOS: export HF_TOKEN='your_key_here'
#    - For Windows: set HF_TOKEN='your_key_here'
# ==============================================================================

# Initialize the OpenAI client to point to Hugging Face's router
try:
    load_dotenv()
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HF_TOKEN"),
    )
except KeyError:
    raise ValueError("Hugging Face token not found. Please set the HF_TOKEN environment variable.")

# Using the specified Qwen2 model
MODEL_NAME = "Qwen/Qwen2-7B-Instruct:featherless-ai"

def generate_email_with_llm(prompt: str) -> str:
    """
    Generates text using the Hugging Face Inference Router with the specified model.
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_tokens=200,  # Increased slightly for better email composition
            temperature=0.8,
        )
        # Extract the generated text from the response
        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error calling Hugging Face API via OpenAI client: {e}")
        # Provide a fallback message in case of an API error
        return "As an expert in AI, I can help your business grow."

# ==============================================================================
# Gmail SMTP (Free Email API)
#
# Instructions:
# 1. Enable 2-Step Verification on your Google Account.
# 2. Generate an App Password from https://myaccount.google.com/apppasswords
# 3. Set your email and app password as environment variables.
#    - export GMAIL_USER='your_email@gmail.com'
#    - export GMAIL_APP_PASSWORD='your_app_password'
# ==============================================================================
def send_email_gmail(to_email, subject, body):
    FROM_EMAIL = os.getenv("GMAIL_USER")  # your gmail_id
    APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD") # generated app password

    if not FROM_EMAIL or not APP_PASSWORD:
        print("❌ Gmail credentials not found. Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.")
        print("Skipping email send.")
        return

    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent successfully to {to_email} via Gmail!")
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication Error: Check your GMAIL_USER and GMAIL_APP_PASSWORD.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# =========================
# Simple Agent Workflow
# =========================
class ResearchAgent:
    def run(self):
        """Finds potential prospects."""
        return [{"name": "Kailash Jain", "email": "kailash.j@atriauniversity.edu.in"}]

class ComposerAgent:
    def run(self, prospect):
        """Writes a personalized email for a given prospect."""
        print(f"Writing email to {prospect['name']}...")
        # *** THIS IS THE ONLY CHANGE NEEDED TO GET ENGLISH OUTPUT ***
        prompt = f"""
        Write a short, polite, and professional email to {prospect['name']}.
        Introduce yourself as an AI consultant.
        Mention that you can help their business with customized AI solutions.
        End with a call to action for a brief call.
        Important: Do not include a subject line or a salutation like 'Dear ...'. Start directly with the email body.
        """
        email_body = generate_email_with_llm(prompt)
        return {"to": prospect["email"], "subject": "AI Solutions for Your Business", "body": email_body}

class OutreachAgent:
    def run(self, email_data):
        """Sends the composed email."""
        send_email_gmail(email_data["to"], email_data["subject"], email_data["body"])

# =========================
# Orchestration
# =========================
if __name__ == "__main__":
    research = ResearchAgent()
    composer = ComposerAgent()
    outreach = OutreachAgent()

    prospects = research.run()

    for prospect in prospects:
        print("-" * 20)
        email_data = composer.run(prospect)
        outreach.run(email_data)
        print("-" * 20)