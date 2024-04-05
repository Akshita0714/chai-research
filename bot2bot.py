#Note from the developer: 

#This code is a simple implementation of a chatbot that uses the Chai Research API to generate responses.
# There are 2 instances of the same chatbot, that can here talk to each other. The conversation starter can be provided by the user.
#This feature is essentially a solution to a personal problem of mine. I love reading stories and I love it when people tell me stories.
#I thought it would be cool if 2 bots talking essentially could provide a story for me to read.
#this is an attempt to enhance user experience.
#additionally, there has been a max depth of conversation limit to prevent infinite loops. This is very customizable depending on the level of subscriber.
#also something I realized today that CHAI already implements xD.

import requests

class Bot:
    def __init__(self, name, user_name, memory="This is my initial memory.", max_depth=5):
        self.name = name
        self.user_name = user_name
        self.memory = memory
        self.chat_history = []
        self.max_depth = max_depth # Maximum depth of conversation to prevent infinite loops

    def send_message(self, message, recipient):
        if len(self.chat_history) < (self.max_depth-1):
            self.chat_history.append({"sender": self.name, "message": message})
            recipient.receive_message(message, self)
        else:
            print("Max conversation depth reached.")

    def receive_message(self, message, sender):
        if len(self.chat_history) < (self.max_depth-1):
            self.chat_history.append({"sender": sender.name, "message": message})
            # print(f"{sender.name}: {message}")
            response = self.generate_response()
            if response:
                print(f"{self.name}: {response}")
                sender.receive_message(response, self)
        else:
            print(f"Please type 'quit' to end the conversation, or 'subscribe' to continue.")

    def generate_response(self):
        response = requests.post(
            'https://guanaco-submitter.chai-research.com/endpoints/onsite/chat',
            headers={'Authorization': "Bearer CR_6700b8e747434541924772becb8fa85a"},
            json={
                "memory": self.memory,
                "prompt": "An engaging conversation.",
                "bot_name": self.name,
                "user_name": self.user_name,
                "chat_history": self.chat_history
            })
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('model_output', 'No message in response')
        else:
            print(f"Error: Unable to get response from the server, status code {response.status_code}")
            return None


class BotConversation:
    def __init__(self, bot1, bot2):
        self.bot1 = bot1
        self.bot2 = bot2
        self.active = True

    def parse_command(self, message):
        """Parse user input for commands and act on them."""
        if message.strip().lower() == "quit":
            print("Ending conversation.")
            self.active = False
            return True
        elif message.strip().lower() == "subscribe":
            print("We will be adding our subscription feature soon. Stay tuned!")
            print('In the meantime, feel free to start a new free chat!')
            self.active = False
            return True
        return False  # Not a command

    def start(self):
        while self.active:
            user_input = input("You: ")
            if self.parse_command(user_input):
                continue  # Skip the rest of the loop if a command is processed
            self.bot1.send_message(user_input, self.bot2)
            if not self.active:  # Check if the conversation was ended by the command
                break

if __name__ == '__main__':
    bot1 = Bot("Bot1", "User1")
    bot2 = Bot("Bot2", "User2")

    conversation = BotConversation(bot1, bot2)
    conversation.start()



#interrupt is too expensive in code space as an improvement. think of another feature if you can.