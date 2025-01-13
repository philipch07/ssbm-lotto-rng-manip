from tagrss import TagRss

# i really should figure out a better way to implement this 
# instead of copy-pasting this for each new file
rng = 0x00000001

TAGS = ['AAAA','1DER','2BIT','2L8','2PAY','401K','4BDN','4BY4','4EVA','7HVN','AOK','ARCH','ARN','ASH','BAST','BBBB','BCUZ','BETA','BOBO','BOMB','BONE','BOO','BORT',
            'BOZO','BUB','BUD','BUZZ','BYRN','CHUM','COOP','CUBE','CUD','DAYZ','DIRT','DIVA','DNCR','DUCK','DUD','DUFF','DV8','ED','ELBO','FAMI','FIDO','FILO','FIRE',
            'FLAV','FLEA','FLYN','GBA','GCN','GLUV','GR8','GRIT','GRRL','GUST','GUT','HAMB','HAND','HELA','HEYU','HI5','HIKU','HOOD','HYDE','IGGY','IKE','IMPA','JAZZ',
            'JEKL','JOJO','JUNK','KEY','KILA','KITY','KLOB','KNEE','L33T','L8ER','LCD','LOKI','LULU','MAC','MAMA','ME','MILO','MIST','MOJO','MOSH','NADA','ZZZZ','NAVI',
            'NELL','NEWT','NOOK','NEWB','ODIN','OLAF','OOPS','OPUS','PAPA','PIT','POP','PKMN','QTPI','RAM','RNDM','ROBN','ROT8','RUTO','SAMI','SET','SETI','SHIG','SK8R',
            'SLIM','SMOK','SNES','SNTA','SPUD','STAR','THOR','THUG','TIRE','TLOZ','TNDO','TOAD','TOMM','UNO','VIVI','WALK','WART','WARZ','WITH','YETI','YNOT','ZAXO',
            'ZETA','ZOD','ZOE','WORM','GEEK','DUDE','WYRN','BLOB']

def get_rng() -> int:
    global rng
    return rng

def set_rng(val: int) -> None :
    global rng
    rng = val

def next_rng(custom_rng_val: int = -1) -> int:
    if custom_rng_val == -1:
        global rng
        rng = (214013*rng + 2531011) & 4294967295
        return rng
    else:
        ret = (214013*custom_rng_val + 2531011) & 4294967295
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

# add goomba parameter to only do it once
def get_trophies_owned(prompt: str = "Type the names of the trophies that you've collected in the gallery. Substrings are allowed, but be careful. Type 'x' or 'q' to finish.\n", 
                       trophies: list[list[str, bool]] = None, 
                       num_remaining_1PO: int = None,
                       goomba: bool = False
                       ) -> (list[list[str, bool]], int):
    
    input_trophy = input(prompt)
    if not input_trophy:
        return trophies, num_remaining_1PO
    while input_trophy.lower() != 'x' and input_trophy.lower() != 'q':
        found = False
        misinput = False
        multiple_trophies = ''
        substr_matches = False
        
        for i, t in enumerate(trophies):
            exact_match = False
            
            if input_trophy in t[0]:
                exact_match = input_trophy == t[0]
                if not exact_match:
                    multiple_trophies += trophy_str(t)
                    # Check if there are other trophies with the same substring.
                    for t_forward in trophies[i+1:]:
                        if input_trophy in t_forward[0]:
                            exact_match = input_trophy == t_forward[0]
                            multiple_trophies += trophy_str(t_forward)
                            substr_matches = True
                    # If so, then do not proceed; break immediately and reprompt.
                    if not exact_match and substr_matches:
                        multiple_trophies = multiple_trophies[:-1].replace("|", "\n")
                        print(f"These trophies contain the substring '{input_trophy}':\n{multiple_trophies}\nPlease retype the trophy name.")
                        break
                    if exact_match:
                        continue
                print(f'{t[0]} collected!')
                confirmed = not input(f"Confirm {t[0]} trophy? Hit [ENTER] if yes, otherwise input a character.\n")
                if confirmed:
                    num_remaining_1PO -= t[1]
                    del trophies[i]
                    found = True
                    break
                else:
                    misinput = True
        else:
            if not found:
                print(f'Could not find {input_trophy}. If this is a trophy that isn\'t in 1PO or 1PL, ignore this message.')
            elif misinput:
                print(f'User misinput detected, please re-input the trophy you received.')
        if goomba and not misinput and found:
            break
        input_trophy = input("Trophy name (x or q to quit):\n")
    
    return trophies, num_remaining_1PO

