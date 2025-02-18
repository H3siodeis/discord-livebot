import discord
import os
from discord.ext import commands

import sys

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
LIVE_URL = "https://www.tiktok.com/@zyrom71/live"
live_message_id = os.getenv("LIVE_MESSAGE_ID")
mention_message_id = None

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} est connecté!", flush=True)
    sys.stdout.flush()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message reçu : {message.content}", flush=True)
    sys.stdout.flush()
    await bot.process_commands(message)


@bot.command()
async def test_channel(ctx):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await ctx.send(f"✅ Le bot a bien trouvé le salon : {channel.name}")
    else:
        await ctx.send(f"❌ Erreur : Le bot ne trouve pas le salon ! Vérifie l'ID ({CHANNEL_ID}).")


@bot.command()
async def live_on(ctx):
    """Commande pour annoncer un live avec un beau message"""
    global live_message_id, mention_message_id
    channel = bot.get_channel(CHANNEL_ID)

    # Vérification des permissions
    if not channel.permissions_for(channel.guild.me).embed_links:
        await ctx.send(
            "🚨 **Erreur** : Le bot n'a pas la permission d'intégrer des liens (Embed Links) dans ce salon."
        )
        return

    # Création de l'embed stylé
    embed = discord.Embed(
        title="🎥 **LIVE EN DIRECT !**",
        description=f"🔗 [Regarder le live ici !]({LIVE_URL})",
        color=discord.Color.green())
    embed.set_thumbnail(
        url=
        "https://cdn.discordapp.com/attachments/1341153573030989964/1341176524316872766/tiktok.png?ex=67b50b79&is=67b3b9f9&hm=2351e72869e127f50040165782757eb96aec7d6bb065469cc531c06abbff11a3&"
    )
    embed.set_footer(text="Rejoignez-nous pour un moment épique ! 🚀")
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1341153573030989964/1341175313874292848/zyrom.jpeg?ex=67b50a58&is=67b3b8d8&hm=f43b6f2a621b8123d475e9f7d16843e5dd75810f9e137d42f0c94d71152ecab1&"
    )

    # Modifier le message existant ou en créer un nouveau
    if live_message_id:
        try:
            msg = await channel.fetch_message(live_message_id)
            await msg.edit(embed=embed)
            print("✅ Message existant modifié.")
        except discord.NotFound:
            print("❌ Message introuvable, envoi d'un nouveau.")
            msg = await channel.send(embed=embed)
            live_message_id = msg.id
    else:
        msg = await channel.send(embed=embed)
        live_message_id = msg.id

    # Supprimer l'ancienne notification @everyone et en envoyer une nouvelle
    if mention_message_id:
        try:
            mention_msg = await channel.fetch_message(mention_message_id)
            await mention_msg.delete()
        except discord.NotFound:
            pass  # Si le message @everyone est déjà supprimé, on l'ignore

    mention_msg = await channel.send(
        "@everyone 🚨 **Le live commence maintenant !** 🔥 Venez nous rejoindre !"
    )
    mention_message_id = mention_msg.id


@bot.command()
async def live_off(ctx):
    """Commande pour signaler la fin du live et supprimer la notification"""
    global live_message_id, mention_message_id
    channel = bot.get_channel(CHANNEL_ID)

    # Création de l'embed pour la fin du live
    embed = discord.Embed(title="❌ **LIVE TERMINÉ**",
                          description="Merci à tous d'avoir participé ! 🙌",
                          color=discord.Color.red())
    embed.set_thumbnail(
        url=
        "https://cdn.discordapp.com/attachments/1341153573030989964/1341176524316872766/tiktok.png?ex=67b50b79&is=67b3b9f9&hm=2351e72869e127f50040165782757eb96aec7d6bb065469cc531c06abbff11a3&"
    )
    embed.set_footer(text="On se retrouve très bientôt pour un nouveau live !")
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1341153573030989964/1341175313874292848/zyrom.jpeg?ex=67b50a58&is=67b3b8d8&hm=f43b6f2a621b8123d475e9f7d16843e5dd75810f9e137d42f0c94d71152ecab1&"
    )

    # Modifier le message existant au lieu d'en recréer un
    if live_message_id:
        try:
            msg = await channel.fetch_message(live_message_id)
            await msg.edit(embed=embed)
            print("✅ Message existant modifié en 'LIVE TERMINÉ'.")
        except discord.NotFound:
            print("❌ Message introuvable, envoi d'un nouveau.")
            msg = await channel.send(embed=embed)
            live_message_id = msg.id
    else:
        msg = await channel.send(embed=embed)
        live_message_id = msg.id

    # Suppression de la notification @everyone
    if mention_message_id:
        try:
            mention_msg = await channel.fetch_message(mention_message_id)
            await mention_msg.delete()
            mention_message_id = None
            print("✅ Notification @everyone supprimée.")
        except discord.NotFound:
            print("❌ Notification @everyone introuvable.")

from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=8000)

# Lancer le serveur Web en parallèle du bot
Thread(target=run_web).start()


bot.run(TOKEN)
