import os
import operator

def createpage(server_name, user_data):
    # Will parse template files and do stringreplaces for data.
    # List of expected placeholders:
    #{%server_name%}
    #{%playerssummary%}
    #{%username%}
    #{%totalloginformatted%}
    #{%totalkilled%}
    #{%totalassistedsuicides%}
    #{%totalsuicides%}
    #{%deathrows%}

    # Create the same variables with the same data:
    playerssummary = ''
    for playername in sorted(user_data.keys(), key=lambda x: x.lower()):
        totalloginformatted = user_data[playername]['totalloginformatted']
        if os.path.exists('../playerskins/'+playername+'.png'):
            playerpicture = '../playerskins/'+playername+'.png'
        else:
            if os.path.exists('../playerskins/'+playername+'.jpg'):
                playerpicture = '../playerskins/'+playername+'.jpg'
            else:
                playerpicture = '../playerskins/defaultplayer.png'
        killedby_num = 0
        if 'killedby' in user_data[playername]:
            amount = 0
            for num in user_data[playername]['killedby']:
                amount = user_data[playername]['killedby'][num]
                killedby_num += amount
        assisted_suicides_num = 0
        if 'assisted_suicides' in user_data[playername]:
            amount = 0
            for num in user_data[playername]['assisted_suicides']:
                amount = user_data[playername]['assisted_suicides'][num]
                assisted_suicides_num += amount
        suicides_num = 0
        if 'suicides' in user_data[playername]:
            amount = 0
            for num in user_data[playername]['suicides']:
                amount = user_data[playername]['suicides'][num]
                suicides_num += amount
        loggeddeaths_num = killedby_num + assisted_suicides_num + suicides_num
        playerssummary = playerssummary+'<tr><td valign=top align=left><a href="#'+playername+'"><strong>'+playername+'</strong></td><td valign=top align=left>'+totalloginformatted+'</td><td valign=top align=left>'+str(loggeddeaths_num)+'</td><td valign=top align=left><img src="'+playerpicture+'" alt="'+playername+'s avatar"></td></tr>'

    #generate the per user part
    userparts = ''
    fusers = open('../templates/userpart.html','r')
    userpart_template = fusers.read()
    fusers.close()
    for playername in sorted(user_data.keys(), key=lambda x: x.lower()):
        working_userpart = userpart_template
        totalloginformatted = user_data[playername]['totalloginformatted']
        if os.path.exists('../playerskins/'+playername+'.png'):
            playerpicture = '../playerskins/'+playername+'.png'
        else:
            if os.path.exists('../playerskins/'+playername+'.jpg'):
                playerpicture = '../playerskins/'+playername+'.jpg'
            else:
                playerpicture = '../playerskins/defaultplayer.png'
        working_userpart = working_userpart.replace('{%playerpicture%}', playerpicture)
        killedby_num = 0
        if 'killedby' in user_data[playername]:
            amount = 0
            for num in user_data[playername]['killedby']:
                amount = user_data[playername]['killedby'][num]
                killedby_num += amount
        working_userpart = working_userpart.replace('{%totalkilled%}', str(killedby_num))
        assisted_suicides_num = 0
        if 'assisted_suicides' in user_data[playername]:
            amount = 0
            for num in user_data[playername]['assisted_suicides']:
                amount = user_data[playername]['assisted_suicides'][num]
                assisted_suicides_num += amount
        working_userpart = working_userpart.replace('{%totalassistedsuicides%}', str(assisted_suicides_num))
        suicides_num = 0
        if 'suicides' in user_data[playername]:
            amount = 0
            for num in user_data[playername]['suicides']:
                amount = user_data[playername]['suicides'][num]
                suicides_num += amount
        working_userpart = working_userpart.replace('{%totalsuicides%}', str(suicides_num))
        loggeddeaths_num = killedby_num + assisted_suicides_num + suicides_num
        working_userpart = working_userpart.replace('{%totaldeaths%}', str(loggeddeaths_num))
        working_userpart = working_userpart.replace('{%totalloginformatted%}', str(totalloginformatted))
        working_userpart = working_userpart.replace('{%username%}', str(playername))
        #Deaths breakdown
        deathrows = ''
        #Killedby
        deathrow = '<tr><td><strong>Killer:</strong></td><td><strong>Times:</strong></td><td><strong>Mugshot:</strong></td></tr>'
        if 'killedby'in user_data[playername]:
            killer_num=0
            for killer in sorted(user_data[playername]['killedby'].items(), key=lambda x: x[1], reverse=True):
                killer = killer[0]
                if killer == 'entity.DartCraft.entityAngryEnderman.name':
                    killerfriendly = 'Enderman'
                else:
                    if killer == 'entity.enderTot.name':
                        killerfriendly= 'Endertot'
                    else:
                        killerfriendly = killer
                #mugshots!
                if os.path.exists('../images/'+killer+'.png'):
                    mugshot = '../images/'+killer+'.png'
                else:
                    if os.path.exists('../images/'+killer+'.jpg'):
                        mugshot = '../images/'+killer+'.jpg'
                    else:
                        if os.path.exists('../playerskins/'+killer+'.png'):
                            mugshot = '../playerskins/'+killer+'.png'
                        else:
                            if os.path.exists('../playerskins/'+killer+'.jpg'):
                                mugshot = '../playerskins/'+killer+'.jpg'
                            else:
                                mugshot = '../images/monsters.jpg'
                if killer_num  == 0:
                    deathrow += '<tr><td title="Nemesis"><strong>'+killerfriendly+'</strong></td><td title="Nemesis"><strong>'+str(user_data[playername]['killedby'][killer])+'</strong></td><td><img src="'+mugshot+'" title="Nemesis"></tr>'
                else:
                    deathrow += '<tr><td>'+killerfriendly+'</td><td>'+str(user_data[playername]['killedby'][killer])+'</td><td><img src="'+mugshot+'" height="50" width="50"></tr>'
                killer_num += 1
            deathrows += deathrow
        #assisted suicides
        deathrow = '<tr><td title="Couldn\'t handle the stress of fighting:"><strong>Assisted suicides:</strong></td><td title="Couldn\'t handle the stress of fighting:"><strong>Times:</strong></td><td title="Couldn\'t handle the stress of fighting:"><strong>Mugshot:</strong></td></tr>'
        if 'assisted_suicides'in user_data[playername]:
            killer_num=0
            for killer in sorted(user_data[playername]['assisted_suicides'].items(), key=lambda x: x[1], reverse=True):
                killer = killer[0]
                splitkiller = killer.split('fighting ')
                killerfriendly = splitkiller[1]
                causefriendly = ''
                if splitkiller[0] == 'fell to death ':
                    causefriendly = 'Fell to death while fighting '
                else:
                    if splitkiller[0] == 'burnt to death ':
                        causefriendly = 'Burnt to death while fighting '
                    else:
                        causefriendly = splitkiller[0]+' while fighting '
                if killerfriendly == 'entity.DartCraft.entityAngryEnderman.name':
                    killerfriendly = 'Enderman'
                else:
                    if killerfriendly == 'entity.enderTot.name':
                        killerfriendly= 'Endertot'

                #mugshots!
                if os.path.exists('../images/'+killerfriendly+'.png'):
                    mugshot = '../images/'+killerfriendly+'.png'
                else:
                    if os.path.exists('../images/'+killerfriendly+'.jpg'):
                        mugshot = '../images/'+killerfriendly+'.jpg'
                    else:
                        if os.path.exists('../playerskins/'+killerfriendly+'.png'):
                            mugshot = '../playerskins/'+killerfriendly+'.png'
                        else:
                            if os.path.exists('../playerskins/'+killerfriendly+'.jpg'):
                                mugshot = '../playerskins/'+killerfriendly+'.jpg'
                            else:
                                mugshot = '../images/monsters.jpg'
                if killer_num  == 0:
                    deathrow += '<tr><td title="To stressfull!"><strong>'+causefriendly+killerfriendly+'</strong></td><td title="To stressfull!"><strong>'+str(user_data[playername]['assisted_suicides'][killer])+'</strong></td><td><img src="'+mugshot+'" title="To stressfull!"></tr>'
                else:
                    deathrow += '<tr><td title="To stressfull!">'+causefriendly+killerfriendly+'</td><td>'+str(user_data[playername]['assisted_suicides'][killer])+'</td><td><img src="'+mugshot+'" height="50" width="50"></tr>'
                killer_num += 1
            deathrows += deathrow
        #suicides
        deathrow = '<tr><td><strong>Emo suicides:</strong></td><td><strong>Times:</strong></td><td><strong>Foto:</strong></td></tr>'
        if 'suicides' in user_data[playername]:
            killer_num=0
            for killer in sorted(user_data[playername]['suicides'].items(), key=lambda x: x[1], reverse=True):
                killer = killer[0]
                if killer == "fallen to death":
                    killerfriendly = "Jumped from a high place"
                    killerfoto = "Fallen"
                else:
                    if killer == "drowned":
                        killerfriendly = "Went swimming and didn't come up for air"
                        killerfoto = "Drowned"
                    else:
                        if killer =="swum in lava":
                            killerfriendly = "Dove into lava to see the light"
                            killerfoto = "Lava"
                        else:
                            if killer == "burnt to death":
                                killerfriendly = "Jumped into the fire to feel the burn"
                                killerfoto = "Burnt"
                            else:
                                killerfriendly = "killer"
                                killerfoto = ''
                #fotos!
                if os.path.exists('../images/'+killerfoto+'.png'):
                    mugshot = '../images/'+killerfoto+'.png'
                else:
                    if os.path.exists('../images/'+killerfoto+'.jpg'):
                        mugshot = '../images/'+killerfoto+'.jpg'
                    else:
                        mugshot = '../images/monsters.jpg'
                if killer_num  == 0:
                    deathrow += '<tr><td title="Favorite way out..."><strong>'+killerfriendly+'</strong></td><td title="Favorite way out..."><strong>'+str(user_data[playername]['suicides'][killer])+'</strong></td><td><img src="'+mugshot+'" title="Favorite way out..."></tr>'
                else:
                    deathrow += '<tr><td>'+killerfriendly+'</td><td>'+str(user_data[playername]['suicides'][killer])+'</td><td><img src="'+mugshot+'" height="50" width="50"></tr>'
                killer_num += 1
            deathrows += deathrow
        working_userpart = working_userpart.replace('{%deathrows%}', deathrows)
        userparts += working_userpart

    f = open('../html/stats.html','w')
    fheader = open('../templates/header.html','r')
    fsummary = open('../templates/summary.html','r')
    ffooter = open('../templates/footer.html','r')

    generatedpage = fheader.read()+fsummary.read()+userparts+ffooter.read()
    generatedpage = generatedpage.replace('{%server_name%}', server_name)
    generatedpage = generatedpage.replace('{%playerssummary%}', playerssummary)
    f.write(generatedpage)
    #print user_data

    f.close()
    fheader.close()
    fsummary.close()
    ffooter.close()