from litellm import completion

response = completion(
    model = "ollama_chat/qwen2.5:3b",

    messages = [
        {"role": "system", "content": "You are a senior developer"},
        {"role": "user", "content": " Explain Python!"}
    ],
    api_base="http://localhost:11434",
    stream = True # off by default, just to be explicit 
)

for chunk in response:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

final_chunk = None
for chunk in response:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
    final_chunk = chunk
# this is the looping condition used when streaimng is on 
# beacuse a custom wrapper is built around the response object, the final chunk is not returned in the first loop, so we need to loop again to get it.