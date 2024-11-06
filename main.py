import discord
from discord.ext import commands
import os
import webserver

# Token aus Replit Secrets
TOKEN = os.environ['discordkey']

# Erstelle eine neue Instanz des Bot-Clients mit den erforderlichen Intents
intents = discord.Intents.default()
intents.message_content = True # Aktivieren der Absicht, den Inhalt der Nachricht zu lesen
intents.reactions = True # Intents für Reaktionen aktivieren
intents.guilds = True # Intents für Gildenereignisse
intents.members = True # Intents für Mitgliederereignisse
bot = commands.Bot(command_prefix='!', intents=intents)

# Die ID des Channels, in den die Regeln gesendet werden sollen
RULES_CHANNEL_ID = 1206043949366644736
# Die ID der Rolle, die benötigt wird, um den !rules Befehl zu benutzen
REQUIRED_ROLE_ID = 1206039496702038016
# Die ID der Rolle, die der Benutzer erhält, wenn er die Regeln akzeptiert
ACCEPT_RULES_ROLE_ID = 1206047472787660881

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')
    # Setze den Status des Bots
    await bot.change_presence(activity=discord.Streaming(name="MrCraft777 auf Twitch", url="https://www.twitch.tv/mrcraft777_live"))

@bot.command()
async def rules(ctx):
    # Überprüfen, ob der Befehl in einem Server-Channel ausgeführt wird
    if ctx.guild:
        # Überprüfen, ob der Benutzer die erforderliche Rolle hat
        if discord.utils.get(ctx.author.roles, id=REQUIRED_ROLE_ID):
            # Hole den Channel, in den die Regeln gesendet werden sollen
            channel = bot.get_channel(RULES_CHANNEL_ID)
            if channel:
                # Erstelle die Einbettung für die Regeln
                rules_embed = discord.Embed(
                    title="Regelwerk",
                    description=(
                        "**[1] Allgemein**\n"
                        "Spam, Beleidigungen, Drohungen, Provokationen jeglicher Art gegen Nutzer ist verboten.\n\n"
                        "**[2] Rassismus**\n"
                        "Jegliche Form von rassistischen, homophoben oder heterosexistischen Äußerungen, Hassreden oder Diskriminierungen sind auf diesem Server strengstens untersagt.\n\n"
                        "**[3] Pornografische Inhalte**\n"
                        "Pornografische Inhalte wie Links, Bilder, Äußerungen etc. sind verboten.\n\n"
                        "**[4] Werbung**\n"
                        "Eigenwerbung für andere Discord Server, Websites oder Produkte ist untersagt, es sei denn, es wird ausdrücklich erlaubt.\n\n"
                        "**[5] Ausnutzen des Teams**\n"
                        "Das unnötige Erstellen von Support-Tickets oder Anpingen von Teammitgliedern ist verboten.\n\n"
                        "**[6] Phishing**\n"
                        "Jegliche Aktivitäten, die darauf abzielen, Benutzerkonten zu stehlen, persönliche Informationen abzufangen oder betrügerische Handlungen durchzuführen, sind strengstens untersagt."
                    ),
                    color=0x25cffe # Randfarbe: #25cffe
                )
                rules_embed.set_footer(text="Craftportal 2024\nWir behalten uns das Recht vor, das Regelwerk jederzeit ändern zu können.")

                # Sende die erste Einbettung (Regeln)
                await channel.send(embed=rules_embed)

                # Erstelle die zweite Einbettung (Bestätigung)
                confirmation_embed = discord.Embed(
                    description="Bitte klicke auf ☑️, um zu bestätigen, dass du das Regelwerk gelesen und akzeptiert hast.",
                    color=0x25cffe # Randfarbe: #25cffe
                )

                # Sende die zweite Einbettung (Bestätigung)
                message = await channel.send(embed=confirmation_embed)

                # Füge die Reaktion hinzu, um auf den Klick zu warten
                await message.add_reaction("☑️")
            else:
                await ctx.send("Rules channel not found.")
        else:
            await ctx.send("You do not have the required role to use this command.")
    else:
        await ctx.send("This command can only be used in a server.")

@bot.event
async def on_raw_reaction_add(payload):
    # Überprüfen, ob die Reaktion im richtigen Kanal hinzugefügt wurde
    if payload.channel_id == RULES_CHANNEL_ID and str(payload.emoji) == "☑️":
        guild = bot.get_guild(payload.guild_id) # Die Gilde holen
        member = guild.get_member(payload.user_id) # Das Mitglied holen

        # Überprüfen, ob der Benutzer die Rolle noch nicht hat und kein Bot ist
        if member and not member.bot:
            role = guild.get_role(ACCEPT_RULES_ROLE_ID) # Die Rolle holen, die hinzugefügt werden soll
            if role:
                await member.add_roles(role) # Rolle hinzufügen
                try:
                    # Nachricht an den Benutzer, dass die Rolle hinzugefügt wurde
                    await member.send("Du hast die Regeln akzeptiert, und die Rolle wurde dir zugewiesen.")
                except discord.Forbidden:
                    # Falls die Nachricht nicht gesendet werden kann (DMs sind geschlossen)
                    print(f"Could not send DM to {member}.")
            else:
                print("Role not found.")
        else:
            print("Member not found or is a bot.")

# Channel-Name aktualisieren, wenn ein neues Mitglied dem Server beitritt
@bot.event
async def on_member_join(member):
    guild = member.guild # Erhalte die Gilde (Server), wo das Mitglied gejoined ist
    channel = guild.get_channel(1280068643903766609) # Ersetze mit deiner Channel-ID

    if channel:
        try:
            # Aktualisiere den Channel-Namen mit der aktuellen Mitgliederanzahl
            new_name = f"📱・𝑴𝑰𝑻𝑮𝑳𝑰𝑫𝑬𝑹: {guild.member_count}"
            await channel.edit(name=new_name)
            print(f'Channel-Name auf "{new_name}" aktualisiert.')
        except Exception as e:
            print(f'Fehler beim Aktualisieren des Channel-Namens: {e}')
    else:
        print(f'Channel mit der ID 1280068643903766609 wurde nicht gefunden.')

webserver.keep_alive()
# Starte den Bot mit dem Token aus Replit Secrets
bot.run(TOKEN)
