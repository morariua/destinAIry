import logging
logger = logging.getLogger(__name__)
## COUNT TOKENS
import tiktoken
encoding_chat_str = 'gpt-3.5-turbo'
encoding_embedding_str = 'text-embedding-ada-002'
def num_tokens_from_string(string: str, encoding_name: str, purpose: str) -> int:
    """Returns the number of tokens in a text string."""
    if encoding_name in ["gpt2", "p50k_base", "cl100k_base"]:
        encoding = tiktoken.get_encoding(encoding_name)
    else:
        encoding = tiktoken.encoding_for_model(encoding_name)
    assert encoding.decode(encoding.encode(string)) == string
    num_tokens = len(encoding.encode(string))
    print(f"{purpose} <{encoding_name}>: {num_tokens} tokens used")
    logger.info(f"{purpose} <{encoding_name}>: {num_tokens} tokens used")
    return num_tokens