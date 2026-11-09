from litellm import completion

response = completion(
    model="ollama_chat/qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain AI agents in 100 words."
        }
    ],
    api_base="http://localhost:11434",
    stream=True
)

for chunk in response:
    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)
# flush helps to immediately put the output to the screen