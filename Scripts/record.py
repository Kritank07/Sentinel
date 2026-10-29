import sounddevice as sd
import soundfile as sf

SECONDS = 15
RATE = 16000

print("Recording... speak now")
audio = sd.rec(int(SECONDS * RATE), samplerate=RATE, channels=1)
sd.wait()
sf.write("samples/scam_call.wav", audio, RATE, subtype="PCM_16")
print("Saved samples/scam_call.wav")

# “Hello, main CBI officer bol raha hoon. Aapka Aadhaar money laundering case mein link hai. Video call pe rahiye aur verification ke liye ₹50,000 transfer kariye, warna arrest hoga.”