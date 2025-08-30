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
`text = "Jarvis, play music"`  
`for str in text.split(' '):`  
`   if "music" in text:`   
`       #Do something`  
What this does, it basically loops over each word in text, and the `in` keyword breaks the text into substrings which are of same size as the search term, here music. So, its really inneffcient, as the worst case senerio states the maximum time complexity as O(m*n).  
So, instead of doing this, the NFA checks each letter, and compares it with the target, and updates states accordingly.  
Not gonna explain it here right now, cuz I wanna implement this rather than typing this out lmao, if future jeet is reading this, visit [What is Finite Automata](https://www.tutorialspoint.com/automata_theory/what_is_finite_automata.htm)

### Unittest module
Using unittest module to perform unit tests, the @patch keyword, which runs a mock instance of the module rather than running the module. Why we wanna do this? Because running the actual functions will have unintended consequences like it might actually place music, we dont want that as that reduces speed and also makes it annoying.  
The linker test for example goes through all the keywords, and uses the self.assertEqual() function to basically say that 'if a == b' then it passes, otherwise not. Its like assert statments but more robust with more functionality.  
The reason that I prefer unittest over pytest is that it is built in python, so less installations so yay!
