# Original work by Savestate
# Some of this code is adapted from gainge aka Judge9

from typing import Optional

# The following global values and constants are provided by Savestate, and the functions are slightly adapted from Savestate and Judge9
#@804d5f90
rng = 0x00000001
a = 214013
c = 2531011
m = 2**32

def get_rng() -> int:
    global rng
    return rng

def set_rng(val: int) -> None :
    global rng
    rng = val

# LCG:
# a = 214013
# c = 2531011
# m = 2^32
# Inputs:
# `@custom` is an int passed in to compute the next rng value after the custom value, unsaved. Defaults to -1, which will use the actual rng value and save it.
def next_rng(custom_rng_val: int = -1) -> int:
    if custom_rng_val == -1:
        global rng
        rng = (a*rng + c) % m
        return rng
    else:
        ret = (a*custom_rng_val + c) % m
        return ret

def get_rand_int(i: int, adv = True) -> int:
    temp_rng = next_rng() if adv else get_rng()
    top_bits = temp_rng >> 16
    return (i*top_bits) >> 16

def get_rand_float() -> int:
    temp_rng = next_rng()
    top_bits = temp_rng >> 16
    return top_bits / 65536

# this function is adapted from judge9
def rng_diff(src: int, tgt: int) -> int:
    if src == tgt:
        return 0
    
    step = 0
    temp_src = src
    temp_tgt = tgt
    
    while temp_src != tgt and temp_tgt != src:
        temp_src = next_rng(temp_src)
        temp_tgt = next_rng(temp_tgt)
        step += 1
    
    return step if temp_src == tgt else -1 * step

# The following functions are all made by myself.
# The code in the `old_code.py.example` file is a mix of my own and some from judge9.

def get_hex(tgt: Optional[int] = None) -> int:
    while True:
        # Get initial input
        val = input("Source RNG value: ") if tgt is not None else input("Target RNG value: ")
        val = val.replace(" ", "")
        
        if val.lower() == 'q': # Escape option
            print("Exiting.")
            quit(0)
        elif val.lower() == 'c' and tgt is not None: # Continue by using old tgt as new src
            if tgt == -1:
                print("Cannot continue off of previous value because you just started.")
            else:
                return tgt
        else:
            try:
                return int(val, 16)
            except ValueError:
                print(f'Invalid input: \'{val}\'.')

def use_coin() -> int:
    # This looks funny, but we're returning the rng value generated here at the end.
    next_rng()
    next_rng()
    return next_rng()

