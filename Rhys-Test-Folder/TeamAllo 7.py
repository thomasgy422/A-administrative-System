students = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen"]
ListOfGroups = [["One", "Two", "Three", "Four","Five"],["Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen"]]
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
ListOfTeams = [[] for i in range(NumOfTeams)]
print(ListOfTeams)

#Creates the dictionary of teams - Team Name : Members
ZipObj = zip(ListOfKeys, ListOfTeams)
DictOfTeams = dict(ZipObj)
print(DictOfTeams)

#Allocator
SoFar = 0
for group in ListOfGroups:
    GroupCounter = 0
    while GroupCounter <= len(group):
        for k, Key in enumerate(DictOfTeams):
            if GroupCounter == len(group):
                GroupCounter = GroupCounter + 1
                SoFar = k
                break
            elif k == 0 and SoFar == len(DictOfTeams):
                SoFar = 0
                DictOfTeams[Key].append(group[GroupCounter])
                GroupCounter = GroupCounter + 1
                SoFar = SoFar + 1
            elif k != SoFar:
                continue
            else:
                DictOfTeams[Key].append(group[GroupCounter])
                GroupCounter = GroupCounter + 1
                SoFar = SoFar + 1

print(DictOfTeams)

for team in DictOfTeams:
    print(team, DictOfTeams[team])

for team in DictOfTeams.keys():
    print(team)


