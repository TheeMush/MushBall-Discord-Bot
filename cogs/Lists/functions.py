from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://testbot:testbot123@testbot.78blp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
roles = cluster["discord"]["account"]

#~~~~~~~~~~FUNCTIONS~~~~~~~~~~#
async def open_account(ctx,user):
    check = roles.find({})
    serverlist = []
    for x in check:
        serverlist.append(x.get('_id'))

    if ctx.guild.id in serverlist:
        yon = True

    else:
        yon = False

    if yon == False:
        newshop = {"_id" : ctx.guild.id}
        roles.insert_one(newshop)
        newrolelist = {'wallet':'** **', 'bank':"** **"}
        roles.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newrolelist}})

    lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
    namelist = []
    for x in lol:
        for y in x['userAccounts']:
            name = list(y.items())[0][1]
            namelist.append(name)
    if user in namelist:
        return
    else:
        newaccountlist = {'id':user,'wallet': 100, 'bank':100}
        roles.update({'_id': ctx.guild.id}, {'$push': {'userAccounts': newaccountlist}})

async def update_bank(ctx,user,change = 0,change2 = 0):
    await open_account(ctx,user)

    lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
    for x in lol:
        for y in x['userAccounts']:
            if y["wallet"] == '** **':
                continue
            if y["id"] == user:
                change = int(y["wallet"])+int(change)                    
                change2 = int(y["bank"])+int(change2)                    
                roles.update_one({ "_id": ctx.guild.id, "userAccounts.id": user }, { "$set": { "userAccounts.$.wallet": change, "userAccounts.$.bank": change2 } })
                bal = [y["wallet"],y["bank"]]
                return bal

async def update_luck(ctx,user,change = 0):
    await update_bank(ctx,user,0,0)

    lol = roles.find({'_id': ctx.guild.id},{'userAccounts'})
    for x in lol:
        for y in x['userAccounts']:
            if y["wallet"] == '** **':
                continue
            if y["id"] == user:
                try:
                    if y["luck"] < 10:
                        roles.update_one({ "_id": ctx.guild.id, "userAccounts.id": user }, { "$set": { "userAccounts.$.luck": 100} })
                        luck = 100
                        return luck
                    if y["luck"] > 100:
                        if user == 569792736367083560:
                            luck = 10000
                            return luck
                        roles.update_one({ "_id": ctx.guild.id, "userAccounts.id": user }, { "$set": { "userAccounts.$.luck": 100} })
                        luck = 100
                        return luck

                    change = int(y["luck"])+int(change) 
                    roles.update_one({ "_id": ctx.guild.id, "userAccounts.id": user }, { "$set": { "userAccounts.$.luck": change} })
                    luck = y["luck"]
                    return luck
                except KeyError:
                    roles.update_one({ "_id": ctx.guild.id, "userAccounts.id": user }, { "$set": { "userAccounts.$.luck": 100} })
                    luck = 100
                    return luck


    #~~~~~~~~~~FUNCTIONS~~~~~~~~~~#