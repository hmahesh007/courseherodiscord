import discord
from discord.ext import commands
import random
import markovify
import zipfile
import os

intents = discord.Intents.default()
intents.message_content = True

# Replace 'YOUR_TOKEN' with your bot's token
TOKEN = os.getenv('DISCORD_TOKEN')
CORPUS_PATH = os.getenv('CORPUS_PATH')
PREFIX = '!'

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

with open(CORPUS_PATH, 'r') as file:
    text = file.read()

# Create a text model using the corpus text
text_model = markovify.Text(text)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(f'{PREFIX}generate_essays'):
        await generate_and_send_essays(message)

async def generate_and_send_essays(message):
    # Generate 10 differently generated essays, each containing 100 random sentences
    generated_text_files = []
    for i in range(10):
        generated_sentences = [text_model.make_sentence() for i in range(100)]
        essay = "\n".join(filter(None, generated_sentences))

        # Create a text file with the essay content
        text_file_name = f'essay_{i+1}.txt'
        with open(text_file_name, 'w') as essay_file:
            essay_file.write(essay)

        # Add the text file to the list of generated text files
        generated_text_files.append(text_file_name)

    # Create a zip file containing all the generated text files
    zip_file_path = create_zip_file(generated_text_files)

    # Send the zip file as a message
    with open(zip_file_path, "rb") as zip_file:
        file = discord.File(zip_file, filename="essays.zip")
        await message.channel.send(file=file)

    # Delete the generated text files
    for text_file in generated_text_files:
        os.remove(text_file)

def create_zip_file(text_files):
    """Creates a zip file containing the specified text files.

    Args:
        text_files (list): A list of text files to be included in the zip file.

    Returns:
        str: The path to the created zip file.
    """

    zip_file_name = "essays.zip"
    with zipfile.ZipFile(zip_file_name, "w") as zip_file:
        for text_file in text_files:
            zip_file.write(text_file)

    return zip_file_name

bot.run(TOKEN)
