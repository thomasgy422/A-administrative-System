students = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]

ListOfGroups = [["One", "Two", "Three", "Four","Five"],["Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]]
TeamHold = []
ListOfTeams = []
ListOfKeys = []

#Size of teams and number of teams needed - TeamSize needs to be input
TeamSize = 3
NumOfTeams = (len(students)//TeamSize)
print(NumOfTeams)

#Creates the a list of key names for the dictionary, e.g. "Team 1" (Need to add +1 to NumOfTeams as not going from index 0 anymore)
for i in range(1,NumOfTeams+1):
    TeamName = "Team " + str(i)
    ListOfKeys.append(TeamName)
print(ListOfKeys)

#Creates the correct number of teams (list elements) in ListOfTeams
#for x in range(0,NumOfTeams):
#    ListOfTeams.append(TeamHold)

ListOfTeams = [[] for i in range(NumOfTeams)]

print(ListOfTeams)

#Creates the dictionary of teams - Team Name : Members
ZipObj = zip(ListOfKeys, ListOfTeams)
DictOfTeams = dict(ZipObj)
print(DictOfTeams)

#How to add members to teams
#DictOfTeams["Team 1"].append("Dave")
#print(DictOfTeams["Team 1"])

#i represents team x
#for i in DictOfTeams:
#    print(i)

#for group in ListOfGroups:
#    for Key in DictOfTeams:
#        for student in group:
#            DictOfTeams[Key].append(student)
#            break

#for group in ListOfGroups:
#    GroupCounter = 0
#    while GroupCounter <= len(group):
#        for Key in DictOfTeams:
#            if GroupCounter == len(group):
#                GroupCounter = GroupCounter + 1
#                break
#            else:
#                DictOfTeams[Key].append(group[GroupCounter])
#                GroupCounter = GroupCounter + 1

#for group in ListOfGroups:
#    GroupCounter = 0
#    while GroupCounter <= len(group):
#        for k, Key in enumerate(DictOfTeams):        
#            if GroupCounter == len(group):
#               GroupCounter = GroupCounter + 1
#                break
#            else:
#                DictOfTeams[Key].append(group[GroupCounter])
#                GroupCounter = GroupCounter + 1
    
#    DictCounter = 0
#    while DictCounter <= len(DictOfTeams):
#        if DictCounter == NumOfTeams-1:
#            DictCounter = 0
#        else:
            
#            DictCounter = DictCounter + 1

#for group in ListOfGroups:
#    GroupCounter = 0
#    while GroupCounter <= len(group):
#        if GroupCounter == len(group):
#            GroupCounter = GroupCounter + 1
#        else:
#            for k, Key in enumerate(DictOfTeams):             
#                DictOfTeams[Key].append(group[GroupCounter])
#                GroupCounter = GroupCounter + 1
#                if GroupCounter == len(group):
#                    break


print(DictOfTeams)
