#!/bin/python3.11

import discord
from discord.ui import View, Button
from collections import defaultdict

raid_responses = defaultdict(lambda: {"✅": [], "❔": [], "❌": []})

class RaidView(View):
    def __init__(self, raid_id):
        super().__init__(timeout=None)
        self.raid_id = raid_id

    async def update_embed(self, interaction):
        embed = interaction.message.embeds[0]
        status = raid_responses[self.raid_id]

        desc = f"**✅ Acceptés ({len(status['✅'])})**\n" + "\n".join(status['✅']) if status['✅'] else "**✅ Acceptés (0)**\n"
        desc += f"\n\n**❔ Indécis ({len(status['❔'])})**\n" + "\n".join(status['❔']) if status['❔'] else "\n\n**❔ Indécis (0)**\n"
        desc += f"\n\n**❌ Refusés ({len(status['❌'])})**\n" + "\n".join(status['❌']) if status['❌'] else "\n\n**❌ Refusés (0)**\n"

        embed.description = desc
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Accepter", style=discord.ButtonStyle.success, emoji="✅")
    async def accept(self, interaction: discord.Interaction, button: Button):
        user = interaction.user.display_name
        for lst in raid_responses[self.raid_id].values():
            if user in lst:
                lst.remove(user)
        raid_responses[self.raid_id]["✅"].append(user)
        await self.update_embed(interaction)

    @discord.ui.button(label="Peut-être", style=discord.ButtonStyle.primary, emoji="❔")
    async def maybe(self, interaction: discord.Interaction, button: Button):
        user = interaction.user.display_name
        for lst in raid_responses[self.raid_id].values():
            if user in lst:
                lst.remove(user)
        raid_responses[self.raid_id]["❔"].append(user)
        await self.update_embed(interaction)

    @discord.ui.button(label="Refuser", style=discord.ButtonStyle.danger, emoji="❌")
    async def decline(self, interaction: discord.Interaction, button: Button):
        user = interaction.user.display_name
        for lst in raid_responses[self.raid_id].values():
            if user in lst:
                lst.remove(user)
        raid_responses[self.raid_id]["❌"].append(user)
        await self.update_embed(interaction)

def create_raid_embed(title: str, date: str, hour: str, creator: str) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description="Aucun inscrit pour le moment.",
        color=discord.Color.dark_gold()
    )
    embed.add_field(name="📅 Date", value=date, inline=True)
    embed.add_field(name="🕘 Heure", value=hour, inline=True)
    embed.set_footer(text=f"Créé par {creator}")
    return embed
