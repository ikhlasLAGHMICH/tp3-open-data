"""Module chatbot pour interroger les données."""
import os
import pandas as pd
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

class DataChatbot:
    """Chatbot pour interroger les données (Ollama en local / OpenRouter en cloud)."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

        # 🔵 CLOUD → OpenRouter
        if os.getenv("OPENROUTER_API_KEY"):
            self.model = "openrouter/mistralai/mistral-7b-instruct:free"
            self.api_base = "https://openrouter.ai/api/v1"
            self.api_key = os.getenv("OPENROUTER_API_KEY")

        # 🟢 LOCAL → Ollama
        else:
            self.model = "ollama/mistral"
            self.api_base = "http://localhost:11434"
            self.api_key = None

        self.context = self._build_context()
        self.history = []

    def _build_context(self) -> str:
        """Construit le contexte des données pour l'IA."""
        sample = self.df.head(3).to_string()
        cols = list(self.df.columns)

        try:
            stats = self.df.describe().to_string()
        except Exception:
            stats = "Non disponible"

        return f"""
Tu es un Data Analyst expert.

INFOS DATASET :
- Colonnes : {cols}
- Total lignes : {len(self.df)}

STATS :
{stats}

ECHANTILLON :
{sample}

Réponds aux questions sur ces données de manière concise.
"""

    def chat(self, user_message: str) -> str:
        """Envoie un message et récupère la réponse."""
        messages = [{"role": "system", "content": self.context}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_message})

        try:
            response = completion(
                model=self.model,
                api_base=self.api_base,
                api_key=self.api_key,   # ← IMPORTANT pour OpenRouter
                messages=messages,
                temperature=0.2
            )

            assistant_msg = response.choices[0].message.content

            self.history.append({"role": "user", "content": user_message})
            self.history.append({"role": "assistant", "content": assistant_msg})

            if len(self.history) > 10:
                self.history = self.history[-10:]

            return assistant_msg

        except Exception as e:
            return f"❌ Erreur LLM : {str(e)}"

    def reset(self):
        self.history = []
