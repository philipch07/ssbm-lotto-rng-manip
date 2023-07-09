# ssbm-lotto-rng-manip

This is a project aimed at understanding SSBM's lottery minigame, as well as the underlying rng functions that SSBM uses.

Watch the below video for a live example.

https://youtu.be/nilRjbvIG4Y

---

# Check Out Other SSBM Tools!
https://github.com/Olivia926/All_Trophies_Help

That's the collection of tools which are relevant to SSBM's All Trophies any% speedrun.

For the time being, I'll keep this repo updated since I prefer working with smaller repos, which I'll then merge into that repo.

---

# Getting Started
You *should*, and big emphasis on *should* use pypy instead of Python. The reason is simple: the first iteration of the rss algorithm goes over all 4.3+ billion possible seeds. The algorithm does quickly decrease in the volume of computations after that, but if you use regular Python, it'll take a ridiculous amount of time to finish the very first computation. Because I don't feel like dealing with managing memory myself, I wrote this in Python and not C. The good news is that pypy basically converts Python to C in a smart way, and then runs the translated code, which runs way faster, while also having vastly improved garbage collection strategies compared to other libraries like Cython.

## Setting up pypy
First, head over to https://www.pypy.org/download.html and select the desired version of pypy for whatever OS you're using. Then, extract the folder.
From here, I just decided to place the pypy folder *inside* of my Python310 folder, that way I wouldn't lose where my pypy is. Fortunately, the current available version of pypy is 3.10 as well, which is perfect. For example, my folder is located at: `C:\Python310\pypy3.9-v7.3.11-win64`.

