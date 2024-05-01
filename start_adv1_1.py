from globals import TAGS, TROPHIES_1PL_1PO_TAGGED
from globals import get_trophies, get_seed, print_tags

# test file for new rng file structure since most of the bulky code and be reused.
# also this does work for the starting adv1_1, but shouldn't be used in real all trophy runs.

def main():
    trophies = get_trophies(TROPHIES_1PL_1PO_TAGGED)

    while not all(not t[1] for t in trophies):
        print(f"Remaining trophies: {sum(1 for x in trophies if x[1])}")
        seed, rolled_tags = get_seed()
        tags_to_roll = []
        while True:
            # advance 22 + 1 times for category roll (1PO vs 1PL); we're looking for anything < 60.
            if ((100 * ((-3310955595 * seed + 3566711417) & 4294967295) >> 16) >> 16) < 60:
                # advance 23 + 1 times for trophy roll and check if it is 1PO
                a = trophies[(((len(trophies)) * ((-3835258655 * seed + 3845303128) & 4294967295) >> 16) >> 16)]
                if a[1]:
                    # the stage trophy is a new 1PO trophy
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
        empty_confirm = input(f"\n\nSTAGE TROPHY: {a[0]} collected? [ENTER] to confirm, anything else to deny.\n")
        if not empty_confirm:
            print(f"Confirmed {a[0]}.")
            del trophies[trophies.index(a)]
        else:
            print(f"Denied {a[0]}.")
        empty_goomba_confirm = input(f"\nGoomba trophy collected? Type the name of the goomba trophy or [ENTER] to skip.\n")
        if empty_goomba_confirm:
            trophies = get_trophies(trophies, empty_goomba_confirm)
    print("Done! All 1PO trophies collected!")

if __name__ == "__main__":
    main()