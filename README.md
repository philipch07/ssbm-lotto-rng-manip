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
In VSC, take a look at the bottom left of the window where it says something like `3.10.X`, which is your current Python version (it's to the RIGHT of `Python`, and NOT the `Python` text itself), and click on it. In the top-middle of your screen should be a dropdown asking you to select your interpreter. Here, you're going to want to click `Find Interpreter Path` and then click `Browse`, then navigate to the pypy folder, and then select the `pypy.exe` within the pypy folder. Now you're all set up!

---

TODO (ordered by importance):
- Improve alg for lotto sim to minimize time spent (and also coins spent, if reasonable)
- Implement course correction (e.g. calculate the current seed after misinputting the number of coins and rerun the algorithm)
- Modify or create a new function to be used where the user is looking to unlock ALL trophies via the lotto (at the end of the speedrun)
- Implement multithreading for rss

For those curious about RSS (random seed search):
RSS is a type of algorithm that aims to find the current random seed, or rng value, of the current game via a sequence of inputs which involve random events. This is important because the rng value will determine what the outcome of a "random" event is. For example, if someone wants a random integer, the random seed will be involved. Additionally, due to previous work from the community, we know how the random seed is used in *some* functions, and using Dolphin's debugger, the random seed can be directly accessed in memory. However, when it comes to speedruns, accessing specific values in the game's memory via an external tool is not viable, hence the requirement to somehow determine what the random seed is by using a sequence of random in-game events.

---
# An In-Depth Explanation of SSBM's RNG system
As you can probably gather from quite a few different sources around the internet, the rng system used by Melee relies on a value being stored and being manipulated by certain functions to produce some desired values. To be more precise, the RNG value, or seed, is at the heart of what drives randomness, and we know that this value advances in a somewhat linear way, via a function called a Linear Congruent Generator. The purpose of the LCG function is to attempt to return every single value from 0 up to some limit, which in SSBM's case is 2^32, such that no value is repeated along the way, and the values returned are in some generally "random" order. That means that naive approaches which would simply list 0 through (2^32) - 1 would be far too "predictable" when it comes to random events. As a result, a better way of going about this would be to use an LCG, which you can easily Google or search on Wikipedia as it is a common and fairly simple topic in the field of cryptography.

In Melee, the LCG has already been discovered to be the following function:

`seed = ((a * seed) + c) % m`

Where `a = 214013`, `c = 2531011`, and `m = 2^32`.

As previously stated however, this is only the heart of what is used to generate random events. The next step is to use this seed to generate a desired number. For example, if we want to pull a random number from [0, 100) (that is, including 0 and excluding 100), but our seed value is 123456, Melee doesn't say that the random number that we get from [0, 100) is just 123456. Instead, Melee calls a function that takes our current seed, manipulates it to generate a number within the ranges of [0, 100), and then returns that newly generated number.

There are two functions where this happens, both of which have been named by the community, but I personally call them the `get_rand_int()` and `get_rand_float()` functions (to be explicit, they are the "get random integer" and "get random float" functions). As noted by Savestate, the `get_rand_int()` function is used generally more often for purposes that we're interested in, whereas `get_rand_float()` seems to have something to do with CPU behavior, but I haven't been able to get any more info on that function. Regardless, we have our sights set on the `get_rand_int()` function, and this is what we're most interested in right now.

## So How Does This Tie Into The Lottery?
From messing around with the lottery using some of Judge9's scripts, Dolphin-memory-engine, and Dolphin's debugging mode, I was able to figure out that the lottery causes the seed to change by 7 intervals every time 1 coin was used to perform a single roll. That number then changed to 10 intervals per 2 coins for a single roll, 13 coins for a single roll, and so on. I then managed to make some reasonable guesses as to how the rng functions were involved in the lottery minigame:

`3 steps` (aka 3 calls to the `get_rand_int()` function) would be performed per each coin, to randomize where their `x`, `y`, and `z` coordinates are when they spawn in for the animation where they enter the lottery machine. After those `3 * number of coins spent` steps are made, then one call is made to determine the success or failure of the roll (that is, whether the trophy is new or not), then one call to determine the actual trophy that the player will receive, and then one call to determine the pose of the trophy (as some trophies have multiple poses). We can make a simple table to illustrate what the internal system looks like and what functions are being called when we roll for a trophy using only **ONE** coin:

| Action Number |  Seed  |     Description of Action    |            Actual Function Being Called           |
|:-------------:|:------:|:----------------------------:|:-------------------------------------------------:|
|       0       | seed_0 |            Nothing           |                      Nothing                      |
|       1       | seed_1 | Generating Coin X coordinate |                 `get_rand_int(15)`                |
|       2       | seed_2 | Generating Coin Y coordinate |                 `get_rand_int(15)`                |
|       3       | seed_3 | Generating Coin Z coordinate |                 `get_rand_int(15)`                |
|       4       | seed_4 |   Roll for Success/Failure   |                 *explained later*                 |
|       5       | seed_5 |        Roll for Trophy       |                 *explained later*                 |
|       6       | seed_6 |          Trophy Pose         | tbh didn't feel like writing this one down so idk |
|       7       | seed_7 |            Nothing           |                      Nothing                      |

Note here that the table isn't totally linear. Instead, it's meant to be interpreted as follows: `seed_0` is passed into the action at Action Number 1, and `seed_1` is the seed *after* the action at Action Number 1 is completed. To say this a different way, `seed_0` is passed into the `get_rand_int(15)` function, which then *advances* the seed to become whatever `seed_1` is, while also returning some random integer in the range [0, 15).

This section is under development and will slowly be developed as I have free time, so please be patient!

---
# Thank You For Reading!

Here's a list of people whose work I used along the way: Savestate, achilles1515, PracticalTAS, and gainge (aka Judge9).

This project would have never been possible if not for them, and a special shoutout to David V. Kimball for making his documentary video on Melee's All Trophies category, and for all the work that he's put into getting this to work in the first place.

Additionally, shoutouts to the Stadium Discord for being an awesome place where other speedrunners can enjoy a variety of different categories belonging to the same game and for being so welcoming to newcomers like myself who have tons of questions!

<3