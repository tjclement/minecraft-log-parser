import os
import operator

waystogodictionary = {
    'killedby':{
        'defaultpicture': '../images/monsters.jpg',
        'descriptions':{
            'entity.DartCraft.entityAngryEnderman.name': 'Ender',
            'entity.enderTot.name': 'Endertot'
        }
    },
    'assisted_suicides':{
        'defaultpicture': '../images/assisted_suicide.jpg',
        'descriptions':{
            'fell to death ': 'Fell to death while fighting ',
            'burnt to death ': 'Burnt to death while fighting '
        }
    },
    'suicides':{
        'defaultpicture': '../images/suicide.jpg',
        'descriptions': {
            'fallen to death': 'Jumped from a high place',
            'drowned': "Went swimming and didn't come up for air",
            "swum in lava": "Dove into lava to see the light",
            "burnt to death": "Jumped into the fire to feel the burn",
            "pricked to death": "Hugged something sharp"
        }
    }
}

def parsekiller(type, killerlog):
    killerdata = []
    killer = killerlog
    killerdescription = None
    killerpicture = None
    if type is 'assisted_suicides':
        splitkiller = killer.split('fighting ')
        discard = parsekiller('killedby',splitkiller[1])
        if splitkiller[0] in waystogodictionary[type]['descriptions']:
            killerdescription = waystogodictionary[type]['descriptions'][splitkiller[0]]+discard[0]
        else:
            killerdescription = killer
        killer = discard[0]
        if discard[1] is None:
            killerpicture = waystogodictionary[type]['defaultpicture']
        else:
            killerpicture = discard[1]
    else:
        if killer in waystogodictionary[type]['descriptions']:
            killerdescription = waystogodictionary[type]['descriptions'][killer]
            killerpicture = findpicture(killer)
        else:
            killerdescription = killer
            killerpicture = findpicture(killer)
        if killerpicture is None:
            killerpicture = waystogodictionary[type]['defaultpicture']
    killerdata = [killerdescription, killerpicture]
    return killerdata

def findpicture(entity):
    extensions = ['.png', '.PNG', '.jpg', '.JPG', '.gif', '.GIF']
    imagedirs = ['../playerskins/', '../images/']
    picture = None
    for directory in imagedirs:
        if picture is None:
            for extension in extensions:
                if os.path.exists(directory+entity.replace(' ', '_')+extension):
                    picture = (directory+entity.replace(' ', '_')+extension)
                    break
    return picture

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
        playerpicture = findpicture(playername)
        if playerpicture is None:
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
        playerssummary = playerssummary+'<tr><td valign=top align=left><a href="#'+playername+'"><strong>'+playername+'</strong></a></td><td valign=top align=left>'+totalloginformatted+'</td><td valign=top align=left>'+str(loggeddeaths_num)+'</td><td valign=top align=left><img src="'+playerpicture+'" alt="'+playername+'s avatar"></td></tr>'

    #generate the per user part
    userparts = ''
    fusers = open('../templates/userpart.html','r')
    userpart_template = fusers.read()
    fusers.close()
    for playername in sorted(user_data.keys(), key=lambda x: x.lower()):
        working_userpart = userpart_template
        totalloginformatted = user_data[playername]['totalloginformatted']
        playerpicture = findpicture(playername)
        if playerpicture is None:
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
                killerdata = parsekiller('killedby',killer[0])
                if killer_num  == 0:
                    deathrow += '<tr><td title="Nemesis"><strong>'+killerdata[0]+'</strong></td><td title="Nemesis"><strong>'+str(user_data[playername]['killedby'][killer[0]])+'</strong></td><td><img src="'+killerdata[1]+'" title="Nemesis"></tr>'
                else:
                    deathrow += '<tr><td>'+killerdata[0]+'</td><td>'+str(user_data[playername]['killedby'][killer[0]])+'</td><td><img src="'+killerdata[1]+'" height="50" width="50"></tr>'
                killer_num += 1
            deathrows += deathrow
        #assisted suicides
        deathrow = '<tr><td title="Couldn\'t handle the stress of fighting:"><strong>Assisted suicides:</strong></td><td title="Couldn\'t handle the stress of fighting:"><strong>Times:</strong></td><td title="Couldn\'t handle the stress of fighting:"><strong>Mugshot:</strong></td></tr>'
        if 'assisted_suicides'in user_data[playername]:
            killer_num=0
            for killer in sorted(user_data[playername]['assisted_suicides'].items(), key=lambda x: x[1], reverse=True):
                killer = killer[0]
                killerdata = parsekiller('assisted_suicides', killer)
                if killer_num  == 0:
                    deathrow += '<tr><td title="To stressfull!"><strong>'+killerdata[0]+'</strong></td><td title="To stressfull!"><strong>'+str(user_data[playername]['assisted_suicides'][killer])+'</strong></td><td><img src="'+killerdata[1]+'" title="To stressfull!"></tr>'
                else:
                    deathrow += '<tr><td title="To stressfull!">'+killerdata[0]+'</td><td>'+str(user_data[playername]['assisted_suicides'][killer])+'</td><td><img src="'+killerdata[1]+'" height="50" width="50"></tr>'
                killer_num += 1
            deathrows += deathrow
        #suicides
        deathrow = '<tr><td><strong>Emo suicides:</strong></td><td><strong>Times:</strong></td><td><strong>Foto:</strong></td></tr>'
        if 'suicides' in user_data[playername]:
            killer_num=0
            for killer in sorted(user_data[playername]['suicides'].items(), key=lambda x: x[1], reverse=True):
                killer = killer[0]
                killerdata = parsekiller('suicides', killer)
                if killer_num  == 0:
                    deathrow += '<tr><td title="Favorite way out..."><strong>'+killerdata[0]+'</strong></td><td title="Favorite way out..."><strong>'+str(user_data[playername]['suicides'][killer])+'</strong></td><td><img src="'+killerdata[1]+'" title="Favorite way out..."></tr>'
                else:
                    deathrow += '<tr><td>'+killerdata[0]+'</td><td>'+str(user_data[playername]['suicides'][killer])+'</td><td><img src="'+killerdata[1]+'" height="50" width="50"></tr>'
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

    f.close()
    fheader.close()
    fsummary.close()
    ffooter.close()