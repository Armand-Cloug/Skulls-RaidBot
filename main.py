#!/bin/python3.11

import discord
import asyncio
import os
import signal
import atexit
from discord.ext import commands
from dotenv import load_dotenv
from discord_embeb import create_raid_embed, RaidView

# Charger les variables d’environnement
load_dotenv()

token = os.getenv('TOKEN')
chan_id = int(os.getenv('CHAN_ID'))              # Pour le message ON/OFF

intents = discord.Intents.all()
bot_client = commands.Bot(command_prefix=":", intents=intents)


# 💡 Fonction appelée quand on quitte (même avec Ctrl+C)
async def send_bot_off_message():
    await bot_client.wait_until_ready()
    channel = bot_client.get_channel(chan_id)
    if channel:
        try:
            await channel.send(" Le bot est maintenant **hors ligne**. 🔌")
            print("[📤] Message OFF envoyé.")
        except Exception as e:
            print(f"[⚠️] Erreur envoi message OFF : {e}")

@bot_client.event
async def setup_hook():
    await bot_client.load_extension("discord_command")  # nom du fichier sans le .py
    try:
        synced = await bot_client.tree.sync()
        print(f"{len(synced)} commande(s) synchronisée(s)")
    except Exception as e:
        print("[❌] Erreur lors de la synchro des commandes.")

@bot_client.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot_client.user}")

     # ✅ Message d'activation et envoi de l'embed
    channel_1 = bot_client.get_channel(chan_id)
    if channel_1:
        await channel_1.send("Le bot est ON ! 🚀")
    else:
        print(f"[⚠️] Channel ID {chan_id} introuvable.")

### MAIN
def main():
    async def shutdown():
        await send_bot_off_message()
        await bot_client.close()

    def signal_handler(*_):
        print("[🛑] Interruption reçue (Ctrl+C), arrêt propre...")
        asyncio.create_task(shutdown())

    # 🔌 Gérer Ctrl+C proprement
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    bot_client.run(token)

if __name__ == '__main__':
    main()
