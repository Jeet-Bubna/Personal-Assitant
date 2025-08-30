def linker(text: str) -> str:
    keywords = {
        "music": ['play', 'pause', 'stop', 'next', 'previous'],
        "search": ['search', 'find', 'lookup'],
        "timer": ['set timer', 'start timer', 'stop timer', 'set a timer', 'start a timer', 'stop the timer']
    }


# USE REGEX FOR THIS, RN I GOTTA GO STUDY FOR EXAMS
# What is regex: Reg ex: regular expresssions, faster than looping over each text to find keywords, 
# instead compile the keywords into a pattern and search the text with it, there are 2 types of 
# engines used to perform regex: DFA (Deterministic Finite Automaton) and NFA (Non-deterministic Finite Automaton)