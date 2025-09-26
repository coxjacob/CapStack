from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Initialize the Ollama Chat Model
chat_model = ChatOllama(model="llama3")

# Create a human message
message = HumanMessage(content="Tell me a fun fact about space.")

# Invoke the chat model
response = chat_model.invoke([message])

# Print the content of the response
print(response.content)