from modules import music
from modules import timer
from modules import search
from sentence_transformers import SentenceTransformer, util

# ********************************************************************************* #

ACCEPTABLE_RATIO = 0.3
NUM_MODULES = 3
CLEANUP_TIME = 2

KEYWORD_END = "end"
KEYWORD_UNK = 'unkown'

categories = {'music': 'music player', 'timer':'timer', 'search':'search engine for a question', KEYWORD_END:'terminate the program'}                       
program_map = {'music':music.music, 'timer':timer.timer, 'search':search.search, 'end':None}

# ********************************************************************************* #

"""

THE DIFFERENT DICTS USED

--------------------------------------------------------------------------------------
categories: {actual name of the category: name we want the embedding system to think}
program map = {actual name of the category: function assosciated with it}
-------------------------------------------------------------------------------------

program_queue_map = {Queue object of the respective program: Program function}
broadcasting queue = {name of the category: queue object for that category}
category_thread_map = {name of the cateogry: thread object for that category}

"""


model = SentenceTransformer('all-MiniLM-L6-v2')                                                         # Uses a small lightweight model to reduce strain while loading

### For embeddings
category_embeddigns = model.encode([desired_category for _, desired_category in categories.items()], normalize_embeddings=True)    # Finds the vector values, normalize_embeddings=True basically makes the length 0, simplifying the calculations from cosine similarities

### For threading
import threading
import queue

### Queue management - Broadcast Queue
main_queue = queue.Queue()
broadcasting_queue = {}
for category in categories:
    broadcasting_queue[category] =  queue.Queue()

program_queue_map = {broadcasting_queue[category]: program_map[category] for category in categories}

def detect_category(text:str) -> str:
    """
    Detects the category of the text to determine which module should be activated

    Args:
    text (str): The text which the user inputs

    Output:
    str: Outputs the category in general form, ie. 'music' and not 'music-player'

    Uses Sentence transformers, a model from hugging face which does embedding detection. This takes 
    care of all the actual sysnonyms and doesnt need us to have a hardcoded keywords dict. How this 
    works is basically it creates multi-dimentional vectors, and then compares them to find how alike 
    they are in dimention, using the cosine similariy fucntion. The highets score is mapped to the 
    respective category, and then returned. FUN FACT: apprently LLM's also use embeddings to cateogirze
    tokens lmao.

    """
    try:
        text_embedding = model.encode(text, normalize_embeddings=True)          # Finds the vector values for the text that we have inputed
        scores = util.cos_sim(text_embedding, category_embeddigns)[0]           # Calculates the score
        if scores.max().item() < ACCEPTABLE_RATIO:                          
            return KEYWORD_UNK
        else:
            best_idx = scores.argmax().item()                          
            return [key for key,_ in categories.items()][best_idx]
    except Exception as e:
        print(f"{e} occured in detect_category")
        return ''


def input_thread() -> None:
    """
    Input thread where continous input will be taken

    """
    while True:
        try:
            text = input("Enter command: ").lower().strip() 
            category = detect_category(text)

            if category != KEYWORD_UNK:
                main_queue.put({'category':category, 'text':text})

            if category == KEYWORD_END:
                print('PROGRAM TERMINATING: Input thread termintated')
                break
        except Exception:
            print('Input Error, please try again')

def broadcaster(main_queue:queue.Queue, broadcasting_queue:dict[str, queue.Queue]) -> None:
    """
    Sends the message from the Main Queue to the concerned Module Queue

    Args
    main_queue: The main queue object
    broadcasting_queue: The broadcasting queue dict, in the form {name of the category:queue object for that category}

    """
    while True:
        try:
            msg = main_queue.get()
            print(f"Received message: {msg}")
            main_queue.task_done()
            category = msg['category']

            #Checks if program needs to end, if so, sends a termination message to all queues.
            if category == KEYWORD_END:
                programs_terminated = []    
                for program,queue in broadcasting_queue.items():
                    queue.put('TERMINATE')
                
                for prog, thread in category_thread_map.items():    # Looks up the thread in a map to check if the thread is alive
                    thread.join(timeout=CLEANUP_TIME)               # Allows the threads to cleanup the ongoing processes for some time
                    if not thread.is_alive():
                        print(f"{prog} has been terminated")
                        programs_terminated.append(prog)
                    else:
                        print(f"{prog} termination failed")
                
                # Checks if all programs have ended, uses program map as categories may have certain categories which 
                # dont direcly relate to programs (eg. end)
                if len(programs_terminated) == len(program_map):
                    print('All programs terminated successfully')
                    break
            else:
                broadcasting_queue[category].put(msg['text'])
        except Exception as e:
            print(f'{e} ocurred in broadcasting thread')

def start_module_threads(program_queue_map:dict) -> dict[str, threading.Thread] | None:
    """
    Starts the threads of modules using a program_queue_map.

    Args
    program_queue_map: The program-queue map, in the form {Queue object of the respective program: Program function}

    Output
    Program thread map (dict): Returns a dict with the program and their respective threads
    
    """
    try:
        program_thread_map = {}
        program_map_with_key_programfunction = {program_function:category_name for category_name, program_function in program_map.items()}
        for queue, program in program_queue_map.items():
            program_thread = threading.Thread(target=program, daemon=True, args=(queue,))
            program_thread.start()
            program_thread_map[program_map_with_key_programfunction[program]] = program_thread
        return program_thread_map
    except Exception as e:
        print(f"{e} occured in start module thread")
        return None


def linker() -> None:
    """
    Initialises threads in the main.py file

    Basically, there are two queues, main queue, and brodcasting queue. the main queue has the text from the orignal input line, 
    which is entered directly by the user. this infromation is then broadcasted in the broadcasting queue (actually they are multiple 
    groups of queues which are updated simultaneously, because queues uses FIFO structure, which doenst let more than one functions
    listen the main queue). So, we communicate via the broadcasting queyes, about the information relating to the category it was sorted 
    into, and from there, it does its work with text. This allows all functions (music, search, timer, input) work even when something 
    is pre-occupied.
    """
    
    try:
        broadcaster_thread = threading.Thread(target=broadcaster, daemon=True, args=(main_queue, broadcasting_queue))
        input_process = threading.Thread(target=input_thread, daemon=False)

        broadcaster_thread.start()
        input_process.start()
        
        global program_thread_map, category_thread_map
        program_thread_map = start_module_threads(program_queue_map)
        if program_thread_map != None:
            category_thread_map = {category:program_thread_map[category] for category in categories}
    except Exception as e:
        print(f"{e} occured in Linker")