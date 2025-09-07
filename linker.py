from modules import music
from modules import timer
from modules import search
from sentence_transformers import SentenceTransformer, util

# ********************************************************************************* #

ACCEPTABLE_RATIO = 0.3
NUM_MODULES = 3
categories = {'music': 'music player', 'timer':'timer', 'search':'search', 'end':'end the program'}                       
program_map = {'music':music.music, 'timer':timer.timer, 'search':search.search}

# ********************************************************************************* #

"""

THE DIFFERENT DICTS USED

--------------------------------------------------------------------------------------
categories: {actual name of the category: name we want the embedding system to think}
program map = {actual name of the category: function assosciated with it}
-------------------------------------------------------------------------------------

program queue map = {Queue object of the respective program: Program function}
broadcasting queue = {name of the category:queue object for that category}

"""


model = SentenceTransformer('all-MiniLM-L6-v2')                                                         # Uses a small lightweight model to reduce strain while loading

## For removing end form cateogries
import copy
real_categories = copy.deepcopy(categories)
real_categories.pop('end')
print('cat', categories, 'real cat', real_categories)


### For embeddings
category_embeddigns = model.encode([desired_category for _, desired_category in categories.items()], normalize_embeddings=True)    # Finds the vector values, normalize_embeddings=True basically makes the length 0, simplifying the calculations from cosine similarities

### For threading
import threading
import queue

### Queue management - Broadcast Queue
main_queue = queue.Queue()
broadcasting_queue = {}
for category in real_categories:
    broadcasting_queue[category] =  queue.Queue()
program_queue_map = {broadcasting_queue[category]: program_map[category] for category in real_categories}


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

    text_embedding = model.encode(text, normalize_embeddings=True)          # Finds the vector values for the text that we have inputed
    scores = util.cos_sim(text_embedding, category_embeddigns)[0]           # Calculates the score
    if scores.max().item() < ACCEPTABLE_RATIO:                          
        return 'unknown'
    else:
        best_idx = scores.argmax().item()
        print('best idx', best_idx)            
        print(categories)              
        return [key for key,_ in categories.items()][best_idx]


def input_thread() -> None:
    """
    Input thread where continous input will be taken

    """
    while True:
        text = input("Enter command: ").lower().strip()
        category = detect_category(text)
        main_queue.put(category)

        if category == 'end':
            print('Terminating program')
            break

def broadcaster(main_queue:queue.Queue, broadcasting_queue:dict[str,queue.Queue]) -> None:
    """
    Sends the message from the Main Queue to the concerned Module Queue

    Args
    main_queue: The main queue object
    broadcasting_queue: The broadcasting queue dict, in the form {name of the category:queue object for that category}

    """
    while True:
        category = main_queue.get()
        print(f"Received message: {category}")
        main_queue.task_done()

        if category == 'end':
            for _,q in broadcasting_queue.items():
                q.put(category)
            print('terminating broadcaster')
            break

        if category != 'unknown':
            broadcasting_queue[category].put(category)

        

def start_module_threads(program_queue_map:dict) -> list[threading.Thread]:
    """
    Starts the threads of modules using a program_queue_map.

    Args
    program_queue_map: The program-queue map, in the form {Queue object of the respective program: Program function}
    
    """
    threads = []
    for queue, program in program_queue_map.items():
        thread = threading.Thread(target=program, daemon=True, args=(queue,))
        thread.start()
        threads.append(thread)
    return threads

def linker():
    """
    Initialises threads in the main.py file

    Basically, there are two queues, main queue, and brodcasting queue. the main queue has the text from the orignal input line, 
    which is entered directly by the user. this infromation is then broadcasted in the broadcasting queue (actually they are multiple 
    groups of queues which are updated simultaneously, because queues uses FIFO structure, which doenst let more than one functions
    listen the main queue). So, we communicate via the broadcasting queyes, about the information relating to the category it was sorted 
    into, and from there, it does its work with text. This allows all functions (music, search, timer, input) work even when something 
    is pre-occupied.
    """

    input_process = threading.Thread(target=input_thread, daemon=False)
    input_process.start()
    broadcaster_thread = threading.Thread(target=broadcaster, daemon=True, args=(main_queue, broadcasting_queue))
    broadcaster_thread.start()
    threads = start_module_threads(program_queue_map)

    input_process.join()
    print('input joined')
    broadcaster_thread.join()
    print('broadcaster joined')

    for thread in threads:
        print(f"joining", thread)
        thread.join()
        print(f"{thread} joined")
    
    print('Program successfully terinated')