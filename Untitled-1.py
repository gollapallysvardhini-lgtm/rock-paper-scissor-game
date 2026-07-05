from pydub import AudioSegment

# Load MP3 file
mp3_file = "lose.mp3"  # Change this to your actual MP3 file name
wav_file = "lose.wav"  # Output WAV file name

# Convert MP3 to WAV
audio = AudioSegment.from_mp3(mp3_file)
audio.export(wav_file, format="wav")

print("Conversion complete! Your WAV file is ready.")
