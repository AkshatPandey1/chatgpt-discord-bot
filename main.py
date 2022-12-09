from dotenv import load_dotenv
from asyncChatGPT.asyncChatGPT import Chatbot
import discord
import os

load_dotenv()

# Initialize client with ability to send and receive messages
client = discord.Client(intents=discord.Intents.all())

# Initialize the chatbot
config = {
    "email": "",
    "password": "",
}

config.update(session_token=os.getenv("SESSION_TOKEN"))
chatbot = Chatbot(config, conversation_id=None)


def messageWithoutPing(message):
    if message.mentions:
        # Get all the mentions in the message
        mentions = message.mentions
        # Get the message content
        content = message.content
        # Loop through all the mentions
        for mention in mentions:
            # Replace the mention with the user's name
            content = content.replace(mention.mention, mention.name)
        # Return the message content
        return content
    return message.content


async def getAIMessage(message):
    chatbot.refresh_session()
    response = await chatbot.get_chat_response(message, output="text")
    responseMessage = response['message']
    return responseMessage


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

stop = False


@client.event
async def on_message(message):
    global stop

    if message.author.id == 367630872066654209:
        return

    if message.author == client.user:
        return

    if message.content == "ai.stop":
        stop = True
        await message.channel.send("Stopping AI")
        return

    if message.content == "ai.start":
        stop = False
        await message.channel.send("Starting AI")
        return

    if message.content == "ai.reset":
        chatbot.reset_chat()
        await message.channel.send("Resetting AI")
        return

    if message.content == "ai.help":
        await message.channel.send("ai.start - Start the AI\nai.stop - Stop the AI\nai.reset - Reset the AI")
        return

    if stop:
        return
    else:
        response = await getAIMessage(messageWithoutPing(message))
        await message.channel.send(response, reference=message)


client.run(os.getenv('TOKEN'))
