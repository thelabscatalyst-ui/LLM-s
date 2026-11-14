"""Run a three-agent workflow using an Ollama model chosen by the user."""

import json
from urllib.error import URLError
from urllib.request import urlopen

from litellm import completion


API_BASE = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:3b"

AGENTS = {
    "Researcher": "You are a careful researcher. Give a clear first answer to the user's request.",
    "Reviewer": "Review the researcher's answer for errors, gaps, and unclear wording. Suggest improvements.",
    "Final assistant": "Write the final answer using the user's request, the research, and the review. Be accurate and direct.",
}


def get_installed_models():
    """Get model names already available in the local Ollama installation."""
    try:
        with urlopen(f"{API_BASE}/api/tags", timeout=3) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(
            "Could not connect to Ollama at http://localhost:11434. "
            "Start Ollama and try again."
        ) from error

    return [item["name"] for item in data.get("models", []) if item.get("name")]


def choose_model(models):
    """Let the user select one of the models installed in Ollama."""
    if not models:
        raise RuntimeError("No Ollama models are installed. Install one and try again.")

    default_index = next(
        (index for index, name in enumerate(models, start=1) if name == DEFAULT_MODEL),
        1,
    )

    print("Installed Ollama models:")
    for index, name in enumerate(models, start=1):
        default_note = " (default)" if index == default_index else ""
        print(f"  {index}. {name}{default_note}")

    while True:
        choice = input(f"Choose a model [default {default_index}]: ").strip()
        if not choice:
            return models[default_index - 1]
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1]
        print(f"Choose a number from 1 to {len(models)}, or press Enter for the default.")


def ask_agent(prompt, system_prompt, model, user_history=None, ai_history=None,
              temperature=0.7, max_tokens=300):
    """Call one agent with the selected model and optional conversation history."""
    messages = [{"role": "system", "content": system_prompt}]

    if user_history and ai_history:
        for user_message, assistant_message in zip(user_history, ai_history):
            messages.append({"role": "user", "content": user_message})
            messages.append({"role": "assistant", "content": assistant_message})

    messages.append({"role": "user", "content": prompt})

    response = completion(
        model=f"ollama_chat/{model}",
        messages=messages,
        api_base=API_BASE,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""


def run_agents(prompt, model, user_history=None, ai_history=None):
    """Run the researcher, reviewer, and final assistant with the same model."""
    research = ask_agent(
        prompt, AGENTS["Researcher"], model, user_history, ai_history
    )
    review_prompt = f"User request:\n{prompt}\n\nResearcher's answer:\n{research}"
    review = ask_agent(review_prompt, AGENTS["Reviewer"], model)
    final_prompt = (
        f"User request:\n{prompt}\n\nResearcher's answer:\n{research}"
        f"\n\nReview:\n{review}"
    )
    return ask_agent(final_prompt, AGENTS["Final assistant"], model)


def main():
    try:
        model = choose_model(get_installed_models())
    except (RuntimeError, EOFError) as error:
        print(f"Error: {error}")
        return

    user_history = []
    ai_history = []
    print(f"Using {model}. Enter 'exit' to quit.")

    while True:
        try:
            prompt = input("\nPrompt: ").strip()
        except EOFError:
            break

        if prompt.lower() == "exit":
            break
        if not prompt:
            continue

        try:
            answer = run_agents(prompt, model, user_history, ai_history)
            print(f"\nResponse: {answer}")
            user_history.append(prompt)
            ai_history.append(answer)
        except Exception as error:
            print(f"Error while calling Ollama: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
