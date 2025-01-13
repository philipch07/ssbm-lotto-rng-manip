import copy
import random
from globals import TAGS, TROPHIES_1PL_LOT, DSTAR
from globals import get_trophies, get_seed, print_tags

# this is meant to get 83/84 of the initial trophies because of reasons that were not explained to me.
# the way this is accomplished is by keeping track of the LOT trophies that are collected, and ensuring that we only ever get 11/12 of them.
# thus the last uncollected trophy is from LOT.

# this also features a new algorithm where fewer coins are spent due to this being run at the beginning of a run.
# note that the greedy algorithm is also toggleable here. (CLI option: confirm trophy, toggle greedy, or toggle coin_saver)

def update_spending_log(coin_count):
    log_file = "coin_spending_log_3_coins.txt"
    spending_data = {}

    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                coin, count = line.strip().rstrip(",").split(": ")
                spending_data[int(coin)] = int(count)
    except FileNotFoundError:
        spending_data = {i: 0 for i in range(1, 21)}

    # Update the spending data
    spending_data[coin_count] += 1

    # Write updated data back to the file
    with open(log_file, "w") as file:
        for coin, count in spending_data.items():
            file.write(f"{coin}: {count},\n")


def coin_step(trophies, clot: int, coins_spent: list[int], seed: int, coins_to_spend):
    chance = int((len(trophies) / 84) * 100)
    temp_seed = (DSTAR[coins_to_spend][0] * seed + DSTAR[coins_to_spend][1]) & 4294967295
    trophy_idx = -1
    invalid = False
    if (100 * temp_seed >> 16) >> 16 < chance:
        # 1 step for trophy roll
        trophy_idx = (len(trophies) * ((214013 * temp_seed + 2531011) & 4294967295) >> 16) >> 16
        # if the trophy is LOT, add it to the count. if this is the LAST LOT trophy, do not accept it.
        # if clot != 11 -> accept the trophy and add clot count if necessary
        # else -> if not LOT, then accept the trophy
        #      -> else do not accept the trophy -> FLAG BRANCH AS INVALID ??
        if clot != 11:
            clot += not trophies[trophy_idx]
        else:
            if not trophies[trophy_idx]:
                invalid = True
    if not invalid:
        # 2 steps to realign rng
        seed = (2851891209 * temp_seed + 505908858) & 4294967295
        coins_spent.append(coins_to_spend)
    
    if trophy_idx == -1:
        # print get dupe trophy
        return trophies, clot, coins_spent, seed, invalid
    if not invalid:
        del trophies[trophy_idx]
    return trophies, clot, coins_spent, seed, invalid


