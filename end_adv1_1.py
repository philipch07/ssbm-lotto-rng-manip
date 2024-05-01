from globals import TAGS, TROPHIES_1PO
from globals import get_trophies, get_seed, print_tags

# this is meant to be used after the lotto is entirely completed, so this should be the last thing to do in the run (250+ trophies required to start).
# this also excludes any bucket related calculations as goomba trophies are only determined after stage load, which
# has a non-constant number of rng calls, and are currently not able to be calculated in advance.

def main():
    trophies = get_trophies(TROPHIES_1PO)
    
    while len(trophies) != 0:
        print(f"Remaining trophies: {len(trophies)}")
        seed, rolled_tags = get_seed()
        tags_to_roll = []
        
        while True:
            # advance 22 + 1 times for category roll
            if (2 * ((-3310955595 * seed + 3566711417) & 4294967295) >> 16) >> 16:
                # 24 + 1 from `get_rand_int(100)` (<60 is a success).
                if (100 * ((-1190463139 * seed + 3357146299) & 4294967295) >> 16) >> 16 < 60: # sometimes this is 65, not sure why.
                    # 25 advances plus 1 for stage trophy roll
                    a = ((len(trophies)) * ((-1422735383 * seed + 2234209426) & 4294967295) >> 16) >> 16 # sometimes this is done out of 88?
                    break
                    # We don't have to check for anything else here since we're assuming all other trophies except for the 1PO trophies are owned.
            seed = (214013*seed + 2531011) & 4294967295
            tag_roll = (145 * (seed >> 16)) >> 16
            while tag_roll in rolled_tags:
                seed = (214013*seed + 2531011) & 4294967295
                tag_roll = (145 * (seed >> 16)) >> 16
            tags_to_roll.append(TAGS[tag_roll])
            del rolled_tags[0]
            rolled_tags.append(tag_roll)
        
        print_tags(tags_to_roll)
        empty_confirm = input(f"\n\nSTAGE TROPHY: {trophies[a]} collected? [ENTER] to confirm, anything else to deny.\n")
        if not empty_confirm:
            print(f"Confirmed {trophies[a]}.")
            del trophies[a]
        else:
            print(f"Denied {trophies[a]}.")
        empty_goomba_confirm = input(f"\nGoomba trophy collected? Type the name of the goomba trophy or [ENTER] to skip.\n")
        if empty_goomba_confirm:
            trophies = get_trophies(trophies, empty_goomba_confirm)
    print("Done! All 1PO trophies collected!")


if __name__ == "__main__":
    main()