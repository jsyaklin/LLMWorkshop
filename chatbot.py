#   Import libraries here
#
#   Refer to https://docs.llamaindex.ai/en/stable/examples/llm/gemini/ for help
#

from llama_index.llms.gemini import Gemini
import os


GOOGLE_API_KEY = ""  # add your GOOGLE API key here
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# Write code to create a chatbot



llm = Gemini(
    model="models/gemini-1.5-flash",
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