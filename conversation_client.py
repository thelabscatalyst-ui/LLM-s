from litellm import completion


def askLLM(prompt, user_history, ai_history,
           temperature=0.7, Max_tokens=150,
           model="ollama_chat/qwen2.5:3b"):

    messages = [
        {
            "role": "system",
            "content": "You are a senior developer"
        }
    ]

    # Add previous conversations in chronological order
    for user_msg, ai_msg in zip(user_history, ai_history):

        messages.append({
            "role": "user",
            "content": user_msg
        })

        messages.append({
            "role": "assistant",
            "content": ai_msg
        })

    # Add the current user prompt
    messages.append({
        "role": "user",
        "content": prompt
    })

    response = completion(
        model=model,
        messages=messages,
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

        try:
            response = askLLM(
                prompt,
                user_response,
                ai_response
            )

            print("Response:", response)

            user_response.append(prompt)
            ai_response.append(response)

        except Exception as e:
            print("Error:", type(e).__name__, str(e))


if __name__ == "__main__":
    main()
