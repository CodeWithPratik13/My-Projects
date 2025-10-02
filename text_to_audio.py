from elevenlabs import stream
from elevenlabs.client import ElevenLabs
import os
from config import Elevenlab_api_key

# Initialize ElevenLabs client with your API key
elevenlabs = ElevenLabs(
    api_key=Elevenlab_api_key
)

# Function to convert text to speech and save as mp3
def text_to_speech_file(text: str, folder: str):
    # Create folder if it doesn't exist
    folder_path = os.path.join("user_upload", folder)
    os.makedirs(folder_path, exist_ok=True)

    # File path
    save_file_path = os.path.join(folder_path, "audio.mp3")

    # Generate audio stream
    audio_stream = elevenlabs.text_to_speech.stream(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # default voice
        model_id="eleven_multilingual_v2"
    )

    # Save to file
    with open(save_file_path, "wb") as f:
        for chunk in audio_stream:
            if isinstance(chunk, bytes):
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

# Example call
# if __name__ == "__main__":
#     text_to_speech_file(
#         "Hey I am Gaurav Shrivas and it's the best Python course",
#         "4f8424f8-5287-11f0-8574-1068388df646"
#     )