import os
from dotenv import load_dotenv
from openai import OpenAI
import json


# Load environment variables
load_dotenv()

# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    # not required if using the default api key name
    api_key=os.environ.get("OPENAI_API_KEY"),
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def add_message(messages, message):
    messages.append(message)


# Prompting function for user input and processing the response
def prompt_user():
    """
    {
        "id": "chatcmpl-9DIioqnO930efJ3vbLITyWc6gCLkP",
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "logprobs": null,
                "message": {
                    "content": "Hello! How can I help you today?",
                    "role": "assistant"
                }
            }
        ],
        "created": 1712957258,
        "model": "gpt-3.5-turbo-0125",
        "object": "chat.completion",
        "system_fingerprint": "fp_c2295e73ad",
        "usage": {
            "completion_tokens": 9,
            "prompt_tokens": 8,
            "total_tokens": 17
        }
    }
    """
    user_input = input("You: ")
    add_message(messages, {"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )
    add_message(messages, response.choices[0].message.to_dict())
    print("AI:", response.choices[0].message.content)
    print("messages:", messages)
    # print(json.dumps(response.to_dict(), indent=4))
    prompt_user()


# Do not use this, it has an irregular response message data structure
def prompt_user2():
    """
    {
        "id": "chatcmpl-9DJC1OPPjDahvHbitKYRCbagWIIHg",
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "logprobs": null,
                "message": {
                    "content": "{\n  \"message\": \"Hello! How can I assist you today?\"\n}",
                    "role": "assistant"
                }
            }
        ],
        "created": 1712959069,
        "model": "gpt-3.5-turbo-0125",
        "object": "chat.completion",
        "system_fingerprint": "fp_c2295e73ad",
        "usage": {
            "completion_tokens": 16,
            "prompt_tokens": 22,
            "total_tokens": 38
        }
    }
    """
    user_input = input("You: ")
    add_message(messages, {"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": user_input}
        ],
    )
    message_content = response.choices[0].message.to_dict()
    print("message_content", message_content)
    add_message(messages, {"role": message_content['role'], "content": message_content['content']})
    print("AI:", response.choices[0].message.content)
    print("messages:", messages)
    # print(json.dumps(response.to_dict(), indent=4))
    prompt_user2()


# Start the interaction
prompt_user()
