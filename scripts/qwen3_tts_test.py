"""
Qwen3 TTS Test — Kaggle Notebook Setup
Run this on Kaggle with GPU (T4 or P100)
"""

# Cell 1: Install dependencies
# !pip install -U qwen-tts
# !pip install -U flash-attn --no-build-isolation

# Cell 2: Download models
# !huggingface-cli download Qwen/Qwen3-TTS-Tokenizer-12Hz --local-dir ./Qwen3-TTS-Tokenizer-12Hz
# !huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign --local-dir ./Qwen3-TTS-12Hz-1.7B-VoiceDesign
# !huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-Base --local-dir ./Qwen3-TTS-12Hz-1.7B-Base

# Cell 3: Check GPU
import torch
print(f"GPU available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU name: {torch.cuda.get_device_name(0)}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# Cell 4: Load model
from qwen_tts import Qwen3TTSModel

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    torch_dtype="auto",
    device_map="auto"
)
print("Model loaded successfully!")

# Cell 5: Design a voice for Spiritual Sleep
spiritual_voice = model.voice_design(
    text="Welcome to Spiritual Sleep. Tonight, we read from the Corpus Hermeticum.",
    instruct="A deep, warm male voice. Slow, measured pace. Authoritative but gentle. British accent."
)

# Cell 6: Design a voice for Story Sleep
story_voice = model.voice_design(
    text="Once upon a time, in a land far away, there lived a princess.",
    instruct="A soft, gentle female voice. Warm, storytelling tone. Slight smile in the voice."
)

# Cell 7: Design a voice for Mind Sleep
mind_voice = model.voice_design(
    text="The A18 chip features a 6-core CPU with 2 performance and 4 efficiency cores.",
    instruct="A clear, neutral male voice. Precise, technical. American accent."
)

# Cell 8: Generate test audio with Spiritual voice
output_spiritual = model.generate(
    text="Salary. From Latin salarium. Salt money. Roman soldiers were paid in salt. This is why we say someone is 'worth their salt'. And this is why we say 'salad'. From Latin salata, salted things. Romans dressed their vegetables with salt.",
    voice=spiritual_voice
)

# Cell 9: Generate test audio with Story voice
output_story = model.generate(
    text="The Snow Queen. Hans Christian Andersen. The mirror and the fragment. The mirror, it was so remarkable that everything reflected in it was diminished and made worse. The most beautiful landscape reflected in it was like boiled spinach. The nicest people were transformed and looked odious.",
    voice=story_voice
)

# Cell 10: Generate test audio with Mind voice
output_mind = model.generate(
    text="iPhone 16. Year introduced 2024. Finish: Black, White, Pink, Teal, Ultramarine. Aluminum design. Ceramic Shield front. Width 71.6 millimeters. Height 147.6 millimeters. Weight 170 grams.",
    voice=mind_voice
)

# Cell 11: Save outputs
import soundfile as sf

sf.write("test_spiritual.wav", output_spiritual.audio, output_spiritual.sample_rate)
sf.write("test_story.wav", output_story.audio, output_story.sample_rate)
sf.write("test_mind.wav", output_mind.audio, output_mind.sample_rate)

print("Test audio files saved!")
print(f"Spiritual: test_spiritual.wav")
print(f"Story: test_story.wav")
print(f"Mind: test_mind.wav")

# Cell 12: Save voice references for later cloning
import numpy as np

# Save the designed voices as reference audio
np.save("voices/spiritual_guide.npy", output_spiritual.audio)
np.save("voices/storyteller.npy", output_story.audio)
np.save("voices/lecturer.npy", output_mind.audio)

print("Voice references saved!")
