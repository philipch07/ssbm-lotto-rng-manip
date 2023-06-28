# ssbm-lotto-rng-manip

This is a project aimed at understanding SSBM's lottery minigame, as well as the underlying rng functions that SSBM uses.

Watch the below video for a live example.

https://youtu.be/nilRjbvIG4Y

---

# Getting Started
You *should*, and big emphasis on *should* use pypy instead of Python. The reason is simple: the first iteration of the rss algorithm goes over all 4.3+ billion possible seeds. The algorithm does quickly decrease in the volume of computations after that, but if you use regular Python, it'll take a ridiculous amount of time to finish the very first computation. Because I don't feel like dealing with managing memory myself, I wrote this in Python and not C. The good news is that pypy basically converts Python to C in a smart way, and then runs the translated code, which runs way faster, while also having vastly improved garbage collection strategies compared to other libraries like Cython.

## Setting up pypy
First, head over to https://www.pypy.org/download.html and select the desired version of pypy for whatever OS you're using. Then, extract the folder.
From here, I just decided to place the pypy folder *inside* of my Python310 folder, that way I wouldn't lose where my pypy is. Fortunately, the current available version of pypy is 3.10 as well, which is perfect. For example, my folder is located at: `C:\Python310\pypy3.9-v7.3.11-win64`.

## Using pypy as the interpreter
In VSC, take a look at the bottom left of the window where it says something like `3.10.X`, which is your current Python version (it's to the RIGHT of `Python`, and NOT the `Python` text itself), and click on it. In the top-middle of your screen should be a dropdown asking you to select your interpreter. Here, you're going to want to click `Find Interpreter Path` and then click `Browse`, then navigate to the pypy folder, and then select the `pypy.exe` within the pypy folder. Now you're all setup!

---

TODO (ordered by importance):
- Improve alg for lotto sim to minimize time spent (and also coins spent, if reasonable)
- Implement course correction (e.g. calculate the current seed after misinputting the number of coins and rerun the algorithm)
- Modify or create a new function to be used where the user is looking to unlock ALL trophies via the lotto (at the end of the speedrun)
- Implement multithreading for rss

For those curious about RSS (random seed search):
RSS is a type of algorithm that aims to find the current random seed, or rng value, of the current game via a sequence of inputs which involve random events. This is important because the rng value will determine what the outcome of a "random" event is. For example, if someone wants a random integer, the random seed will be involved. Additionally, due to previous work from the community, we know how the random seed is used in *some* functions, and using Dolphin's debugger, the random seed can be directly accessed in memory. However, when it comes to speedruns, accessing specific values in the game's memory via an external tool is not viable, hence the requirement to somehow determine what the random seed is by using a sequence of random in-game events.

Of each of these contributors, here's a list of those whose work I used along the way: Savestate, achilles1515, PracticalTAS, and gainge (aka Judge9).