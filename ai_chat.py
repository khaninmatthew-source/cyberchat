import streamlit as st
import google.genai as genai
import io
from PIL import Image

st.set_page_config(page_title="Gemini Quantum Core", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .stApp { background-color: #020104 !important; color: #00ffcc !important; font-family: 'Inter', sans-serif !important; overflow-x: hidden; }
    header, footer {visibility: hidden !important;}
    .cyber-background { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; }
    .bg-grid { position: absolute; width: 100%; height: 100%; background-image: linear-gradient(rgba(0, 255, 204, 0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 204, 0.015) 1px, transparent 1px); background-size: 40px 40px; background-position: center center; }
    .pulse-path { stroke-dasharray: 30, 150; stroke-dashoffset: 180; animation: laserRun 3s infinite linear; }
    .pulse-path-fast { stroke-dasharray: 15, 100; stroke-dashoffset: 115; animation: laserRun 1.8s infinite linear; }
    @keyframes laserRun { to { stroke-dashoffset: 0; } }
    h1 { font-family: 'Orbitron', sans-serif !important; background: linear-gradient(135deg, #00ffcc 0%, #ff007f 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900 !important; font-size: 2.4rem !important; letter-spacing: 2px !important; text-shadow: 0 0 20px rgba(0, 255, 204, 0.2); z-index: 2; position: relative; }
    .cyber-alert { background: rgba(255, 0, 127, 0.04); border: 1px solid rgba(255, 0, 127, 0.25); border-radius: 14px; padding: 15px 20px; margin: 20px 0; box-shadow: 0 0 15px rgba(255, 0, 127, 0.05); z-index: 2; position: relative; }
    .stChatMessage { background: rgba(6, 4, 15, 0.85) !important; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(0, 255, 204, 0.12) !important; border-radius: 18px !important; margin-bottom: 16px !important; padding: 16px !important; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5); z-index: 2; position: relative; }
    .stChatInputContainer { border-radius: 24px !important; border: 2px solid #ff007f !important; background-color: #05030d !important; box-shadow: 0 0 25px rgba(255, 0, 127, 0.15) !important; z-index: 2; position: relative; }
    .stChatInputContainer:focus-within { border-color: #00ffcc !important; box-shadow: 0 0 25px rgba(0, 255, 0, 0.25) !important; }
    .stSpinner > div { border-top-color: #00ffcc !important; }
    </style>
    <div class="cyber-background">
        <div class="bg-grid"></div>
        <svg width="100%" height="100%" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice" xmlns="http://w3.org">
            <defs>
                <filter id="glow-cyan" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5" result="blur" /><feComposite in="SourceGraphic" in2="blur" operator="over" /></filter>
                <filter id="glow-pink" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5" result="blur" /><feComposite in="SourceGraphic" in2="blur" operator="over" /></filter>
            </defs>
            <!-- СЛОЖНАЯ СЕТЬ МИКРОДОРОЖЕК С УГЛАМИ 45 ГРАДУСОВ -->
            <g stroke-width="1.2" fill="none">
                <!-- Квантовый Пучок Вверх -->
                <path d="M500,400 L500,50 M470,400 L470,220 L380,130 L380,50 M440,400 L440,250 L320,130 L320,50 M530,400 L530,220 L620,130 L620,50 M560,400 L560,250 L680,130 L680,50" stroke="rgba(0, 255, 204, 0.1)" />
                <path d="M500,400 L500,50 M470,400 L470,220 L380,130 L380,50 M530,400 L530,220 L620,130 L620,50" stroke="#00ffcc" class="pulse-path" filter="url(#glow-cyan)" />
                <!-- Системные подписи на плате -->
                <text x="505" y="80" fill="rgba(0, 255, 204, 0.3)" font-family="Orbitron" font-size="8">SYS_BUS_A</text>
                <text x="325" y="80" fill="rgba(0, 255, 204, 0.3)" font-family="Orbitron" font-size="8">VCC_CORE</text>

                <!-- Квантовый Пучок Вниз -->
                <path d="M500,600 L500,950 M460,600 L460,780 L340,900 L340,950 M420,600 L420,810 L260,950 M540,600 L540,780 L660,900 L660,950 M580,600 L580,810 L740,950" stroke="rgba(255, 0, 127, 0.1)" />
                <path d="M500,600 L500,950 M460,600 L460,780 L340,900 L340,950 M540,600 L540,780 L660,900 L660,950" stroke="#ff007f" class="pulse-path-fast" filter="url(#glow-pink)" />

                <!-- Квантовый Пучок Влево -->
                <path d="M400,500 L50,500 M400,460 L220,460 L130,370 L50,370 M400,420 L250,420 L100,270 L50,270 M400,540 L220,540 L130,630 L50,630 M400,580 L250,580 L100,730 L50,730" stroke="rgba(0, 255, 204, 0.1)" />
                <path d="M400,500 L50,500 M400,460 L220,460 L130,370 L50,370 M400,540 L220,540 L130,630 L50,630" stroke="#00ffcc" class="pulse-path-fast" filter="url(#glow-cyan)" />

                <!-- Квантовый Пучок Вправо -->
                <path d="M600,500 L950,500 M600,460 L780,460 L870,370 L950,370 M600,420 L750,420 L850,270 L950,270 M600,540 L780,540 L870,630 L950,630 M600,580 L750,580 L850,730 L950,730" stroke="rgba(255, 0, 127, 0.1)" />
                <path d="M600,500 L950,500 M600,460 L780,460 L870,370 L950,370 M600,540 L780,540 L870,630 L950,630" stroke="#ff007f" class="pulse-path" filter="url(#glow-pink)" />
            </g>

            <!-- СВЕРХДЕТАЛИЗИРОВАННЫЙ СВЕТЯЩИЙСЯ ЧИП (ЦЕНТР) -->
            <g transform="translate(400, 400)" opacity="0.16">
                <!-- 1. Внешнее монтажное кольцо -->
                <rect x="0" y="0" width="200" height="200" rx="16" fill="none" stroke="#ff007f" stroke-width="2" opacity="0.5"/>
                <!-- 2. Главная подложка процессора -->
                <rect x="10" y="10" width="180" height="180" rx="12" fill="#070414" stroke="#ff007f" stroke-width="4" filter="url(#glow-pink)"/>
                <!-- 3. Золотые ножки контактов (Многослойные) -->
                <g fill="#00ffcc" opacity="0.8">
                    <rect x="18" y="35" width="6" height="3"/><rect x="18" y="55" width="6" height="3"/><rect x="18" y="75" width="6" height="3"/><rect x="18" y="95" width="6" height="3"/><rect x="18" y="115" width="6" height="3"/><rect x="18" y="135" width="6" height="3"/><rect x="18" y="155" width="6" height="3"/>
                    <rect x="176" y="35" width="6" height="3"/><rect x="176" y="55" width="6" height="3"/><rect x="176" y="75" width="6" height="3"/><rect x="176" y="95" width="6" height="3"/><rect x="176" y="115" width="6" height="3"/><rect x="176" y="135" width="6" height="3"/><rect x="176" y="155" width="6" height="3"/>
                    <rect x="35" y="18" width="3" height="6"/><rect x="55" y="18" width="3" height="6"/><rect x="75" y="18" width="3" height="6"/><rect x="95" y="18" width="3" height="6"/><rect x="115" y="18" width="3" height="6"/><rect x="135" y="18" width="3" height="6"/><rect x="155" y="18" width="3" height="6"/>
                    <rect x="35" y="176" width="3" height="6"/><rect x="55" y="176" width="3" height="6"/><rect x="75" y="176" width="3" height="6"/><rect x="95" y="176" width="3" height="6"/><rect x="115" y="176" width="3" height="6"/><rect x="135" y="176" width="3" height="6"/><rect x="155" y="176" width="3" height="6"/>
                </g>
                <!-- 4. Металлическая защитная крышка кристалла -->
                <rect x="35" y="35" width="130" height="130" rx="8" fill="#0f0b26" stroke="#00ffcc" stroke-width="2" filter="url(#glow-cyan)"/>
                <!-- Inner Сircuit (Внутренние дорожки кристалла) -->
                <rect x="55" y="55" width="90" height="90" rx="4" fill="#030208" stroke="#ff007f" stroke-width="1" stroke-dasharray="4,4"/>
                <!-- 5. Вычислительное Квантовое Ядро -->
                <rect x="70" y="70" width="60" height="60" rx="2" fill="#010003" stroke="#00ffcc" stroke-width="2"/>
                <!-- Лазерный прицел внутри ядра -->
                <line x1="75" y1="100" x2="125" y2="100" stroke="#ff007f" stroke-width="1.5" filter="url(#glow-pink)"/>
                <line x1="100" y1="75" x2="100" y2="125" stroke="#ff007f" stroke-width="1.5" filter="url(#glow-pink)"/>
                <circle cx="100" cy="100" r="14" fill="none" stroke="#00ffcc" stroke-width="2" filter="url(#glow-cyan)"/>
                <circle cx="100" cy="100" r="4" fill="#00ffcc"/>
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
