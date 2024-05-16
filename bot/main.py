import re
import os
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
dtoken = os.getenv("DKEY")
api_key = os.getenv("GKEY")

# Configure generative AI API
genai.configure(api_key=api_key)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1950,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Initialize bot
intents = nextcord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged on as {client.user}!")

@client.slash_command(name="test", description="Send your input to Generative AI")
async def test(interaction: Interaction, question: str):
    await interaction.response.send_message("Generating response...", ephemeral=True)

    convo = model.start_chat(history=[])
    convo.send_message(question)
    response = convo.last.text

    # Truncate the response if it exceeds the character limit
    if len(response) > 2000:
        response = response[:1997] + "..."

    await interaction.followup.send(f"Generative AI response:\n{response}")

client.run(dtoken)
