students = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]

ListOfGroups = [["One", "Two", "Three", "Four","Five"],["Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]]
TeamHold = []
ListOfTeams = []

#Size of teams and number of teams needed - TeamSize needs to be input
TeamSize = 3
NumOfTeams = (len(students)//TeamSize)
print(NumOfTeams)

#Creates the correct number of teams (list elements) in ListOfTeams
for x in range(0,NumOfTeams):
    ListOfTeams.append(TeamHold)
print(ListOfTeams)

#Team Allocator
  
#Isolates each group in ListOfTeams
for group in ListOfGroups:
    print(group)

    for team in ListOfTeams:     
        print(team)
        for student in group:
            print(student)
            team.append(student)


#Isolates each team in ListOfTeams
#for team in ListOfTeams:
#    print(team)

#i = 0 
#while i <= NumOfTeams:
#    for group in ListOfGroups:
#        #for student in group: 
#        TeamHold.append(group[i])           
#        i = i + 1

