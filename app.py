import streamlit as st
import requests
from datetime import date, timedelta
from io import BytesIO

# -------------------------
# CONFIGURACION GENERAL
# -------------------------

API_NASA = "cculbllTfiO6PvRwefklymbBUAEyoqE22v1O4KdW"
APOD_URL = "https://api.nasa.gov/planetary/apod"

st.set_page_config(
    page_title="NASA - Javi",
    page_icon="🚀",
    layout="wide"
)

# Forzar modo oscuro del tema de Streamlit
st.markdown("""
    <style>
    /* Fuerza el modo oscuro de Streamlit */
    :root {
        color-scheme: dark !important;
    }
    [data-theme="light"] {
        color-scheme: dark !important;
    }
    [data-theme="light"] * {
        background-color: transparent !important;
        color: inherit !important;
    }
    </style>
""", unsafe_allow_html=True)


# -------------------------
# ESTILOS FUTURISTAS
# -------------------------

st.markdown(
    """
<style>
body {
    background: radial-gradient(circle at top, #0b1020, #000010);
    color: #e0ecff;
    font-family: "Segoe UI", Roboto, sans-serif;
}

h1 {
    text-align: center;
    color: #9fd0ff !important;
    text-shadow: 0 0 25px #1e90ff;
    letter-spacing: 2px;
}

h2, h3 {
    color: #b7ceff !important;
    text-shadow: 0 0 10px #1e90ff55;
}

.futura-box {
    border-radius: 16px;
    border: 1px solid #2b5cff80;
    background: linear-gradient(135deg, rgba(15,25,60,0.9), rgba(5,10,25,0.95));
    box-shadow: 0 0 25px rgba(46,117,255,0.35);
    padding: 20px;
}

.small-text {
    font-size: 12px;
    opacity: 0.7;
}

hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #3b82f680, transparent);
    margin: 20px 0;
}

.stButton>button {
    border-radius: 999px;
    padding: 0.5rem 1.5rem;
    border: 1px solid #3b82f6;
    background: linear-gradient(135deg, #1d4ed8, #0f172a);
    color: #e5ecff;
    box-shadow: 0 0 15px #1d4ed880;
    transition: all 0.2s ease-in-out;
    font-weight: 600;
}

.stButton>button:hover {
    box-shadow: 0 0 25px #60a5fa;
    transform: translateY(-1px) scale(1.01);
}

.chip {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid #3b82f6aa;
    font-size: 11px;
    margin-right: 6px;
    margin-bottom: 4px;
    background: rgba(15,23,42,0.8);
}

.fav-card {
    border-radius: 12px;
    border: 1px solid #facc15aa;
    background: radial-gradient(circle at top, rgba(250,204,21,0.18), rgba(15,15,30,0.95));
    padding: 10px;
    box-shadow: 0 0 18px rgba(250,204,21,0.3);
}

.top-bar {
    text-align: center;
    font-size: 14px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #60a5fa;
    margin-bottom: 8px;
}
</style>
""",
    unsafe_allow_html=True
)

# -------------------------
# FUNCIONES LOGICAS
# -------------------------

def obtener_apod(fecha=None):
    params = {"api_key": API_NASA}
    if fecha:
        params["date"] = fecha

    r = requests.get(APOD_URL, params=params)
    if r.status_code != 200:
        return None
    return r.json()

# NUEVA FUNCION: Traducción sin límite
def traducir_es(texto):
    """Traduce cualquier texto largo en múltiples bloques (sin límite de 500 chars)."""
    if not texto:
        return ""

    partes = []
    bloque = 400

    for i in range(0, len(texto), bloque):
        segmento = texto[i:i+bloque]
        try:
            r = requests.get(
                "https://api.mymemory.translated.net/get",
                params={"q": segmento, "langpair": "en|es"},
                timeout=10
            )
            trad = r.json()["responseData"]["translatedText"]
            partes.append(trad)
        except:
            partes.append(segmento)

    return " ".join(partes)


def descargar_imagen(url):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return BytesIO(resp.content), url.split("/")[-1]
    except:
        return None, None
    return None, None

# -------------------------
# ESTADO DE SESION
# -------------------------

if "apod_actual" not in st.session_state:
    st.session_state["apod_actual"] = None

if "favoritos" not in st.session_state:
    st.session_state["favoritos"] = []

# -------------------------
# CABECERA
# -------------------------

st.markdown("<div class='top-bar'>Panel de Visualizacion Astronomica – NASA APOD</div>", unsafe_allow_html=True)
st.title("🚀 Imagen Astronómica del Día – por Javier")
st.markdown(
    "Explora el archivo completo de la **NASA** (APOD) desde 1995 hasta hoy, "
    "traduccion al español, galeria, favoritos y panel estilo centro de control. 🌌"
)
st.markdown("<hr />", unsafe_allow_html=True)

# -------------------------
# LAYOUT PRINCIPAL
# -------------------------

col_control, col_main = st.columns([1.2, 2.8])

# -------------------------
# PANEL IZQUIERDO
# -------------------------

