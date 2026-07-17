import streamlit as st
import google.genai as genai

# Стильные премиум-настройки страницы
st.set_page_config(page_title="CyberChat AI", page_icon="⚡", layout="centered")
st.markdown("""
    <style>
    /* Главный фон приложения */
    .stApp { 
        background: linear-gradient(135deg, #0f0c20 0%, #15102a 100%); 
        color: #00ffcc; 
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    /* Поле ввода сообщения */
    .stChatInputContainer { 
        border-radius: 20px; 
        border: 2px solid #ff007f !important;
        box-shadow: 0 0 15px #ff007f;
    }
    /* Главный заголовок */
    h1 { 
        background: linear-gradient(45deg, #00ffcc, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: 1px;
    }
    /* Стиль карточек сообщений ИИ */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-left: 4px solid #00ffcc;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.caption("Профессиональный ИИ-ассистент нового поколения")

# Твой проверенный рабочий API-ключ (без точек в начале!)
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
if prompt := st.chat_input("Спросите меня о чем угодно..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("⚡ Нейросеть генерирует ответ..."):
            try:
                # ВЫЗОВ СВЕРХБЫСТРОЙ МОДЕЛИ GEMINI 3.5
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        max_output_tokens=300,  # Заставляем ИИ отвечать емко и мгновенно
                        temperature=0.7
                    )
                )
                answer = response.text
                
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                message_placeholder.error(f"Произошла ошибка API: {e}")
