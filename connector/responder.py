import openai
import requests
import tempfile
import os


def respond(text, config):
    """Send text to GPT and output audio via TTS."""
    openai.api_key = config.get('openai_api_key')
    model = config.get('openai_model', 'gpt-3.5-turbo')

    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": text}]
    )
    reply = completion.choices[0].message['content']

    tts_api = config.get('tts_api')
    if not tts_api:
        print(reply)
        return

    # Example for ElevenLabs
    response = requests.post(
        tts_api,
        json={"text": reply},
        headers={"xi-api-key": config.get('tts_api_key')}
    )

    if response.ok:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            f.write(response.content)
            os.system(f"afplay {f.name}")
            os.unlink(f.name)
    else:
        print(reply)
