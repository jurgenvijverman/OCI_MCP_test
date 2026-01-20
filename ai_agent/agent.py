
"""
AI Agent CLI: Asks a question, fetches network config from MCP server using MCP SDK, and answers using OpenAI API.

Requirements:
- Install MCP SDK: pip install model-context-protocol
- Install OpenAI SDK: pip install openai
"""

import sys
import openai
# from mcp import McpClient  # Uncomment when MCP SDK is installed
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Placeholder for MCP SDK usage
def get_network_config():
	# TODO: Replace with MCP SDK call, e.g.:
	# client = McpClient(MCP_SERVER_URL)
	# return client.get("/network/config")
	import requests
	resp = requests.get(f"{MCP_SERVER_URL}/network/config")
	return resp.json()

def ask_openai(question, context):
	openai.api_key = OPENAI_API_KEY
	prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
	response = openai.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "You are an expert on Oracle Cloud Infrastructure network configuration."},
			{"role": "user", "content": prompt}
		],
		max_tokens=400,
		temperature=0.2
	)
	return response.choices[0].message.content.strip()


def main():
	print("AI Agent for Oracle Cloud Network Configuration. Type your question and press Enter. Press Ctrl+C to exit.")
	network_config = get_network_config()
	try:
		while True:
			question = input("\n> ")
			if not question.strip():
				continue
			answer = ask_openai(question, str(network_config))
			print("\nAI Agent Answer:\n", answer)
	except KeyboardInterrupt:
		print("\nExiting agent.")

if __name__ == "__main__":
	main()
