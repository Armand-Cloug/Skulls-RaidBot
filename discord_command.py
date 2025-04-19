#!/bin/python3.11

import discord
import os
from discord.ext import commands
from discord import app_commands
from discord import Interaction
from discord_embeb import create_raid_embed, RaidView

# Pour passer le bot_client dans les scrapers
from main import bot_client

role_admin="Officer" 

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

class RaidCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="raid", description="📅 Planifie un raid avec embed interactif.")
    @app_commands.describe(
        titre="Titre du raid",
        date="Date du raid (ex: 22 avril 2025)",
        heure="Heure du raid (ex: 20:45)"
    )
    async def raid(self, ctx: commands.Context, titre: str, date: str, heure: str):
        raid_id = f"{ctx.message.id if ctx.message else ctx.interaction.id}"

        embed = create_raid_embed(titre, date, heure, ctx.author.display_name)
        view = RaidView(raid_id)

        await ctx.send(embed=embed, view=view)


# Fonction pour enregistrer le cog
async def setup(bot):
    await bot.add_cog(RebootCommand(bot))
    await bot.add_cog(RaidCommands(bot))