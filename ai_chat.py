import streamlit as st
import google.genai as genai
import io
from PIL import Image

# Ультра-премиальные настройки страницы
st.set_page_config(page_title="Gemini Quantum Core", page_icon="⚡", layout="centered")

# Высокодетализированный дизайн с живой анимированной материнской платой на фоне
st.markdown("""
    <style>
    @import url('https://googleapis.com');

    /* Главное рабочее пространство глубокого космического цвета */
    .stApp { 
        background-color: #06040d !important;
        color: #00ffcc !important; 
        font-family: 'Inter', sans-serif !important;
        overflow-x: hidden;
    }
    
    header, footer {visibility: hidden !important;}

    /* === ЖИВАЯ АНИМАЦИЯ МАТЕРИНСКОЙ ПЛАТЫ И НЕОНОВЫХ ЛИНИЙ === */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        /* Цифровая сетка дорожек */
        background-image: 
            linear-gradient(rgba(0, 255, 204, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 204, 0.04) 1px, transparent 1px);
        background-size: 40px 40px;
        background-position: center center;
        z-index: 0;
        pointer-events: none;
    }

    /* Создаем центральную плату процессора */
    .stApp::after {
        content: "";
        position: fixed;
        top: 50%; left: 50%;
        width: 180px; height: 180px;
        transform: translate(-50%, -50%);
        background: #0d0a21;
        border: 3px solid #ff007f;
        border-radius: 12px;
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.4), inset 0 0 15px rgba(0, 255, 204, 0.2);
        z-index: 0;
        pointer-events: none;
        opacity: 0.15; /* Мягкая прозрачность, чтобы не перекрывать текст сообщений */
    }

    /* Декоративные линии, которые пускают неоновые импульсы во все стороны */
    .neon-lines-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
    }

    /* Стилизация бегущих импульсов */
    .neon-line {
        position: absolute;
        background: linear-gradient(90deg, transparent, #00ffcc, transparent);
        opacity: 0.4;
    }

    /* Вертикальные линии */
    .neon-line.v-up {
        width: 2px; height: 50vh; left: 50%; bottom: 50%;
        background: linear-gradient(0deg, transparent, #00ffcc, transparent);
        animation: pulseUp 3s infinite linear;
    }
    .neon-line.v-down {
        width: 2px; height: 50vh; left: 50%; top: 50%;
        background: linear-gradient(180deg, transparent, #ff007f, transparent);
        animation: pulseDown 3s infinite linear;
    }
    /* Горизонтальные линии */
    .neon-line.h-left {
        width: 50vw; height: 2px; top: 50%; right: 50%;
        background: linear-gradient(270deg, transparent, #00ffcc, transparent);
        animation: pulseLeft 3.5s infinite linear;
    }
    .neon-line.h-right {
        width: 50vw; height: 2px; top: 50%; left: 50%;
        background: linear-gradient(90deg, transparent, #ff007f, transparent);
        animation: pulseRight 3.5s infinite linear;
    }

    /* Квантовые анимации импульсов от центра */
    @keyframes pulseUp {
        0% { background-position: 0% 100%; transform: scaleY(0); transform-origin: bottom; opacity: 0; }
        50% { opacity: 0.7; }
        100% { background-position: 0% 0%; transform: scaleY(1); transform-origin: bottom; opacity: 0; }
    }
    @keyframes pulseDown {
        0% { background-position: 0% 0%; transform: scaleY(0); transform-origin: top; opacity: 0; }
        50% { opacity: 0.7; }
        100% { background-position: 0% 100%; transform: scaleY(1); transform-origin: top; opacity: 0; }
    }
    @keyframes pulseLeft {
        0% { background-position: 100% 0%; transform: scaleX(0); transform-origin: right; opacity: 0; }
        50% { opacity: 0.7; }
        100% { background-position: 0% 0%; transform: scaleX(1); transform-origin: right; opacity: 0; }
    }
    @keyframes pulseRight {
        0% { background-position: 0% 0%; transform: scaleX(0); transform-origin: left; opacity: 0; }
        50% { opacity: 0.7; }
        100% { background-position: 100% 0%; transform: scaleX(1); transform-origin: left; opacity: 0; }
    }

    /* Шапка сайта в стиле Sci-Fi дисплея */
    h1 { 
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(135deg, #00ffcc 0%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important; 
        font-size: 2.4rem !important; 
        letter-spacing: 2px !important;
        text-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
        z-index: 2;
        position: relative;
    }

    /* Стильная карточка предупреждения */
    .cyber-alert {
        background: rgba(255, 0, 127, 0.05); 
        border: 1px solid rgba(255, 0, 127, 0.3); 
        border-radius: 14px; 
        padding: 15px 20px; 
        margin: 20px 0;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.1);
        z-index: 2;
        position: relative;
    }

    /* Полупрозрачные карточки сообщений (Эффект матового стекла) */
    .stChatMessage {
        background: rgba(13, 10, 33, 0.75) !important; 
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 255, 204, 0.15) !important; 
        border-radius: 18px !important; 
        margin-bottom: 16px !important;
        padding: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        z-index: 2;
        position: relative;
    }

    .stChatMessage:hover {
        border-color: rgba(0, 255, 204, 0.4) !important;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.1);
    }

    /* Кибер-поле ввода */
    .stChatInputContainer { 
        border-radius: 24px !important; 
        border: 2px solid #ff007f !important; 
        background-color: #0d0a21 !important;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.2) !important;
        z-index: 2;
        position: relative;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #00ffcc !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.3) !important;
    }

    .stSpinner > div {
        border-top-color: #00ffcc !important;
    }
    </style>
    
    <!-- Добавляем контейнер с анимированными линиями в тело сайта -->
    <div class="neon-lines-container">
        <div class="neon-line v-up"></div>
        <div class="neon-line v-down"></div>
        <div class="neon-line h-left"></div>
        <div class="neon-line h-right"></div>
    </div>
""", unsafe_allow_html=True)