def input_tag(rolled_tags: list[str]) -> list[int]:
    global TAGS
    new_tag = input(f"tag #{len(rolled_tags) + 1}: ")
    if new_tag.upper() in TAGS:
        rolled_tags.append(TAGS.index(new_tag.upper()))
    else:
        print('Invalid tag, probably a typo')
    return rolled_tags

def find_ideal_seed(trophies: list[str], temp_seed: int = -1, num_advances: int = 0) -> (int, int, int):
    trophy_stage_roll = -1
    # position_roll = -1
    while True:
        # Advance seed for success/failure roll, and check that it passes (the return value is `< 60`.)
        # 22 advances plus 1 from `get_rand_int(100)`.
        success_roll = (100 * ((-3310955595 * temp_seed + 3566711417) & 4294967295) >> 16) >> 16
        if success_roll < 60: # sometimes this is 65, not sure what the cause for this is though.
            # Advance seed for trophy roll, and check that it's a 1PO trophy (the second value of the returned index is `True`)
            # 23 advances plus 1 from `get_rand_int(NUM_AVAILABLE_TROPHIES - num_owned_trophies) == get_rand_int(len(trophies))`
            trophy_stage_roll = ((len(trophies)) * ((-3835258655 * temp_seed + 3845303128) & 4294967295) >> 16) >> 16
            if trophies[trophy_stage_roll][1]:
                return num_advances, trophy_stage_roll, temp_seed
        temp_seed = (214013 * temp_seed + 2531011) & 4294967295
        num_advances += 1

