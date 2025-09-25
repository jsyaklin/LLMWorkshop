import os

#   Import libraries here
#
from llama_index.core.llms import ChatMessage
from llama_index.llms.google_genai import GoogleGenAI



#   Refer to https://developers.llamaindex.ai/python/examples/llm/google_genai/ for help
#

GOOGLE_API_KEY = ""  # add your GOOGLE API key here
os.environ["GOOGLE_API_KEY"] = "AIzaSyBHoN7nIQswCc1Ie25dmbNyfSf8VKAhNHc"

llm = GoogleGenAI(
    model="models/gemini-2.5-flash",
    # api_key="some key",  # uses GOOGLE_API_KEY env var by default
)

messages = [
    ChatMessage(role="user", content="Hello friend!"),
    ChatMessage(role="assistant", content="Yarr what is shakin' matey?"),
    ChatMessage(
        role="user", content="Help me decide what to have for dinner."
    ),
]

resp = llm.chat(messages)
print(resp)


# Write code to create a chatbot

