from modules import music
from modules import timer
from modules import search
from sentence_transformers import SentenceTransformer, util

# Uses Sentence transformers, a model from hugging face which does embedding detection. This takes 
# care of all the actual sysnonyms and doesnt need us to have a hardcoded keywords dict. How this 
# works is basically it creates multi-dimentional vectors, and then compares them to find how alike 
# they are in dimention, using the cosine similariy fucntion. The highets score is mapped to the 
# respective category, and then returned.

ACCEPTABLE_RATIO = 0.3

model = SentenceTransformer('all-MiniLM-L6-v2')                         # Uses a small lightweight model to reduce strain while loading
categories = ["music player", "timer"]                                  # Pre-defined categories, and maybe later precalculated vector values
cat_embeddings = model.encode(categories, normalize_embeddings=True)    # Finds the vector values, normalize_embeddings=True basically makes the length 0, simplifying the calculations from cosine similarities

def detect_category(text:str) -> str:
    text_embedding = model.encode(text, normalize_embeddings=True)      # Finds the vector values for the text that we have inputed
    scores = util.cos_sim(text_embedding, cat_embeddings)[0]            # Calculates the score
    if scores.max().item() < ACCEPTABLE_RATIO:
        return 'search'
    else:
        best_idx = scores.argmax().item()
        return categories[best_idx]

def linker(text: str) -> str:
    """
    Links the different programs by calling them.

    Args:
    text (str): Takes the string obtained from the TTS as input

    Output:
    Outputs the category as a success token.

    Basically, takes the text, searches for the keywords using word embedding, and then calls the
    Requried program for the category detected.
    
    """

    category = detect_category(text)
    match category:
        case 'music player':
            music.music(text)
        case 'timer':
            timer.timer(text)
        case 'search':
            search.search(text)
    
    return category