import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("key.env")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("📋 النماذج المتاحة في حسابك:\n")
try:
    models = client.models.list()
    for m in models.data:
        print(f"  ✅ {m.id}")
except Exception as e:
    print("❌ خطأ:", e)