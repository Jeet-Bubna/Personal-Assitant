from modules import music
from modules import timer
from modules import search
from sentence_transformers import SentenceTransformer, util

# Uses Sentence transformers, a model from hugging face which does embedding detection. This takes 
# care of all the actual sysnonyms and doesnt need us to have a hardcoded keywords dict. How this 
# works is basically it creates multi-dimentional vectors, and then compares them to find how alike 
# they are in dimention, using the cosine similariy fucntion. The highets score is mapped to the 
# respective category, and then returned. FUN FACT: apprently LLM's also use embeddings to cateogirze
# tokens lmao.

ACCEPTABLE_RATIO = 0.3
NUM_MODULES = 3


model = SentenceTransformer('all-MiniLM-L6-v2')                         # Uses a small lightweight model to reduce strain while loading
categories = ["music player", "timer"]                                  # Pre-defined categories, and maybe later precalculated vector values
cat_embeddings = model.encode(categories, normalize_embeddings=True)    # Finds the vector values, normalize_embeddings=True basically makes the length 0, simplifying the calculations from cosine similarities

### For threading
import threading
import queue
broadcasting_queue = [queue.Queue() for i in range(NUM_MODULES)]
main_queue = queue.Queue()

def detect_category(text:str) -> str:
    text_embedding = model.encode(text, normalize_embeddings=True)      # Finds the vector values for the text that we have inputed
    scores = util.cos_sim(text_embedding, cat_embeddings)[0]            # Calculates the score
    if scores.max().item() < ACCEPTABLE_RATIO:
        return 'search'
    else:
        best_idx = scores.argmax().item()                               # NAME CONVENTION: Apparently idx --> index not 'id'
        return categories[best_idx]


def input_thread():
    while True:
        text = input("Enter command: ")
        main_queue.put(text)

def brodcaster(main_queue):
    while True:
        msg = main_queue.get()
        print(f"Received message: {msg}")
        main_queue.task_done()

        category = detect_category(msg)
        match category:
            case 'music player':
                broadcasting_queue[0].put(msg)
            case 'timer':
                broadcasting_queue[1].put(msg)
            case 'search':
                broadcasting_queue[2].put(msg)


def linker():
    """
    Initialises threads in the main.py file

    Args:
    input_thread: Is the function which takes input present in the main file
    main_queue: The main queue defined in the main program

    Basically, there are two queues, main queue, and brodcasting queue. the main queue has the text from the orignal input line, 
    which is entered directly by the user. this infromation is then broadcasted in the broadcasting queue (actually they are multiple 
    groups of queues which are updated simultaneously, because queues uses FIFO structure, which doenst let more than one functions
    listen the main queue). So, we communicate via the broadcasting queyes, about the information relating to the category it was sorted 
    into, and from there, it does its work with text. This allows all functions (music, search, timer, input) work even when something 
    is pre-occupied.
    """
    # broadcaster_process = threading.Thread(target=linker, daemon=True, args=(main_queue, ))
    # broadcaster_process.start()

    input_process = threading.Thread(target=input_thread, daemon=False)
    input_process.start()

    music_process = threading.Thread(target=music.music, daemon=True, args=(broadcasting_queue[0],))
    music_process.start()

    timer_process = threading.Thread(target=timer.timer, daemon=True, args=(broadcasting_queue[1],))
    timer_process.start()

    search_process = threading.Thread(target=search.search, daemon=True, args=(broadcasting_queue[2],))
    search_process.start()

    brodcaster(main_queue)

    #input_process.join() 

    # This is important, as we want this function, the init_thread functions to not finish, or else it will return causing the main progam 
    # to return, and the program will not interate, causing a message 'enter command' and then it will just end. This is because the input 
    # process is on a daemon thread, which is considered as a 'background' task, and if the non-daemon thread (in this case, the main program) 
    # thread finishes, it wont wait for the non-daemon threads to finish, causing the program to end abruptly.