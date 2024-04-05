#Note from the developer: 

#This code is a simple implementation of a chatbot that uses the Chai Research API to generate responses.
# There are 2 instances of the same chatbot, that can here talk to each other. The conversation starter can be provided by the user.
#so if the user wants a story to be told, the user can provide the story starter and the bots will continue the story.
#this feature is an attempt to enhance user experience.
#additionally, there has been a max depth of conversation limit to prevent infinite loops. This is very customizable depending on the level of subscriber.
#also something I realized today that CHAI already implements xD.

import requests
from cmd import Cmd

class Bot:
    def __init__(self, name, user_name, memory="This is my initial memory.", max_depth=10):
        self.name = name
        self.user_name = user_name
        self.memory = memory
        self.chat_history = []
        self.max_depth = max_depth # Maximum depth of conversation to prevent infinite loops

    def send_message(self, message, recipient):
        if len(self.chat_history) < self.max_depth:
            self.chat_history.append({"sender": self.name, "message": message})
            recipient.receive_message(message, self)
        else:
            print("Max conversation depth reached.")

    def receive_message(self, message, sender):
        if len(self.chat_history) < self.max_depth:
            self.chat_history.append({"sender": sender.name, "message": message})
            # print(f"{sender.name}: {message}")
            response = self.generate_response()
            if response:
                print(f"{self.name}: {response}")
                sender.receive_message(response, self)
        else:
            print(f"Conversation depth limit reached. No further messages will be exchanged.")

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
        self.active = True  # Tracks if the conversation is active

    def parse_command(self, message):
        """Parse user input for commands and act on them."""
        if message == "/end":
            print("Ending conversation.")
            self.active = False
            return True  #  command was processed
        elif message == "/history":
            print("Chat History:")
            for entry in self.bot1.chat_history:
                print(f"{entry['sender']}: {entry['message']}")
            for entry in self.bot2.chat_history:
                print(f"{entry['sender']}: {entry['message']}")
            return True  # Indicates a command was processed
       
        return False  #  no command 

    def start(self):
        while self.active:
            user_input = input("You: ")
            if self.parse_command(user_input):
                continue  # Skip loop if command given
            self.bot1.send_message(user_input, self.bot2)
            if not self.active:
                break  # Exit the loop if the conversation was ended by a command


if __name__ == '__main__':
    bot1 = Bot("Bot1", "User1")
    bot2 = Bot("Bot2", "User2")

    conversation = BotConversation(bot1, bot2)
    conversation.start()


#interrupt is too expensive in code space as an improvement. think of another feature if you can.