# OpenAI ChatGPT CLI

A command-line interface for interacting with OpenAI's language models, created by Addhe Warman Putra (Awan).

## Features

* Interactive command-line interface for conversations with AI
* Support for multiple OpenAI models (GPT-4, GPT-3.5-turbo, etc.)
* Customizable model parameters (temperature, max tokens, etc.)
* Conversation history tracking
* Character-by-character response display for a more natural feel
* Easy-to-use command-line arguments for model configuration

## Requirements

* Python 3.8 or later
* OpenAI API key (Get it from [OpenAI Platform](https://platform.openai.com/api-keys))
* Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone git@github.com:addhe/openai-chatgpt-cli.git
cd openai-chatgpt-cli
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
   1. Sign up or log in to [OpenAI Platform](https://platform.openai.com)
   2. Navigate to [API Keys section](https://platform.openai.com/api-keys)
   3. Create a new API key
   4. Set the API key in your environment:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

Run the script with default settings:
```bash
python main.py
```

### Advanced Usage

The script supports several command-line arguments for customization:

```bash
python main.py [--model MODEL] [--temperature TEMP] [--max-tokens TOKENS] [--top-p TOP_P]
```

Available options:
- `--model`: Choose the OpenAI model (default: gpt-4.5-preview)
- `--temperature`: Set the response creativity (0.0-2.0, default: 1.0)
- `--max-tokens`: Set maximum response length (default: 2048)
- `--top-p`: Set nucleus sampling parameter (0.0-1.0, default: 1.0)

Examples:
```bash
# Use GPT-3.5-turbo with lower temperature
python main.py --model gpt-3.5-turbo --temperature 0.7

# Use GPT-4 with longer maximum response
python main.py --model gpt-4 --max-tokens 4096

# Customize multiple parameters
python main.py --model gpt-4 --temperature 0.8 --max-tokens 3072 --top-p 0.9
```

## Interactive Commands

While in the chat interface:
- Type your message and press Enter to send
- Type `exit()` to quit the program

## Notes

* Response time may vary depending on the model and request complexity
* API usage is subject to OpenAI's pricing and rate limits
* Generated responses may vary in accuracy and completeness
* Always review the generated content for accuracy

## License

This project is licensed under the MIT License - see the LICENSE file for details.
