import discord
from discord.ext import commands
import mysql.connector
import os
import sys
from dotenv import load_dotenv
import json

# Pour passer le bot_client dans les scrapers
from main import bot_client

role_admin="La Team" 

class RebootCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="reboot_sk",
        description="🔁 Redémarre le bot via PM2."
    )
    @commands.is_owner()
    async def reboot(self, ctx: commands.Context):
        await ctx.reply("♻️ Redémarrage du bot via **PM2** en cours...", ephemeral=True)

        print(f"[🔁] Reboot demandé par {ctx.author} via /reboot")

        # ✅ Restart via PM2
        os.system("pm2 restart bot-skulls")  # ← "discord-bot" est le nom que tu donnes avec pm2 start

        # 🛑 Fermer proprement l'instance actuelle du bot
        await self.bot.close()

# Fonction pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(RebootCommand(bot))