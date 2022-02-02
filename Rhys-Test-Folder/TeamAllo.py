#want to group students based on priority 
#so using coding experience as priority, boolean answer (yes/no)
#want 2 groups, one full of students who answered yes and one full of those that answered no
#would then want to allocate all the yes people into groups first, so depending on how many groups depends on how many passes over
#once the group of yes students is depeleted repeat the process by adding the no students into the groups 


students = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
teamSize = 2




def TeamAllo(list, teamSize): 

    ListOfTeams = []

    NumOfStudents = len(list)

    NumOfSplits = NumOfStudents // teamSize

    Test = students[::teamSize]

    return(NumOfStudents, NumOfSplits, Test)



print(TeamAllo(students, 2))
