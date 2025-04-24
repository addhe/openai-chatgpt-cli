import os
import time
import argparse
from openai import OpenAI

def setup_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API Key.")
    return OpenAI(api_key=api_key)

def generate_content(prompt: str, conversation_history: list, model_config: dict):
    try:
        client = setup_openai_client()

        # Add new user prompt to the conversation history
        conversation_history.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model_config["model"],
            messages=conversation_history,
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            top_p=model_config["top_p"]
        )

        message = response.choices[0].message.content

        # Add assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": message})

        # Print response character by character with a slight delay
        for char in message:
            print(char, end="", flush=True)
            time.sleep(0.02)
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="OpenAI Chat CLI")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.5-preview",
        help="OpenAI model to use (default: gpt-4.5-preview)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Sampling temperature (default: 1.0)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Maximum tokens in response (default: 2048)"
    )
    parser.add_argument(
        "--top-p",
        type=float,
        default=1.0,
        help="nucleus sampling parameter (default: 1.0)"
    )
    return parser.parse_args()

def main(input_prompt=None):
    """Main function that handles the chat interface."""
    args = parse_arguments()

    model_config = {
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "top_p": args.top_p
    }

    welcoming_text = f"""
    Welcome to {model_config['model']} Text Generator made by (Awan),
    Happy chat and talk with your {model_config['model']} AI Generative Model
    Addhe Warman Putra - (Awan)
    type 'exit()' to exit from program
    """
    print(welcoming_text)

    # Initialize conversation history with system message
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    if input_prompt is None:
        while True:
            prompt = input("\n> ")
            if prompt.lower() == "exit()":
                print("\nGoodbye!")
                exit()
            generate_content(prompt, conversation_history, model_config)
    else:
        if input_prompt.lower() == "exit()":
            print("\nGoodbye!")
            exit()
        generate_content(input_prompt, conversation_history, model_config)

if __name__ == "__main__":
    main()
