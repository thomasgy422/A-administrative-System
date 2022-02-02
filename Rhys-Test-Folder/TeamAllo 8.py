students = ["21","23","25","27","31","24","28","29","22","26","30","32"]
#Converts received size variable from string to int
size = 4
#Calculates the number of teams needed based off students in database and the inputted size selection
NumOfTeams = (len(students))//size
#Initialises lists
ListOfTeams = []
ListOfKeys = []

PreListOfGroups =[["21","23","25","27","31"],["24","28"],["29"],[],["22"],["26","30","32"]]
ListOfGroups = [x for x in PreListOfGroups if x != []]

for i in range(1, NumOfTeams+1):
    TeamName = "Team " + str(i)
    ListOfKeys.append(TeamName)
#Creates the correct number of teams (list elements) in ListOfTeams
ListOfTeams = [[] for i in range(NumOfTeams)]
#Creates the dictionary of teams - Team Name : Members
ZipObj = zip(ListOfKeys, ListOfTeams)
DictOfTeams = dict(ZipObj)
#Team Allocator
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

for team in DictOfTeams:
    print(team, DictOfTeams[team])