def main():
    debug = True
    a = 1000 if debug else 1
    for iteration in range(a):
        trophies = [['ray gun', True], ['super scope', True], ['fire flower', True], ['star rod', True], ['home-run bat', True], ['fan', True], 
                    ['red shell', False], ['flipper', True], ['mr. saturn', True], ['bob-omb', True], ['super mushroom', True], ['starman mario', True], 
                    ['barrel cannon', True], ['party ball', True], ['crate', True], ['barrel', True], ['capsule', True], ['egg', True], ['squirtle', True], 
                    ['blastoise', True], ['clefairy', True], ['weezing', True], ['chansey', False], ['goldeen', True], ['snorlax', True], 
                    ['chikorita', True], ['cyndaquil', True], ['bellossom', True], ['wobbuffet', True], ['scizor', True], ['porygon2', True], 
                    ['toad', True], ['coin', True], ['kirby hat 1', True], ['kirby hat 2', True], ['kirby hat 3', True], ['lakitu', True], 
                    ['birdo', True], ['klap trap', True], ['slippi toad', True], ['koopa troopa', True], ['topi', True], ['metal mario', True], 
                    ['daisy', True], ['thwomp', True], ['bucket', True], ['racing kart', True], ['baby bowser', True], ['raphael raven', True], 
                    ['dixie kong', False], ['dr. stewart', True], ['andross 64', True], ['metroid', True], ['ridley', True], 
                    ['fighter kirby', False], ['ball kirby', True], ['waddle dee', True], ['rick', True], ['jeff', False], ['starman earthbound', True], 
                    ['bulbasaur', True], ['poliwhirl', True], ['eevee', False], ['totodile', True], ['crobat', True], ['igglybuff', True], 
                    ['steelix', True], ['heracross', True], ['professor oak', False], ['misty', False], ['zero-one', True], ['maruo maruhige', False], 
                    ['ryota hayami', True], ['ray mk ii', False], ['heririn', True], ['excitebike', True], ['ducks', True], ['bubbles', False], 
                    ['eggplant man', False], ['balloon fighter', True], ['dr wright', True], ['donbe & hikari', True], ['monster', True]]
        total_coins = 0
        if debug:
            seed = random.randint(0, 4294967295)
        else:
            seed = get_seed()[0]
        count_lot = 0
        
        while len(trophies) != 1:
            # print(f"Remaining trophies: {len(trophies)}")
            temp_seed = seed
            # temp_trophies = trophies
            # mode = input("[y] for greedy, anything else for coin saver: ").lower() == "y"
            mode = False
            
            if mode:
                # greedy mode
                chance = int((len(trophies) / 84) * 100)
                trophy_idx = -1
                coins = 0
                # advance twice
                temp_seed = (2851891209 * seed + 505908858) & 4294967295
                for i in range(20):
                    # 3 steps for success/failure roll
                    temp_seed = (-3124220955 * temp_seed + 3539360597) & 4294967295
                    if (100 * temp_seed >> 16) >> 16 < chance:
                        # 1 step for trophy roll
                        trophy_idx = (len(trophies) * ((214013 * temp_seed + 2531011) & 4294967295) >> 16) >> 16
                        # if the trophy is LOT, add it to the count. if this is the LAST LOT trophy, do not accept it.
                        if count_lot != 11:
                            count_lot += not trophies[trophy_idx][1]
                        else:
                            if not trophies[trophy_idx][1]:
                                continue
                        coins = i + 1
                        total_coins += i + 1
                        # 2 steps to realign rng
                        seed = (2851891209 * temp_seed + 505908858) & 4294967295
                        if debug:
                            update_spending_log(coins)
                        break
                if trophy_idx == -1:
                    coins += 1
                    total_coins += 1
                    # print("No new trophy, spend 1 coin to advance rng.")
                    # advance by 7 to account for lack of trophy -> inputting 1 coin to advance rng
                    seed = (203977589 * seed + 548247209) & 4294967295
                    if debug:
                        update_spending_log(1)
                else:
                    # confirm trophy has been receieved
                    # print(f"spend {coins} coins to get trophy: {trophies[trophy_idx][0]}")
                    if debug:
                        del trophies[trophy_idx]
                    else:
                        trophies = get_trophies(trophies, trophies[trophy_idx][0])
            else:
                max_depth = 9
                max_breadth = 3
                initial_trophy_count = len(trophies)
                max_new_trophies = 0
                min_coins_spent = 999
                best_path = []
                queue = []
                for i in range(max_breadth):
                    queue.append((copy.deepcopy([t[1] for t in trophies]), copy.deepcopy(count_lot), copy.deepcopy([]), copy.deepcopy(seed), i + 1))
                while len(queue) > 0:
                    # print(len(queue))
                    q = queue.pop(0)
                    c = coin_step(*q)
                    # invalid check
                    if not c[4]:
                        if len(c[2]) == max_depth or len(c[2]) == len(trophies):
                            if max_new_trophies < initial_trophy_count - len(c[0]):
                                min_coins_spent = sum(c[2])
                                best_path = c[2]
                                max_new_trophies = initial_trophy_count - len(c[0])
                                count_lot = c[1]
                            elif max_new_trophies == initial_trophy_count - len(c[0]) and sum(c[2]) < min_coins_spent:
                                min_coins_spent = sum(c[2])
                                best_path = c[2]
                                count_lot = c[1]
                        else:
                            for i in range(max_breadth):
                                queue.append((copy.deepcopy(c[0]), copy.deepcopy(c[1]), copy.deepcopy(c[2]), copy.deepcopy(c[3]), i + 1))
                    else:
                        # branch is dead due to invalid (this means it ends up completing the LOT set, which it shouldn't do)
                        pass
                # queue is now empty; we've traversed the tree.
                # now in theory we should have the best path as defined by the number of coins to spend.
                # can then traverse this path by telling the user to spend the number of coins in the path.
                # and we can keep track of what's supposed to happen by using the respective rng steps.
                for c in best_path:
                    temp_seed = (DSTAR[c][0] * seed + DSTAR[c][1]) & 4294967295
                    chance = int((len(trophies) / 84) * 100)
                    trophy_idx = -1
                    if (100 * temp_seed >> 16) >> 16 < chance:
                        # 1 step for trophy roll
                        trophy_idx = (len(trophies) * ((214013 * temp_seed + 2531011) & 4294967295) >> 16) >> 16
                    # 2 steps to realign rng
                    seed = (2851891209 * temp_seed + 505908858) & 4294967295
                    
                    if trophy_idx == -1:
                        # print get dupe trophy
                        # print(f"spend {c} coins to get DUPLICATE trophy\n")
                        pass
                    else:
                        # print(f"spend {c} coins to get trophy: {trophies[trophy_idx][0]}")
                        if not debug:
                            trophies = get_trophies(trophies, trophies[trophy_idx][0])
                        else:
                            del trophies[trophy_idx]
                            update_spending_log(c)
                    total_coins += c
        print(f"Iteration {iteration} done! Coins spent: ", total_coins)


if __name__ == "__main__":
    main()