students = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]
ListOfGroups = [["One", "Two", "Three", "Four", "Five"], ["Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]]

#Priority grouping

if priority == Experience:
    #Has experience
    HasExp = User.query.filter(RhysTestTable.experienced == 1).all()
    #No experience
    NoExp = User.query.filter(RhysTestTable.experienced == 0).all()

    ListOfGroups = []
    for i in range(2):
        ListOfGroups.append([])
    ListOfGroups[0].append(HasExp)
    ListOfGroups[1].append(NoExp)

#Make sure values here match to the correct degree answer in the database
if priority == degree:
    BSc = User.query.filter(User.degree == 1).all()
    BA = User.query.filter(User.degree == 2).all()
    BEng = User.query.filter(User.degree == 3).all()
    LLB = User.query.filter(User.degree == 4).all()

    ListOfGroups = []
    for i in range(4):
        ListOfGroups.append([])
    ListOfGroups[0].append(BSc)
    ListOfGroups[1].append(BA)
    ListOfGroups[2].append(BEng)
    ListOfGroups[3].append(LLB)
