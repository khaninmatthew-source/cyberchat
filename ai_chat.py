import streamlit as st
import google.genai as genai

# Улучшенные премиум-настройки страницы
st.set_page_config(page_title="CyberChat Premium", page_icon="⚡", layout="centered")

# Высокодетализированный Cyberpunk CSS-дизайн
st.markdown("""
    <style>
    /* Живой футуристичный фон с глубоким градиентом */
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #120e2e 0%, #080616 100%);
        color: #00ffcc; 
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Декоративная неоновая сетка на фоне сайта */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: 
            linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        z-index: 0;
        pointer-events: none;
    }

    /* Главный 3D заголовок с хромированным градиентом и свечением */
    h1 { 
        background: linear-gradient(135deg, #00ffcc 30%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.8rem !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
        margin-bottom: 5px !important;
        z-index: 1;
    }

    /* Профессиональное неоновое окно предупреждения */
    .cyber-alert {
        background: rgba(255, 0, 127, 0.07);
        border: 1px solid #ff007f;
        border-radius: 12px;
        padding: 15px 20px;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.15), inset 0 0 10px rgba(255, 0, 127, 0.1);
        z-index: 1;
        position: relative;
    }

    /* Эффект матового стекла (Glassmorphism) для карточек сообщений */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 204, 0.1) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        padding: 15px !important;
        margin-bottom: 15px !important;
        transition: all 0.3s ease;
    }

    /* Свечение карточки при наведении мышки */
    .stChatMessage:hover {
        border-color: rgba(0, 255, 204, 0.3) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 255, 204, 0.08);
        transform: translateY(-2px);
    }

    /* Кнопка отправки и поле ввода */
    .stChatInputContainer { 
        border-radius: 24px !important; 
        border: 2px solid #ff007f !important;
        background-color: #0d0a21 !important;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.25);
    }
    
    .stChatInputContainer:focus-within {
        border-color: #00ffcc !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.35);
    }

    /* Кастомизация индикатора загрузки нейросети */
    .stSpinner > div {
        border-top-color: #00ffcc !important;
    }
    </style>
""", unsafe_allow_html=True)

# Отрендеринг заголовка
st.markdown("<h1>⚡ CyberChat Premium AI</h1>", unsafe_allow_html=True)

# Красивый детализированный блок предупреждения с поддержкой стилей
st.markdown("""
    <div class='cyber-alert'>
        <span style='color: #ff007f; font-weight: bold;'>🚨 КРИТИЧЕСКОЕ ПРАВИЛО СЕТИ:</span> 
        <span style='color: #ffffff;'>Делайте обязательную паузу в <b>5-10 секунд</b> перед каждым новым запросом. При слишком частых кликах защитный протокол ИИ уйдёт в перезагрузку!</span>
    </div>
""", unsafe_allow_html=True)

st.caption("Профессиональный ИИ-ассистент нового поколения • Версия 2.0 Global")

# Твой проверенный рабочий API-ключ из Secrets
API_KEY = st.secrets["API_KEY"]

# Создаем современный клиент по новым правилам Google
client = genai.Client(api_key=API_KEY)

# Создаем память для чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Показываем прошлые сообщения на экране
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода
if prompt := st.chat_input("Вход в терминал ИИ... Задайте любой вопрос..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("⚡ Сканирование квантовой матрицы ответа..."):
            try:
                # ВЫЗОВ СВЕРХБЫСТРОЙ МОДЕЛИ GEMINI 3.5
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        max_output_tokens=300,
                        temperature=0.7
                    )
                )
                answer = response.text
                
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                message_placeholder.error(f"Произошла ошибка API шифрования: {e}")
