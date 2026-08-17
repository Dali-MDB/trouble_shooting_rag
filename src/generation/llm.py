import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

class LLM:
    def __init__(self, model = "dots-studio/dots-3-note-preview:free", reasoning: bool=False):
        self.model = model
        self.reasoning = reasoning
        self.system_prompt = """
                            You are a troubleshooting assistant.

Answer the user's question using ONLY the information provided in the knowledge base.

Do not use your general knowledge or make assumptions.

If the knowledge base does not contain enough information to answer the question, say that you don't know based on the available knowledge base.

Do not provide recommendations or explanations that are not supported by the knowledge base.
                            """


    def answer(self, query: str, knowledge_base : str, history: list|None=None):
        if history is None or history == []:
            history = [ {"role":"system", "content": self.system_prompt}]

        
        augmented_query = query + "\n\nknowledge base: " + knowledge_base
        history.append({"role":"user", "content": augmented_query})
        #  API call 
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv("OPENROUTER_API_KEY")}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": self.model,
            "messages": history,
            "reasoning": {"enabled": self.reasoning}
        })
        )

        # Extract the assistant message with reasoning_details
        response = response.json()
        response = response['choices'][0]['message']

        #remove the backed query (cuz we only need to append the query without knowledge base to the histoyu)
        history.pop()
        history.append({"role":"user", "content": query})

        #append the response to history
        history.append({"role":"assistant", "content": response.get('content')})
        return response.get('content')
