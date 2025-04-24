import sys
import unittest
import argparse
from io import StringIO
from unittest.mock import patch, MagicMock

from main import generate_content, main, setup_openai_client, parse_arguments


class TestMain(unittest.TestCase):

    def setUp(self):
        # Mock OpenAI client
        self.mock_client = MagicMock()
        self.mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="This is a fake response from the OpenAI API."))]
        )
        self.client_patcher = patch('main.setup_openai_client', return_value=self.mock_client)
        self.client_patcher.start()

    def tearDown(self):
        patch.stopall()

    def test_parse_arguments(self):
        # Test default arguments
        with patch('sys.argv', ['main.py']):
            args = parse_arguments()
            self.assertEqual(args.model, "gpt-4.5-preview")
            self.assertEqual(args.temperature, 1.0)
            self.assertEqual(args.max_tokens, 2048)
            self.assertEqual(args.top_p, 1.0)

        # Test custom arguments
        with patch('sys.argv', ['main.py', '--model', 'gpt-4', '--temperature', '0.7',
                               '--max-tokens', '4096', '--top-p', '0.9']):
            args = parse_arguments()
            self.assertEqual(args.model, "gpt-4")
            self.assertEqual(args.temperature, 0.7)
            self.assertEqual(args.max_tokens, 4096)
            self.assertEqual(args.top_p, 0.9)

    def test_main(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        with patch('sys.argv', ['main.py', '--model', 'gpt-4']):
            main(input_prompt="Hello, world!")

        sys.stdout = sys.__stdout__

        actual_output = captured_output.getvalue().strip()

        expected_output_start = """
        Welcome to gpt-4 Text Generator made by (Awan),
        Happy chat and talk with your gpt-4 AI Generative Model
        Addhe Warman Putra - (Awan)
        type 'exit()' to exit from program
        """.strip()

        # Normalize both strings to ignore leading/trailing whitespace
        actual_lines = [line.strip() for line in actual_output.splitlines()]
        expected_lines = [line.strip() for line in expected_output_start.splitlines()]

        for expected_line in expected_lines:
            self.assertIn(expected_line, actual_lines)

        # Ensure the response is in the actual output
        self.assertIn("This is a fake response from the OpenAI API.", actual_output)

    @patch('os.getenv', return_value='fake-api-key')
    def test_setup_openai_client(self, mock_getenv):
        client = setup_openai_client()
        self.assertIsNotNone(client)
        mock_getenv.assert_called_once_with("OPENAI_API_KEY")

    @patch('os.getenv', return_value=None)
    def test_setup_openai_client_missing_key(self, mock_getenv):
        with self.assertRaises(ValueError) as context:
            setup_openai_client()
        self.assertEqual(str(context.exception), "Missing OpenAI API Key.")

    def test_generate_content(self):
        conversation_history = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

        model_config = {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9
        }

        # Store initial conversation history length
        initial_history_len = len(conversation_history)

        generate_content("Hello, world!", conversation_history, model_config)

        # Verify the API was called with correct parameters
        self.mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4",
            messages=conversation_history[:initial_history_len + 1],  # Only include system and user messages
            temperature=0.7,
            max_tokens=2048,
            top_p=0.9
        )

        # Verify the conversation history was updated correctly after the API call
        self.assertEqual(len(conversation_history), initial_history_len + 2)  # system + user + assistant
        self.assertEqual(conversation_history[1], {"role": "user", "content": "Hello, world!"})
        self.assertEqual(conversation_history[2],
                        {"role": "assistant", "content": "This is a fake response from the OpenAI API."})


if __name__ == "__main__":
    unittest.main()
