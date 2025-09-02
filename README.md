# Personal AI Assistant

## What I Learnt
### DFA and NFA systems for keyword detection
**As of 30-8-25**  
DFA and NFA are a part of the REGEX (Regular Expression). This is used to find certain phrases in a given string easily. This is done by the python `re` module.  
What is regex: Reg ex: regular expresssions, faster than looping over each text to find keywords, instead compile the keywords into a pattern and search the text with it, there are 2 types of engines used to perform regex: DFA (Deterministic Finite Automaton) and NFA (Non-deterministic Finite Automaton)  

#### What is DFA and NFA
DFA and NFA have 'A' in common. This stands for Automaton. An automaton is a conceptual simplified computer. A finite automaton is called as finite, because it contains a finite number of states. Pythons `re` module uses NFA instead of DFA.

#### Why is NFA more effecient than a simple for loop or python's inbuilt `in` keyword?
While using a for loop, for example in this code  
```
text = "Jarvis, play music"`  
for str in text.split(' '):  
   if "music" in text:   
       #Do something```  
```
What this does, it basically loops over each word in text, and the `in` keyword breaks the text into substrings which are of same size as the search term, here music. So, its really inneffcient, as the worst case senerio states the maximum time complexity as O(m*n).  
So, instead of doing this, the NFA checks each letter, and compares it with the target, and updates states accordingly.  
Not gonna explain it here right now, cuz I wanna implement this rather than typing this out lmao, if future jeet is reading this, visit [What is Finite Automata](https://www.tutorialspoint.com/automata_theory/what_is_finite_automata.htm)

### Unittest module
Using unittest module to perform unit tests, the @patch keyword, which runs a mock instance of the module rather than running the module. Why we wanna do this? Because running the actual functions will have unintended consequences like it might actually place music, we dont want that as that reduces speed and also makes it annoying.  
The linker test for example goes through all the keywords, and uses the self.assertEqual() function to basically say that 'if a == b' then it passes, otherwise not. Its like assert statments but more robust with more functionality.  
The reason that I prefer unittest over pytest is that it is built in python, so less installations so yay!

### Embedding system for keyword detection
As i reaserched more and more, i realised that my current system which used regex is based on certain keywords, which do not contain all possible words for music, timer, etc. So thats why I am going to use Embedding systems for keyword detection. Embedding works by esstentially creating a vector of the cateogry, for example: music. This gives us a vector. Now, the input text is converted into a vector. Based on the similarities in direction and lenght of the vector, it calculates a similarity score. And then the highest score is mapped to the most likely function, and hence it works for all edge cases. I am going to use sentence_transformers from Hugging Face. 

#### Using of Threading instead of Multiprocosessing like i thouht befoere
Before, i used threading module in my earlier processes. So, i use multiprocessing. Threading is just creating threads, and the problem with python is that it still treats a thread not as a standalone operation. So, the code runs one time only. This causes marginal difference in runtime difference. So, we use multiproccessing output, which creates differenct interpreters so it can truely run as an independent script, and simultanesously. However, the trade off is some run-time performance, which may be a problem but I am going to use this for now as playing music seems like a pretty CPU intensive job. Wait, as im typing this, threading will be better! RIGHT! Music is not that user intensive, and its essentially waiting for input output, which is what threading! Oh god im dumb, sorry for that guys

#### What 'joining' threads really mean
So, i was just experimenting, and i had a line of code which said 'input process.join()'. Naturally, i thought this isnt necessary, as we are not joining other threads right? So i deleted it and found that the entire input system was broken..  
The reason is simple: the input process thread was a daemon thread. A daemon thread is like a background worker thread, and if the non-daemon threads (ie. the main threads) are finished, the program will finish. What joining means, it doesnt mean that you kill the thread and join it, it means that you halt the execultion of code, wait for the thread to finish, and then you just join the thread with the main program. Now, because the input process is a loop, it never ends, so by mistake, i made a very elegant solution to a trivial problem.