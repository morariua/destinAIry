import os
from . import shared_keys, secret_keys
from .chatTempl import few_shot_system_prompt_template, human_template
## Wrap openai with langchain
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain

from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import openai
openai.api_type = shared_keys.OPENAI_API_TYPE
chatAI = ChatOpenAI(temperature=float(shared_keys.TEMPERATURE),
                    openai_api_key=secret_keys.OPENAI_API_KEY,
                    max_tokens=int(shared_keys.MAX_TOKENS)
                    )

def generate_response(text: str, first_name: str, last_name: str, nationality: str, age: str, gender: str,
                      destinations: str, duration: str, start_date: str):
    system_message_prompt = SystemMessagePromptTemplate.from_template(few_shot_system_prompt_template.format())
    print(f"system_message_prompt: {system_message_prompt}\n")

    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    print(f"human_message_prompt: {human_message_prompt}\n")

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    print(f"chat_prompt: {chat_prompt}\n")
    response = chatAI(chat_prompt.format_prompt(text=text, first_name=first_name, last_name=last_name, nationality=nationality,
                                                age=age, gender=gender, destinations=destinations, duration=duration, start_date=start_date).to_messages())
    return response

