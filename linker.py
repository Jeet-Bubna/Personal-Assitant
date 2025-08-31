import re
from modules import music
from modules import timer
from modules import search

# Defining Keywords which have to be present in the text for the program to detect
# Sometime, maybe we'll make use another more efficient system to get what is the main task, some day 

keywords = {
    "timer": ['set timer', 'start timer', 'stop timer', 'set a timer', 'start a timer', 'stop the timer'],
        "music": ['play', 'pause', 'stop', 'next', 'previous'],
        "search": ['search', 'find', 'lookup']
        
    }

#  #"(?P<music>\bplay\b|\bpause\b|\bstop\b)|(?P<timer>\bset timer\b|\bstart timer\b|\bstop timer\b)
# This is the format that we need the REGEX pattern to look like. The ?P thing is to define the grpname
# So that we can easily backtrack and return the group name if found. The \b just finds a blank space,
# Effectively ensuring that its a word, as a word as a blank space before and after it. The | symbol 
# is an or symbol, so either play or pause or search if found, like that. Read this later and see if 
# This explanation makes sense lmao. Then, you just compile it, and the re.compile() function does most 
# of the job for you, you just need to add the | between groups because that way uk u can seperate grps 
# and stuff. Then we just add the closing bracket and works.

pattern_parts = []
for category, words in keywords.items():
    words = [rf'\b{word}\b' for word in words]
    pattern = f'(?P<{category}>' + r"|".join(words) + ")"
    pattern_parts.append(pattern)

#TODO: MAKE SURE THAT THE LONGER COMMANDS (STOP THE TIMER) ARE ABOVE SHORTER COMMANDS (STOP -- the music)

combined_pattern = re.compile("|".join(pattern_parts), re.IGNORECASE)

def linker(text: str) -> str:
    """
    Links the different programs by calling them.

    Args:
    text (str): Takes the string obtained from the TTS as input

    Output:
    Outputs the confirmation string "success" if the text is sent to the concerned program

    Basically, takes the text, searches for the keywords using regex, and then calls the
    Requried program for the category detected.
    
    """
    category = ''
    match = combined_pattern.search(text)
    if match:
        category = match.lastgroup
    else:
        return None
    
    match category:
        case 'music':
            music.music(text)
        case 'timer':
            timer.timer(text)
        case 'search':
            search.search(text)
    
    #print(f"CATEGORY: {category}. Program has been sent to func")
    return category

