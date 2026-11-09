import litellm

text = """
Artificial Intelligence is transforming
the way software applications are developed.
"""

tokens = litellm.token_counter(
    model="ollama_chat/qwen2.5:3b",
    messages=[
        {"role": "user", "content": text}
    ]
)

print("Token count:", tokens)

# this is just an estimate of the tokens on the basis of llmlite tokenizer, actual token count may vary 
