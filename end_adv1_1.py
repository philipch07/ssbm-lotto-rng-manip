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

def check_buckets(trophy: str, buckets: list[list[str]], delete: bool = True) -> (list[list[str]], list[str]):
    rem = []
    for i, b in enumerate(buckets):
        for j, t in enumerate(b):
            if trophy == t:
                if delete:
                    del b[j]
                    if not len(b):
                        del buckets[i]
                else:
                    rem = buckets[i]
                return buckets, rem

def input_trophies_owned(prompt: str = "Type the names of the trophies that you've collected in the gallery. Substrings are allowed, but be careful. Type 'x' or 'q' to finish.\n", 
                       trophies: list[str] = None, 
                       buckets: list[list[str]] = None
                       ) -> (list[str], list[list[str]]):
    
    input_trophy = input(prompt)
    if not input_trophy:
        return trophies
    while input_trophy.lower() != 'x' and input_trophy.lower() != 'q':
        confirmed = False
        misinput = False
        multiple_trophies = ''
        substr_matches = False
        
        for i, t in enumerate(trophies):
            exact_match = False
            
            if input_trophy in t:
                exact_match = input_trophy == t
                if not exact_match:
                    multiple_trophies += trophy_str(t)
                    # Check if there are other trophies with the same substring.
                    for t_forward in trophies[i+1:]:
                        if input_trophy in t_forward:
                            exact_match = input_trophy == t_forward
                            multiple_trophies += trophy_str(t_forward)
                            substr_matches = True
                    # If so, then do not proceed; break immediately and reprompt.
                    if not exact_match and substr_matches:
                        multiple_trophies = multiple_trophies[:-1].replace("|", "\n")
                        print(f"These trophies contain the substring '{input_trophy}':\n{multiple_trophies}\nPlease retype the trophy name.")
                        break
                    if exact_match:
                        continue
                trophies, buckets, confirmed = confirm_trophy(roll=i, trophies=trophies, buckets=buckets)
                if confirmed:
                    break
                else:
                    misinput = True
        else:
            if not confirmed:
                print(f'Did not collect {input_trophy}.')
            elif misinput:
                print(f'User misinput detected, please re-input the trophy you received.')
        input_trophy = input("Trophy name (x or q to quit):\n")
    
    return trophies, buckets

def confirm_trophy(roll: int, trophies: list[str], buckets: list[list[str]]) -> (list[str], list[list[str]], bool):
    confirmed = not input(f"Confirm {trophies[roll].upper()} trophy? Hit [ENTER] if yes, otherwise input a character.\n")
    if confirmed:
        print(f"Confirmed that you received {trophies[roll]}.")
        buckets, _ = check_buckets(trophies[roll], buckets=buckets)
        del trophies[roll]
    return trophies, buckets, confirmed

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
        # 24 advances plus 1 from `get_rand_int(100)`.
        success_roll = (100 * ((-1190463139 * temp_seed + 3357146299) & 4294967295) >> 16) >> 16
        if success_roll < 65: # sometimes this is 65, not sure what the cause for this is though.
            # Advance seed for trophy roll, and check that it's a 1PO trophy (the second value of the returned index is `True`)
            # 25 advances plus 1 from `get_rand_int(NUM_AVAILABLE_TROPHIES - num_owned_trophies) == get_rand_int(len(trophies))`
            trophy_stage_roll = ((len(trophies)) * ((-1422735383 * temp_seed + 2234209426) & 4294967295) >> 16) >> 16
            return num_advances, trophy_stage_roll, temp_seed
            # We don't have to check for anything else here since we're assuming all other trophies except for the 1PO trophies are owned.
        temp_seed = (214013 * temp_seed + 2531011) & 4294967295
        num_advances += 1

