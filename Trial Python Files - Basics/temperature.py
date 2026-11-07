from litellm import completion

response = completion(
    model="ollama_chat/qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Suggest a creative name for an AI startup."
        }
    ],
    api_base="http://localhost:11434",
    temperature=3.0
)

print(response.choices[0].message.content)