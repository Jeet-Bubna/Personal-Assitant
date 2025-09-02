import vlc
from yt_dlp import YoutubeDL
import time

# Using yt-dlp to download songs locally and play them using vlc, right now just to prove concept
# TODO: implement the automatic linker generator and all

ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "outtmpl": "song.%(ext)s"
    }

def music(queue):
    while True:
        text = queue.get()
        print(f'Text recieveed in music_thread: {text}')
        url = "https://www.youtube.com/watch?v=4TVT7IOqH1Y" #for now, for testing purposes
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        player = vlc.MediaPlayer(filename)
        player.play()
        time.sleep(10)
        player.pause()
        time.sleep(4)
        player.play()



"""
Problem: How to know which song the user wants to play?

1) We could use a template, like jarvis play ---- and then whatever comes after play is the song name, but that doesnt work well with edge cases
    Yes, and this would be easier to work with, and like super fast to implement
    BUT, I have done this before and it is too easy and I want to do something new
2) We could build an algorithm or smth which denotes that this phrase or word is how likely to be a song name
    Yes, and this would really make me understand algorigthms
    BUT, This might take too much time and i probably dont have enough math knowledge to accomplish this properly
3) We could have a list of all the songs, atleast populat songs in a file, and then check if it matches
    Yes, and this would make the program faster and more reliable, and this will be SUPER easy to implement
    BUT, This type of data might not be available, and is not that elegent, and will not handle well with edge cases

LETS GO WITH 2 because I want to do something new

Now, what do commands look like?
They will be: 
Jarvis, play some muisc
jarvis, play something
play something, jarvis
play bruno mars, jarvis
play xx song from xy artist jarvis
jarvis put some tunes from xy artist

This is the general structure, now i notice some common things,
1) it will have jarvis (because without that the program wont even start, atleat thats what the idea is for now, maybe later we can have a timer 
or something which will act as a countdown where two successive commands can be said without having to say jarvis)
2) it will have some music related name (either song name, artist name, or a the literal word music or songs or tunes or words like that)

To seperate out the music related word, we just need to remove all the keywords (play, stop, and all) and other enlgish things (verbs, adverbs) and 
just keep nouns and other words. This will ensure that any edge case is handled. This can also easily be done by just having a giant list of verbs 
and adverbs and use regex to filter the text, and return that which is only a noun. Lets try that.

Oh wait, the song name might itself have an adverb or verb, so that method doesnt work.

So one things for sure, we need to remove, jarvis and other commands (play, pause etc) from the text. But, what if the song's name itself has these keywords?
Like PLAYboi carti has play in his name, so that play part will get removed if we are not careful. Is there a common relation between the play that we want, 
and its surrounding keywords? lets see - 

Jarvis, play something -- Before: Noun (we know that noun), After: Noun(we dont know that noun)
play something, jarvis -- Before: nothing, After: Noun (we dont know)

So, now that I am looking at it, its becoming increasingly hard to find an algorithm which is rigid enough that it will handle all test cases. So, eiter I
can make an algorithm and tell the users to tell it instructions some way, but thats just not that cool now. A newborn baby could do that. So, I guess 
the most interesting option is to go with the AI option and then implement the fallback list option or this option if that doesnt get done by a week lets say.

So, building an AI is complicated -- im gonna need lots of data, which i think can be done pretty easily using chat gpt, so thats not a problem
the problem is going to be to make it really really fast so that it can work nearly as fast as an algorithm. Also, i know nothing about AI so i will have to
reaserch and find a good type of AI to fit here, which can run very fast. So lets get to it

One question remains, do i need to know the full technical background behind how ai's work? or is it fine if i implement it and see where it takes me. Ill 
just implement a very basic ai first and see how to improve it later.

Was reaserching, and found an alogrithm named KMP (Kruth Morris Prat) Algorithm. This might work for the algorithm to find Jarvis in the text. But, for this
task, no this wont work. KMP works bascially by created a LPS (longest prefix suffix) table. So, instead of starting over, it just goes back to where the prefix
matched. Like, its hard to explain in words here, just watch this video - https://www.youtube.com/watch?v=ynv7bbcSLKE

OK, so we might be able to use fuzzy matching here? fuzzy matching is bascially like regex matching, but instead of matching it word to word, it like matches it 
based on are the words there. Like imagine a string "Jarvis play music" and "play tunes jarvis". if we use regex matching, it wont come up as same, unless we
specify that tunes is also a recognised word, but in fuzzy matching, it will come up pretty high. although, this doesnt really help us find the song name now that
i think about it, as we dont know what to match it to. So, that doesnt work, hmm so im pretty sure i will have to build ai only.

While reaserching, i realised that word-embeddings will be a better suit for linker program, as that basically gets rid of the need for keywords entirely. First,
Imma work on that for now. Now that is done, imma build the music player

Tried to look for new ways, like tried to use spotify's api but that doesnt allow for entire playback, only pausing and resuming, so we cannot play actual songs, 
thats a no no.

YES! got it to work, using yt-dlp only tho, i cannot find a better way - one thought does come to mind, like we just implement what spotify does and play the song
WHILE its downloading, so essentially its very very very fast, ill see if i can implement that.


"""
    

