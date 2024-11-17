def cg_creation(file_name):
    cg_name = input("what's the name of your new culture group? Type the ID, so all lowercase: ")
    new_file.write(cg_name + " = {\n\t")
    culture_create = culture_creation(cg_name)
    while culture_create == "1":
        new_file.write("\n\t")
        culture_create = culture_creation(cg_name)
        if culture_create == "2":
            break
    new_file.write("\n\tmale_names = {\n\t\t#Add Names Here\n\t}\n\tfemale_names = {\n\t\t#Add Names Here\n\t}\n\tdynasty_names = {\n\t\t#Add Names Here\n\t}\n}")
    cg_choice = input("Do you want to create a new culture group in the " + file_name + " group? 1 for yes, 2 for no: ")
    return cg_choice

def culture_creation(cg_name):
    culture = input("Type in the ID of your new culture! Again, all lowercase: ")
    new_file.write(culture + " = {\n\t")
    primary_nation = input("If your culture has a primary nation, input their tag here. If not, simply hit enter: ")
    if primary_nation == "":
        new_file.write("}")
    else:
        new_file.write( "\tprimary = " + primary_nation + "\n\t}")
    culture_choice = input("Do you want to create a new culture in the " + cg_name + " group? 1 for yes, 2 for no: ")
    return culture_choice

file_create = input("Do you wish to create a new file? 1 for yes, 2 for no: ")

if file_create == "1":
    file_prompt = input("What do you want to call your file (without '.txt')? Input the name of an already existing file if you want to add more cultures to it: ")
    file_name = file_prompt + ".txt"
    try:
        with open(file_name, 'x') as new_file:
            cg_create = cg_creation(new_file)
            while cg_create == "1":
                new_file.write("\n")
                cg_create = cg_creation(file_name)
                if cg_create == "2":
                    break
    except FileExistsError:
        new_file = open(file_name, 'a')
        new_file.write("\n")
        cg_create = cg_creation(file_name)
        while cg_create == "1":
            new_file.write("\n")
            cg_create = cg_creation(file_name)
            if cg_create == "2":
                break

