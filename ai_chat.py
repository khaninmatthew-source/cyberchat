import streamlit as st, google.genai as genai, io; from PIL import Image
st.set_page_config(page_title="Gemini Cybercore", page_icon="⚡", layout="centered")
st.markdown("""<style>
@import url('https://googleapis.com');
.stApp { background: #020005 !important; color: #00ffcc !important; font-family: 'Inter', sans-serif !important; overflow-x: hidden; }
header, footer {visibility: hidden !important;}
.cyber-bg { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; }
.bg-grid { position: absolute; width: 100%; height: 100%; background-image: linear-gradient(rgba(0,255,204,0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,204,0.015) 1px, transparent 1px); background-size: 30px 30px; background-position: center; }
.pulse-c { stroke-dasharray: 40, 120; stroke-dashoffset: 160; animation: run 2s infinite linear; filter: drop-shadow(0 0 8px #00ffcc); }
.pulse-p { stroke-dasharray: 30, 100; stroke-dashoffset: 130; animation: run 1.5s infinite linear; filter: drop-shadow(0 0 8px #ff007f); }
@keyframes run { to { stroke-dashoffset: 0; } }
h1 { font-family: 'Orbitron', sans-serif !important; background: linear-gradient(135deg, #00ffcc, #ff007f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900 !important; font-size: 2.6rem !important; text-shadow: 0 0 25px rgba(0,255,204,0.4); margin-bottom: 0px; }
.cyber-alert { background: rgba(255,0,127,0.06); border: 2px solid #ff007f; border-radius: 14px; padding: 15px; margin: 20px 0; box-shadow: 0 0 25px rgba(255,0,127,0.3), inset 0 0 15px rgba(255,0,127,0.2); }
.stChatMessage { background: rgba(5,3,12,0.9) !important; backdrop-filter: blur(15px); border: 1px solid rgba(0,255,204,0.2) !important; border-radius: 18px !important; margin-bottom: 16px !important; box-shadow: 0 0 15px rgba(0,0,0,0.6); }
.stChatMessage:hover { border-color: #00ffcc !important; box-shadow: 0 0 25px rgba(0,255,204,0.3) !important; transform: scale(1.01); transition: all 0.2s ease; }
.stChatInputContainer { border-radius: 24px !important; border: 2px solid #ff007f !important; background: #05030d !important; box-shadow: 0 0 30px rgba(255,0,127,0.3) !important; }
.stChatInputContainer:focus-within { border-color: #00ffcc !important; box-shadow: 0 0 35px rgba(0,255,204,0.5) !important; }
.stSpinner > div { border-top-color: #00ffcc !important; }
</style>
<div class="cyber-bg"><div class="bg-grid"></div>
<svg width="100%" height="100%" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice" xmlns="http://w3.org">
<g stroke-width="2" fill="none" opacity="0.35">
<path d="M500,400V0M470,400V200L350,80V0M440,400V230L260,50V0M530,400V200L650,80V0M560,400V230L740,50V0" stroke="rgba(0,255,204,0.2)"/>
<path d="M500,400V0M470,400V200L350,80V0M530,400V200L650,80V0" stroke="#00ffcc" class="pulse-c"/>
<path d="M500,600v400M460,600v180L320,900v50M420,600v210L240,950M540,600v180L680,900v50M580,600v210L760,950" stroke="rgba(255,0,127,0.2)"/>
<path d="M500,600v400M460,600v180L320,900v50M540,600v180L680,900v50" stroke="#ff007f" class="pulse-p"/>
<path d="M400,500H0M400,460H220L120,360H0M400,420H250L100,270H0M400,540H220L120,640H0M400,580H250L100,730H0" stroke="rgba(0,255,204,0.2)"/>
<path d="M400,500H0M400,460H220L120,360H0M400,540H220L120,640H0" stroke="#00ffcc" class="pulse-c"/>
<path d="M600,500H1000M600,460H780L880,360H1000M600,420H750L850,270H1000M600,540H780L880,640H1000M600,580H750L850,730H1000" stroke="rgba(255,0,127,0.2)"/>
<path d="M600,500H1000M600,460H780L880,360H1000M600,540H780L880,640H1000" stroke="#ff007f" class="pulse-p"/>
</g>
<g transform="translate(380,380)" opacity="0.4">
<rect x="0" y="0" width="240" height="240" rx="20" fill="#04010a" stroke="#ff007f" stroke-width="5" filter="drop-shadow(0 0 20px #ff007f)"/>
<rect x="20" y="20" width="200" height="200" rx="12" fill="#09051c" stroke="#00ffcc" stroke-width="3" filter="drop-shadow(0 0 15px #00ffcc)"/>
<g fill="#ff007f">
<rect x="5" y="40" width="10" height="5"/><rect x="5" y="70" width="10" height="5"/><rect x="5" y="100" width="10" height="5"/><rect x="5" y="130" width="10" height="5"/><rect x="5" y="160" width="10" height="5"/><rect x="5" y="190" width="10" height="5"/>
<rect x="225" y="40" width="10" height="5"/><rect x="225" y="70" width="10" height="5"/><rect x="225" y="100" width="10" height="5"/><rect x="225" y="130" width="10" height="5"/><rect x="225" y="160" width="10" height="5"/><rect x="225" y="190" width="10" height="5"/>
<rect x="40" y="5" width="5" height="10"/><rect x="70" y="5" width="5" height="10"/><rect x="100" y="5" width="5" height="10"/><rect x="130" y="5" width="5" height="10"/><rect x="160" y="5" width="5" height="10"/><rect x="190" y="5" width="5" height="10"/>
<rect x="40" y="225" width="5" height="10"/><rect x="70" y="225" width="5" height="10"/><rect x="100" y="225" width="5" height="10"/><rect x="130" y="225" width="5" height="10"/><rect x="160" y="225" width="5" height="10"/><rect x="190" y="225" width="5" height="10"/>
</g>
<rect x="60" y="60" width="120" height="120" rx="8" fill="#020005" stroke="#ff007f" stroke-width="2" stroke-dasharray="6,6"/>
<rect x="80" y="80" width="80" height="80" rx="4" fill="#000" stroke="#00ffcc" stroke-width="3" filter="drop-shadow(0 0 10px #00ffcc)"/>
<line x1="85" y1="120" x2="155" y2="120" stroke="#ff007f" stroke-width="2"/><line x1="120" y1="85" x2="120" y2="155" stroke="#ff007f" stroke-width="2"/>
<circle cx="120" cy="120" r="20" fill="none" stroke="#00ffcc" stroke-width="2.5"/><circle cx="120" cy="120" r="6" fill="#00ffcc"/>
<text x="25" y="215" fill="rgba(0,255,204,0.4)" font-family="Orbitron" font-size="9" font-weight="bold">HEX_CORE_v3.5</text>
<text x="145" y="35" fill="rgba(255,0,127,0.4)" font-family="Orbitron" font-size="9" font-weight="bold">VRM_VCC</text>
</g></svg></div>""", unsafe_allow_html=True)
st.markdown("<h1>⚡ Quantum Core Premium AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='cyber-alert'><span style='color:#ff007f;font-weight:bold;'>🚨 СИСТЕМНЫЙ ПРОТОКОЛ:</span> <span style='color:#fff;'>Пауза <b>5-10 секунд</b> между запросами. Для генерации картинок пишите <b>нарисуй...</b></span></div>", unsafe_allow_html=True)
st.caption("Quantum Grid Engine v3.5 • Экстремальная неоновая сборка")
API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)
if "messages" not in st.session_state: st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.image(message["content"]) if message["type"] == "image" else st.markdown(message["content"])
if prompt := st.chat_input("Запуск квантового потока данных..."):
    with st.chat_message("user"): st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        if prompt.lower().startswith(("нарисуй", "draw", "картинка", "image", "создай картинку")):
            with st.spinner("🤖 Генерация графической матрицы Imagen 3..."):
                try:
                    result = client.models.generate_images(model='imagen-3.0-generate-002', prompt=prompt, config=genai.types.GenerateImagesConfig(number_of_images=1, output_mime_type="image/jpeg", aspect_ratio="1:1"))
                    for generated_image in result.generated_images:
                        image = Image.open(io.BytesIO(generated_image.image.image_bytes)); message_placeholder.image(image)
                        st.session_state.messages.append({"role": "assistant", "content": image, "type": "image"})
                except Exception as e: message_placeholder.error(f"Сбой графического ядра: {e}")
        else:
            with st.spinner("⚡ Вычисление ответа через ядро Gemini Cloud..."):
                try:
                    response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt, config=genai.types.GenerateContentConfig(max_output_tokens=1500, temperature=0.7))
                    answer = response.text; message_placeholder.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer, "type": "text"})
                except Exception as e: message_placeholder.error(f"Критический сбой шифрования потока: {e}")
