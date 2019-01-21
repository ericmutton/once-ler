import discord
import asyncio
import json

#read and load configuration file data
with open("config.json") as config:
    data = json.loads(config.read())
    token = data["token"]

onceler = discord.Client()

@onceler.event
async def on_ready():
    print(f"logged in as {onceler.user}")

@onceler.event
async def on_guild_join(joined_guild):
    reason = "to enable once-ler's #once channel feature"
    seed_role = discord.utils.get(joined_guild.roles, name="Truffula Seed")
    if seed_role is None: #check for lack of "Truffula Seed" role
        seed_role = await joined_guild.create_role(name="Truffula Seed", reason=reason) #create "Truffula Seed" role
        await seed_role.edit(position=1) #set precidence of "Truffula Seed" role to be directly above "@everyone" role
        #add "Truffula Seed" role to every current member
        for member in joined_guild.members:
            await member.add_roles(seed_role)
            print(f"the Once-ler gave {member} one truffula seed")
    default_role = joined_guild.default_role #"@everyone" role
    overwrites = {
        default_role: discord.PermissionOverwrite(send_messages=False),
        seed_role: discord.PermissionOverwrite(send_messages=True)
        }
    if discord.utils.get(joined_guild.channels, name="once") is None: #check for lack of "#once" text channel
        await joined_guild.create_text_channel(name="once", overwrites=overwrites, reason=reason) #create "#once" text channel

@onceler.event
async def on_member_join(member):
    #add Truffula Seed role to every new member
    role = discord.utils.get(member.guild.roles, name="Truffula Seed")
    if role is not None: #check for existence of "Truffula Seed" role
        await member.add_roles(role)
        print(f"the Once-ler gave {member} one truffula seed")

@onceler.event
async def on_message(message):
    #remove Truffula Seed role from any member who writes in "#once"
    if message.channel.name == "once":
        author = message.author
        role = discord.utils.get(author.guild.roles, name="Truffula Seed")
        if role is not None: #check for existence of "Truffula Seed" role
            await author.remove_roles(role)
            print(f"{author} planted their truffula seed")

onceler.run(token)
