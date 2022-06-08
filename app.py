from src.controller import StudentController

command = None
while command != "exit":
    command = input("command? ")
    print(command)

    controller = StudentController()
    if command == "save":
        controller.save()
        print("New student created")

    if command == "sscore":
        id_ = input("id?: ")
        score = input("score? ")
        controller.set_score(int(id_), int(score))

    if command == "gscore":
        id_ = input("id?: ")
        print(controller.get_score(int(id_)))