# Отрендеринг заголовка
st.markdown("<h1>⚡ Quantum Core Premium AI</h1>", unsafe_allow_html=True)

st.markdown("""
    <div class='cyber-alert'>
        <span style='color: #ff007f; font-weight: bold;'>🚨 СИСТЕМНЫЙ ПРОТОКОЛ:</span> 
        <span style='color: #ffffff;'>Выдерживайте паузу в <b>5-10 секунд</b> перед отправкой пакетов данных. Для рендеринга графики пишите <b>нарисуй...</b></span>
    </div>
""", unsafe_allow_html=True)

st.caption("Quantum Grid Engine v3.5 • Все системы стабильны")

# Получаем ключ из секретов хостинга
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
                    result = client.models.generate_images(
                        model='imagen-3.0-generate-002',
                        prompt=prompt,
                        config=genai.types.GenerateImagesConfig(
                            number_of_images=1,
                            output_mime_type="image/jpeg",
                            aspect_ratio="1:1"
                        )
                    )
                    
                    for generated_image in result.generated_images:
                        image = Image.open(io.BytesIO(generated_image.image.image_bytes))
                        message_placeholder.image(image)
                        st.session_state.messages.append({"role": "assistant", "content": image, "type": "image"})
                        
                except Exception as e:
                    message_placeholder.error(f"Сбой графического ядра: {e}")
        else:
            with st.spinner("⚡ Вычисление ответа через ядро Gemini Cloud..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=prompt,
                        config=genai.types.GenerateContentConfig(
                            max_output_tokens=1500,
                            temperature=0.7
                        )
                    )
                    answer = response.text
                    message_placeholder.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer, "type": "text"})
                except Exception as e:
                    message_placeholder.error(f"Критический сбой шифрования потока: {e}")
