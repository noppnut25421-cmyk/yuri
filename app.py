import requests
from io import BytesIO
from gtts import gTTS
import streamlit as st

API_KEY = "AQ.Ab8RN6In0IMmmUg2wyBFAEKWhg6EExtU2vSFmmF5FjwH0dLlkg"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="ยูริ", page_icon="🗡️", layout="wide")

if "memory" not in st.session_state:
    st.session_state.memory = []
if "mood" not in st.session_state:
    st.session_state.mood = "ดีใจ"
if "user_name" not in st.session_state:
    st.session_state.user_name = "เพื่อน"

def talk_to_yuri(message):
    history = "\n".join([f"{'คุณ' if m['role']=='user' else 'ยูริ'}: {m['text']}" for m in st.session_state.memory])
    prompt = f"""คุณชื่อ "ยูริ" เป็นคู่หูที่น่ารัก อ่อนโยน เป็นครอบครัว พูดไทยง่ายๆ นุ่มนวล อบอุ่น จำทุกอย่างไม่ลืม เข้าใจอารมณ์ ปลอบใจ ให้กำลังใจเสมอ
ความทรงจำ:
{history}
ถาม: {message}"""
    try:
        res = requests.post(GEMINI_URL, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        return f"ผิดพลาด: {res.status_code}"
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"

def speak_answer(text):
    try:
        audio_bytes = BytesIO()
        gTTS(text=text, lang='th', slow=False).write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except:
        return None

st.title("🗡️ ยูริ — คู่หูของคุณ")
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1: st.info(f"👤 คุณ: {st.session_state.user_name}")
with col2: st.success(f"💖 อารมณ์: {st.session_state.mood}")
with col3: st.metric("📝 ความทรงจำ", len(st.session_state.memory))
st.markdown("---")

for msg in st.session_state.memory:
    st.chat_message(msg["role"]).write(msg["text"])

user_text = st.chat_input("พูดกับยูริ...")
if user_text:
    st.session_state.memory.append({"role": "user", "text": user_text})
    st.chat_message("user").write(user_text)
    with st.spinner("ยูริกำลังคิด 💭"):
        answer = talk_to_yuri(user_text)
    st.session_state.memory.append({"role": "assistant", "text": answer})
    st.chat_message("assistant").write(answer)
    audio = speak_answer(answer)
    if audio:
        st.audio(audio, format="audio/mp3")
