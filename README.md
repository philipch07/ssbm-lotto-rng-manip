# ssbm-lotto-rng-manip

This is a project aimed at understanding SSBM's lottery minigame, as well as the underlying rng functions that SSBM uses.

Watch the below video for a live example.

https://youtu.be/nilRjbvIG4Y

TODO (ordered by importance):
- Improve alg for lotto sim to minimize time spent (and also coins spent, if reasonable)
- Implement course correction (e.g. calculate the current seed after misinputting the number of coins and rerun the algorithm)
- Modify or create a new function to be used where the user is looking to unlock ALL trophies via the lotto (at the end of the speedrun)
- Implement multithreading for rss

For those curious about RSS (random seed search):
RSS is a type of algorithm that aims to find the current random seed, or rng value, of the current game via a sequence of inputs which involve random events. This is important because the rng value will determine what the outcome of a "random" event is. For example, if someone wants a random integer, the random seed will be involved. Additionally, due to previous work from the community, we know how the random seed is used in *some* functions, and using Dolphin's debugger, the random seed can be directly accessed in memory. However, when it comes to speedruns, accessing specific values in the game's memory via an external tool is not viable, hence the requirement to somehow determine what the random seed is by using a sequence of random in-game events.

Of each of these contributors, here's a list of those whose work I used along the way: Savestate, achilles1515, PracticalTAS, and gainge (aka Judge9).