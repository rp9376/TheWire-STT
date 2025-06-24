from ollama import Client
import os
clear_terminal = lambda: os.system('cls' if os.name == 'nt' else 'clear')


model = 'llama3.1:70b'

def create_client():
    return Client(
        host='http://10.45.10.10:11434',
        headers={'x-some-header': 'some-value'}
    )



def get_user_message():
    return input("Enter your message: ")

def chat_with_ollama(client, model, user_message):
    response = client.chat(model, messages=[
        {
            'role': 'user',
            'content': user_message,
        },
    ])
    return response['message']['content']

def main():
    client = create_client()

    user_message = get_user_message()
    reply = chat_with_ollama(client, model, user_message)
    print(reply)

if __name__ == "__main__":
    main()