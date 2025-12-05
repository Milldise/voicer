import streamlit as st
import edge_tts
import asyncio
import os

# --- Настройки страницы ---
st.set_page_config(page_title="Kazakh Voice AI", page_icon="🎤")

# --- Заголовок и стиль ---
st.title("🇰🇿 Kazakh AI Voice")
st.write("Введи текст, выбери голос и нажми кнопку.")

# --- Выбор голоса ---
voice_option = st.selectbox(
    "Выбери голос:",
    ("👨 Daulet (Мужской)", "👩 Aigul (Женский)")
)

# Определяем техническое имя голоса
if "Daulet" in voice_option:
    VOICE = "kk-KZ-DauletNeural"
else:
    VOICE = "kk-KZ-AigulNeural"

# --- Поле ввода текста ---
text = st.text_area("Текст на казахском:", height=150, placeholder="Сәлем! Қалың қалай?")


# --- Логика генерации ---
async def generate_audio(text, voice):
    output_file = "output_audio.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file


if st.button("🔊 Озвучить", type="primary"):
    if not text:
        st.error("Пожалуйста, введите текст!")
    else:
        with st.spinner("Генерирую озвучку..."):
            try:
                # Запуск асинхронной функции
                out_file = asyncio.run(generate_audio(text, VOICE))

                # Показываем плеер
                st.audio(out_file, format="audio/mp3")

                # Даем скачать
                with open(out_file, "rb") as file:
                    st.download_button(
                        label="📥 Скачать MP3",
                        data=file,
                        file_name="kazakh_voice.mp3",
                        mime="audio/mp3"
                    )
            except Exception as e:
                st.error(f"Ошибка: {e}")