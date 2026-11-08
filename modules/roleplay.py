import os
import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/chat"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_reply(messages, system_prompt, model="llama3.2"):
    # Groq mode is enabled by AI_PROVIDER=groq in Streamlit Cloud Secrets.
    if st.secrets.get("AI_PROVIDER", "ollama").lower():
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            payload = {
                "model": model,
                "messages": [{"role": "system", "content": system_prompt}] + messages,
                "temperature": 0.7,
                "max_tokens": 800,
            }
            response = requests.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=90,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except KeyError:
            return "Groq API key is missing. Add GROQ_API_KEY in Streamlit Cloud Secrets."
        except requests.exceptions.Timeout:
            return "The cloud AI request timed out. Please try again."
        except requests.exceptions.HTTPError as error:
            try:
                details = response.json().get("error", {}).get("message", "")
            except Exception:
                details = ""
            return f"Groq API error: {details or error}"
        except Exception as error:
            return f"Cloud AI error: {error}"

    # Local mode: Ollama
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Please start Ollama and try again."
    except requests.exceptions.Timeout:
        return "The AI model took too long. Try a smaller model such as qwen2.5:3b."
    except Exception as error:
        return f"AI Error: {error}"
