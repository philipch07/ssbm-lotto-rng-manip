from tagrss import TagRss

# while it might be nice to use sets instead of lists, we do actually need the order of the trophies.

TAGS = ['AAAA','1DER','2BIT','2L8','2PAY','401K','4BDN','4BY4','4EVA','7HVN','AOK','ARCH','ARN','ASH','BAST','BBBB','BCUZ','BETA','BOBO',
        'BOMB','BONE','BOO','BORT','BOZO','BUB','BUD','BUZZ','BYRN','CHUM','COOP','CUBE','CUD','DAYZ','DIRT','DIVA','DNCR','DUCK','DUD',
        'DUFF','DV8','ED','ELBO','FAMI','FIDO','FILO','FIRE','FLAV','FLEA','FLYN','GBA','GCN','GLUV','GR8','GRIT','GRRL','GUST','GUT',
        'HAMB','HAND','HELA','HEYU','HI5','HIKU','HOOD','HYDE','IGGY','IKE','IMPA','JAZZ','JEKL','JOJO','JUNK','KEY','KILA','KITY','KLOB',
        'KNEE','L33T','L8ER','LCD','LOKI','LULU','MAC','MAMA','ME','MILO','MIST','MOJO','MOSH','NADA','ZZZZ','NAVI','NELL','NEWT','NOOK',
        'NEWB','ODIN','OLAF','OOPS','OPUS','PAPA','PIT','POP','PKMN','QTPI','RAM','RNDM','ROBN','ROT8','RUTO','SAMI','SET','SETI','SHIG',
        'SK8R','SLIM','SMOK','SNES','SNTA','SPUD','STAR','THOR','THUG','TIRE','TLOZ','TNDO','TOAD','TOMM','UNO','VIVI','WALK','WART','WARZ',
        'WITH','YETI','YNOT','ZAXO','ZETA','ZOD','ZOE','WORM','GEEK','DUDE','WYRN','BLOB']

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

TROPHIES_1PO = ['warp star', 'beam sword', 'green shell', 'freezie', 'parasol', 'screw attack', 'charizard', 'electrode', 'staryu', 'marill', 
                'vegetable', 'banzai bill', 'four giants', 'master sword', 'koopa paratroopa', 'redead', 'octorok', 'like like', 'plum', 
                'viruses', 'goron', 'fire kirby', 'paula', 'cleffa', 'love giant', 'pit', 'ayumi tachibana']

TROPHIES_1PL_1PO = ['warp star', 'ray gun', 'super scope', 'fire flower', 'star rod', 'beam sword', 'homerun bat', 'fan', 'green shell', 
                    'flipper', 'freezie', 'mr saturn', 'bobomb', 'super mushroom', 'starman mario', 'parasol', 'screw attack', 
                    'barrel cannon', 'party ball', 'crate', 'barrel', 'capsule', 'egg', 'charizard', 'squirtle', 'blastoise', 'clefairy', 
                    'electrode', 'weezing', 'goldeen', 'staryu', 'snorlax', 'chikorita', 'cyndaquil', 'bellossom', 'marill', 'wobbuffet', 
                    'scizor', 'porygon2', 'toad', 'coin', 'vegetable', 'kirby hat 1', 'kirby hat 2', 'kirby hat 3', 'banzai bill', 
                    'lakitu', 'birdo', 'klap trap', 'four giants', 'master sword', 'slippy toad', 'koopa troopa', 'koopa paratroopa', 
                    'redead', 'octorok', 'like like', 'topi', 'metal mario', 'plum', 'daisy', 'thwomp', 'viruses', 'bucket', 'racing kart', 
                    'baby bowser', 'raphael raven', 'goron', 'dr stewart', 'jody summer', 'andross 64', 'metroid', 'ridley', 
                    'fire kirby', 'ball kirby', 'waddle dee', 'rick', 'paula', 'starman earthbound', 'bulbasaur', 'poliwhirl', 'totodile', 
                    'crobat', 'cleffa', 'igglybuff', 'steelix', 'heracross', 'zeroone', 'ryota hayami', 'love giant', 'heririn', 
                    'excitebike', 'ducks', 'balloon fighter', 'pit', 'dr wright', 'donbe & hikari', 'ayumi tachibana', 'monster']

