import os
from . import shared_keys, secret_keys
from .chatTempl import chat_prompt
## Wrap openai with langchain
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain


chatAI = ChatOpenAI(temperature=float(shared_keys.TEMPERATURE),
                    openai_api_key=secret_keys.OPENAI_API_KEY,
                    max_tokens=int(shared_keys.MAX_TOKENS))