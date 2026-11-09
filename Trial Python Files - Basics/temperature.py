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
# i tried temperatur with multiple values and saw the results

print(response.choices[0].message.content)

# Top B is also called nucleus sampling, it is a technique used in natural language processing to generate text by sampling from the most probable next words based on a given context. Instead of always selecting the single most likely next word, top-p sampling considers a subset of words whose cumulative probability exceeds a certain threshold (p). This allows for more diverse and creative text generation, as it introduces randomness into the selection process while still maintaining coherence with the context.