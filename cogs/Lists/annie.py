import discord
import os
import random
import requests
from bs4 import BeautifulSoup
from discord.ext import commands


embed=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed.add_field(name=f"The resurrection fern can last at least 100 years without water.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed2=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed2.add_field(name=f"Mimosa pudica, or sensitive plant, folds up when touched.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed3=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832721290052894740/image0.jpg")
embed3.add_field(name=f"Ophrys apifera, or the bee orchid, mimics female bees and emits pheromones to attract male bees for pollination.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed4=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed4.add_field(name=f"Types of berries (botanical term) include bananas, cucumbers, tomatoes and grapes.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed5=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed5.add_field(name=f"Pumpkins, zucchini, and acorn squash are all the same species, Cucurbita pepo.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed6=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed6.add_field(name=f"Spanish Moss,  Tillandsia usneoides, is neither spanish, nor moss. It belongs to the Bromeliads, or Pineapple family.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed7=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed7.add_field(name=f"Passiflora mixta, is a passion fruit flower that is long and tubular. It has coevolved with the sword-billed hummingbird, which has the longest bill in comparison to body in the world.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed8=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed8.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832721013199339520/image0.jpg")
embed8.add_field(name=f"Sunflowers, like others in the Aster family, have two types of flowers. There’s a ray floret and disc floret.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed9=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed9.add_field(name=f"A vegetable is a culinary term, everything you know is a lie.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed10=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed10.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832723033847496765/image0.jpg")
embed10.add_field(name=f"The scales you see on a dragonfruit are modified leaves of a Cactus.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed11=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed11.add_field(name=f"Cacti spines are modified leaves. The photosynthetic part of the cactus is a modified stem.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed12=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed12.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832723281239867433/image0.jpg")
embed12.add_field(name=f"Venus fly-traps are native to the Carolinas.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed13=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed13.add_field(name=f"Ferns are the second largest vascular plant group, and angiosperms (flowering plants) are the first.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed15=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed15.add_field(name=f"Ferns reproduce via spores, water aids in reproduction.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed16=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed16.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832724342030336040/image0.jpg")
embed16.add_field(name=f"The cinnamon fern, has dimorphic leaves—they have fertile fronds with spores on them, and infertile fronds.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed17=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed17.add_field(name=f"Palms can take up to 80 years to reach sexual maturity.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed19=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed19.add_field(name=f"The pineapple family is mostly epiphytic. This means they do not grow in soil, but rather on rocks or on trees.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed20=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed20.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832725433660473364/image0.jpg")
embed20.add_field(name=f"Wild bananas have large seeds.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed21=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed21.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832725738020274248/image0.jpg")
embed21.add_field(name=f"Leaves of three, leave them be. This is poison ivy.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed22=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed22.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832728485956157510/image0.jpg")
embed22.add_field(name=f"Euphorbia, in the Spurge family, underwent convergent evolution to look like cacti. Meaning, it evolved under a similar environment to cacti, and independently evolved similar physical appearances.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed24=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed24.add_field(name=f"The rose family has many fruits we eat. Raspberries, almonds, plums, pears, blackberries and peaches are all in the rose family!", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed25=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed25.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832729903089844285/image0.jpg")
embed25.add_field(name=f"Almonds are not a nut. They are a seed within the stone pit of its fruit (similar to peaches).", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed26=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed26.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832730377679929414/image0.jpg")
embed26.add_field(name=f"Avocado flowers are both male and female, otherwise called imperfect flowers.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed27=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed27.add_field(name=f"Brassica oleracea uncultuvated, is called wild cabbage. However, cultivation has created cabbage, broccoli, cauliflower, kale, brussel sprouts, collard greens and more.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed28=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed28.add_field(name=f"Hibiscus is in the same family as chocolate, or cacao.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed29=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed29.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832734489826033674/image0.jpg")
embed29.add_field(name=f"Spotted bee balm (picture) is in the mint family. Basil, rosemary and lavender are all found in the mint family as well!", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed30=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed30.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832735750121455616/image0.jpg")
embed30.add_field(name=f"Welwitschia mirabilis is found in the Namib desert. IT ONLY HAS TWO LARGE OPPOSITE LEAVES!!!!! They grow indefinitely and fold over.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed31=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed31.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832735219945177088/image0.jpg")
embed31.add_field(name=f"The ginkgo tree is dioecious, which means there’s a female tree and a male tree. The female seed produces an awful odor.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed32=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed32.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832736536314904586/image0.jpg")
embed32.add_field(name=f"Magnolias have primitive fruit. The red that you see are called “arils” which are a coating over the seeds to attract birds.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed33=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed33.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832737452513951744/image0.jpg")
embed33.add_field(name=f"The taro family, or Aroids have unique floral structures. there’s a spathe and spadix, which is unique to only this family.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed34=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed34.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832737934163050526/image0.webp")
embed34.add_field(name=f"Onions and garlic are in the same family. They are bulbs, which is a stem that grows underground with modified leaves!", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 

embed35=discord.Embed(title="<a:eggplantpepe:832813974281912321>  Annie's Plant Facts  <a:eggplantpepe:832813974281912321>", color=0x01a500)
embed35.set_thumbnail(url="https://cdn.discordapp.com/attachments/785655928347295744/832738765541212217/image0.jpg")
embed35.add_field(name=f"The barbados cherry is not a cherry at all! It is in the family malpighiaceae and has very distinct flowers with clawed petals.", value="‎‎‎‎‎‎‎‎‎‎‎‎‎‎", inline=False) 


embedlist = [embed,embed2,embed3,embed4,embed5,embed6,embed7,embed8,embed9,embed10,embed11,embed12,	
             embed13,embed15,embed16,embed17,embed19,embed20,embed21,embed22,embed24,embed25,embed26,embed27,embed28,embed29,	
             embed30,embed31,embed32,embed33,embed34,embed35]
    
    