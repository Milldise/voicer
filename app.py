import streamlit as st
import edge_tts
import asyncio
import os

# --- Настройки страницы ---
st.set_page_config(page_title="Kazakh Voice AI", page_icon="🇰🇿")

# --- Стилизация ---
st.markdown("""
    <style>
    .stTextArea textarea {font-size: 18px !important;}
    </style>
    """, unsafe_allow_html=True)

st.title("🇰🇿 Казахская озвучка")
st.caption("Использует движок Microsoft Azure (Daulet & Aigul)")

# --- Выбор голоса ---
# Сделаем Daulet голосом по умолчанию
voice_choice = st.radio(
    "Выберите голос:",
    ("👨 Daulet (Мужской)", "👩 Aigul (Женский)"),
    horizontal=True
)

if "Daulet" in voice_choice:
    VOICE = "kk-KZ-DauletNeural"
else:
    VOICE = "kk-KZ-AigulNeural"

# --- Ввод текста ---
input_text = st.text_area(
    "Введите текст на казахском:",
    height=150,
    placeholder="Мысалы: Сәлем! Бүгін ауа райы қандай?"
)


# --- Функция генерации (с исправлением ошибки Loop) ---
async def generate_audio_stream(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def run_async_generation(text, voice, output_file):
    # Создаем новый цикл событий для каждого нажатия кнопки
    # Это решает проблему "No audio received" в Streamlit Cloud
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(generate_audio_stream(text, voice, output_file))
        return True
    except Exception as e:
        st.error(f"Ошибка при подключении к Microsoft: {e}")
        return False
    finally:
        loop.close()


# --- Кнопка ---
if st.button("🔊 Озвучить текст", type="primary"):
    # Проверка на пустоту
    if not input_text or input_text.strip() == "":
        st.warning("⚠️ Пожалуйста, напишите хоть что-нибудь в поле ввода!")
    else:
        output_file = "kazakh_audio.mp3"

        with st.spinner("Генерация..."):
            # Запускаем генерацию
            success = run_async_generation(input_text, VOICE, output_file)

            if success and os.path.exists(output_file):
                # Показываем плеер
                st.audio(output_file, format="audio/mp3")

                # Кнопка скачивания
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="📥 Скачать MP3",
                        data=file,
                        file_name="audio.mp3",
                        mime="audio/mp3"
                    )
            elif success:
                st.error("Файл не был создан. Попробуйте еще раз.")