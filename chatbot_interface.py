import requests
from cmd import Cmd

class ChatBotInterface(Cmd):
    prompt = 'You: '
    intro = 'Chat with the Bot. Type "quit" to exit.'

    def __init__(self):
        super().__init__()
        self.memory = "I am Bot, and this is my mind."
        self.bot_name = "Bot"
        self.user_name = "User"
        self.chat_history = []

    def default(self, line):
        if line.lower() == 'quit':
            return True
        self.send_message(line)

    def send_message(self, message):
        self.chat_history.append({"sender": self.user_name, "message": message})
        response = requests.post('https://guanaco-submitter.chai-research.com/endpoints/onsite/chat',
                                 headers={'Authorization': "Bearer CR_6700b8e747434541924772becb8fa85a"},
                                 json={
                                     "memory": self.memory,
                                     "prompt": "An engaging conversation with Bot.",
                                     "bot_name": self.bot_name,
                                     "user_name": self.user_name,
                                     "chat_history": self.chat_history
                                 })
        if response.status_code == 200:
            response_data = response.json()
    
            bot_message = response_data.get('model_output', 'No message in response')
            print(f"{self.bot_name}: {bot_message}")
            self.chat_history.append({"sender": self.bot_name, "message": bot_message})
        else:
            print(f"Error: Unable to get response from the server, status code {response.status_code}")

if __name__ == '__main__':
    ChatBotInterface().cmdloop()
