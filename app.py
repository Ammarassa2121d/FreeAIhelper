import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("key.env")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# 🎯 اختر النموذج من القائمة هنا
MODEL = "qwen/qwen3.8-27b"
# بدائل:
# MODEL = "openai/gpt-oss-120b"
# MODEL = "allam-2-7b"
# MODEL = "openai/gpt-oss-20b"

st.set_page_config(page_title="مساعدي الذكي", page_icon="🤖")
st.title("🤖 مساعدي الذكي")

# إعدادات جانبية
with st.sidebar:
    st.header("⚙️ الإعدادات")
    model_choice = st.selectbox(
        "اختر النموذج:",
        [
            "qwen/qwen3.8-27b",
            "openai/gpt-oss-120b",
            "allam-2-7b",
            "openai/gpt-oss-20b",
        ],
        index=0
    )
    temperature = st.slider("الإبداعية", 0.0, 1.0, 0.7, 0.1)
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = [
            {"role": "system", "content": "أنت مساعد ذكي ومفيد، تجيب بالعربية بوضوح."}
        ]
        st.rerun()

# تهيئة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنت مساعد ذكي ومفيد، تجيب بالعربية بوضوح."}
    ]

# عرض الرسائل السابقة
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        st.write(msg["content"])

# إدخال المستخدم
if prompt := st.chat_input("اكتب رسالتك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    
    with st.chat_message("assistant", avatar="🤖"):
        try:
            response = client.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages,
                temperature=temperature,
                stream=True  # ← يظهر الرد كلمة كلمة (تجربة أفضل)
            )
            
            # تجميع الرد المتدفق
            reply = ""
            placeholder = st.empty()
            for chunk in response:
                if chunk.choices[0].delta.content:
                    reply += chunk.choices[0].delta.content
                    placeholder.write(reply + "▌")
            placeholder.write(reply)
            
            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )
        except Exception as e:
            st.error(f"❌ خطأ: {e}")