# this time we're going to have to figure out the order of the trophies for the 1PO+1PL list
def main():
    # here, we're going to store the trophies list a little differently than in previous implementations
    # instead of keeping track whether a trophy is owned and if a trophy is in the desired category, we can just keep track of if the trophy is 1PO or not.
    trophies = [['warp star', True], ['ray gun', False], ['super scope', False], ['fire flower', False], ['star rod', False], ['beam sword', True], 
                ['homerun bat', False], ['fan', False], ['green shell', True], ['flipper', False], ['freezie', True], ['mr saturn', False], 
                ['bobomb', False], ['super mushroom', False], ['starman mario', False], ['parasol', True], ['screw attack', True], 
                ['barrel cannon', False], ['party ball', False], ['crate', False], ['barrel', False], ['capsule', False], ['egg', False], 
                ['charizard', True], ['squirtle', False], ['blastoise', False], ['clefairy', False], ['electrode', True], ['weezing', False], 
                ['goldeen', False], ['staryu', True], ['snorlax', False], ['chikorita', False], ['cyndaquil', False], ['bellossom', False], 
                ['marill', True], ['wobbuffet', False], ['scizor', False], ['porygon2', False], ['toad', False], ['coin', False], ['vegetable', True], 
                ['kirby hat 1', False], ['kirby hat 2', False], ['kirby hat 3', False], ['banzai bill', True], ['lakitu', False], ['birdo', False], 
                ['klap trap', False], ['four giants', True], ['master sword', True], ['slippy toad', False], ['koopa troopa', False], 
                ['koopa paratroopa', True], ['redead', True], ['octorok', True], ['like like', True], ['topi', False], ['metal mario', False], 
                ['plum', True], ['daisy', False], ['thwomp', False], ['viruses', True], ['bucket', False], ['racing kart', False], 
                ['baby bowser', False], ['raphael raven', False], ['goron', True], ['dr stewart', False], ['jody summer', False], 
                ['andross 64', False], ['metroid', False], ['ridley', False], ['fire kirby', True], ['ball kirby', False], ['waddle dee', False], 
                ['rick', False], ['paula', True], ['starman earthbound', False], ['bulbasaur', False], ['poliwhirl', False], ['totodile', False], 
                ['crobat', False], ['cleffa', True], ['igglybuff', False], ['steelix', False], ['heracross', False], ['zeroone', False], 
                ['ryota hayami', False], ['love giant', True], ['heririn', False], ['excitebike', False], ['ducks', False], ['balloon fighter', False], 
                ['pit', True], ['dr wright', False], ['donbe & hikari', False], ['ayumi tachibana', True], ['monster', False]]
    num_remaining_1PO = 27
    # Get the trophies owned from the gallery
    trophies, num_remaining_1PO = get_trophies_owned(trophies=trophies, num_remaining_1PO=num_remaining_1PO)
    
    # stage_trophy_spawn_locations = ['first wall', 'low wall', 'on top of the bricks', 'pipe before cliff']
    while num_remaining_1PO > 0:
        print('Now go to the tag menu and roll 5 tags and enter each of them here.')
        
        # tagRSS
        # the list of tags that are rolled
        rolled_tags = []
        # let the user input each of the rolled tags
        while len(rolled_tags) != 5:
            rolled_tags = input_tag(rolled_tags=rolled_tags)
        potential_seed = TagRss(rolled_tags)
        
        while len(potential_seed) > 1:
            print(f"There are {len(potential_seed)} potential seeds, please keep rolling tags as prompted.")
            rolled_tags = input_tag(rolled_tags=rolled_tags)
            
            bad_seeds = []
            # since we're iterating through the list, i don't think we can remove the bad seed from the list, so we keep a list of the bad seeds and remove them later.
            for i, seed in enumerate(potential_seed):
                if seed[1][len(rolled_tags) - 1] != rolled_tags[-1]:
                    # insert at the beginning of the list so we don't have to reverse the list when deleting (deleting from the end will prevent deleting wrong indexes.)
                    bad_seeds.insert(0, i)
            
            for b in bad_seeds:
                del potential_seed[b]
        
        seed = potential_seed[0][2][len(rolled_tags) - 5]
        num_advances, trophy_roll, temp_seed = find_ideal_seed(trophies=trophies, temp_seed=seed)
        
        # here we determine the rng manip path via rolling tags
            # in the future, possibly implement CSS manip path since it should probably take less time
        tags_to_roll = []
        while num_advances != 0:
            temp_num_advances = num_advances
            set_rng(seed)
            while num_advances > 0:
                tag_roll = get_rand_int(145)
                num_advances -= 1
                while tag_roll in rolled_tags:
                    tag_roll = get_rand_int(145)
                    num_advances -= 1
                tags_to_roll.append(TAGS[tag_roll])
                del rolled_tags[0]
                rolled_tags.append(tag_roll)
            
            if num_advances != 0:
                num_advances, trophy_roll, temp_seed = find_ideal_seed(trophies=trophies, temp_seed=temp_seed, num_advances=temp_num_advances)
        
        if len(tags_to_roll) == 0:
            print("No rolls are necessary")
        else:
            # print the last 5 tags to roll, cuz too many tags will clutter the prompt
            print(f'You need to roll {len(tags_to_roll)} tags')
            num_tags_to_print = min(5, len(tags_to_roll))
            for tags in tags_to_roll[-1*num_tags_to_print:]:
                print(tags)
            print("\n\nSTOP ROLLING NOW")
        print(f'Trophy from 1-1: {trophies[trophy_roll][0]}')
        # print(f'Spawn position: {stage_trophy_spawn_locations[position_roll]}')
        # confirm stage trophy was collected
        not_empty_confirmation = input(f"Did you pick up the {trophies[trophy_roll][0]} trophy? Hit enter if yes, otherwise input a character.\n")
        if not not_empty_confirmation:
            print(f"Confirmed that you received {trophies[trophy_roll][0]}.")
            num_remaining_1PO -= trophies[trophy_roll][1]
            del trophies[trophy_roll]
        # check if goomba trophy was collected
        trophies, num_remaining_1PO = get_trophies_owned(prompt="If you collected a goomba trophy, enter the name, otherwise just hit enter\n",
                                                        trophies=trophies, num_remaining_1PO=num_remaining_1PO, goomba=True)
        
        print(f"NUMBER OF REMAINING 1PO TROPHIES: {num_remaining_1PO}")
    print("Done")


if __name__ == "__main__":
    main()