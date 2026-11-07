from litellm import completion

def askLLM(prompt, temperature=0.7, Max_tokens=150, model="ollama_chat/qwen2.5:3b"):
    response = completion(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        api_base="http://localhost:11434",
        temperature=temperature,
        max_tokens=Max_tokens
    )

    return response.choices[0].message.content

def main():
    print("Enter a prompt or enter exit to quit:")

    while True: 
        prompt = input("Prompt: ").strip()
        if prompt.lower() == "exit":
            break

        response = askLLM(prompt)
        print("Response:", response)

if __name__ == "__main__":
    main()


        
