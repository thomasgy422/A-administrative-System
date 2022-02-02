students = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]

#def PriorityGroups():
#    ListOfGroups = []
#    #ListOfGroups = [["One","Two"],["Three", "Four"]] 
#    return ListOfGroups

ListOfGroups = [["One", "Two", "Three", "Four","Five"],["Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]]
TeamHold = []
ListOfTeams = []

#Size of teams and number of teams needed - TeamSize needs to be input
TeamSize = 3
NumOfTeams = (len(students)/TeamSize)
print(NumOfTeams)

#Team Allocator
i = 0 
while i <= NumOfTeams:
    for group in ListOfGroups:
        #for student in group: 
        TeamHold.append(group[i])           
        i = i + 1

print(TeamHold)
        
        #TeamHold.append(student)

ListOfTeams.append(TeamHold)
print(ListOfTeams)
    
    #for student in range(len(group)):
        #TeamHold.append(group[student]) 
        #print(TeamHold)

#Result 
# append team to ListOfTeams e.g. add ["One", "Six"] to ListOfTeams
#ListOfTeams = [["One", "Six"],["Two", "Seven"],["Three", "Eight"], ["Four", "Nine"], ["Five", "Ten"]]