with col_control:
    st.markdown("<div class='futura-box'>", unsafe_allow_html=True)
    st.subheader("🎛 Panel de control")

    hoy = date.today()
    fecha_min = date(1995, 6, 16)

    fecha_seleccionada = st.date_input(
        "Fecha de la imagen (desde 1995)",
        value=hoy,
        min_value=fecha_min,
        max_value=hoy
    )

    mostrar = st.button("Mostrar imagen de esta fecha")

    st.markdown("---")

    dias_galeria = st.slider(
        "Galeria de los últimos N días",
        min_value=3,
        max_value=10,
        value=5
    )
    cargar_galeria = st.button("Cargar galería")

    st.markdown("---")

    ver_favs = st.checkbox("Mostrar sección de favoritos", value=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# PANEL PRINCIPAL
# -------------------------

with col_main:

    if mostrar:
        with st.spinner("Obteniendo imagen desde NASA..."):
            datos_apod = obtener_apod(str(fecha_seleccionada))
            st.session_state["apod_actual"] = datos_apod

    datos_apod = st.session_state.get("apod_actual", None)

    if datos_apod:

        titulo_es = traducir_es(datos_apod.get("title", ""))
        descripcion_es = traducir_es(datos_apod.get("explanation", ""))

        media_type = datos_apod.get("media_type", "desconocido")
        fecha_str = datos_apod.get("date", "")
        copyright_ = datos_apod.get("copyright", "No especificado")
        url = datos_apod.get("url", "")
        hdurl = datos_apod.get("hdurl", url)

        # -------------------------
        # BLOQUE PRINCIPAL (ARREGLADO)
        # -------------------------

        st.markdown("<div class='futura-box'>", unsafe_allow_html=True)
        st.subheader(f"🌌 {titulo_es}")
        st.caption(f"Fecha NASA APOD: {fecha_str}")

        if media_type == "image":
            st.image(url, use_container_width=True)
        else:
            st.warning("Este APOD es un video. Se mostrará el reproductor:")
            st.video(url)

        st.markdown("### 🛰 Descripción oficial de la NASA")
        st.write(descripcion_es)

        col_b1, col_b2 = st.columns([1.2, 1.2])

        with col_b1:
            if media_type == "image":
                img_bytes, nombre = descargar_imagen(hdurl)
                if img_bytes:
                    st.download_button(
                        label="💾 Descargar imagen HD",
                        data=img_bytes,
                        file_name=nombre,
                        mime="image/jpeg"
                    )

        with col_b2:
            if st.button("⭐ Agregar a favoritos"):
                if not any(f["date"] == fecha_str for f in st.session_state["favoritos"]):
                    st.session_state["favoritos"].append(
                        {"date": fecha_str, "title_es": titulo_es, "url": url, "media_type": media_type}
                    )
                    st.success("Agregado a favoritos.")
                else:
                    st.info("Ya está en favoritos.")

        st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # PANEL TÉCNICO
        # -------------------------

        col_tech1, col_tech2 = st.columns([1.2, 1.8])

        with col_tech1:
            st.markdown("<div class='futura-box'>", unsafe_allow_html=True)
            st.markdown("### 📡 Ficha técnica (datos reales NASA)")
            st.write(f"**Fecha APOD:** {fecha_str}")
            st.write(f"**Tipo de medio:** {media_type}")
            st.write(f"**Autor:** {copyright_}")
            st.write(f"**URL estándar:** {url}")
            if hdurl != url:
                st.write(f"**URL HD:** {hdurl}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_tech2:
            st.markdown("<div class='futura-box'>", unsafe_allow_html=True)
            st.markdown("### 🔭 Información adicional NASA")
            st.write("🔹 **Título original:** " + datos_apod.get("title", ""))
            st.write("🔹 **Título traducido:** " + titulo_es)
            st.write("🔹 **Descripción traducida:**")
            st.write(descripcion_es)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("Selecciona una fecha y pulsa **Mostrar imagen**.")

    # -------------------------
    # GALERIA
    # -------------------------

    st.markdown("<hr />", unsafe_allow_html=True)

    if cargar_galeria:
        st.subheader("🖼 Galería reciente")

        dias = []
        for i in range(dias_galeria):
            dia = date.today() - timedelta(days=i)
            datos_dia = obtener_apod(str(dia))
            if datos_dia:
                dias.append(datos_dia)

        cols = st.columns(3)
        idx = 0

        for datos_dia in dias:
            with cols[idx % 3]:
                st.markdown("<div class='futura-box'>", unsafe_allow_html=True)
                st.caption(datos_dia["date"])
                st.write("**" + traducir_es(datos_dia["title"]) + "**")
                if datos_dia["media_type"] == "image":
                    st.image(datos_dia["url"], use_container_width=True)
                else:
                    st.video(datos_dia["url"])
                st.markdown("</div>", unsafe_allow_html=True)
            idx += 1

    # -------------------------
    # FAVORITOS
    # -------------------------

    if ver_favs:
        st.markdown("<hr />", unsafe_allow_html=True)
        st.subheader("⭐ Tus favoritos")

        if not st.session_state["favoritos"]:
            st.info("Aún no tienes favoritos.")
        else:
            cols_fav = st.columns(3)
            for i, fav in enumerate(st.session_state["favoritos"]):
                with cols_fav[i % 3]:
                    st.markdown("<div class='fav-card'>", unsafe_allow_html=True)
                    st.caption(fav["date"])
                    st.write("**" + fav["title_es"] + "**")
                    if fav["media_type"] == "image":
                        st.image(fav["url"], use_container_width=True)
                    else:
                        st.video(fav["url"])
                    st.markdown("</div>", unsafe_allow_html=True)



