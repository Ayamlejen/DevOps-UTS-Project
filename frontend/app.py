import streamlit as st
import requests
import pandas as pd
import os
import html


# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Music Genre AI",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv("API_URL", "http://localhost:8000")


# ==========================================
# CUSTOM CSS
# ==========================================

st.html("""
<style>

/* Background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f1020 0%,
        #19152f 55%,
        #21183b 100%
    );
    color: #f5f3ff;
}

/* Hilangkan header bawaan */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Konten utama */
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #151326;
    border-right: 1px solid #30294b;
}

/* Judul */
.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.hero-subtitle {
    color: #b8b1d1;
    font-size: 16px;
    line-height: 1.7;
}

/* Label section */
.section-title {
    color: #ffffff;
    font-size: 23px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Kartu */
.custom-card {
    background: rgba(35, 29, 61, 0.85);
    border: 1px solid #453866;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 18px;
}

/* Kartu hasil */
.result-card {
    background: linear-gradient(135deg, #35245c, #241c43);
    border: 1px solid #8b5cf6;
    border-radius: 18px;
    padding: 28px;
    text-align: center;
    margin-top: 15px;
    min-height: 175px;
}

/* Genre */
.genre-result {
    font-size: 38px;
    font-weight: 800;
    color: #c4b5fd;
    text-transform: uppercase;
}

/* Confidence */
.confidence-result {
    font-size: 30px;
    font-weight: 700;
    color: #ffffff;
}

/* Tombol */
.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 700;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #6d28d9, #7e22ce);
    border: none;
    color: white;
    transform: translateY(-2px);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    border: 1px dashed #8065bd;
    border-radius: 14px;
    padding: 15px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #282044;
    border: 1px solid #514174;
    padding: 18px;
    border-radius: 14px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #453866;
    border-radius: 12px;
    overflow: hidden;
}

/* Divider */
hr {
    border-color: #403458;
}

/* Footer */
.footer {
    text-align: center;
    color: #9388b2;
    font-size: 13px;
    padding: 25px 0 5px 0;
}

</style>
""")


# ==========================================
# SESSION STATE
# ==========================================

if "prediction_result" not in st.session_state:
    st.session_state["prediction_result"] = None

if "history_data" not in st.session_state:
    st.session_state["history_data"] = None


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.html("""
    <div style="padding-top: 10px;">
        <h1 style="color: white;">🎵 Music Genre AI</h1>

        <p style="color: #b8b1d1;">
            CNN-Based Music Classification
        </p>

        <hr style="border-color: #403458;">

        <h3 style="color: white;">
            📌 Tentang Aplikasi
        </h3>

        <p style="color: #d1cbe3; line-height: 1.6;">
            Aplikasi ini menggunakan
            Convolutional Neural Network (CNN)
            untuk mengidentifikasi genre musik
            berdasarkan file audio.
        </p>

        <hr style="border-color: #403458;">

        <h3 style="color: white;">🎧 Fitur</h3>

        <ul style="color: #d1cbe3; line-height: 2;">
            <li>Upload audio WAV</li>
            <li>Prediksi genre musik</li>
            <li>Confidence prediction</li>
            <li>Riwayat klasifikasi</li>
        </ul>

        <hr style="border-color: #403458;">

        <p style="color: #9388b2; font-size: 13px;">
            Machine Learning Project
        </p>

        <p style="color: #9388b2; font-size: 13px;">
            Frontend: Streamlit
        </p>

        <p style="color: #9388b2; font-size: 13px;">
            Backend: FastAPI
        </p>

        <p style="color: #9388b2; font-size: 13px;">
            Database: PostgreSQL
        </p>
    </div>
    """)


# ==========================================
# HEADER
# ==========================================

st.html("""
<div style="
    background: linear-gradient(120deg, #35245c, #241b42);
    border: 1px solid #59427e;
    border-radius: 22px;
    padding: 35px;
    margin-bottom: 30px;
">

    <div style="font-size: 45px;">🎵</div>

    <div class="hero-title">
        Music Genre Classification
    </div>

    <div class="hero-subtitle">
        Kenali genre musik secara otomatis menggunakan
        teknologi Deep Learning dan Convolutional Neural Network.

        <br>

        Upload audio Anda dan biarkan AI menganalisisnya.
    </div>

</div>
""")


