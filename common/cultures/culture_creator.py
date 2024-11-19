import os
os.chdir(os.path.dirname(__file__)) # Neat trick to ensure python is actually in the file's directory
                                    # otherwise e.g. double-clicking the file won't work

ANSI = 'iso-8859-1' # ANSI/Win-1252/Latin-1 encoding that eu4 text files should use
UTF8 = 'utf-8-bom' # UTF-8 BOM encoding that eu4 localisation files should use


def yes_no(prompt: str): # type annotations are very useful for autocomplete and checking for mistakes
    'Helper function for yes/no questions'
    if input(prompt + " (y/n): ").lower() in 'yes': # this is also true for 'y' or 'ye' or 'YES'
        return True
    return False

def is_valid_text(text:str): # Python strings are in unicode by default
    'Check that input text is valid in ANSI encoding'
    try:
        text.encode(ANSI)
        return True
    except UnicodeEncodeError:
        return False

def reconstruct(s, tabs: int): # uh... code
    'Print code structure in proper eu4 code formatting'
    if type(s) is str:
        return f'{'\t'*tabs}{s}\n'
    elif type(s) is list:
        out = '%s%s = {\n' % ('\t'*tabs, s[0])
        for x in s[1:]:
            out += reconstruct(x, tabs+1)
        out += '%s}\n' % ('\t'*tabs)
        return out
    else:
        raise ValueError(f'Issue at level {tabs}')

### input code ###

cultures = [] # To make sure the same identifiers aren't reused
culture_groups = []

def write_to(file):
    'The "main" function, writing culture groups to the output file'
    global culture_groups # allows access to the global-scope 'culture_groups' from a local function scope
    data = []
    while True:
        inp = input("Enter the name of a new culture group: ")
        if not inp:
            break
        if not is_valid_text(inp):
            print(f"  The name '{inp}' contains illegal characters.")
            continue # continue with next loop
        if inp in culture_groups:
            print("  This culture group exists already.")
            continue
        culture_groups.append(inp)
        data.append(create_culture_group(inp))
    if data: # No data -> nothing to write
        print("Writing to file...")
        for x in data:
            file.write(reconstruct(x, 0))
    print("Done")

def create_culture_group(name:str):
    'Define a culture group'
    global cultures
    data = [name] # first item in the list is the name, others are the content
    
    n = create_list(f"Enter the male names for {name}", '#Add Group Names Here')
    data.append(['male_names', ' '.join(n)])
    n = create_list(f"Enter the female names for {name}", '#Add Group Names Here')
    data.append(['female_names', ' '.join(n)])
    n = create_list(f"Enter the dynasty names for {name}", '#Add Group Names Here')
    data.append(['dynasty_names', ' '.join(n)])

    while True:
        inp = input(f"Enter the name of a culture to add to {name} (empty to stop): ").lower()
        if not inp:
            break
        if not is_valid_text(inp):
            print(f"  The name '{inp}' contains illegal characters.")
            continue
        if inp in cultures:
            print(f"  The culture '{name}' exists already.")
            continue
        cultures.append(inp)
        data.append(create_culture(inp))
    return data

def create_culture(name:str):
    'Define a culture'
    data = [name]
    inp = input(f"Enter the primary nation of {name}: ")
    if inp:
        data.append(f'primary = {inp}')

    n = create_list(f"Enter the male names for {name}", '#Add Names Here')
    data.append(['male_names', ' '.join(n)])
    n = create_list(f"Enter the female names for {name}", '#Add Names Here')
    data.append(['female_names', ' '.join(n)])
    n = create_list(f"Enter the dynasty names for {name}", '#Add Names Here')
    data.append(['dynasty_names', ' '.join(n)])
    return data

def create_list(prompt, default):
    'Create a list of names for the cultures'
    names = []
    print(prompt + " (empty to stop): ")
    while inp := input(): # Fancy way to both assign to variable (inp) and check if it's true (not empty string)
        if not is_valid_text(inp):
            print(f"  The text '{inp}' contains illegal characters.")
            continue
        names.append(inp)
    if not names: # if no names are given, insert the "add here" placeholder
        names.append(default)
    return names

### main code ###

try: # big try-except as otherwise the temporary console opened by double-clicking this file just closes on exception
    print("Welcome to the Culture Creator!\n\nAny question can be answered with nothing to end/exit.\n")
    while True:
        inp = input("\nEnter the filename (existing or new file): ")
        if not inp:
            break
        if not inp.endswith('.txt'): # instead of telling the user to leave it out, just add only if needed
            inp += '.txt'
        if os.path.isfile(inp):
            if not yes_no(f"Add to existing file '{inp}'?"): # asking for confirmation in case of filename typo
                break
            try:
                with open(inp, 'a', encoding=ANSI) as f: # encoding should be ANSI to include more special characters
                    write_to(f) # the default UTF-8 isn't properly supported, it just kinda works since UTF-8 is backwards-
            except OSError:     # compatible with ASCII characters, but that's missing special characters such as äóç
                print("  Could not open that file.")
                continue
        else:
            if not yes_no(f"Create new file '{inp}'?"):
                break
            with open(inp, 'w', encoding=ANSI) as f:
                write_to(f)
    input("Press enter to exit...")
except Exception as e:
    #raise  # uncomment this to track down exceptions in IDE
    print(f"Error: {e}")
    input("Press enter to exit...")