# Lottery simulator
def lotto_sim(num_owned_trophies: int, num_remaining_1p_lotto: int, src: int, trophies: list[list[str, int, bool]]) -> None:
    NUM_AVAILABLE_TROPHIES = 84
    set_rng(src)
    
    # Overall stats
    total_coins = 0
    resets = 0
    
    # Now we can start the lottery simulation.
    print(f'Beginning lottery simulation with seed {hex(src)[:-1]}')
    while num_remaining_1p_lotto > 0:
        # The purpose of the first call is just to randomize the position of the coin animation as it decreases to 00.
        get_rand_int(15)
        
        # Setting up variables to be used in the coin loop
        temp_rng = src = get_rng()
        coins = 0
        first_outcome_index = -1
        
        # The coin loop; determines how many coins to use to 1) get a trophy and 2) ensure that the trophy is in the 1p/lotto category
        while True:
            coins += 1
            
            # If we have to use more than 20 coins, just spend one to update the rng value and move on.
            if coins > 20:
                # Updating counters
                resets += 1
                total_coins += 1
                
                # Because we're just going to spend one coin, we can use the pre-computed first outcome.
                if first_outcome_index == -1:
                    print(f'Reset #{resets}. No ideal outcome. Just spend 1 coin to get a dupe trophy.')
                else:
                    print(f'Reset #{resets}. No ideal outcome. Just spend 1 coin to get {trophies[first_outcome_index][0]}')
                    trophies[first_outcome_index][1] = 0
                    num_owned_trophies += 1
                # Now we want to spend the one coin.
                # Before we can do that, remember that we already advanced the rng by a total of 20 coins.
                # So we need to reset our rng to the correct position.
                set_rng(src)
                use_coin()
                next_rng()
                next_rng()
                break

            # set rng to be src each time at the beginning
            set_rng(temp_rng)
            
            # 3 steps are called per coin. 
            temp_rng = use_coin()
            
            # Now the game determines whether this roll is sucessful or not. This changes depending on the following formula
            success_roll = get_rand_int(100)
            rem_trophies = NUM_AVAILABLE_TROPHIES - num_owned_trophies
            chance = int((rem_trophies / NUM_AVAILABLE_TROPHIES) * 100)
            if (success_roll < chance):
                # In this case, we get a new trophy.
                trophy_roll_rand_int = get_rand_int(rem_trophies)
                # The actual trophy that we roll is found by only counting through trophies that we dont have owned.
                # For example, if we roll `15` (0-indexed), then the actual trophy that we get is not just the `15`th trophy (0-indexed), but it's the `15`th (0-indexed) *unowned* trophy.
                # We'll use `trophy_roll_actual_index` to store the actual index of the trophy that we roll in the big Trophies list above.
                # And we'll reuse `trophy_roll_rand_int` as a counter to let us know when we've gone through that number of unowned trophies.
                trophy_roll_actual_index = -1
                for t in trophies:
                    trophy_roll_actual_index += 1
                    if t[1] == 1:
                        trophy_roll_rand_int -= 1
                        if trophy_roll_rand_int == -1:
                            break
                # At the end of this loop, `trophy_roll_actual_index` should give us the index of the trophy in the big Trophies list that we actually rolled, and not just `get_rand_int(x)`.
                # If the boolean field in the trophies tuple is True and it is not owned, then we want to use this number of coins.
                if trophies[trophy_roll_actual_index][2] and trophies[trophy_roll_actual_index][1] == 1:
                    print(f'{coins} -> {trophies[trophy_roll_actual_index][0]}')
                    # Mark that we now own the trophy and update counters.
                    trophies[trophy_roll_actual_index][1] = 0
                    num_owned_trophies += 1
                    num_remaining_1p_lotto -= 1
                    total_coins += coins
                    break
                elif coins == 1:
                    first_outcome_index = trophy_roll_actual_index
                # Note that we don't use an else case here, because we did not get a trophy in the 1p/lotto category, so we loop again.
            # Similarly, we don't use an else case here because we did not get a new trophy, so we loop again.
        # Now, the game advances the RNG one more time to determine the pose of the received trophy.
        next_rng()
    
    print('-------------------------------')
    print('Results')
    print('-------------------------------')
    print(f'Total trophies collected: {num_owned_trophies}')
    print(f'Total number of resets: {resets}')
    print(f'Total coins spent {total_coins}')

# RSS algrorithm
def rss(init_possible_seeds: list[int], trophy_roll_cond_amt: int, successful: bool, chance: int, trophy_roll_int: int) -> list[int]:
    ret = []
    for i in init_possible_seeds:
        set_rng(i)
        get_rand_int(15)
        use_coin()
        temp_success_roll = get_rand_int(100)
        temp_trophy_roll = get_rand_int(trophy_roll_cond_amt)
        if successful and temp_success_roll < chance and temp_trophy_roll == trophy_roll_int:
            next_rng()
            ret.append(get_rng())
        elif not successful and temp_success_roll >= chance and temp_trophy_roll == trophy_roll_int:
            next_rng()
            ret.append(get_rng())
    return ret

# Simple function to append to a string depending on some trophy flags
def trophy_str(t: list[str, int, bool]) -> str:
    ret = f'- {t[0]} '
    if t[1] == 0:
        ret += f' (owned)|'
    else:
        ret += f' (new)|'
    return ret