## Using pypy as the interpreter
In VSC, take a look at the bottom left of the window where it says something like `3.10.X`, which is your current Python version (it's to the RIGHT of `Python`, and NOT the `Python` text itself), and click on it. In the top-middle of your screen should be a dropdown asking you to select your interpreter. Here, you're going to want to click `Find Interpreter Path` and then click `Browse`, then navigate to the pypy folder, and then select the `pypy.exe` within the pypy folder. Now you're all set up!

---

## TODO (ordered by importance):
- Improve alg for lotto sim to minimize time spent (and also coins spent, if reasonable)
- Implement course correction (e.g. calculate the current seed after misinputting the number of coins and rerun the algorithm)
- Modify or create a new function to be used where the user is looking to unlock ALL trophies via the lotto (at the end of the speedrun)
- Implement multiprocessing for rss

For those curious about RSS (random seed search):
RSS is a type of algorithm that aims to find the current random seed, or rng value, of the current game via a sequence of inputs which involve random events. This is important because the rng value will determine what the outcome of a "random" event is. For example, if someone wants a random integer, the random seed will be involved. Additionally, due to previous work from the community, we know how the random seed is used in *some* functions, and using Dolphin's debugger, the random seed can be directly accessed in memory. However, when it comes to speedruns, accessing specific values in the game's memory via an external tool is not viable, hence the requirement to somehow determine what the random seed is by using a sequence of random in-game events.

---
# An In-Depth Explanation of SSBM's RNG system
As you can probably gather from quite a few different sources around the internet, the rng system used by Melee relies on a value being stored and being manipulated by certain functions to produce some desired values. To be more precise, the RNG value, or seed, is at the heart of what drives randomness, and we know that this value advances in a somewhat linear way, via a function called a Linear Congruent Generator. The purpose of the LCG function is to attempt to return every single value from 0 up to some limit, which in SSBM's case is $2^{32}$, such that no value is repeated along the way, and the values returned are in some generally "random" order. That means that naive approaches which would simply list $0$ through $2^{32} - 1$ would be far too "predictable" when it comes to random events. As a result, a better way of going about this would be to use an LCG, which you can easily Google or search on Wikipedia as it is a common and fairly simple topic in the field of cryptography.

In Melee, the LCG has already been discovered to be the following function:

$seed = ((a * seed) + c) \% m$

Where $a = 214013$, $c = 2531011$, and $m = 2^{32}$.

As previously stated however, this is only the heart of what is used to generate random events. The next step is to use this seed to generate a desired number. For example, if we want to pull a random number from $[0, 100)$ (that is, including $0$ and excluding $100$), but our seed value is $123456$, Melee doesn't say that the random number that we get from $[0, 100)$ is just $123456$. Instead, Melee calls a function that takes our current seed, manipulates it to generate a number within the ranges of $[0, 100)$, and then returns that newly generated number.

There are two functions where this happens, both of which have been named by the community, but I personally call them the `get_rand_int()` and `get_rand_float()` functions (to be explicit, they are the "get random integer" and "get random float" functions). As noted by Savestate, the `get_rand_int()` function is used generally more often for purposes that we're interested in, whereas `get_rand_float()` seems to have something to do with CPU behavior, but I haven't been able to get any more info on that function. Regardless, we have our sights set on the `get_rand_int()` function, and this is what we're most interested in right now.

## So How Does This Tie Into The Lottery?
From messing around with the lottery using some of Judge9's scripts, Dolphin-memory-engine, and Dolphin's debugging mode, I was able to figure out that the lottery causes the seed to change by 7 intervals every time 1 coin was used to perform a single roll. That number then changed to 10 intervals per 2 coins for a single roll, 13 coins for a single roll, and so on. I then managed to make some reasonable guesses as to how the rng functions were involved in the lottery minigame:

`3 steps` (aka 3 calls to the `get_rand_int()` function) would be performed per each coin, to randomize where their `x`, `y`, and `z` coordinates are when they spawn in for the animation where they enter the lottery machine. After those $3 *$ `number of coins spent` steps are made, then one call is made to determine the success or failure of the roll (that is, whether the trophy is new or not), then one call to determine the actual trophy that the player will receive, and then one call to determine the pose of the trophy (as some trophies have multiple poses). We can make a simple table to illustrate what the internal system looks like and what functions are being called when we roll for a trophy using only **ONE** coin:

| Table 1: Lottery Actions and RNG Calls |
|------------------------------------------|

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

Note here that the table isn't totally linear. Instead, it's meant to be interpreted as follows: `seed_0` is passed into the action at Action Number 1, and `seed_1` is the seed *after* the action at Action Number 1 is completed. To say this a different way, `seed_0` is passed into the `get_rand_int(15)` function, which then *advances* the seed to become whatever `seed_1` is, while also returning some random integer in the range $[0, 15)$.

If we instead think about this in a more continuous way via a loop, we can basically "connect" `seed_7` above and `seed_0`, and let a function simply loop over all of this, which allows us to effectively predict what the RNG value will be at each step of the lottery. Therefore, all that's left is to figure out how exactly the RNG values are used by the `get_rand_int()` functions, and how we can fully simulate the lottery minigame itself!

# Figuring Out The Lottery

In simulating the lottery, we know that the RNG values are predictable at each step, and because we know exactly how the `get_rand_int()` functions work, we can also figrue out exactly what those functions return, which means that there shouldn't be anything else that we have to worry about... right?

Nope! This gets a bit more complicated, but also significantly more interesting. The trophies that a player can get are split up into a few different categories. These are:

| Table 2: Lottery Trophy Categories |
|------------------------------------------|

|              Category Name             | Abbreviation | # of Trophies |
|:--------------------------------------:|:------------:|:-------------:|
|                1p/lotto                |     `1PL`    |       72      |
|                 1p Only                |     `1PO`    |       27      |
|           Lotto only initial           |     `LOI`    |       12      |
|        Lotto only after 1p clear       |    `LO1P`    |       23      |
|   Lotto only after all chars unlocked  |     `LOC`    |       10      |
|         Lotto only after 200 vs        |    `LOVS`    |       16      |
| Lotto only after 250 trophies unlocked |     `LOT`    |       4       |
|            Special Trophies            |     `ST`     |       48      |

The first two categories are the 1p categories, but the special thing about the first category is that the trophies that spawn in 1p modes must belong to that first category. Therefore, it would be ideal to pick up as many of the `1PL` trophies as possible before trying to get all the `1PO` trophies. All of the trophies that involve the lottery are trophies that can only be found in the lottery, with the exception of the first category. And all of the `ST` trophies are unlocked by completing different "achievements" of sorts, such as the Diskun trophy, which requires completing every Bonus except for the 1 million VS matches bonus. Here we can see that the total number of trophies that a player can get from just the lottery and 1p mode is $212$. Then, there are $3$ fighter trophies per fighter, making for $3 * 26$ (including Shiek) $= 78$ trophies, which combined with $212$ gives a total of $290$ trophies: the exact number of trophies needed in order to complete the speedrun.

## How Does Melee Use RNG In The Lottery?

From these categories and requirements, we can now figure out how many trophies are available inside the Lottery. For example, at the very beginning of the game, there are $2$ lottery categories available: `1PL` and `LOI`, which gives a total of $84$ possible trophies. When the game starts for the first time on a new save, it automatically gives the player a random trophy from the `1PL` category. That means that on a new save, $\frac{83}{84}$ trophies are available in the lottery. This fraction is exactly what the game uses to determine whether a new trophy should be rolled or not; it takes the number of unowned trophies of the current number of possible lottery trophies and divides it by the current number of possible lottery trophies. So, since the initial lottery pool is `1PL` and `LOI`, there are $72 + 12 = 84$ possible trophies, and since $1$ trophy is given to the player on the launch of the game, we get: $\frac{84 - 1}{84} = \frac{83}{84}$ as the probability that a player gets a new trophy from the lottery, which we'll call `chance`. In **Table 1**, action state 4, which is the roll for success or failure is exactly what happens here: the `get_rand_int(100)` function is called and if the value returned is strictly less than `chance`, then the roll is a success. Fun fact: the probability of getting a new trophy is actually just $\lfloor$`chance`$\rfloor$, that is, `chance` rounded down to the nearest whole number (which is the same as `chance` with the decimals truncated).

## Why Not Get Every Possible Trophy?

Now that we know if we get a new trophy versus an old trophy, does it even matter what trophy we get? The answer is that the actual trophy that we get doesn't matter as much as the category that the trophy belongs to. Referring to **Table 2**, we can see that there are quite a few categories, but each of these categories actually unlock within the lottery in the order that they're listed (with the exception of `1PO` and `ST` not being unlockable in the lottery). The exact function for how this happens isn't fully known since I didn't spend a lot of time exploring it, but the behavior is known and works as follows. `1PL` and `LOI` both fill the lottery system to begin, for a total of $84$ trophies. Once all the trophies in the `LOI` category (and yes, specifically the `LOI` category only) are owned by the player, then the `LOIP` category is unlocked, regardless of the requirement being fulfilled, thus increasing the total number of trophies in the lottery to $107$. Then, after ALL $107$ trophies from `1PL`, `LOI`, and `LOIP` are owned, then the $16$ trophies from the `LOVS` category are added, also bypassing the requirement being fulfilled. After all the trophies from the `LOVS` category are owned, then the $10$ trophies from the `LOC` category are added, regardless of the requirement being fulfilled. At this point, the very last category that can be added to the lottery is the `LOT` category, which has only $4$ trophies, but unlike all the aforementioned categories, the `LOT` category *only unlocks from the player owning 250 trophies*.

Unfortunately, simply unlocking every trophy from the lottery is not the best way about this. The reason is because of how the routing works: ideally all the trophies from the `1PL` category are gathered from the lottery, such that a runner can go ahead and grind out the trophies in the `1PO` category. The reason why this is considered a grind is because the approach for gathering the `1PO` trophies is still rather primitive; and the most recent world record (Olivia's 14h24m27s) used a strategy involving Puff in order to gather trophies by stomping on every goomba in the first stage of Adventure mode (aka "Adventure 1-1") while looking for the trophy that spawns on the stage, which I recently found was significantly slower than just using Falcon, which Olivia also combined with focusing on primarily gathering the trophy that spawns on the stage instead, which saves a significant amount of time. Some preliminary testing was done to see what trophies would spawn on Adventure 1-1, and it was discovered that `1PO` trophies would be more likely to spawn if the trophies in the `1PL` were already owned, which would save more time, however, I recently discovered that the trophies that spawn on the stage can be manipulated via rng, but quite a few more hours across multiple days will have to go into that in order for us to figure out how to better optimize that segment. And going back to the lottery, as explained in the previous paragraph, getting the trophies in the `LOI` category will increase the number of trophies in the lottery, thus decreasing the likelihood of getting the remaining trophies from the `1PL` category.

I'm not actually sure if this segment is useful because of the fact that the stage trophies themselves can simply be RNG manip'd, but I'll continue on with our current assumption that a runner will get the `1PL` trophies and then complete the `1PO` category, and then return to the lottery at the end of the run. Regardless, this sets up the foundation for the problem at hand, and it perfectly sets up how action state 5 from **Table 1** works (the roll for the actual trophy): it calls `get_rand_int(rem_trophies)`, where `rem_trophies` is the number of remaining trophies in the current lottery pool which are not yet owned by the player. This is the most complex part of the problem because it's a variable, and it also means that the result changes depending on the current state, thus expanding this from a problem of "How do we guarantee that we get a new trophy each time?" to "Now that I know we roll a new trophy, how do I make sure we get the exact trophy that we want?" type of problem.

Melee also approaches this in a somewhat strange way: it holds a list of all possible trophies, and of the trophies that are currently able to be gotten in the lottery, it sets a flag to true or false. Then, it also keeps track of which trophy is currently owned. Now when a number, which we'll call `num`, is rolled between $[0, $ `rem_trophies`$)$ (by the `get_rand_int(rem_trophies)` function call, as mentioned earlier), the game then loops over all *unowned* trophies while counting until it hits the number `num` from earlier, at which point it picks the current trophy and tells some other functions to display that trophy, which is what action state 6 is: a roll for the trophy pose when it's displayed on screen. Technically the fastest way to handle this would be to benchmark how long each trophy pose takes to render, as it may be possible that not all trophy poses render in the same amount of time, possibly in the same way how something like a Kirby Hat 1 trophy takes significantly longer than a Capsule trophy, as the time for certain shaders to compute over a different set of polygons might be something to think about. Regardless, it may not be worth thinking about over some other factors which I'll mention soon. Also, another way to think about how the game finds which trophy to return is by thinking about it keeping two lists; the list of unowned trophies in the current lottery pool, such that the int returned by `get_rand_int(rem_trophies)` can give you the trophy returned by using that as the index in the list. For memory concerns, it's technically more ideal to just reuse the existing list and keep a flag (aka a boolean) to keep track of whether a trophy is owned or not. And fortunately, this logic is also very similar for if the roll is unsuccessful; I forgot to mention earlier that this entire paragraph is running under the assumption that the roll for success/failure (action state 4 from **Table 1**) is successful. In the case that the roll is unsuccessful, the game runs a function call via `get_rand_int(num_owned_trophies)`, where  `num_owned_trophies` is the number of owned trophies, as the name suggests, and the previous logic can be translated for how the game determines which duplicate trophy should be returned, however, we don't really have to worry about this since it's generally not worth computing or worrying about.

# Recap \#1!

Now that all of this has been said, there are three major things to focus on inside of the fact that there are $3 * $ `num_coins` $+ 3$ rng advances when a lottery roll happens. The first is that we need to keep track of ensuring that a roll is successful. The second is that we need to keep track of the fact that the trophy that we get is desired, aka it should be in the `1PL` category, and not the `LOI` category. And lastly, the previous concern is dependent on what trophies the player currently has. The last point is the most important, as because a player can input up to $20$ coins in one lottery roll, if we wish to compute the most optimal way for a player to get all $71$ (because one trophy is already owned given to the player when booting the game) `1PL` trophies, that would take $20^{71}$ computations, purely for figuring out what the results are. This doesn't even bring into the picture the concern about memory, RAM, computation power, let alone the fact that it's many magnitudes larger than the number of atoms in the obeservable universe (a quick search says $10^{78}$ to $10^{82}$). So, like any other normal person, I've implemented a greedy algorithm that simply searches for the first possible number of coins that's needed to unlock a `1PL` trophy, and if no trophy can be found within a $20$ coin window, then I tell the player to "reset", which is, to simply input $1$ coin: a cheap way to change the current RNG value such that a set of up to $20$ new possibilities can be computed.

This section is under development and will slowly be developed as I have free time, so please be patient!

---
# Thank You For Reading!

Here's a list of people whose work I used along the way: Savestate, achilles1515, PracticalTAS, TauKhan, and gainge (aka Judge9).

This project would have never been possible if not for them, and a special shoutout to David V. Kimball for making his documentary video on Melee's All Trophies category, and for all the work that he's put into getting this to work in the first place.

Additionally, shoutouts to the Stadium Discord for being an awesome place where other speedrunners can enjoy a variety of different categories belonging to the same game and for being so welcoming to newcomers like myself who have tons of questions!

<3