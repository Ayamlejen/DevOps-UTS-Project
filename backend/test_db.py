from db import test_connection

try:
    test_connection()

except Exception as e:
    print("Koneksi database gagal!")
    print("Penyebab:", e)
    