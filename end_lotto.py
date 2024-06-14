from globals import get_seed


def main():
    num_owned_trophies = int(input("Input number of trophies owned: "))
    percent = input("Chance of getting a new trophy on the lotto screen (ex: 53.2% should be input as 53.2)\n")
    total_available_trophies = 133 + (num_owned_trophies >= 250) * 4
    num_rem_trophies = round(float(percent) / 100 * total_available_trophies) + (num_owned_trophies >= 250) * 4
    
    print(f"Remaining trophies: {num_rem_trophies}")
    
    seed, _ = get_seed()
    print("\n")
    temp_seed = seed
    count = 1
    coins = 0
    
    while num_rem_trophies != 0:
        # recalculate the percent chance of getting a new trophy
        percent = ((total_available_trophies - num_rem_trophies) // total_available_trophies) * 100
        # 2 steps to account for initial rng calls
        temp_seed = (2851891209 * temp_seed + 505908858) & 4294967295
        # find the minimum number of coins needed to get a new trophy from 1 to 20
        for i in range(20):
            # 3 steps to account for a coin being spent
            temp_seed = (-3124220955 * temp_seed + 3539360597) & 4294967295
            # note that the percent will increase by 5 per each coin spent
            if (100 * temp_seed >> 16) >> 16 < (percent + 5 * i):
                # 2 steps to account for ending rng calls
                temp_seed = (2851891209 * temp_seed + 505908858) & 4294967295
                print(f"new trophy #{count}: {i + 1} coins")
                coins += i + 1
                num_rem_trophies -= 1
                num_owned_trophies += 1
                if num_owned_trophies == 250:
                    total_available_trophies = 137
                    num_rem_trophies += 4
                break
        else:
            # none of the 20 coins resulted in a new trophy, so we just spend 1 coin and move on
            temp_seed = (203977589 * seed + 548247209) & 4294967295
            print("1 coin for dupe trophy")
        count += 1
    print(f"\nTotal coins: {coins}.")


if __name__ == "__main__":
    main()