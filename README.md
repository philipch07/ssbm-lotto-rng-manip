# ssbm-lotto-rng-manip

This project was initially aimed at understanding SSBM's lottery minigame but it had some expansions as I made some new discoveries about how RNG works for generating new name tags as well as generating trophies in the first stage of the single player adventure mode.


# Check Out Other SSBM Tools!

https://github.com/Olivia926/All_Trophies_Help

That's the collection of tools which are relevant to SSBM's All Trophies any% speedrun, but this repo is the main repo that I'll be contributing to for ease of use.

# Getting Started

Most scripts have been optimized to avoid having to iterate over every single one of the 4.3+ billion seeds. I started this project in Python because I thought this project would be relatively quick and small, which of course was an extreme understatement. That being said, Python's slower speeds compared to languages such as C or Rust aren't an issue because of the optimizations made in the Reverse Seed Search (RSS) algorithm thanks to TauKhan.

If you just want to try out one of these scripts, make sure you have Python installed and in your PATH. Then in a terminal, navigate to the folder containing this repo, or whichever scripts you want to use (for this example, let's say I want to run `initial_birdo.py`). Then in the terminal, navigate to the directory containing the script, type `python ./initial_birdo.py`, and it'll run the script (if not, check your directory and also if you need to type `python3` instead of `python`). From there, your terminal should look like mine in the video. If you want to exit python in the terminal, you can either close the terminal window or type `quit()` and hit enter.

## Melee Speedruns and these scripts:
For any non-stadium speedruns which may require birdo in any way, `initial_birdo.py` should be used. For the all trophies speedrun, `initial_birdo.py` is used at the beginning, followed up by `end_lotto.py`, and finally `end_adv1_1.py` to end the run. Note that the lottery must be completed before the end of the adventure run! This is because that's the order that I tested the scripts in, and any inconsistencies might result in the scripts being completely unusable.

## Explanation of notable files:
`initial_birdo.py` is intended to be used at the very beginning of a game launch in order to get birdo from the starting 5 coins from the lottery minigame. Note that this file is heavily commented, so if you're looking to learn what the code is like, start reading here!

`end_adv1_1.py` is intended to be used at the end of an all trophies run.

`end_lotto.py` is intended to be used at the end of an all trophies run.

`tagrss.py`is TauKhan's extremely efficient implementation of tagRSS (explanation below). This isn't meant to be run by itself, but can be used if the user knows what they're doing.

`globals.py` handles all of the additional utility calls, and contains specific lists of trophies. This file helps to reduce duplicate code across multiple files by keeping it in one central location. At the moment, it handles managing a user's owned trophies, determining the seed by calling `tagrss.py` alongside some other logic, and printing the tags that a user should roll for any necessary rng manipulation.

`trophies.txt` is a list of all the trophies in the game that are needed, with certain names being adjusted due to duplicate or confusing names.

## Explanation of other files
`initial_lotto.py`, `old_adv1_1.py`, `old_code.py.example`, and `start_adv1_1.py` all should NOT be used for any speedrun purposes, as these files are out of date. I kept them here because it could potentially contain some helpful information (for example, the initial lotto script has some similar logic used `end_lotto.py`, albeit far more primitive), and they have some examples of my initial approaches to problems, which may be helpful for other speedrunning communities. `start_adv1_1.py` was a test for using `globals.py` to handle cleaning up some of the duplicate logic that I kept implementing every time I wanted to solve a new rng manip problem with tagRSS as my starting point. It is also extremely similar to `end_adv1_1.py` and should also work properly from what I've tested.

---

## TODO (ordered by importance):

- ~~Create a script for when a runner is looking to unlock all trophies at the end of the run (`end_lotto.py`)~~
- Rewrite this file so it's more readable and has a better narrative.
- Implement course correction (create a way for scripts to undo mistakes or recompute the current seed if the user misinputs) [this is not likely to be implemented since it is very time consuming... in other words, be careful when inputting!]
- ~~Fix `end_adv1_1.py` bugs~~
- ~~Create an easier way to reduce repeated logic for new scripts~~
- ~~Fix readme issues (incorrect information due to misremembering)~~
  - ~~Explanation of improved RSS algorithm by explaining how `get_rand_int()` works~~
  - ~~Explanation of new routing + previous assumptions which no longer hold~~
- ~~Create a script for adv 1-1 trophy manip (including birdo unlock)~~

## What is RSS (random seed search)?

RSS is a type of algorithm that aims to find the current random seed, or rng value, of the current game via a sequence of inputs which involve random events. This is important because the rng value will determine what the outcome of a "random" event is. For example, if someone wants a random integer, the random seed will be involved. Additionally, due to previous work from the community, we know how the random seed is used in _some_ functions, and using Dolphin's debugger, the random seed can be directly accessed in memory. However, when it comes to speedruns, accessing specific values in the game's memory via an external tool would not be viable as it would give a player more information that they wouldn't be able to access from in game actions, hence it would be more acceptable to attempt to determine the random seed by using a sequence of random in-game events.

---

# An In-Depth Explanation of SSBM's RNG system

As you can probably gather from quite a few different sources around the internet, the rng system used by Melee relies on a value being stored and being manipulated by certain functions to produce some desired values. To be more precise, the RNG value, or seed, is at the heart of what drives randomness, and we know that this value advances in a linear way by way of a function called a Linear Congruent Generator (LCG). The purpose of the LCG function is to attempt to return every single value from 0 up to some limit, which in SSBM's case is $2^{32}$, such that no value is repeated along the way, and the values returned are in some generally "random" order. That means that naive implementations of an LCG would simply list $0$ through $2^{32} - 1$ and would be far too "predictable" when it comes to random events. As a result, a better way of going about this would be to use an LCG, which you can easily Google or search on Wikipedia as it is a common and fairly simple topic in the field of cryptography.

In Melee, the LCG has already been discovered to be the following function:

$seed = ((a * seed) + c) \% m$

Where $a = 214013$, $c = 2531011$, and $m = 2^{32}$.

As previously stated however, this is only the heart of what is used to generate random events. The next step is to use this seed to generate a desired number. For example, if we want to pull a random number from $[0, 100)$ (that is, including $0$ and excluding $100$), but our seed value is $123456$, Melee doesn't say that the random number that we get from $[0, 100)$ is just $123456$. Instead, Melee calls a function that takes our current seed, makes the seed step once according to the LCG function, then manipulates it to generate a number within the ranges of $[0, 100)$, and then returns that newly generated number.

There are two functions where this happens, both of which have been named by other folks in the community, but I personally call them the `get_rand_int()` and `get_rand_float()` functions (to be explicit, they are the "get random integer" and "get random float" functions). As noted by Savestate, the `get_rand_int()` function is used generally more often for purposes that we're interested in, whereas `get_rand_float()` seems to have something to do with CPU behavior, but I haven't been able to get any more info on that function. Additionally, TauKhan has noted that one of the main issues with Melee's RNG is the inability to understand the recursive particle generation function which calls on the `get_rand_float()` function which would be nice to calculate since it could aid in more optimal RNG manipulation in the future. Regardless, we have our sights set on the `get_rand_int()` function, and this is what we're most interested in right now.

## So How Does This Tie Into The Lottery?

From messing around with the lottery using some of Judge9's scripts, Dolphin-memory-engine, and Dolphin's debugging mode, I was able to figure out that the lottery causes the seed to change by 7 intervals every time 1 coin was used to perform a single roll. That number then changed to 10 intervals per 2 coins for a single roll, 13 coins for a single roll, and so on. I then managed to make some reasonable guesses as to how the rng functions were involved in the lottery minigame:

`3 steps` (aka 3 calls to the `get_rand_int()` function) would be performed per each coin, to randomize where their `x`, `y`, and `z` coordinates are when they spawn in for the animation where they enter the lottery machine. After those $3 *$ `number of coins spent` steps are made, then one call is made to determine the success or failure of the roll (that is, whether the trophy is new or not), then one call to determine the actual trophy that the player will receive, and then one call to determine the pose of the trophy (as some trophies have multiple poses). We can make a simple table to illustrate what the internal system looks like and what functions are being called when we roll for a trophy using only **ONE** coin:

| Table 1: Lottery Actions and RNG Calls |
| -------------------------------------- |

| Action Number | Seed In | Seed Out |   Description of Action   | Actual Function Called |
|:-------------:|:-------:|:--------:|:-------------------------:|:----------------------:|
|       1       |   s_1   |    s_2   |          No idea          |   `get_rand_int(15)`   |
|       2       |   s_2   |    s_3   |          No idea          |  `get_rand_float(??)`  |
|       3       |   s_3   |    s_4   |          No idea          |  `get_rand_float(??)`  |
|       4       |   s_4   |    s_5   |          No idea          |  `get_rand_float(??)`  |
|       5       |   s_5   |    s_6   |  Roll for success/failure |   `get_rand_int(100)`  |
|       6       |   s_6   |    s_7   |      Roll for trophy      |    _explained later_   |
|       7       |   s_7   |    s_8   | Trophy pose (unconfirmed) |  `get_rand_float(1?)`  |

Note that this table was updated to better reflect how the rng value/seed is actually being used by these functions. For example, at action number $1$, we can see that `get_rand_int(15)` actually takes in the first seed, $s_1$, manipulates it such that it becomes some seed $s_2$ (via the LCG function above), then returns an int from the range $[0, 15)$.

Additionally, note that the table does have some `??` values and a `1?` value, which is meant to mark that certain values may change due to certain internal variables that we currently do not have knowledge about. Fortunately for us, we don't actually need to get the result of these functions as the output doesn't seem to affect what we're looking for, however, the fact that those functions do advance the seed does mean that it is something that we must keep track of. As a result, we can still utilize these functions in a different way: to advance the seed as necessary without doing any extra computation for returning any unneeded "random" integers or floats.

We can then think about this as a loop, as the lottery page doesn't call any rng updates in the background, which means that the rng value is still static. As a result, we can simply pass in the resulting rng value from one usage into the next usage and so on, thus allowing us to essentially loop over the table to then figure out if the values returned by the functions are desirable or not. Therefore, all that's left is to figure out how exactly the RNG values are used by the `get_rand_int()` functions, and how we can fully simulate the lottery minigame itself!

# Figuring Out The Lottery

In simulating the lottery, we know that the RNG values are predictable at each step, and because we know exactly how the `get_rand_int()` functions work, we can also figrue out exactly what those functions return, which means that there shouldn't be anything else that we have to worry about... right?

Nope! This gets a bit more complicated, but also significantly more interesting. The trophies that a player can get are split up into a few different categories. These are:

| Table 2: Lottery Trophy Categories |
| ---------------------------------- |

|              Category Name             | Abbreviation | # of Trophies |
|:--------------------------------------:|:------------:|:-------------:|
|                1P/Lotto                |     `1PL`    |       72      |
|                 1P Only                |     `1PO`    |       27      |
|        Lotto only after initial        |     `LOI`    |       12      |
|        Lotto only after 1P clear       |    `LO1P`    |       23      |
|   Lotto only after all chars unlocked  |     `LOC`    |       10      |
|          1P/Lotto after 200 vs         |    `1PLVS`   |       16      |
| Lotto only after 250 trophies unlocked |     `LOT`    |        4      |
|            Special Trophies            |     `ST`     |       48      |

The first two categories and the `1PLVS` category are the 1P (single player) categories, but the special thing about this ategory is that the trophies that spawn in 1P modes must belong to that first category. Therefore, it would be ideal to pick up as many of the `1PL` and `1PLVS` trophies as possible before trying to get all the `1PO` trophies. All of the trophies that involve the lottery are denoted by the letter `L`, where all trophies that are only accessible via 1P or the lotto are followed by an `O`. Additionally, all trophies that are unlockable via the lottery and 1P modes are denoted as `1PL`.

All of the `ST` trophies are unlocked by completing different "achievements" of sorts, such as the Diskun trophy, which requires completing every Bonus except for the 1 million VS matches bonus. Here we can see that the total number of trophies that a player can get from just the lottery and 1P mode is $212$. Then, there are $3$ fighter trophies per fighter, making for $3 * 26$ (including Shiek) $= 78$ trophies, which combined with $212$ gives a total of $290$ trophies: the exact number of trophies needed in order to complete the speedrun. There is a catch here though; the game internally is prepared for $293$ trophies as there does exist a loop that runs specifically $293$ times to check for all the trophies. The reason is because $3$ trophies are considered Japanese exclusive trophies, which are not accessible on the NTSC 1.02 version of the game (this might need to be fact checked). Regardless, the game does still award the achievement for collecting all trophies upon collecting $290$ trophies, and so the all trophies speedrun is based on the player being awarded this achievement.

## How Does Melee Use RNG In The Lottery?

From these categories and requirements, we can now figure out how many trophies are available inside the Lottery. For example, at the very beginning of the game, there are $2$ lottery categories available: `1PL` and `LOI`, which gives a total of $72 + 12 = 84$ possible trophies. When the game starts for the first time on a new save, it automatically gives the player a random trophy from the `1PL` category. That means that on a new save, $\frac{83}{84}$ trophies are available in the lottery. This fraction is exactly what the game uses to determine whether a new trophy should be rolled or not; it takes the number of unowned trophies of the current number of possible lottery trophies and divides it by the current number of possible lottery trophies. Again, since the initial lottery pool is `1PL` and `LOI`, there are $72 + 12 = 84$ possible trophies, and since $1$ trophy is given to the player on the launch of the game, we get: $\frac{84 - 1}{84} = \frac{83}{84}$ as the probability that a player gets a new trophy from the lottery, which we'll round down to the nearest integer and then assign to a variable named `chance`. In **Table 1**, action number 5, which is the roll for success or failure is exactly what happens here: the `get_rand_int(100)` function is called and if the value returned is strictly less than `chance`, then the roll is a success. Fun fact: the probability of getting a new trophy is actually just $\lfloor$ `chance` $\rfloor$, which means that the stuff after the decimal point doesn't actually matter, which means that $3.14\%$ is equivalent to $3\%$.

When it comes to determining the actual trophy that's received from the lottery after the roll for success or failure, the game then iterates over a specific list of trophies which is dependent on success or failure. In the case of success, Melee then goes over the list of all trophies and saves the number of trophies which are not yet owned by the player and are available in the lottery which I'll name `rem_trophies`, passes `rem_trophies` into **Table 1**, Action number 6, which is the roll for the trophy. Then, of the list or array of trophies unowned but available in the lottery, `get_rand_int(rem_trophies)` is called in order to return a random trophy from that list. Lastly, dependent on the trophy, the game will call one more rng function to determine the trophy pose, however, this can vary from trophy to trophy as not all trophies have multiple poses. In the case that a failure was rolled instead, then the game follows the same process as above except instead of looking at trophies that are not yet owned and available in the lottery, the game instead looks at trophies that are already owned and available in the lottery. That way, it's going to guarantee that it'll return a new trophy on a success roll or a duplicate trophy on a failure roll.

## So What's The Fastest Way To Get The Trophies From The Lottery?

Because this is meant to be used for a speedrun and not just a showcase, optimizations will be necessary. Before we discuss possibilities, it's important to first define how speed even works in the lottery. So far, it's clear that adding more coins into the lottery machine takes more time, as each additional coin beyond $1$ coin will play an animation where it has to enter the machine. Additionally, the $3$ RNG calls per coin can also change the position of the coin, which might delay the start of the lottery animation. This is not entirely known, but also may not be worth considering as the time it would save would most likely not be worth it as we can simply aim to spend the fewest coins necessary. This is one of the first "minimization" goals that we can have with this algorithm: simply minimize the number of coins spent, and everything should be fine, right?

Another minimization problem that we can consider is minimizing the number of rolls that have to be made, but this problem is extremely complex because each roll creates a new universe of possibilities: for example, if we get a Barrel Trophy by spending $1$ coin, but we get a Barrel Cannon Trophy by spending $2$ coins, then all subsequent trophies in each scenario will be different because the index of each trophy after the one that was received would be different, and so on. One could even call it a set of 20 parallel universes which open up, or perhaps 20 possible universes collide at this multiversal junction such that only one can be chosen to be the desired path, which is fairly reasonable considering the fact that the sheer number of computations to fully analyze all possibilities would simply be $20^n$, where $n$ is the number of rolls that are being made.

Minimizing the number of rolls is probably even more important than just minimizing the number of coins spent, as the fewest number of rolls means that the least amount of time is spent rolling. For example, rolling $1$ coin costs about $3$ seconds, and even rolling $20$ coins costs about $5$ seconds. Therefore, rolling $20$ coins ends up taking even less than rolling $1$ coin twice, although there is the added cost of having to farm coins. That being said, being able to roll fewer times will generally save more time; consider the difference between resetting $3$ times and spending $1$ coin afterwards, which is $4$ rolls, or approximately $12$ seconds. If we can simply roll once and spend, for example, $20$ coins, it would only take $5$ seconds instead, which is a timesave that adds up at the end of this lottery segment, since it could happen multiple times. Also, depending on the number of times that a reset would occur, it could possibly even save on coins.

The issue with this minimization problem is the fact that the number of computations becomes impossible very quickly, as previously mentioned. Therefore with some new routing, the lottery has been pushed back to be just about the very last thing in the run (with the exception of collecting `1PO` trophies which should ideally be the very last thing to do) for a few reasons, in order of importance:

- collecting the `1PO` trophies still requires collecting all other trophies first, however, to save on time from rolling in the lottery, it would be fastest to simply collect every trophy in the lottery first and then collect the `1PO` trophies.
    - this routing is generally worth it since it makes rolling for trophies in the lottery a far simpler problem
    - previous work put into figuring out buckets and stuff for `1PO` trophies along with certain rules for which trophies would spawn made this look even more appealing of a route, however that research turned out to be incorrect after some testing. Regardless, this route is still nicer as it will make implementing `end_lotto.py` (which doesn't exist yet, but will soon) far simpler for myself while also being able to save more time compared to using the older and very inefficient `initial_lotto.py`.
- the lottery no longer significantly relies on RNG and therefore doesn't have to be done early with the exception of getting birdo, which can now be done with `initial_birdo.py`, which is a tool that is useful for other speedrun.com categories which would involve getting Birdo to unlock random stage selection.
- coins will naturally be generated as the run goes on, thus saving some time where coins might end up getting overgenerated.

# Reverse Seed Search (RSS): A New Type Of Problem

RSS is a new type of algorithm aimed at finding the RNG value of the game without using any tools which rely on directly reading memory values to figure out what the RNG value is. This is important because it prevents runners from directly manipulating the game's RNG value off screen, such that they get more desirable events which would not normally happen without direct memory manipulation. As a result, designing an algorithm to efficiently and correctly determine what the RNG value is via in-game events is important for purposes of integrity.

This type of algorithm already exists, and was first implemented by Judge9 using the character select screen (CSS), as randoming a new character would advance the RNG 2 times consistently, which made for a relatively straightforward algorithm which would search for the RNG value that would result in getting a specific sequence of characters. The minimum length of a sequence of random characters to determine what the RNG seed is $9$, but keep in mind that the total number of possible seeds is $2^{32}$, which is approximately $4.3$ _billion_ values to try. Fortunately there are only 25 possible values to keep track of, which makes the program generally simple but still very helpful to have. More information can be found in Judge9's video here: https://youtu.be/wuLz2QptDkY. I would highly recommend watching this as it gives a great overview of the CRSS (character selection screen reverse seed search -> character reverse seed search) problem and how it was approached. TauKhan also implemented a similar algorithm with a large amount of optimizations in order to achieve ridiculously quick times. Unfortunately they didn't post the code, so it isn't used right now, but Judge9's algorithm is more than enough and is used routinely for Peach's Break The Targets (BTT) speedrun, as well as a few other custom BTT Mismatch stages intended for Peach.

The next type of RSS algorithm is TagRSS, where generating player tags using the random button would advance the RNG 1 time. This problem became more complex as the game stores the 5 most recent unique tags that are rolled, and would internally reroll until it got a new tag. The internal rerolls wouldn't be displayed, so in order for a player to determine if they're on the correct seed, there could be quite a few rerolls in between each tag, or very few rerolls in between. As a result, I felt deterred and decided to skip this problem, but luckily TauKhan quickly picked up the problem and once again implemented an insanely optimized approach in Python that solves the problem ridiculously quickly. TauKhan's algorithm takes the 5 tags that a player rolls and figures out what the seed is by splitting up the possible seeds into buckets and determining whether certain seeds are viable by performing a series of linear transforms, which is generally predictable due to the nature of working with linear functions (recall that Melee's RNG uses an LCG, which is linear). This is the `tagrss.py` file in the repo.

And last but not least is my own RSS algorithm, or LottoRSS, designed specifically using the lottery functions that I previously described. The implmentation is fairly primitive and involves quite a bit of brute force, but it does get the job done (only with pypy though, as it takes quite literally forever with Python). This one is far more straightforward, as it simply involves determining the RNG by inputting the trophies that a player already has, and then inputting whatever trophies are returned by the lottery until the algorithm determines what seed the game is currently on. This is done by keeping track of whether the trophy received was a duplicate trophy, which means that we know that the roll for success or failure was a failure, and that the subsequent roll for the trophy gave a specific value, thus greatly narrowing the list of possible seeds as the probability of getting a duplicate is extremely low at the beginning of using the lottery. In the case that a trophy is not a duplicate, there are many more possible seeds, but the trophy that's received will still shrink the possible list of seeds considerably. Additionally, repeating this process will eventually determine what the current seed is; usually around 5 rolls are enough to figure out what the seed is. Considering that the current implementation is rather slow, it's better to use TauKhan's TagRSS algorithm, especially in the case of `initial_birdo.py`, and then inputting that into my lotto sim function to bypass the slow LottoRSS algorithm that I currently have.

# Thank You For Reading!

Chances are, I probably didn't explain something very well, or you might have questions. In that case, feel free to reach out to me!

Here's a list of people whose work I used along the way: Savestate, achilles1515, PracticalTAS, TauKhan, and gainge (aka Judge9).

This project would have never been possible if not for them, and a special shoutout to David V. Kimball for making his documentary video on Melee's All Trophies category, and for all the work that he's put into getting this to work in the first place.

Additionally, shoutouts to the Stadium Discord for being an awesome place where other speedrunners can enjoy a variety of different categories belonging to the same game and for being so welcoming to newcomers like myself who have tons of questions!

<3
