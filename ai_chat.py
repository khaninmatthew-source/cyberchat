import streamlit as st
import google.genai as genai
import io
from PIL import Image

# Ультра-премиальные настройки страницы Google Material Design
st.set_page_config(page_title="Gemini Cyber Premium", page_icon="🤖", layout="centered")

# Высокодетализированный дизайн по стандартам Google Material 3
st.markdown("""
    <style>
    /* Подключаем премиальный шрифт Inter с серверов Google */
    @import url('https://googleapis.com');

    /* Главное рабочее пространство (Тёмная тема нового поколения) */
    .stApp { 
        background-color: #0B0E14 !important;
        color: #E3E2E6 !important; 
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }
    
    /* Скрываем стандартные декорации Streamlit для чистоты интерфейса */
    header, footer {visibility: hidden !important;}

    /* Роскошный градиентный заголовок в стиле презентаций Google AI */
    h1 { 
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #A8C7FA 0%, #D3E3FD 30%, #7CACF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important; 
        font-size: 2.5rem !important; 
        letter-spacing: -0.5px !important;
        margin-bottom: 2px !important;
    }
    
    /* Индикатор версии Google Cloud */
    .google-badge {
        display: inline-block;
        background: rgba(124, 172, 248, 0.08);
        color: #7CACF8;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 8px;
        border: 1px solid rgba(124, 172, 248, 0.15);
        margin-bottom: 20px;
    }

    /* Элегантный сервисный баннер безопасности */
    .google-alert {
        background: rgba(242, 184, 11, 0.05); 
        border: 1px solid rgba(242, 184, 11, 0.25); 
        border-radius: 16px; 
        padding: 16px 20px; 
        margin: 20px 0;
        font-size: 0.9rem;
        line-height: 1.5;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Интеллектуальные карточки сообщений с плавной анимацией */
    .stChatMessage {
        background: #131722 !important; 
        border: 1px solid #1E2530 !important; 
        border-radius: 20px !important; 
        margin-bottom: 16px !important;
        padding: 18px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
        animation: fadeIn 0.4s ease-out;
    }

    /* Интерактивный эффект выделения при наведении */
    .stChatMessage:hover {
        border-color: #2A3547 !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    }

    /* Высокотехнологичное поле ввода (Material 3 Input) */
    .stChatInputContainer { 
        border-radius: 28px !important; 
        border: 1px solid #2A3547 !important; 
        background-color: #131722 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.25s ease;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #7CACF8 !important;
        box-shadow: 0 8px 32px rgba(124, 172, 248, 0.15) !important;
    }

    /* Кастомизация текста внутри поля ввода */
    textarea {
        color: #E3E2E6 !important;
    }

    /* Плавная анимация появления контента */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Стильная кастомизация системного спиннера */
    .stSpinner > div {
        border-top-color: #7CACF8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Рендеринг интерфейса Google Enterprise
st.markdown("<h1>Gemini Premium Cloud</h1>", unsafe_allow_html=True)
st.markdown("<div class='google-badge'>VERTEX AI LATEST ENGINE</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='google-alert'>
        <span style='color: #F2B80B; font-weight: 600;'>⚠️ СИСТЕМНОЕ УВЕДОМЛЕНИЕ:</span> 
        <span style='color: #C4C6D0;'>В связи с ограничениями бесплатного шлюза, делайте обязательную паузу в <b>5-10 секунд</b> между запросами. Чтобы сгенерировать иллюстрацию, начните текст со слова <b>нарисуй</b>.</span>
    </div>
""", unsafe_allow_html=True)

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

if prompt := st.chat_input("Введите поисковый или графический запрос для Gemini..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if prompt.lower().startswith(("нарисуй", "draw", "картинка", "image", "создай картинку")):
            with st.spinner("🤖 Google Imagen обрабатывает графический массив данных..."):
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
                    message_placeholder.error(f"Ошибка удалённого рендеринга Imagen: {e}")
        else:
            with st.spinner("🤖 Квантовая сборка ответа Gemini Enterprise..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=prompt,
                        config=genai.types.GenerateContentConfig(
                            max_output_tokens=1500, # Увеличили длину сообщений!
                            temperature=0.7
                        )
                    )
                    answer = response.text
                    message_placeholder.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer, "type": "text"})
                except Exception as e:
                    message_placeholder.error(f"Сбой ядра Gemini Cloud API: {e}")
