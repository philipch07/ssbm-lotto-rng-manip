from tagrss import TagRss

# no readme for this atm, so ill explain everything in this file
# this assumes that you start on a fresh save of the game; no trophies owned besides the one you start with
# and only the 5 coins that you start on

# TO USE: run the file
# 1: go to gallery and enter the name (or substring) of the trophy that you own
# 2: go to vs mode -> name entry -> NEW -> left, down, down (these inputs will get you to the RANDOM button)
# 3: hit the random button and enter the tag that you get into the program 5 times (so you roll 5 tags total)
# 4a: if you get lucky, then the program will tell you if you can roll certain tags. 
#     roll the number of times it says (it will print the tags to help you along the way)
# 4b: if you dont get lucky, the program will explain why and tell you to reset the run and also reset the script.
# if you have any other questions, please let me know!
# i am also thinking about putting all of this in a big fat loop so that this script doesn't have to be restarted, but will hold off for now unless if someone really wants it!

def trophy_str(t: list[str, int, bool]) -> str:
    ret = f'- {t[0]} '
    added_str = f' (new)|' if t[1] else f' (owned)|'
    return ''.join([ret, added_str])


def main():
    # Initial trophy list: [trophy_name]
    # Using a list here instead of a set to also allow for substring searches instead of just exact string searches.
    # This section of the code can be replaced by OCR when possible
    trophies = ['ray gun', 'super scope', 'fire flower', 'star rod', 'home-run bat', 'fan', 'red shell', 'flipper', 
                'mr. saturn', 'bob-omb', 'super mushroom', 'starman1', 'barrel cannon', 'party ball', 'crate', 'barrel', 
                'capsule', 'egg', 'squirtle', 'blastoise', 'clefairy', 'weezing', 'chansey', 'goldeen', 'snorlax', 
                'chikorita', 'cyndaquil', 'bellossom', 'wobbuffet', 'scizor', 'porygon2', 'toad', 'coin', 'kirby hat 1', 
                'kirby hat 2', 'kirby hat 3', 'lakitu', 'birdo', 'klap trap', 'slippi toad', 'koopa troopa', 'topi', 
                'metal mario', 'daisy', 'thwomp', 'bucket', 'racing kart', 'baby bowser', 'raphael raven', 
                'dixie kong', 'dr. stewart', 'jody summer', 'andross 64', 'metroid', 'ridley', 'fighter kirby', 
                'ball kirby', 'waddle dee', 'rick', 'jeff', 'starman2', 'bulbasaur', 'poliwhirl', 'eevee', 'totodile', 
                'crobat', 'igglybuff', 'steelix', 'heracross', 'professor oak', 'misty', 'zero-one', 'maruo maruhige', 
                'ryota hayami', 'ray mk ii', 'heririn', 'excitebike', 'ducks', 'bubbles', 'eggplant man', 
                'balloon fighter', 'dr wright', 'donbe & hikari', 'monster']
    
    # Upon a new game launch, a random 1PL trophy is given to the player.
    # The user should input this trophy; note that substrings are allowed but the user should be careful.
    # If any trophy which isn't in the initial lotto pool is entered, then it will be ignored.
    # Exit the loop by entering 'x' or 'q'.
    # Substring edge-case examples: `barrel` -> barrel / barrel cannon, or `ball` -> party ball or ball kirby, etc.
    
    owned_trophy = input("Type the names of the trophy in the gallery. Substrings are allowed, but be careful.\n")
    found = False
    birdo_index = -1
    while not found:
        multiple_trophies = ''
        substr_matches = 0
        
        for i, t in enumerate(trophies):
            exact_match = False
            
            if owned_trophy in t:
                exact_match = owned_trophy == t
                if not exact_match:
                    multiple_trophies = ''.join([multiple_trophies, trophy_str(t)])
                    substr_matches += 1
                    # Check if there are other trophies with the same substring.
                    for t_ in trophies[i+1:]:
                        if owned_trophy in t_:
                            if owned_trophy == t_:
                                exact_match = True
                            multiple_trophies = ''.join([multiple_trophies, trophy_str(t_)])
                            substr_matches += 1
                    # If so, then do not proceed; break immediately and reprompt.
                    if not exact_match and substr_matches > 1:
                        multiple_trophies = multiple_trophies[:-1].translate(str.maketrans("|", "\n"))
                        print(f"These trophies contain the substring '{owned_trophy}':\n{multiple_trophies}\nPlease retype the trophy name:")
                        break
                    if exact_match:
                        continue
                print(f'{t} collected!')
                found = True
                birdo_index = 37 if i > 37 else 36
                trophies.remove(t)
                break
        else:
            if not found:
                print(f'Could not find {owned_trophy}. If this is a 1p only trophy, ignore this message. Otherwise, double check your input.')
            owned_trophy = input("")
    # deleting stuff so there are fewer variables to look at in the debugger
    # del found, exact_match, multiple_trophies, owned_trophy, substr_matches, i
    
    print('Go to the tag menu and roll 5 tags (type them in and hit enter between each).')
    
    # using a list here to lookup the corresponding tag to a given index in O(1).
    TAGS = ['AAAA','1DER','2BIT','2L8','2PAY','401K','4BDN','4BY4','4EVA','7HVN','AOK','ARCH','ARN','ASH','BAST','BBBB','BCUZ','BETA','BOBO',
            'BOMB','BONE','BOO','BORT','BOZO','BUB','BUD','BUZZ','BYRN','CHUM','COOP','CUBE','CUD','DAYZ','DIRT','DIVA','DNCR','DUCK','DUD',
            'DUFF','DV8','ED','ELBO','FAMI','FIDO','FILO','FIRE','FLAV','FLEA','FLYN','GBA','GCN','GLUV','GR8','GRIT','GRRL','GUST','GUT',
            'HAMB','HAND','HELA','HEYU','HI5','HIKU','HOOD','HYDE','IGGY','IKE','IMPA','JAZZ','JEKL','JOJO','JUNK','KEY','KILA','KITY','KLOB',
            'KNEE','L33T','L8ER','LCD','LOKI','LULU','MAC','MAMA','ME','MILO','MIST','MOJO','MOSH','NADA','ZZZZ','NAVI','NELL','NEWT','NOOK',
            'NEWB','ODIN','OLAF','OOPS','OPUS','PAPA','PIT','POP','PKMN','QTPI','RAM','RNDM','ROBN','ROT8','RUTO','SAMI','SET','SETI','SHIG',
            'SK8R','SLIM','SMOK','SNES','SNTA','SPUD','STAR','THOR','THUG','TIRE','TLOZ','TNDO','TOAD','TOMM','UNO','VIVI','WALK','WART','WARZ',
            'WITH','YETI','YNOT','ZAXO','ZETA','ZOD','ZOE','WORM','GEEK','DUDE','WYRN','BLOB']
    # using a list would be would be O(n) work for string comparison, and O(1) work for returning the index.
    # using a set would be O(1) work for string comparison and a lot of work for returning the index as sets are unindexed.
    # using a dictionary with an index as the value would be O(1) work for string comparison, and O(1) work for returning the index.
    TAGS_DICT = {"AAAA": 0,"1DER": 1,"2BIT": 2,"2L8": 3,"2PAY": 4,"401K": 5,"4BDN": 6,"4BY4": 7,"4EVA": 8,"7HVN": 9,"AOK": 10,"ARCH": 11,
                "ARN": 12,"ASH": 13,"BAST": 14,"BBBB": 15,"BCUZ": 16,"BETA": 17,"BOBO": 18,"BOMB": 19,"BONE": 20,"BOO": 21,"BORT": 22,
                "BOZO": 23,"BUB": 24,"BUD": 25,"BUZZ": 26,"BYRN": 27,"CHUM": 28,"COOP": 29,"CUBE": 30,"CUD": 31,"DAYZ": 32,"DIRT": 33,
                "DIVA": 34,"DNCR": 35,"DUCK": 36,"DUD": 37,"DUFF": 38,"DV8": 39,"ED": 40,"ELBO": 41,"FAMI": 42,"FIDO": 43,"FILO": 44,
                "FIRE": 45,"FLAV": 46,"FLEA": 47,"FLYN": 48,"GBA": 49,"GCN": 50,"GLUV": 51,"GR8": 52,"GRIT": 53,"GRRL": 54,"GUST": 55,
                "GUT": 56,"HAMB": 57,"HAND": 58,"HELA": 59,"HEYU": 60,"HI5": 61,"HIKU": 62,"HOOD": 63,"HYDE": 64,"IGGY": 65,"IKE": 66,
                "IMPA": 67,"JAZZ": 68,"JEKL": 69,"JOJO": 70,"JUNK": 71,"KEY": 72,"KILA": 73,"KITY": 74,"KLOB": 75,"KNEE": 76,"L33T": 77,
                "L8ER": 78,"LCD": 79,"LOKI": 80,"LULU": 81,"MAC": 82,"MAMA": 83,"ME": 84,"MILO": 85,"MIST": 86,"MOJO": 87,"MOSH": 88,
                "NADA": 89,"ZZZZ": 90,"NAVI": 91,"NELL": 92,"NEWT": 93,"NOOK": 94,"NEWB": 95,"ODIN": 96,"OLAF": 97,"OOPS": 98,"OPUS": 99,
                "PAPA": 100,"PIT": 101,"POP": 102,"PKMN": 103,"QTPI": 104,"RAM": 105,"RNDM": 106,"ROBN": 107,"ROT8": 108,"RUTO": 109,
                "SAMI": 110,"SET": 111,"SETI": 112,"SHIG": 113,"SK8R": 114,"SLIM": 115,"SMOK": 116,"SNES": 117,"SNTA": 118,"SPUD": 119,
                "STAR": 120,"THOR": 121,"THUG": 122,"TIRE": 123,"TLOZ": 124,"TNDO": 125,"TOAD": 126,"TOMM": 127,"UNO": 128,"VIVI": 129,
                "WALK": 130,"WART": 131,"WARZ": 132,"WITH": 133,"YETI": 134,"YNOT": 135,"ZAXO": 136,"ZETA": 137,"ZOD": 138,"ZOE": 139,
                "WORM": 140,"GEEK": 141,"DUDE": 142,"WYRN": 143,"BLOB": 144}
    
    # now for tagRSS we need the user to input the tags that they've rolled in the game.
    rolled_tags = []
    # minimizing function re-evaluation overhead in the following loops
    rt_append = rolled_tags.append
    # let the user input exactly 5 tags to narrow down the possible seeds from 4 billion to ~5 or less seeds
    while len(rolled_tags) != 5:
        # instead of using an abstracted tag input, i'm writing it inline to reduce overhead from function calls
        new_tag = input(f"tag #{len(rolled_tags) + 1}: ")
        ind = TAGS_DICT.get(new_tag.upper(), -1)
        if ind != -1:
            rt_append(ind)
        else:
            print('Invalid tag, please check for any typos.')
    
    # `rolled_tags` now contains the 5 tags that the user rolled.
    # we can now narrow down the player's current seed by using TagRSS.
    # if lucky, we can find the exact seed and skip the following loop.
    potential_seed = TagRss(rolled_tags)
    
    # if more than one seed, then instruct user to roll more tags (in the future, OCR should be able to grab all the tags for us)
    while len(potential_seed) > 1:
        print(f"There are {len(potential_seed)} potential seeds, please keep rolling tags as prompted.")
        # same inline tag input as above
        new_tag = input(f"tag #{len(rolled_tags) + 1}: ")
        ind = TAGS_DICT.get(new_tag.upper(), -1)
        if ind != -1:
            rt_append(ind)
            
            # re-evaluate the potential seeds and remove the bad seeds
            # for each potential seed, check if the corresponding tag for the most recent rolled tag's index is the same.
            # if not, add the index of the seed to the list of bad seeds.
            bad_seeds = [i for i, seed in enumerate(potential_seed) if seed[1][len(rolled_tags) - 1] != rolled_tags[-1]]
            
            # we reverse the list of bad seeds in order to prevent deleting things due to shifting indexes
            # ex: let [0, 4, 7, 8, 12, 13] be our list of seeds, and [0, 2, 3] be the indices of the seeds we want to delete.
            # a naive approach would result in the list becoming:
            #   [0, 4, 7, 8, 12, 13] -> [4, 7, 8, 12, 13] -> [4, 7, 12, 13] -> [4, 7, 12].
            # however, deleting the indicies in a descending order will return the correct list: 
            #   [0, 4, 7, 8, 12, 13] -> [0, 4, 7, 12, 13] -> [0, 4, 12, 13] -> [4, 12, 13]
            for b in reversed(bad_seeds):
                del potential_seed[b]
        else:
            print('Invalid tag, probably a typo')
    
    # now we can guarantee that there is only one seed remaining, so we can save it here.
    seed = potential_seed[0][2][len(rolled_tags) - 5]
    # simulate the lottery to figure out what seed returns birdo within the first 5 coins of the lottery
    tags_to_roll = []
    coins_to_spend = -1
    
    while True:
        # at the beginning of the lottery, the rng is advanced once.
        seed = (214013*seed + 2531011) & 4294967295
        coin_seed = seed
        # the number of coins to spend are an integer in the range of [1, 5]
        # note: the logic in the loop could be very slightly optimized although it requires a little bit of pre-computations
        #       however, the potential savings from the slight optimizations are not worth the code being more confusing.
        #       additionally, the current implementation stays closer to the machine code logic used when tracing rng calls.
        for coins_to_spend in [1, 2, 3, 4, 5]:
            # when spending a coin, the game advances the rng 3 times.
            coin_seed = (-3124220955*coin_seed + 3539360597) & 4294967295
            # get_rand_int() calls will also advance the rng value 1 time, which is done in the line below.
            roll_seed = (214013*coin_seed + 2531011) & 4294967295
            # now we simulate the actual get_rand_int(100) call, as we just advanced the rng value 1 time in `roll_seed` (above).
            # the math to calculate the limit (the right hand side of the inequality) for the success roll is: int((83 / 84) * 100) = 98.
            if ((100 * (roll_seed >> 16)) >> 16) < 98:
                # get_rand_int() calls will also advance the rng value 1 time, which is done in the line below.
                roll_seed = (214013*roll_seed + 2531011) & 4294967295
                # now we simulate the actual get_rand_int(83) call, which is the trophy roll.
                # we can simply check if the resulting index is the index is the same as birdo's index.
                if ((83 * (roll_seed >> 16)) >> 16) == birdo_index:
                    break
        else:
            # at this point, the simulation determined that we can't get birdo at this seed after trying 1 thru 5 coins.
            # normally we would have to advance the rng once before calling `get_rand_int()`, but seed is already advanced (top of the while loop)
            tag_roll = (145 * (seed >> 16)) >> 16
            while tag_roll in rolled_tags:
                seed = (214013*seed + 2531011) & 4294967295
                tag_roll = (145 * (seed >> 16)) >> 16
            tags_to_roll.append(TAGS[tag_roll])
            del rolled_tags[0]
            rolled_tags.append(tag_roll)
            
            # An optional if-statement to let the user know if the number of tags to roll is uncomfortably large.
            # if len(tags_to_roll) > 1000:
            #     print('this seed requires over 1000 steps; just reset and try again :(')
            #     quit()
            continue
        # when we break from the for loop, it skips the else statement and will hit this break statement.
        # if we don't break from the for loop, then it runs the else statement and skips this break statement due to the above continue statement.
        break
    
    # now we tell the player how many tag rolls need to be made
    if len(tags_to_roll) == 0:
        print("No rolls are necessary")
    else:
        # print the last 5 tags to roll, as too many tags will clutter the prompt
        print(f'You need to roll {len(tags_to_roll)} tags')
        num_tags_to_print = min(5, len(tags_to_roll))
        for tags in tags_to_roll[-1*num_tags_to_print:]:
            print(tags)
    # and lastly, the number of coins to be spent in the lotto.
    print(f'Coins to spend in lotto: {coins_to_spend}')

if __name__ == "__main__":
    main()