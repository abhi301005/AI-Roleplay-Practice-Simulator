
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"


def generate_reply(messages, system_prompt, model="llama3.2"):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt}
        ] + messages,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        return response.json()["message"]["content"]

    except requests.exceptions.ConnectionError:
        return (
            "Ollama is not running. "
            "Please start Ollama and try again."
        )

    except requests.exceptions.Timeout:
        return (
            "The AI model took too long. "
            "Try a smaller model such as qwen2.5:3b."
        )

    except Exception as error:
        return f"AI Error: {error}"
