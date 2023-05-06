from . import langllamaSetup, chatTempl, indexLoader, openaiSetup
import logging
logger = logging.getLogger(__name__)

def setup_chatgpt():
    ## FIRST - load ChatGPT
    openaiSetup.initialize_ChatGPT_objects()
    ## NOTE: Load template texts first before loading indexes
    chatTempl.load_template_texts()
    ## NOTE: Load indexes first before loading tools
    indexLoader.load_indexes_v2()
    print("AI_LOG: Loaded Indexes!")
    logger.info("AI_LOG: Loaded Indexes!")
    ## NOTE: Load LLM Chains first before loading tools
    openaiSetup.load_LLMChains()
    ## NOTE: Load tools first before loading custom prompts!
    openaiSetup.load_langchain_tools()
    openaiSetup.load_llamaindex_tools_v2()
    print("AI_LOG: Loaded Tools!")
    logger.info("AI_LOG: Loaded Tools!")
    chatTempl.load_custom_prompts() ## Needed if using custom agent
    print("AI_LOG: Loaded Custom Prompts!")
    logger.info("AI_LOG: Loaded Custom Prompts!")
    langllamaSetup.load_memory_v2()
    print("AI_LOG: Loaded Memory!")
    logger.info("AI_LOG: Loaded Memory!")
    langllamaSetup.load_custom_AgentExecutor_v2(chatTempl.prompt_English)
    print("AI_LOG: Loaded AgentExecutor Chain!")
    logger.info("AI_LOG: Loaded AgentExecutor Chain!")


import secrets

class SecretKeyGenerator:
    @staticmethod
    def generate_secret_key():
        return secrets.token_hex(32)