TROPHIES_1PL_1PO_TAGGED = [['warp star', True], ['ray gun', False], ['super scope', False], ['fire flower', False], ['star rod', False], ['beam sword', True], 
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

def get_trophies(base_trophy_set, input_trophy = None):
    trophies = base_trophy_set
    skip = input_trophy is not None
    if input_trophy is None:
        input_trophy = input("Type the names of the trophies that you've collected in the gallery. Substrings are allowed, but be careful. Type 'x' or 'q' to finish.\n")
    while input_trophy.lower() != 'x' and input_trophy.lower() != 'q':
        found = False
        misinput = False
        multiple_trophies = ''
        substr_matches = False
        
        for i, t in enumerate(trophies):
            exact_match = False
            tt = t[0] if len(t) == 2 else t
            if input_trophy in tt:
                exact_match = input_trophy == tt
                if not exact_match:
                    multiple_trophies += trophy_str(tt)
                    for t_forward in trophies[i+1:]:
                        ttt = t_forward[0] if len(t_forward) == 2 else t_forward
                        if input_trophy in ttt:
                            exact_match = input_trophy == ttt
                            multiple_trophies += trophy_str(t_forward)
                            substr_matches = True
                    if not exact_match and substr_matches:
                        multiple_trophies = multiple_trophies[:-1].replace("|", "\n")
                        print(f"These trophies contain the substring '{input_trophy}':\n{multiple_trophies}\nPlease retype the trophy name.")
                        break
                    if exact_match:
                        continue
                print(f'{tt} found!')
                confirmed = not input(f"Confirm {tt} trophy? Hit [ENTER] if yes, otherwise input a character.\n")
                if confirmed:
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
        if skip and found:
            break
        else:
            input_trophy = input("Trophy name (x or q to quit):\n")
    return trophies

def get_seed() -> (int, [int]):
    """ Returns the seed and the list of rolled tags as a tuple."""
    print('Go to the tag menu and roll 5 tags (type them in and hit enter between each).')
    rolled_tags = []
    rt_append = rolled_tags.append
    while len(rolled_tags) != 5:
        new_tag = input(f"tag #{len(rolled_tags) + 1}: ")
        ind = TAGS_DICT.get(new_tag.upper(), -1)
        if ind != -1:
            rt_append(ind)
        else:
            print('Invalid tag, please check for any typos.')
    
    potential_seed = TagRss(rolled_tags)
    while len(potential_seed) > 1:
        print(f"There are {len(potential_seed)} potential seeds, please keep rolling tags as prompted.")
        new_tag = input(f"tag #{len(rolled_tags) + 1}: ")
        ind = TAGS_DICT.get(new_tag.upper(), -1)
        if ind != -1:
            rt_append(ind)
            bad_seeds = [i for i, seed in enumerate(potential_seed) if seed[1][len(rolled_tags) - 1] != rolled_tags[-1]]
            for b in reversed(bad_seeds):
                del potential_seed[b]
        else:
            print('Invalid tag, probably a typo')
    
    # i should test the weird case of [l8er, bone, opus, dayz, coop]
    return potential_seed[0][2][len(rolled_tags) - 5], rolled_tags

def trophy_str(t: list[str, int, bool]) -> str:
    ret = f'- {t} '
    added_str = f' (new)|' if t[1] else f' (owned)|'
    return ''.join([ret, added_str])

def print_tags(tags_to_roll: list[str]):
    if len(tags_to_roll) == 0:
        print("No rolls are necessary")
    else:
        # print the last 5 tags to roll, as too many tags will clutter the prompt
        print(f'You need to roll {len(tags_to_roll)} tags')
        num_tags_to_print = min(5, len(tags_to_roll))
        for tags in tags_to_roll[-1*num_tags_to_print:]:
            print(tags)