# this time we're going to have to figure out the order of the trophies for the 1PO+1PL list
def main():
    # here, we're going to store the trophies list a little differently than in previous implementations
    # instead of keeping track whether a trophy is owned and if a trophy is in the desired category, we can just keep track of if the trophy is 1PO or not.
    trophies = ['warp star', 'beam sword', 'green shell', 'freezie', 'parasol', 'screw attack', 'charizard', 'electrode', 'staryu', 'marill', 
                'vegetable', 'banzai bill', 'four giants', 'master sword', 'koopa paratroopa', 'redead', 'octorok', 'like like', 'plum', 
                'viruses', 'goron', 'fire kirby', 'paula', 'cleffa', 'love giant', 'pit', 'ayumi tachibana']
    buckets = [['beam sword', 'paula'], ['freezie', 'parasol', 'screw attack'], ['ayumi', 'love giant'], ['staryu', 'charizard'], 
               ['like like', 'redead'], ['four giants'], ['plum'], ['cleffa', 'electrode', 'marill'], ['fire kirby'], ['banzai bill', 'paratroopa'], 
               ['green shell'], ['pit'], ['vegetable', 'warp star'], ['viruses'], ['octorok'], ['goron', 'master sword']]
    # Get the trophies owned from the gallery
    trophies, buckets = input_trophies_owned(trophies=trophies, buckets=buckets)
    
    # stage_trophy_spawn_locations = ['first wall', 'low wall', 'on top of the bricks', 'pipe before cliff']
    while len(trophies) > 0:
        # tagRSS
        print('Now go to the tag menu and roll 5 tags and enter each of them here.')
        
        rolled_tags = []
        # let the user input each of the rolled tags
        while len(rolled_tags) != 5:
            rolled_tags = input_tag(rolled_tags=rolled_tags)
        potential_seed = TagRss(rolled_tags)
        
        # if more than one seed, then instruct user to roll more tags (in the future, OCR should be able to grab all the tags for us)
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
        
        # At this point, we've figured out what the seed is.
        # Now we want to find an ideal seed.
        # print('Found the current seed, calculating ideal seed...')
        seed = potential_seed[0][2][len(rolled_tags) - 5]
        num_advances, trophy_stage_roll, temp_seed = find_ideal_seed(trophies=trophies, temp_seed=seed)
        
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
                num_advances, trophy_stage_roll, temp_seed = find_ideal_seed(trophies=trophies, temp_seed=temp_seed, num_advances=temp_num_advances)
        
        # At this point, we are certain that 1) we know what our current seed is, and 2) we can manipulate the seed to get a desired outcome.
        if len(tags_to_roll) == 0:
            print("No rolls are necessary")
        else:
            # print the last 5 tags to roll, cuz too many tags will clutter the prompt
            print(f'You need to roll {len(tags_to_roll)} tags')
            num_tags_to_print = min(5, len(tags_to_roll))
            for tags in tags_to_roll[-1*num_tags_to_print:]:
                print(tags)
        trophy_name = trophies[trophy_stage_roll]
        print(f'Trophy from 1-1: {trophy_name.upper()}')
        # need to check if goomba trophy is desirable or dupe
        _, rem = check_buckets(trophy=trophy_name, buckets=buckets, delete=False)
        goomba_trophies = {}
        if len(rem) > 1:
            print(f"Goomba trophies:")
            i = 1
            for t in rem:
                if t != trophy_name:
                    goomba_trophies[i] = t
                    print(f'\t{i}: {t.upper()}')
        # confirm stage trophy was collected
        trophies, buckets, _ = confirm_trophy(roll=trophy_stage_roll, trophies=trophies, buckets=buckets)
        # there can only be up to 2 goomba trophies for any given trophy, according to buckets
        # if there's only 1 goomba trophy, then just confirm if the player picked it up.
        if len(goomba_trophies) == 1:
            trophies, buckets, _ = confirm_trophy(roll=trophies.index(goomba_trophies[1]), trophies=trophies, buckets=buckets)
        else:
            goomba_trophy = input(f"Which goomba trophy did you collect? Press [ENTER] if neither.\n\t[1] {goomba_trophies[1].upper()}\n\t[2] {goomba_trophies[2].upper()}")
            if int(goomba_trophy) == 1 or int(goomba_trophy) == 2:
                trophies, buckets, _ = confirm_trophy(roll=trophies.index(goomba_trophies[int(goomba_trophy)]), trophies=trophies, buckets=buckets)
        
        print(f"NUMBER OF REMAINING 1PO TROPHIES: {len(trophies)}")
    print("Done")


if __name__ == "__main__":
    main()