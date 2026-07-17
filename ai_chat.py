import streamlit as st, google.genai as genai, io; from PIL import Image
st.set_page_config(page_title="Gemini Quantum Core", page_icon="⚡", layout="centered")
st.markdown("""<style>
@import url('https://googleapis.com');
.stApp { background: #010003 !important; color: #00ffcc !important; font-family: 'Inter', sans-serif !important; overflow-x: hidden; }
header, footer {visibility: hidden !important;}
.cyber-bg { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; }
.bg-grid { position: absolute; width: 100%; height: 100%; background-image: linear-gradient(rgba(0,255,204,0.012) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,204,0.012) 1px, transparent 1px); background-size: 25px 25px; background-position: center; }
.pulse-c { stroke-dasharray: 50, 150; stroke-dashoffset: 200; animation: run 2.2s infinite linear; filter: drop-shadow(0 0 10px #00ffcc); }
.pulse-p { stroke-dasharray: 40, 110; stroke-dashoffset: 150; animation: run 1.6s infinite linear; filter: drop-shadow(0 0 10px #ff007f); }
@keyframes run { to { stroke-dashoffset: 0; } }
h1 { font-family: 'Orbitron', sans-serif !important; background: linear-gradient(135deg, #00ffcc, #ff007f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900 !important; font-size: 2.6rem !important; text-shadow: 0 0 25px rgba(0,255,204,0.4); }
.cyber-alert { background: rgba(255,0,127,0.05); border: 2px solid #ff007f; border-radius: 14px; padding: 15px; margin: 20px 0; box-shadow: 0 0 25px rgba(255,0,127,0.25), inset 0 0 15px rgba(255,0,127,0.15); }
.stChatMessage { background: rgba(4,2,10,0.92) !important; backdrop-filter: blur(15px); border: 1px solid rgba(0,255,204,0.18) !important; border-radius: 18px !important; margin-bottom: 16px !important; box-shadow: 0 0 20px rgba(0,0,0,0.7); }
.stChatMessage:hover { border-color: #00ffcc !important; box-shadow: 0 0 25px rgba(0,255,204,0.25) !important; transform: scale(1.01); transition: all 0.2s ease; }
.stChatInputContainer { border-radius: 24px !important; border: 2px solid #ff007f !important; background: #04020a !important; box-shadow: 0 0 30px rgba(255,0,127,0.25) !important; }
.stChatInputContainer:focus-within { border-color: #00ffcc !important; box-shadow: 0 0 35px rgba(0,255,204,0.45) !important; }
.stSpinner > div { border-top-color: #00ffcc !important; }
</style>
<div class="cyber-bg"><div class="bg-grid"></div>
<svg width="100%" height="100%" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice" xmlns="http://w3.org">
<g stroke-width="1.5" fill="none" opacity="0.45">
<path d="M500,400V0M470,400V200L350,80V0M440,400V230L260,50V0M530,400V200L650,80V0M560,400V230L740,50V0M410,200H590M350,80H650" stroke="rgba(0,255,204,0.15)"/>
<path d="M500,400V0M470,400V200L350,80V0M530,400V200L650,80V0" stroke="#00ffcc" class="pulse-c"/>
<path d="M500,600v400M460,600v180L320,900v50M420,600v210L240,950M540,600v180L680,900v50M580,600v210L760,950M320,900h360" stroke="rgba(255,0,127,0.15)"/>
<path d="M500,600v400M460,600v180L320,900v50M540,600v180L680,900v50" stroke="#ff007f" class="pulse-p"/>
<path d="M400,500H0M400,460H220L120,360H0M400,420H250L100,270H0M400,540H220L120,640H0M400,580H250L100,730H0M220,460v80" stroke="rgba(0,255,204,0.15)"/>
<path d="M400,500H0M400,460H220L120,360H0M400,540H220L120,640H0" stroke="#00ffcc" class="pulse-c"/>
<path d="M600,500H1000M600,460H780L880,360H1000M600,420H750L850,270H1000M600,540H780L880,640H1000M600,580H750L850,730H1000M780,460v80" stroke="rgba(255,0,127,0.15)"/>
<path d="M600,500H1000M600,460H780L880,360H1000M600,540H780L880,640H1000" stroke="#ff007f" class="pulse-p"/>
</g>
<g font-family="Orbitron" font-size="11" fill="rgba(0,255,204,0.25)" font-weight="bold">
<text x="30" y="50">TEMP: 34°C</text><text x="30" y="75">VOLT: 1.25V</text>
<text x="830" y="50">FREQ: 5.8 GHz</text><text x="830" y="75">CORE: OCTA</text>
<text x="30" y="940">DATA_BUS: 0101011010</text><text x="820" y="940">SYSTEM: ONLINE</text>
</g>
<g stroke="rgba(0,255,204,0.2)" stroke-width="1.5" fill="none">
<path d="M20,60V20H60M940,20h40v40M20,940v40h40M980,940v-40h-40"/>
<circle cx="50" cy="50" r="8"/><circle cx="950" cy="50" r="8"/>
</g>
<g transform="translate(370,370)" opacity="0.45">
<rect x="0" y="0" width="260" height="260" rx="24" fill="none" stroke="#3b2d54" stroke-width="2"/>
<rect x="10" y="10" width="240" height="240" rx="20" fill="#030108" stroke="#ff007f" stroke-width="5" filter="drop-shadow(0 0 20px #ff007f)"/>
<rect x="30" y="30" width="200" height="200" rx="14" fill="#080417" stroke="#00ffcc" stroke-width="3" filter="drop-shadow(0 0 15px #00ffcc)"/>
<g fill="#ff007f">
<rect x="15" y="50" width="12" height="4"/><rect x="15" y="75" width="12" height="4"/><rect x="15" y="100" width="12" height="4"/><rect x="15" y="125" width="12" height="4"/><rect x="15" y="150" width="12" height="4"/><rect x="15" y="175" width="12" height="4"/><rect x="15" y="200" width="12" height="4"/>
<rect x="233" y="50" width="12" height="4"/><rect x="233" y="75" width="12" height="4"/><rect x="233" y="100" width="12" height="4"/><rect x="233" y="125" width="12" height="4"/><rect x="233" y="150" width="12" height="4"/><rect x="233" y="175" width="12" height="4"/><rect x="233" y="200" width="12" height="4"/>
<rect x="50" y="15" width="4" height="12"/><rect x="75" y="15" width="4" height="12"/><rect x="100" y="15" width="4" height="12"/><rect x="125" y="15" width="4" height="12"/><rect x="150" y="15" width="4" height="12"/><rect x="175" y="15" width="4" height="12"/><rect x="200" y="15" width="4" height="12"/>
<rect x="50" y="233" width="4" height="12"/><rect x="75" y="233" width="4" height="12"/><rect x="100" y="233" width="4" height="12"/><rect x="125" y="233" width="4" height="12"/><rect x="150" y="233" width="4" height="12"/><rect x="175" y="233" width="4" height="12"/><rect x="200" y="233" width="4" height="12"/>
</g>
<rect x="70" y="70" width="120" height="120" rx="10" fill="#010004" stroke="#ff007f" stroke-width="2" stroke-dasharray="5,5"/>
<rect x="90" y="90" width="80" height="80" rx="6" fill="#000" stroke="#00ffcc" stroke-width="3.5" filter="drop-shadow(0 0 12px #00ffcc)"/>
<g stroke="#ff007f" stroke-width="1.5">
<rect x="100" y="100" width="25" height="25" rx="2" fill="none"/><rect x="135" y="100" width="25" height="25" rx="2" fill="none"/>
<rect x="100" y="135" width="25" height="25" rx="2" fill="none"/><rect x="135" y="135" width="25" height="25" rx="2" fill="none"/>
</g>
<circle cx="130" cy="130" r="28" fill="none" stroke="#00ffcc" stroke-width="2" stroke-dasharray="4,2"/>
<circle cx="130" cy="130" r="8" fill="#00ffcc" filter="drop-shadow(0 0 5px #00ffcc)"/>
<text x="35" y="222" fill="rgba(0,255,204,0.5)" font-family="Orbitron" font-size="9" font-weight="bold">SOCKET_LGA_VERTEX</text>
</g></svg></div>""", unsafe_allow_html=True)
st.markdown("<h1>⚡ Quantum Core Premium AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='cyber-alert'><span style='color:#ff007f;font-weight:bold;'>🚨 СИСТЕМНЫЙ ПРОТОКОЛ:</span> <span style='color:#fff;'>Пауза <b>5-10 секунд</b> между запросами. Для генерации картинок пишите <b>нарисуй...</b></span></div>", unsafe_allow_html=True)
st.caption("Quantum Grid Engine v3.5 • Максимальная инженерная детализация")
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
