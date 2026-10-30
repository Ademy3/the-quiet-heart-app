import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import io

st.set_page_config(
    page_title="The Quiet Heart - Generator",
    page_icon="🤍",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
        color: #f0f6fc;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤍 The Quiet Heart")
st.caption("Generador oficial de tarjetas de frases para redes sociales")

TEMPLATES = {
    "Plantilla 1: Emotional Quote (Atardecer en el mar)": "template1.jpg",
    "Plantilla 2: Inspirational Landscape (Montañas con niebla)": "template2.jpg",
    "Plantilla 3: Deep Reflection (Diario y café)": "template3.jpg",
    "Plantilla 4: Bold Statement (Viajero en cumbre)": "template4.jpg",
    "Plantilla 5: Lessons & Lists (Flor y escritorio)": "template5.jpg",
    "Plantilla 6: Reflective Question (Muelle en el lago)": "template6.jpg",
    "Plantilla 7: Stories 9:16 (Océano rosa)": "template7.jpg"
}

template_choice = st.selectbox("1. Selecciona la Plantilla:", list(TEMPLATES.keys()))

default_quote = "The quietest growth happens when you stop asking for permission to be whole."
user_quote = st.text_area("2. Frase en Inglés (generada por tu Gem):", value=default_quote, height=100)

col1, col2 = st.columns(2)
with col1:
    font_size = st.slider("Tamaño de letra:", min_value=28, max_value=72, value=48)
with col2:
    text_color = st.color_picker("Color de texto:", value="#FDFBF7")

if st.button("✨ Generar Imagen HD Sin Marca de Agua", type="primary"):
    bg_filename = TEMPLATES[template_choice]
    bg_path = os.path.join("assets", bg_filename)
    logo_path = os.path.join("assets", "logo.png")
    font_path = os.path.join("assets", "PlayfairDisplay-Regular.ttf")

    if os.path.exists(bg_path):
        bg_img = Image.open(bg_path).convert("RGBA")
        w, h = bg_img.size

        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(bg_img)

        # Formatear líneas
        lines = textwrap.wrap(user_quote, width=28)
        line_height = int(font_size * 1.35)
        total_text_h = len(lines) * line_height
        start_y = int((h - total_text_h) * 0.42)

        # Dibujar frase con sombra suave
        for i, line in enumerate(lines):
            bbox = font.getbbox(line)
            line_w = bbox[2] - bbox[0]
            x = (w - line_w) // 2
            y = start_y + i * line_height

            # Sombra
            draw.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0, 160))
            # Texto principal
            draw.text((x, y), line, font=font, fill=text_color)

        # Estampar Logo del Corazón centrado abajo
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo_w = int(w * 0.16)
            logo_h = int(logo.height * (logo_w / logo.width))
            logo_resized = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

            logo_x = (w - logo_w) // 2
            logo_y = h - logo_h - int(h * 0.06)

            bg_img.paste(logo_resized, (logo_x, logo_y), logo_resized)

        final_img = bg_img.convert("RGB")
        st.image(final_img, caption="Resultado final listo para guardar", use_container_width=True)

        buf = io.BytesIO()
        final_img.save(buf, format="PNG", quality=95)
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Descargar Imagen a la Galería",
            data=byte_im,
            file_name="the_quiet_heart_post.png",
            mime="image/png"
        )
