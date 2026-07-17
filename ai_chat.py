import streamlit as st
import google.genai as genai
import io
from PIL import Image

st.set_page_config(page_title="Gemini Quantum Core", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .stApp { background-color: #040208 !important; color: #00ffcc !important; font-family: 'Inter', sans-serif !important; overflow-x: hidden; }
    header, footer {visibility: hidden !important;}
    .cyber-background { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; }
    .bg-grid { position: absolute; width: 100%; height: 100%; background-image: linear-gradient(rgba(0, 255, 204, 0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 204, 0.02) 1px, transparent 1px); background-size: 50px 50px; background-position: center center; }
    .pulse-path { stroke-dasharray: 40, 200; stroke-dashoffset: 240; animation: laserRun 4s infinite linear; }
    .pulse-path-fast { stroke-dasharray: 20, 150; stroke-dashoffset: 170; animation: laserRun 2.5s infinite linear; }
    @keyframes laserRun { to { stroke-dashoffset: 0; } }
    h1 { font-family: 'Orbitron', sans-serif !important; background: linear-gradient(135deg, #00ffcc 0%, #ff007f 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900 !important; font-size: 2.4rem !important; letter-spacing: 2px !important; text-shadow: 0 0 20px rgba(0, 255, 204, 0.2); z-index: 2; position: relative; }
    .cyber-alert { background: rgba(255, 0, 127, 0.04); border: 1px solid rgba(255, 0, 127, 0.25); border-radius: 14px; padding: 15px 20px; margin: 20px 0; box-shadow: 0 0 15px rgba(255, 0, 127, 0.05); z-index: 2; position: relative; }
    .stChatMessage { background: rgba(8, 5, 20, 0.82) !important; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(0, 255, 204, 0.12) !important; border-radius: 18px !important; margin-bottom: 16px !important; padding: 16px !important; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); z-index: 2; position: relative; }
    .stChatMessage:hover { border-color: rgba(0, 255, 204, 0.3) !important; box-shadow: 0 0 20px rgba(0, 255, 204, 0.08); }
    .stChatInputContainer { border-radius: 24px !important; border: 2px solid #ff007f !important; background-color: #080514 !important; box-shadow: 0 0 25px rgba(255, 0, 127, 0.15) !important; z-index: 2; position: relative; }
    .stChatInputContainer:focus-within { border-color: #00ffcc !important; box-shadow: 0 0 25px rgba(0, 255, 0, 0.25) !important; }
    .stSpinner > div { border-top-color: #00ffcc !important; }
    </style>
    <div class="cyber-background">
        <div class="bg-grid"></div>
        <svg width="100%" height="100%" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice" xmlns="http://w3.org">
            <defs>
                <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4" result="blur" /><feComposite in="SourceGraphic" in2="blur" operator="over" /></filter>
                <filter id="glow-pink" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4" result="blur" /><feComposite in="SourceGraphic" in2="blur" operator="over" /></filter>
            </defs>
            <g stroke-width="1.5" fill="none">
                <path d="M500,410 L500,100 M480,410 L480,200 L400,120 L400,50 M520,410 L520,200 L600,120 L600,50" stroke="rgba(0, 255, 204, 0.15)" />
                <path d="M500,410 L500,100 M480,410 L480,200 L400,120 L400,50 M520,410 L520,200 L600,120 L600,50" stroke="#00ffcc" class="pulse-path" filter="url(#glow-cyan)" />
                <path d="M500,590 L500,900 M470,590 L470,750 L350,870 L350,950 M530,590 L530,750 L650,870 L650,950" stroke="rgba(255, 0, 127, 0.15)" />
                <path d="M500,590 L500,900 M470,590 L470,750 L350,870 L350,950 M530,590 L530,750 L650,870 L650,950" stroke="#ff007f" class="pulse-path-fast" filter="url(#glow-pink)" />
                <path d="M410,500 L50,500 M410,470 L250,470 L150,370 L0,370 M410,530 L250,530 L150,630 L0,630" stroke="rgba(0, 255, 204, 0.15)" />
                <path d="M410,500 L50,500 M410,470 L250,470 L150,370 L0,370 M410,530 L250,530 L150,630 L0,630" stroke="#00ffcc" class="pulse-path-fast" filter="url(#glow-cyan)" />
                <path d="M590,500 L950,500 M590,470 L750,470 L850,370 L1000,370 M590,530 L750,530 L850,630 L1000,630" stroke="rgba(255, 0, 127, 0.15)" />
                <path d="M590,500 L950,500 M590,470 L750,470 L850,370 L1000,370 M590,530 L750,530 L850,630 L1000,630" stroke="#ff007f" class="pulse-path" filter="url(#glow-pink)" />
            </g>
            <g transform="translate(410, 410)" opacity="0.18">
                <rect x="0" y="0" width="180" height="180" rx="14" fill="#09061a" stroke="#ff007f" stroke-width="4" filter="url(#glow-pink)"/>
                <rect x="20" y="20" width="140" height="140" rx="8" fill="#110d2c" stroke="#00ffcc" stroke-width="2" filter="url(#glow-cyan)"/>
                <g fill="#ff007f">
                    <rect x="5" y="30" width="8" height="4"/><rect x="5" y="50" width="8" height="4"/><rect x="5" y="70" width="8" height="4"/><rect x="5" y="90" width="8" height="4"/><rect x="5" y="110" width="8" height="4"/><rect x="5" y="130" width="8" height="4"/><rect x="5" y="145" width="8" height="4"/>
                    <rect x="167" y="30" width="8" height="4"/><rect x="167" y="50" width="8" height="4"/><rect x="167" y="70" width="8" height="4"/><rect x="167" y="90" width="8" height="4"/><rect x="167" y="110" width="8" height="4"/><rect x="167" y="130" width="8" height="4"/><rect x="167" y="145" width="8" height="4"/>
                    <rect x="30" y="5" width="4" height="8"/><rect x="50" y="5" width="4" height="8"/><rect x="70" y="5" width="4" height="8"/><rect x="90" y="5" width="4" height="8"/><rect x="110" y="5" width="4" height="8"/><rect x="130" y="5" width="4" height="8"/><rect x="145" y="5" width="4" height="8"/>
                    <rect x="30" y="167" width="4" height="8"/><rect x="50" y="167" width="4" height="8"/><rect x="70" y="167" width="4" height="8"/><rect x="90" y="167" width="4" height="8"/><rect x="110" y="167" width="4" height="8"/><rect x="130" y="167" width="4" height="8"/><rect x="145" y="167" width="4" height="8"/>
                </g>
                <rect x="55" y="55" width="70" height="70" rx="4" fill="#05030a" stroke="#00ffcc" stroke-width="1.5"/>
                <line x1="65" y1="65" x2="115" y2="65" stroke="#ff007f" stroke-width="2"/><line x1="65" y1="115" x2="115" y2="115" stroke="#ff007f" stroke-width="2"/><circle cx="90" cy="90" r="10" fill="none" stroke="#00ffcc" stroke-width="2" filter="url(#glow-cyan)"/>
            </g>
        </svg>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ Quantum Core Premium AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='cyber-alert'><span style='color: #ff007f; font-weight: bold;'>🚨 СИСТЕМНЫЙ ПРОТОКОЛ:</span> <span style='color: #ffffff;'>Выдерживайте паузу в <b>5-10 секунд</b> перед отправкой пакетов данных. Для рендеринга графики пишите <b>нарисуй...</b></span></div>", unsafe_allow_html=True)
st.caption("Quantum Grid Engine v3.5 • Все системы стабильны")

API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "image":
            st.image(message["content"])
        else:
            st.markdown(message["content"])

if prompt := st.chat_input("Запуск квантового потока данных..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        if prompt.lower().startswith(("нарисуй", "draw", "картинка", "image", "создай картинку")):
            with st.spinner("🤖 Генерация графической матрицы Imagen 3..."):
                try:
                    result = client.models.generate_images(model='imagen-3.0-generate-002', prompt=prompt, config=genai.types.GenerateImagesConfig(number_of_images=1, output_mime_type="image/jpeg", aspect_ratio="1:1"))
                    for generated_image in result.generated_images:
                        image = Image.open(io.BytesIO(generated_image.image.image_bytes))
                        message_placeholder.image(image)
                        st.session_state.messages.append({"role": "assistant", "content": image, "type": "image"})
                except Exception as e:
                    message_placeholder.error(f"Сбой графического ядра: {e}")
        else:
            with st.spinner("⚡ Вычисление ответа через ядро Gemini Cloud..."):
                try:
                    response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt, config=genai.types.GenerateContentConfig(max_output_tokens=1500, temperature=0.7))
                    answer = response.text
                    message_placeholder.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer, "type": "text"})
                except Exception as e:
                    message_placeholder.error(f"Критический сбой шифрования потока: {e}")
