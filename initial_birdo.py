from tagrss import *

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

rng = 0x00000001

def get_rng() -> int:
    global rng
    return rng

def set_rng(val: int) -> None :
    global rng
    rng = val

def next_rng(custom_rng_val: int = -1) -> int:
    if custom_rng_val == -1:
        global rng
        rng = (SEEDMULT*rng + SEEDCONST) & MAXINT
        return rng
    else:
        ret = (SEEDMULT*custom_rng_val + SEEDCONST) & MAXINT
        return ret

def get_rand_int(i: int, adv = True) -> int:
    temp_rng = next_rng() if adv else get_rng()
    top_bits = temp_rng >> 16
    return (i*top_bits) >> 16

def trophy_str(t: list[str, int, bool]) -> str:
    ret = f'- {t[0]} '
    if t[1] == 0:
        ret += f' (owned)|'
    else:
        ret += f' (new)|'
    return ret

def main():
    # Initial trophy list: [trophy_name]
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
    
    # the game starts off with 1 trophy already owned.
    
    # In a run, some 1p/lotto trophies have already been collected.
    # The user should input these trophies; substrings will be allowed but the user should be careful.
    # Note that if any trophies not in the initial lotto pool are entered, then they will be ignored for now.
    # Exit the loop by entering 'x' or 'q'.
    # Careful about `barrel` -> barrel / barrel cannon, or `ball` -> party ball or ball kirby, etc.
    
    # debugging shortcut
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
                    multiple_trophies += trophy_str(t)
                    substr_matches += 1
                    # Check if there are other trophies with the same substring.
                    for t_ in trophies[i+1:]:
                        if owned_trophy in t_:
                            if owned_trophy == t_:
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
    del found, exact_match, multiple_trophies, owned_trophy, substr_matches, i
    
    print('ok now go to the tag menu and roll 5 tags (type them in and hit enter between each)')
    
    # tagRSS time
    TAGS = ['AAAA','1DER','2BIT','2L8','2PAY','401K','4BDN','4BY4','4EVA','7HVN','AOK','ARCH','ARN','ASH','BAST','BBBB','BCUZ','BETA','BOBO','BOMB','BONE','BOO','BORT',
             'BOZO','BUB','BUD','BUZZ','BYRN','CHUM','COOP','CUBE','CUD','DAYZ','DIRT','DIVA','DNCR','DUCK','DUD','DUFF','DV8','ED','ELBO','FAMI','FIDO','FILO','FIRE',
             'FLAV','FLEA','FLYN','GBA','GCN','GLUV','GR8','GRIT','GRRL','GUST','GUT','HAMB','HAND','HELA','HEYU','HI5','HIKU','HOOD','HYDE','IGGY','IKE','IMPA','JAZZ',
             'JEKL','JOJO','JUNK','KEY','KILA','KITY','KLOB','KNEE','L33T','L8ER','LCD','LOKI','LULU','MAC','MAMA','ME','MILO','MIST','MOJO','MOSH','NADA','ZZZZ','NAVI',
             'NELL','NEWT','NOOK','NEWB','ODIN','OLAF','OOPS','OPUS','PAPA','PIT','POP','PKMN','QTPI','RAM','RNDM','ROBN','ROT8','RUTO','SAMI','SET','SETI','SHIG','SK8R',
             'SLIM','SMOK','SNES','SNTA','SPUD','STAR','THOR','THUG','TIRE','TLOZ','TNDO','TOAD','TOMM','UNO','VIVI','WALK','WART','WARZ','WITH','YETI','YNOT','ZAXO',
             'ZETA','ZOD','ZOE','WORM','GEEK','DUDE','WYRN','BLOB']
    
    rolled_tags = []
    while len(rolled_tags) != 5:
        new_tag = input(f"tag #{len(rolled_tags) + 1}: ")
        if new_tag.upper() in TAGS:
            rolled_tags.append(TAGS.index(new_tag.upper()))
        else:
            print('invalid tag, either there was a typo or the script is broken D:')
    
    # now `rolled_tags` should contain the list of trophies
    potential_seed = TagRss(rolled_tags)
    
    # if there's only one seed, then we can move on ahead
    if len(potential_seed) == 1:
        print('found a seed, now calculating rng manip path...')
        # run a lotto sim to figure out if we can get birdo in the first 5 coins
        # if it's not possible, then advance seed by 1 until we find a possible seed, and manip via generating tags (and maybe css in the future?)
        seed = potential_seed[0][2]
        set_rng(seed)
        next_rng()
        # this is the seed that we want to get to, if we can find it in a reasonable amount of time
        found_seed = False
        num_advances = 0
        coins_to_spend = 0
        tags_to_roll = []
        temp_rng = get_rng()
        
        while not found_seed:
            for i in range(1, 6):
                set_rng(temp_rng)
                # 3 per coin
                next_rng(), next_rng(), next_rng()
                temp_rng = get_rng()
                # int((83 / 84) * 100) = 98; this is the success roll
                if get_rand_int(100) < 98:
                    # this is the actual trophy roll
                    trophy_roll_rand_int = get_rand_int(83)
                    
                    if trophy_roll_rand_int == birdo_index:
                        coins_to_spend = i
                        found_seed = True
                        break
            else:
                # if we get thru the for-loop and dont find birdo then add to the number of advances
                num_advances += 1
                if num_advances > 100:
                    print('this seed requires over 100 steps; just reset and try again :(')
                    quit()
                # advance rng by 1 step and see if it works
                set_rng(seed)
                for _ in range(num_advances):
                    next_rng()
                temp_rng = get_rng()
                # ideal_seed = previous(get_rng())
        
        # bring back the rng value back to the seed so we can figure out if we can get to the desired seed (via the `num_advances`)
        set_rng(seed)
        
        # at this point we now know how many times to advance and how many coins to spend in the lotto.
        # we just have to tell the user how to advance the seed to the desired seed, using `num_advances`.
        # this means that we need to simulate tagRSS to get to the desired seed, if possible.
        temp_num_advances = 1
        while temp_num_advances < num_advances:
            tag_roll = get_rand_int(145)
            temp_num_advances += 1
            while tag_roll in rolled_tags:
                tag_roll = get_rand_int(145)
                temp_num_advances += 1
            tags_to_roll.append(TAGS[tag_roll])
            rolled_tags.pop(0)
            rolled_tags.append(tag_roll)
        
        if temp_num_advances == num_advances:
            if len(tags_to_roll) == 0:
                print('NO ROLLS NECESSARY!!!')
            else:
                print(f'ok now u gotta roll {len(tags_to_roll)} tags, good luck o7\n')
                for t in tags_to_roll:
                    print(t)
                print('\n##### OK STOP NOW #####')
                # print(f'seed after manip: {get_rng()}')
            print(f'COINS TO SPEND IN LOTTO: {coins_to_spend}')
        else:
            print('unlucky rng means that things don\'t align nicely here :/ reset run and restart the script')
    else:
        print('well tagRSS couldn\'t find your seed so... just reset and restart the script')

if __name__ == "__main__":
    main()