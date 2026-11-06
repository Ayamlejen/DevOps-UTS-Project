
import numpy as np
import librosa
import torch
import torch.nn.functional as F


def audio_to_melspectrogram(
    audio_path,
    sample_rate=22050,
    duration=30,
    n_mels=128,
    n_fft=2048,
    hop_length=512,
    target_height=128,
    target_width=256
):

    # 1. Membaca audio
    audio, sr = librosa.load(
        audio_path,
        sr=sample_rate,
        duration=duration,
        mono=True
    )

    # 2. Memastikan panjang audio 30 detik
    target_length = sample_rate * duration

    if len(audio) < target_length:
        audio = np.pad(
            audio,
            (0, target_length - len(audio))
        )
    else:
        audio = audio[:target_length]

    # 3. Membuat Mel-Spectrogram
    mel_spec = librosa.feature.melspectrogram(
        y=audio,
        sr=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0
    )

    # 4. Konversi ke decibel
    mel_spec = librosa.power_to_db(
        mel_spec,
        ref=np.max
    )

    # 5. Normalisasi Z-score
    mean = mel_spec.mean()
    std = mel_spec.std()

    mel_spec = (mel_spec - mean) / (std + 1e-8)

    # 6. Mengubah menjadi tensor
    mel_tensor = torch.tensor(
        mel_spec,
        dtype=torch.float32
    ).unsqueeze(0).unsqueeze(0)

    # 7. Resize ke ukuran 128 x 256
    mel_tensor = F.interpolate(
        mel_tensor,
        size=(target_height, target_width),
        mode="bilinear",
        align_corners=False
    )

    # 8. Menghilangkan dimensi batch
    mel_tensor = mel_tensor.squeeze(0)

    return mel_tensor
