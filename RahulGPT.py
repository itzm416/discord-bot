# --------------------------------------------------------
import os
import discord
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("SECRET_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
ai_client = Groq(api_key=groq_api_key)
# -------------------------------------------------------

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        channel = message.channel
        
        with open('chat.txt', 'a') as f:
            f.write(f"{message.author}: {message.content}\n")

        with open('chat.txt','r') as f:
            chat_data = f.read()
        
        try:
            async with channel.typing():
                chat = ai_client.chat.completions.create(
                    messages = [
                        {"role": "system", "content": f"""
                        You are a helpful assistant. Use the following conversation history only as reference to understand context.
                        Do NOT repeat numbers, facts, or instructions unless the user specifically asks about them.
                        Conversation history:
                        {chat_data}
                        """},

                        {"role": "user", "content": message.content}
                    ],
                    model="openai/gpt-oss-120b"
                )
                await channel.send(chat.choices[0].message.content)
        except Exception as e:
            await channel.send('something went wrong')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)