def main():
    # Initial trophy list: [trophy_name, not_owned=1/owned=0, 1p_lotto=True/lotto_only=False]
    trophies = [['ray gun', 1, True], ['super scope', 1, True], ['fire flower', 1, True], ['star rod', 1, True], ['home-run bat', 1, True], ['fan', 1, True], 
                ['red shell', 1, False], ['flipper', 1, True], ['mr. saturn', 1, True], ['bob-omb', 1, True], ['super mushroom', 1, True], ['starman1', 1, True], 
                ['barrel cannon', 1, True], ['party ball', 1, True], ['crate', 1, True], ['barrel', 1, True], ['capsule', 1, True], ['egg', 1, True], ['squirtle', 1, True], 
                ['blastoise', 1, True], ['clefairy', 1, True], ['weezing', 1, True], ['chansey', 1, False], ['goldeen', 1, True], ['snorlax', 1, True], 
                ['chikorita', 1, True], ['cyndaquil', 1, True], ['bellossom', 1, True], ['wobbuffet', 1, True], ['scizor', 1, True], ['porygon2', 1, True], 
                ['toad', 1, True], ['coin', 1, True], ['kirby hat 1', 1, True], ['kirby hat 2', 1, True], ['kirby hat 3', 1, True], ['lakitu', 1, True], 
                ['birdo', 1, True], ['klap trap', 1, True], ['slippi toad', 1, True], ['koopa troopa', 1, True], ['topi', 1, True], ['metal mario', 1, True], 
                ['daisy', 1, True], ['thwomp', 1, True], ['bucket', 1, True], ['racing kart', 1, True], ['baby bowser', 1, True], ['raphael raven', 1, True], 
                ['dixie kong', 1, False], ['dr. stewart', 1, True], ['jody summer', 1, True], ['andross 64', 1, True], ['metroid', 1, True], ['ridley', 1, True], 
                ['fighter kirby', 1, False], ['ball kirby', 1, True], ['waddle dee', 1, True], ['rick', 1, True], ['jeff', 1, False], ['starman2', 1, True], 
                ['bulbasaur', 1, True], ['poliwhirl', 1, True], ['eevee', 1, False], ['totodile', 1, True], ['crobat', 1, True], ['igglybuff', 1, True], 
                ['steelix', 1, True], ['heracross', 1, True], ['professor oak', 1, False], ['misty', 1, False], ['zero-one', 1, True], ['maruo maruhige', 1, False], 
                ['ryota hayami', 1, True], ['ray mk ii', 1, False], ['heririn', 1, True], ['excitebike', 1, True], ['ducks', 1, True], ['bubbles', 1, False], 
                ['eggplant man', 1, False], ['balloon fighter', 1, True], ['dr. wright', 1, True], ['donbe & hikari', 1, True], ['monster', 1, True]]
    
    # the game starts off with 1 trophy already owned.
    num_owned_trophies = 0
    num_remaining_1p_lotto = 72
    NUM_AVAILABLE_TROPHIES = 84
    
    # In a run, some 1p/lotto trophies have already been collected.
    # The user should input these trophies; substrings will be allowed but the user should be careful.
    # Note that if any trophies not in the initial lotto pool are entered, then they will be ignored for now.
    # Exit the loop by entering 'x' or 'q'.
    # Careful about `barrel` -> barrel / barrel cannon, or `ball` -> party ball or ball kirby, etc.
    owned_trophy = input("Type the names of the trophies that you've collected in the gallery. Substrings are allowed, but be careful. Type 'x' or 'q' to finish.\n")
    while owned_trophy.lower() != 'x' and owned_trophy.lower() != 'q':
        found = False
        multiple_trophies = ''
        substr_matches = 0
        
        for i, t in enumerate(trophies):
            exact_match = False
            
            if owned_trophy in t[0]:
                exact_match = owned_trophy == t[0]
                if not exact_match:
                    multiple_trophies += trophy_str(t)
                    substr_matches += 1
                    # Check if there are other trophies with the same substring.
                    for t_ in trophies[i+1:]:
                        if owned_trophy in t_[0]:
                            if owned_trophy == t_[0]:
                                exact_match = True
                            multiple_trophies += trophy_str(t_)
                            substr_matches += 1
                    # If so, then do not proceed; break immediately and reprompt.
                    if not exact_match and substr_matches > 1:
                        multiple_trophies = multiple_trophies[:-1].replace("|", "\n")
                        print(f"These trophies contain the substring '{owned_trophy}':\n{multiple_trophies}\nPlease retype the trophy name:")
                        break
                    if exact_match:
                        continue
                t[1] = 0
                print(f'{t[0]} collected!')
                num_owned_trophies += 1
                found = True
                if t[2]:
                    num_remaining_1p_lotto -= 1
                break
        else:
            if not found:
                print(f'Could not find {owned_trophy}. If this is a 1p only trophy, ignore this message. Otherwise, double check your input.')
        owned_trophy = input("")
    
    # Now begins the RSS for lotto section.
    # Here, the idea is that the user will spend x coins on the lottery to receive some trophies.
    # There are 2 visual aspects of each roll that we can use:
    #   The roll's success (aka new trophy is rolled, or an old trophy is rolled)
    #   The actual trophy received
    # Both of these outcomes can help us to find whatever seed we're currently at.
    # The ideal outcome would be that the first roll is rejected, as that would significantly cut down on the portion of seeds to calculate.
    # For now, I'll still implement a basic algorithm to just test every seed.
    # Before we do that though, we need to collect the user's input.
    possible_seeds = []
    first_run = True
    
    print("Input the results of using the lottery.")
    while len(possible_seeds) != 1:
        trophy_roll_name = input("Trophy received from lotto:\n")
        successful = False
        
        found = False
        trophy_roll_int = -1
        orig_owned_trophies = num_owned_trophies
        
        # Validating trophy received from lotto and updating counters/flags
        while not found:
            multiple_trophies = ''
            substr_matches = 0
            for i, t in enumerate(trophies):
                # `trophy_roll_int` is a counter to help figure out what the result of the get_rand_int() function as we only get the actual trophy name.
                # Because the field at t[1] is 1 if we own it, and is 0 otherwise, then we know that if the roll is a new trophy, then the
                # sum of the t[1] values will tell us what index we're at since it "skips" counting the trophies that are already owned.
                trophy_roll_int += t[1]
                exact_match = False
                
                if trophy_roll_name in t[0]:
                    exact_match = trophy_roll_name == t[0]
                    if not exact_match:
                        multiple_trophies += trophy_str(t)
                        substr_matches += 1
                        # Check if there are other trophies with the same substring.
                        for t_ in trophies[i+1:]:
                            if trophy_roll_name in t_[0]:
                                if trophy_roll_name == t_[0]:
                                    exact_match = True
                                multiple_trophies += trophy_str(t_)
                        # If so, then do not proceed; break immediately and reprompt.
                        if not exact_match and substr_matches > 1:
                            multiple_trophies = multiple_trophies[:-1].replace("|", "\n")
                            trophy_roll_name = input(f"These trophies contain the substring '{trophy_roll_name}':\n{multiple_trophies}\nPlease retype the trophy name:")
                            break
                        if exact_match:
                            continue
                    # If the trophy is not owned yet, then the roll is 'succesful' as it's a new trophy.
                    successful = t[1] == 1
                    if successful:
                        t[1] = 0
                        num_owned_trophies += 1
                        if t[2]:
                            num_remaining_1p_lotto -= 1
                    else:
                        # On the other hand, if the trophy is owned, then we know that it must be the `i - trophy_roll_int - 1`th unowned trophy.
                        trophy_roll_int = i - trophy_roll_int - 1
                    print(f'{t[0]} collected!')
                    found = True
                    break
            # If the trophy was not found at all, then the user must be reprompted.
            if not found:
                print(f'Could not find {trophy_roll_name}')
                trophy_roll_name = input("Trophy received from lotto:\n")
        
        trophy_roll_cond_amt = NUM_AVAILABLE_TROPHIES - orig_owned_trophies if successful else orig_owned_trophies
        chance = int((trophy_roll_cond_amt / NUM_AVAILABLE_TROPHIES) * 100)

        print('Beginning computations...')
        # only iterate thru all 4 billion possible values on the first run
        if first_run:
            possible_seeds = rss(range(2**32), trophy_roll_cond_amt, successful, chance, trophy_roll_int)
            first_run = False
        else:
            possible_seeds = rss(possible_seeds, trophy_roll_cond_amt, successful, chance, trophy_roll_int)
        
        print(f'num of possible seeds: {len(possible_seeds)}')
        
        if len(possible_seeds) == 0:
            print('No seeds found, either there\'s a bug or you misinput something. Try rerunning the program and be careful with your inputs.')
            quit()
    
    print(f'The current seed is: {possible_seeds[0]}')
    # Now that we have exactly 1 seed, we can now run the lottery simulator.
    lotto_sim(num_owned_trophies, num_remaining_1p_lotto, possible_seeds[0], trophies)
    print('\nProgram finished. At the moment, there is no course correction, so please try to input the correct trophies!')

# def main():
#     # gets the number of steps between seeds
#     src = get_hex()
#     tgt = get_hex()
#     print(rng_diff(src, tgt))
    
if __name__ == "__main__":
    main()