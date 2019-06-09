import discord
import random
import asyncio
import json
import os
import requests


TOKEN = 'PLS ADD UR ACCOUNT TOKEN'

Host = 'STE UR NAME IF U WANT (SHOWN ON THE END OF THE MESSAGES)' #just set ur name :P
sudo = [] # Bot Admins (ids) (DISVORD USER IDS OF BOT ADMINS)

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.lower().startswith("v!"):
        if message.content.lower().startswith("v!help"):
            page = message.content.replace("v!help ","")
            if page != "":
                try:
                    page = int(page)
                except:
                    page = 1
            else:
                page = 1
            
            channel = message.author
            
            # HELP PAGE ONE
            #page1.set_author(name="Author Name", url="https://nami-mc.site", icon_url="https://vignette.wikia.nocookie.net/darling-in-the-franxx/images/b/b3/Zero_Two_appearance.jpg")
            page1=discord.Embed(title="Help 1/1", url="https://ddragon.volibot.com/", description=" ", color=0x61686a)
            page1.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAfBdMvSPGEbeE5VeyQ3x1cI-HtGHoxaNcMg_EhE9056g8RYaK")
            page1.add_field(name="v!help <page number>", value="Sends u This help Page", inline=False)
            if message.author.id in sudo: 
                page1.add_field(name="v!stop",value="[ADMIN COMMAND] \n allowes the admin to stop the bot")
            
            page1.set_footer(text="Bot Powered by: "+str(Host))
            
            if page == 1:
                await channel.send(embed=page1)
            else:
                await channel.send("No Help Page with That Number")
            
            await message.add_reaction(emoji="✔")
            print("Sending Help to: "+message.author.name)
        
        elif message.content.lower() == 'v!stop' and message.author.id in sudo: #only stop if its an admin
            try:
                await message.delete()
            except:
                await message.channel.send("Cant Delete this ur message ! pls cleanup yourself if needed!")

            await client.logout()
        
        elif message.content.lower().startswith("v!champ "):
            champion = message.content.lower().replace("v!champ ","").replace(" ","") #first i want everything small
            champion = champion.capitalize()  # First letter getting big! 
            
            # Fix some champions here until i have a better method
            if champion.lower() == "missfortune":
                champion = "MissFortune"
            elif champion.lower() == "twistedfate":
                champion = "TwistedFate"
            elif champion.lower() == "xinzhao":
                champion = "XinZhao"
            elif champion.lower() == "masteryi":
                champion = "MasterYi"


            print(champion)
            if os.path.isfile("data/champion/"+champion+".json"):
                with open("data/champion/"+champion+".json","r") as champ:
                    data = json.load(champ)
                    data = data['data'] # short this little shit a bit

                    # create a webhook to send multiple embeds :3
                    
                    webhook_id = -1
                    webhooks = await message.channel.webhooks() # get existing webhhoks so i dont create 1000 webhooks (normally it should delete the one after use)
                    for hook in webhooks:
                        if hook.name == "Volibot Helper":
                            webhook = hook
                            webhook_id = hook.id

                    if webhook_id == -1:
                        with open("images/helper.jpg", "rb") as image:
                            f = image.read()
                        webhook = await message.channel.create_webhook(name="Volibot Helper",avatar=f ,reason="Volibot needs a small workaround to send multiple embeds(sry for that)")
                        webhook_id = webhook.id
                    


                    # now ... EMBED! 
                    embed=discord.Embed() # title="Title", description="Desciption"
                    embed.set_author(name=data[champion]['name'], icon_url="https://ddragon.volibot.com/cdn/4.20.2/img/champion/"+champion+".png")
                    embed.add_field(name=data[champion]['title'].capitalize() ,value="||  ||", inline=False)
                    
                    embed.add_field(name="=====================================================",value="||  ||", inline=False)
                    
                    taggs = ""
                    for tag in data[champion]['tags']:
                        taggs = taggs +"\n"+tag
                    if taggs == "":
                        taggs = "/////////////////"

                    embed.add_field(name="Type: ", value=taggs, inline=True)

                    embed.add_field(name="Partype: ", value=data[champion]['partype'], inline=True)
                    
                    embed.add_field(name="Attack: ", value=str(data[champion]['info']['attack']), inline=True)
                    
                    embed.add_field(name="Defense: ", value=str(data[champion]['info']['defense']), inline=True)
                    embed.add_field(name="Magic: ", value=str(data[champion]['info']['magic']), inline=True)
                    embed.add_field(name="Difficulty: ", value=str(data[champion]['info']['difficulty']), inline=True)
                    embed.add_field(name="=====================================================",value="||  ||", inline=False)
                    
                    skins = ""
                    for skin in data[champion]['skins']:
                        if skin['name'] == 'default':
                            skins = "Default"
                        else:
                            skins = skins +", " + skin['name']

                    embed.add_field(name="Skins: ", value=skins,inline=False)
                    
                    embed.add_field(name="=====================================================",value="||  ||", inline=False)
                    stats = data[champion]['stats']
                    embed.add_field(name="HP: ",value=str(stats['hp']), inline=True)
                    embed.add_field(name="Mana: ",value=str(stats['mp']), inline=True)
                    embed.add_field(name="HP Regen: ",value=str(stats['hpregen']), inline=True)
                    embed.add_field(name="Armor: ",value=str(stats['armor']), inline=True)
                    embed.add_field(name="Attackdamage: ",value=str(stats['attackdamage']), inline=True)
                    embed.add_field(name="Attackrange: ",value=str(stats['attackrange']), inline=True)
                    
                    
                    
                    embed.add_field(name="=====================================================",value="||  ||", inline=False)
                    
                    embed.add_field(name="Story: ", value=data[champion]['blurb'].replace("<br>",""), inline=False)

                    allytips = "" # just to prevent errors
                    for item in data[champion]['allytips']:
                        allytips = allytips +"\n"+ item

                    if allytips == "":
                        allytips = "/////////////////"

                    embed.add_field(name="Allytips: ", value=allytips, inline=False)

                    enemytips = "" # error prevention too
                    for item in data[champion]['enemytips']:
                        enemytips = enemytips +"\n"+item
                    
                    if enemytips == "":
                        enemytips = "/////////////////"

                    embed.add_field(name="Enemytips: ", value=enemytips, inline=False)
                    
                    embed.add_field(name="=====================================================",value="||  ||", inline=False)
                    
                    embed.set_footer(text="Bot Powered by: "+Host)

                    await webhook.send(embed=embed)
                    #await message.channel.send(embed=embed)

                    #now ... EMBED! 
                    embed2=discord.Embed() # title="Title", description="Desciption"
                    embed2.set_author(name=data[champion]['name'], icon_url="https://ddragon.volibot.com/cdn/4.20.2/img/champion/"+champion+".png")
                    embed2.add_field(name=data[champion]['title'].capitalize() ,value="||  ||", inline=False)
                    
                    embed2.add_field(name="=====================================================",value="||  ||", inline=False)
                    
                    spells = ""
                    all_spells = data[champion]["spells"]
                    for spell in all_spells:
                        spells = spells +", "+spell['name']
                    
                    embed2.add_field(name="Spells:",value=spells[1:],inline=False) #[1:] cuts off the first character (here ",")
                    embed2.add_field(name="**Q** ("+data[champion]["spells"][0]['name'].capitalize()+"): ", value="||  ||", inline=False)
                    embed2.add_field(name="Basics:", value="Maxrank: "+str(all_spells[0]['maxrank'])+"\n" +"Cooldown: "+all_spells[0]['cooldownBurn']+"\n" +"Cost: "+all_spells[0]['costBurn'], inline=True)
                    embed2.add_field(name="Description:", value=data[champion]['spells'][0]['description'], inline=True)
                    
                    embed2.add_field(name="**W** ("+data[champion]["spells"][1]['name'].capitalize()+"): ", value="||  ||", inline=False)
                    embed2.add_field(name="Basics:", value="Maxrank: "+str(all_spells[1]['maxrank'])+"\n" +"Cooldown: "+all_spells[1]['cooldownBurn']+"\n" +"Cost: "+all_spells[1]['costBurn'], inline=True)
                    embed2.add_field(name="Description:", value=data[champion]['spells'][1]['description'], inline=True)
                    
                    embed2.add_field(name="**E** ("+data[champion]["spells"][2]['name'].capitalize()+"): ", value="||  ||", inline=False)
                    embed2.add_field(name="Basics:", value="Maxrank: "+str(all_spells[2]['maxrank'])+"\n" +"Cooldown: "+all_spells[2]['cooldownBurn']+"\n" +"Cost: "+all_spells[2]['costBurn'], inline=True)
                    embed2.add_field(name="Description:", value=data[champion]['spells'][2]['description'], inline=True)
                    
                    embed2.add_field(name="**R** ("+data[champion]["spells"][3]['name'].capitalize()+"): ", value="||  ||", inline=False)
                    embed2.add_field(name="Basics:", value="Maxrank: "+str(all_spells[3]['maxrank'])+"\n" +"Cooldown: "+all_spells[3]['cooldownBurn']+"\n" +"Cost: "+all_spells[3]['costBurn'], inline=True)
                    embed2.add_field(name="Description:", value=data[champion]['spells'][3]['description'], inline=True)
                    
                    embed2.add_field(name="=====================================================",value="||  ||", inline=False)

                    await webhook.send(embed=embed2)

            else:
                await message.channel.send("This Champions Does not Exist :o")

            

        

@client.event
async def on_ready():
    print("========================")
    print('Online as')
    print(client.user.name)
    await client.change_presence(activity=discord.Activity(name='use v!help')) #game=discord.Game(name="")
    print("========================")

client.run(TOKEN)