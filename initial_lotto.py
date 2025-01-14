import copy
import random
from globals import TAGS, TROPHIES_1PL_LOI, DSTAR
from globals import get_trophies, get_seed, print_tags

# this is meant to get 83/84 of the initial trophies because of reasons that were not explained to me.
# the way this is accomplished is by keeping track of the LOI trophies that are collected, and ensuring that we only ever get 11/12 of them.
# thus the last uncollected trophy is from LOI.

# this also features a new algorithm where fewer coins are spent due to this being run at the beginning of a run.
# note that the greedy algorithm is also toggleable here.

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


def log_total_coins_spent(coins):
    try:
        with open("total_coins_spent_3_8_dfs.txt", "a") as file:
            file.write(f"{coins}\n")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_total_coins_spent(fname):
    total_coin_costs = []
    try:
        # change filename to match necessary stuff
        with open(fname, "r") as file:
            # Read each line, convert to integer, and append to the list
            total_coin_costs = [int(line.strip()) for line in file]
    except Exception as e:
        print(f"An error occurred: {e}")
    return total_coin_costs


def plot_data():
    import matplotlib.pyplot as plt
    import re
    filenames = ["./old_scripts_and_other/coin_spending_logs/total_coins_spent_greedy.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_20_3_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_20_2_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_5_6_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_5_5_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_4_7_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_4_6_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_9_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_8_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_7_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_20_3_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_20_2_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_5_6_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_5_5_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_4_7_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_4_6_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_9_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_8_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_7_dfs+et.txt",
                 ]

    file_data = []
    for filename in filenames:
        file_data.append(read_total_coins_spent(filename))

    num_files = len(file_data)
    columns = 4  # Number of columns for subplots
    rows = (num_files // columns) + (num_files % columns > 0)

    plt.figure(figsize=(20, 12))

    for i, data in enumerate(file_data):
        plt.subplot(rows, columns, i + 1)
        plt.hist(data, bins=20, edgecolor='black', alpha=0.7)
        plt.title(re.search(r'[^/]+$', filenames[i]).group(0)[18:-4].replace("_", "^", 1).replace("_", " ", 1), fontsize=10)
        plt.xlabel("Coin Values", fontsize=8)
        plt.ylabel("Frequency", fontsize=8)
        plt.tight_layout()

    plt.show()


def coin_step(trophies, clot: int, coins_spent: list[int], seed: int, coins_to_spend):
    chance = int((len(trophies) / 84) * 100)
    temp_seed = (DSTAR[coins_to_spend][0] * seed + DSTAR[coins_to_spend][1]) & 4294967295
    trophy_idx = -1
    invalid = False
    if (100 * temp_seed >> 16) >> 16 < chance + (5 * (coins_to_spend - 1)):
        # 1 step for trophy roll
        trophy_idx = (len(trophies) * ((214013 * temp_seed + 2531011) & 4294967295) >> 16) >> 16
        # if the trophy is LOI, add it to the count. if this is the LAST LOI trophy, do not accept it.
        # if clot != 11 -> accept the trophy and add clot count if necessary
        # else -> if not LOI, then accept the trophy
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


def coin_sim(trophies, seed, debug, max_depth, max_breadth, count_lot):
    total_coins = 0
    while len(trophies) != 1:
        if not debug:
            print(f"\ntrophies remaining: {len(trophies)}")
        temp_seed = seed
        # if you want to add a toggle, do that here.
        # note that you'll have to add break statements to exit the loop when you switch between the modes. i've commented them below.
        # just note that there's practically 0 reason to do this. im providing the option because i was asked to.
        # remember to comment out the `mode = False` line below.
        # if not debug:
        #     mode = input("press [ENTER] for coin saver, anything else for greedy: \n").lower() != ""

        # default to coin saver
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
                if (100 * temp_seed >> 16) >> 16 < chance + (5 * i):
                    # 1 step for trophy roll
                    trophy_idx = (len(trophies) * ((214013 * temp_seed + 2531011) & 4294967295) >> 16) >> 16
                    # if the trophy is LOI, add it to the count. if this is the LAST LOI trophy, do not accept it.
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
                        # update_spending_log(coins)
                        pass
                    break
            if trophy_idx == -1:
                coins += 1
                total_coins += 1
                # print("No new trophy, spend 1 coin to advance rng.")
                # advance by 7 to account for lack of trophy -> inputting 1 coin to advance rng
                seed = (203977589 * seed + 548247209) & 4294967295
                if debug:
                    # update_spending_log(1)
                    pass
            else:
                # confirm trophy has been receieved
                if debug:
                    del trophies[trophy_idx]
                else:
                    print(f"spend {coins} coins to get trophy: {trophies[trophy_idx][0]}")
                    trophies = get_trophies(trophies, trophies[trophy_idx][0])
                    # mode = input("Press [ENTER] to continue in greedy, else any other button to switch to greedy.") == ""
                    # if not mode:
                    #     total_coins += c
                    #     break
        else:
            initial_trophy_count = len(trophies)
            partial_trophies = [t[1] for t in trophies]
            max_new_trophies = 0
            min_coins_spent = 999
            best_path = []
            # DFS
            stack = []
            for i in range(max_breadth):
                stack.append((copy.deepcopy(partial_trophies), copy.deepcopy(count_lot), copy.deepcopy([]), copy.deepcopy(seed), i + 1))
            while len(stack) > 0:
                q = stack.pop()
                c = coin_step(*q)
                # invalid check
                if not c[4]:
                    if len(c[2]) == max_depth or len(c[2]) == initial_trophy_count - 1:
                        if max_new_trophies < initial_trophy_count - len(c[0]):
                            min_coins_spent = sum(c[2])
                            best_path = c[2]
                            max_new_trophies = initial_trophy_count - len(c[0])
                            count_lot = c[1]
                        elif max_new_trophies == initial_trophy_count - len(c[0]) and sum(c[2]) < min_coins_spent:
                            min_coins_spent = sum(c[2])
                            best_path = c[2]
                            count_lot = c[1]
                        # early term
                        if max_new_trophies == max_depth or max_new_trophies == initial_trophy_count - 1:
                            break
                    else:
                        for i in range(max_breadth, 0, -1):
                            stack.append((copy.deepcopy(c[0]), copy.deepcopy(c[1]), copy.deepcopy(c[2]), copy.deepcopy(c[3]), i))
                else:
                    # branch is dead due to invalid (this means it ends up completing the LOI set, which it shouldn't do)
                    pass
            
            # stack is now empty; we've traversed the tree.
            # the best path is defined by the number of coins to spend.
            for c in best_path:
                temp_seed = (DSTAR[c][0] * seed + DSTAR[c][1]) & 4294967295
                chance = int((len(trophies) / 84) * 100)
                trophy_idx = -1
                if (100 * temp_seed >> 16) >> 16 < chance + (5 * (c - 1)):
                    # 1 step for trophy roll
                    trophy_idx = (len(trophies) * ((214013 * temp_seed + 2531011) & 4294967295) >> 16) >> 16
                # 2 steps to realign rng
                seed = (2851891209 * temp_seed + 505908858) & 4294967295
                
                if trophy_idx == -1:
                    # print get dupe trophy
                    if not debug:
                        print(f"spend {c} coins to get DUPLICATE trophy\n")
                else:
                    if not debug:
                        print(f"spend {c} coins to get trophy: {trophies[trophy_idx][0]}")
                        trophies = get_trophies(trophies, trophies[trophy_idx][0])
                        # mode = input("Press [ENTER] to continue in coin saver, else any other button to switch to greedy.") != ""
                        # if mode:
                        #     total_coins += c
                        #     break
                    else:
                        del trophies[trophy_idx]
                        # update_spending_log(c)
                total_coins += c
                # early terminate when simulating
                if debug and total_coins > 170:
                    return -1
    return total_coins


def main():
    max_depth = 9
    max_breadth = 3

    trophies = get_trophies(TROPHIES_1PL_LOI)
    count_lot = 12 - sum([1 for x in trophies if not x[1]])
    seed, rolled_tags = get_seed()
    tags_to_roll = []

    total_coins = 999
    print(f"\nsimulating trophies using {max_breadth}^{max_depth} DFS...")
    
    while total_coins > 170 or total_coins == -1:
        total_coins = coin_sim(copy.deepcopy(trophies), copy.deepcopy(seed), True, max_depth, max_breadth, copy.deepcopy(count_lot))
        print(f"total coins simulated: {total_coins if total_coins != -1 else "170+"}")
        if total_coins < 170 and total_coins != -1:
            break
        seed = (214013*seed + 2531011) & 4294967295
        tag_roll = (145 * (seed >> 16)) >> 16
        while tag_roll in rolled_tags:
            seed = (214013*seed + 2531011) & 4294967295
            tag_roll = (145 * (seed >> 16)) >> 16
        tags_to_roll.append(TAGS[tag_roll])
        del rolled_tags[0]
        rolled_tags.append(tag_roll)
    
    print_tags(tags_to_roll)
    total_coins = coin_sim(copy.deepcopy(trophies), copy.deepcopy(seed), False, max_depth, max_breadth, copy.deepcopy(count_lot))
    
    # if debug:
    #     total_coins = coin_sim(copy.deepcopy(trophies), copy.deepcopy(seed), True, max_depth, max_breadth, copy.deepcopy(count_lot))
    #     print(f"Iteration {iteration} done! Coins spent: ", total_coins)
    #     log_total_coins_spent(total_coins)
    print(f"83/84 trophies collected! Last trophy remaining: {trophies[0][0]}.")
    print(f"Total coins spent: {total_coins}")


if __name__ == "__main__":
    main()