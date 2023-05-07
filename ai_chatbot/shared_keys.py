import os

OPENAI_CHAT_MODEL = os.environ.get("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
OPENAI_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
TEMPERATURE = os.environ.get("TEMPERATURE", "0")
CHUNK_SIZE = os.environ.get("CHUNK_SIZE", "256")
CHUNK_OVERLAP = os.environ.get("CHUNK_OVERLAP", "20")
MAX_TOKENS = os.environ.get("MAX_TOKENS", "512")
MAX_CHAR_INPUT = os.environ.get("MAX_CHAR_INPUT", "100")
LAST_K_CHAT_HISTORY_MESSAGES_IN_MEMORY = os.environ.get("LAST_K_CHAT_HISTORY_MESSAGES_IN_MEMORY", "1")
MAX_RETRIES = os.environ.get("MAX_RETRIES", "1")
OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE", "open_ai")

os.environ["OPENAI_ORG_KEY"] = ""
os.environ["OPENAI_API_VERSION"] = ""
os.environ["OPENAI_API_TYPE"] = "open_ai"

## For UI
INPUT_EXCEEDED_MESSAGE = "Sorry, you have typed too many words. Can you try to shorten your query?"