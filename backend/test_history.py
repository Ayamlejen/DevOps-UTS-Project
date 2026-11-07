from db import SessionLocal
from db_models import PredictionHistory

db = SessionLocal()

try:
    data = PredictionHistory(
        filename="test_music.wav",
        predicted_genre="jazz",
        confidence=0.95
    )

    db.add(data)
    db.commit()

    print("Data berhasil disimpan!")

    hasil = db.query(PredictionHistory).all()

    print("\nRiwayat prediksi:")

    for item in hasil:
        print(
            item.id,
            item.filename,
            item.predicted_genre,
            item.confidence,
            item.created_at
        )

except Exception as e:
    db.rollback()
    print("Gagal:", e)

finally:
    db.close()
