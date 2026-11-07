from litellm import OpenAI, completion

def askLLM(prompt, user_history, ai_history, temperature=0.7, Max_tokens=150, model="ollama_chat/qwen2.5:3b"):
    response = completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a senior developer"
            },
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "assistant",
                "content": user_history
            },
            {
                "role": "assistant",
                "content": ai_history
            }
        ],

        api_base="http://localhost:11434",
        temperature=temperature,
        max_tokens=Max_tokens
    )

    return response.choices[0].message.content

def main():
    user_response = []
    ai_response = []

    print("Enter a prompt or enter exit to quit:")

    while True:
        prompt = input("Prompt: ").strip()
        if prompt.lower() == "exit":
            break

        response = askLLM(prompt, user_response, ai_response)
        print("Response:", response)

        user_response.append(prompt)
        ai_response.append(response)

if __name__ == "__main__":
    main()
