import streamlit as st
import requests
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="Music Genre Classification",
    page_icon="🎵",
    layout="centered"
)

# URL Backend FastAPI
API_URL = "http://localhost:8000"

# Judul aplikasi
st.title("🎵 Music Genre Classification")
st.write(
    "Sistem klasifikasi genre musik menggunakan "
    "Convolutional Neural Network (CNN)."
)

st.divider()

# Upload audio
st.subheader("Upload Audio")

uploaded_file = st.file_uploader(
    "Pilih file audio berformat WAV",
    type=["wav"]
)

# Prediksi
if uploaded_file is not None:

    st.audio(uploaded_file)

    if st.button("Klasifikasikan Genre", type="primary"):

        with st.spinner("Sedang melakukan prediksi..."):

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

                    st.success("Prediksi berhasil!")

                    st.subheader("Hasil Prediksi")

                    st.metric(
                        "Genre Musik",
                        result["predicted_genre"].upper()
                    )

                    st.metric(
                        "Confidence",
                        f'{result["confidence_percentage"]}%'
                    )

                    st.write(
                        "Nama file:",
                        result["filename"]
                    )

                else:
                    st.error(
                        f"Gagal melakukan prediksi: "
                        f"{response.text}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Backend tidak dapat dihubungi. "
                    "Pastikan FastAPI sedang berjalan."
                )

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

st.divider()

# Riwayat prediksi
st.subheader("📋 Riwayat Prediksi")

if st.button("Tampilkan Riwayat"):

    try:
        response = requests.get(
            f"{API_URL}/history",
            timeout=30
        )

        if response.status_code == 200:

            history = response.json()

            if history:

                df = pd.DataFrame(history)

                st.dataframe(
                    df,
                    use_container_width=True
                )

            else:
                st.info("Belum ada riwayat prediksi.")

        else:
            st.error("Gagal mengambil riwayat prediksi.")

    except requests.exceptions.ConnectionError:
        st.error("Backend tidak dapat dihubungi.")