# ==========================================
# UPLOAD AUDIO
# ==========================================

st.html("""
<div class="section-title">
    🎧 Klasifikasi Audio
</div>
""")

with st.container(border=True):

    st.markdown("#### Upload File Musik")

    st.write(
        "Pilih file audio berformat WAV untuk "
        "memulai proses identifikasi genre musik."
    )

    uploaded_file = st.file_uploader(
        "Pilih file audio",
        type=["wav"],
        help="Format yang didukung: WAV"
    )

    if uploaded_file is not None:

        st.success(
            f"File berhasil dipilih: {uploaded_file.name}"
        )

        st.audio(uploaded_file)

        if st.button(
            "✨ Klasifikasikan Genre Musik",
            type="primary",
            use_container_width=True
        ):

            with st.spinner("AI sedang menganalisis audio..."):

                try:

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "audio/wav"
                        )
                    }

                    response = requests.post(
                        f"{API_URL}/predict",
                        files=files,
                        timeout=180
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.session_state["prediction_result"] = result

                        st.success(
                            "Prediksi berhasil dilakukan!"
                        )

                    else:

                        st.error(
                            f"Gagal melakukan prediksi: {response.text}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Backend tidak dapat dihubungi. "
                        "Pastikan container Backend sedang berjalan."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "Proses prediksi membutuhkan waktu terlalu lama."
                    )

                except Exception as e:

                    st.error(f"Terjadi kesalahan: {e}")


# ==========================================
# HASIL PREDIKSI
# ==========================================

if st.session_state["prediction_result"] is not None:

    result = st.session_state["prediction_result"]

    st.markdown("---")

    st.html("""
    <div class="section-title">
        📊 Hasil Analisis Musik
    </div>
    """)

    st.success("Prediksi berhasil dilakukan!")

    col1, col2 = st.columns(2)

    with col1:

        genre = html.escape(
            str(result["predicted_genre"])
        )

        st.html(f"""
        <div class="result-card">

            <div style="font-size: 35px;">🎼</div>

            <div style="color: #c4b5fd; font-size: 15px;">
                Genre Musik
            </div>

            <div class="genre-result">
                {genre}
            </div>

        </div>
        """)

    with col2:

        confidence = html.escape(
            str(result["confidence_percentage"])
        )

        st.html(f"""
        <div class="result-card">

            <div style="font-size: 35px;">🎯</div>

            <div style="color: #c4b5fd; font-size: 15px;">
                Confidence
            </div>

            <div class="confidence-result">
                {confidence}%
            </div>

        </div>
        """)

    filename = html.escape(
        str(result["filename"])
    )

    st.markdown(
        f"**Nama file:** `{filename}`"
    )


# ==========================================
# RIWAYAT PREDIKSI
# ==========================================

st.markdown("---")

st.html("""
<div class="section-title">
    📋 Riwayat Prediksi
</div>
""")

st.write(
    "Lihat daftar audio yang telah dianalisis sebelumnya."
)

if st.button(
    "🔄 Tampilkan Riwayat",
    use_container_width=True
):

    try:

        with st.spinner("Mengambil data riwayat..."):

            response = requests.get(
                f"{API_URL}/history",
                timeout=30
            )

        if response.status_code == 200:

            history = response.json()

            st.session_state["history_data"] = history

        else:

            st.error(
                "Gagal mengambil riwayat prediksi."
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Backend tidak dapat dihubungi."
        )

    except Exception as e:

        st.error(
            f"Terjadi kesalahan: {e}"
        )


if st.session_state["history_data"] is not None:

    history = st.session_state["history_data"]

    if history:

        df = pd.DataFrame(history)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total riwayat prediksi: {len(df)} data"
        )

    else:

        st.info(
            "Belum ada riwayat prediksi."
        )


# ==========================================
# FOOTER
# ==========================================

st.html("""
<div class="footer">

    <hr>

    🎵 Music Genre Classification System

    <br><br>

    Powered by Streamlit, FastAPI, PostgreSQL & CNN

</div>
""")