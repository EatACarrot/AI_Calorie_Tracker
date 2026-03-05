import os

from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user, system

load_dotenv(".env")
client = Client(api_key = os.getenv("XAI_API_KEY"))

chat = client.chat.create(model="grok-4-1-fast-reasoning")
chat.append(system("You are Grok, a highly intelligent, helpful AI assistant."))
chat.append(user("What is the meaning of life, the universe, and everything?"))
response = chat.sample()
print(response.content)