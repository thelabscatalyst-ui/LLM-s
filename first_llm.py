from litellm import completion

response = completion(
    model = "ollama_chat/qwen2.5:3b",

    messages = [
        {"role": "system", "content": "You are a senior developer"},
        {"role": "user", "content": "Return information about three programming languages, for each langauge include name difficulty, primary_use. return only valid JSON, no markdown formatting"}
    ],
    api_base="http://localhost:11434"
)

print(response.choices[0].message.content)
