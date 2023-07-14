"""
Reverse seed search script for reversing current random seed in SSBM based on sequence of repeated random nametag rolls.
Author: tauKhan

Use function TagRss to reverse list of matching seeds from 5 consequent random tags.

In SSBM, random numbers are generated using a simple LCG to advance seed. This search algorithm uses the linear
properties of the generator to quickly rule out large chunks of possible starting seeds. The main observation is that
composition of linear functions is linear. With seed advance denoted as next, therefore next(next(s)) or
next(next(next(s))) etc. are linear functions of seed s. Furthermore, linear combination of linear functions is linear,
so for instance a * next(s) + b * next(next(s)) + c * next(next(next(s))) is linear. Second important property is that
the random integer function with which random tags are determined in SSBM, divides the seed space into neat continuous
intervals corresponding to each possible outcome. For instance, the result of random_int(s) is 0 iff 0 <= s <= 29622271,
random_int(s) is 1 iff 29622272 <= s <= 59244543 and so on. This is very useful because certain nametag appearing in
sequence at a given place means a seed after corresponding number of advances must be within a continuous interval. For
instance, if 2nd nametag corresponds to 1, then 29622272 <= next(next(seed)) <= 59244543. Similarly, linear combinations
gain eligibility intervals. Say tag1 is 0, and tag2 is 1. Then -2*29622271 + 3*29622272 <= -2*next(seed) + 3*next(next((seed))
<= -2*0 + 3*59244543.

The script operates by using linear combinations of seed advances that together have a small co-efficient, so the value
of that linear function changes little as you change seed. With such combinations its quick to calculate where
eligible areas of seeds appear. The used combination co-efficients are listed as vectors in CONSTRICTS constant list.
"""

TAGS = ['AAAA','1DER','2BIT','2L8','2PAY','401K','4BDN','4BY4','4EVA','7HVN','AOK','ARCH','ARN','ASH','BAST','BBBB','BCUZ','BETA','BOBO','BOMB','BONE','BOO','BORT',
             'BOZO','BUB','BUD','BUZZ','BYRN','CHUM','COOP','CUBE','CUD','DAYZ','DIRT','DIVA','DNCR','DUCK','DUD','DUFF','DV8','ED','ELBO','FAMI','FIDO','FILO','FIRE',
             'FLAV','FLEA','FLYN','GBA','GCN','GLUV','GR8','GRIT','GRRL','GUST','GUT','HAMB','HAND','HELA','HEYU','HI5','HIKU','HOOD','HYDE','IGGY','IKE','IMPA','JAZZ',
             'JEKL','JOJO','JUNK','KEY','KILA','KITY','KLOB','KNEE','L33T','L8ER','LCD','LOKI','LULU','MAC','MAMA','ME','MILO','MIST','MOJO','MOSH','NADA','ZZZZ','NAVI',
             'NELL','NEWT','NOOK','NEWB','ODIN','OLAF','OOPS','OPUS','PAPA','PIT','POP','PKMN','QTPI','RAM','RNDM','ROBN','ROT8','RUTO','SAMI','SET','SETI','SHIG','SK8R',
             'SLIM','SMOK','SNES','SNTA','SPUD','STAR','THOR','THUG','TIRE','TLOZ','TNDO','TOAD','TOMM','UNO','VIVI','WALK','WART','WARZ','WITH','YETI','YNOT','ZAXO',
             'ZETA','ZOD','ZOE','WORM','GEEK','DUDE','WYRN','BLOB']

MAX_STAGES = 5

CONSTMULTIP = [
[[-27, 0, 18, 8, 1, 0], 3221225472],
[[0, 27, 0, -18, -8, -1] , 1073741824],
[[5, -3, -26, 30, -1, -13] , 1563581562 ],
[[-14, -20, -18, -3, -18, -23] , 509367736 ],
[[24, -5, 22, 15, -5, -15] , 1016946651 ]
]
CONSTRICTS = [
[
[[0, 18, 8, 1, 0] ,27],
[[5, -4, -7, 6, 15] ,51],
[[5, 14, 1, 7, 15] ,78],
[[-15, -4, -2, -11, -8] ,92],
],
[
[[-10, -8, -9, -5, 7] ,143],
[[-10, 10, -1, -4, 7] ,170],
[[-5, 6, -8, 2, 22] ,221],
[[4, -6, 10, -17, 0] ,335],
[[-1, 0, 2, -15, 22] ,556],
],

[
[[15, 3, -2, 1, -2] ,1627],
[[0, -1, -4, -10, -10] ,1719],
[[5, 13, -3, -3, 5] ,1797],
[[1, 0, -25, 3, -5] ,3154],
[[3, -12, 6, 9, -3] ,3227],
[[-7, -2, 5, 5, 4] ,3397],
],

[
[[3, -13, 2, -1, -13] ,4946],
[[3, 5, 10, 0, -13] ,4973],
[[6, 13, -28, 0, 0] ,4951],
[[6, 31, -20, 1, 0] ,4978],
[[8, 1, 3, 6, 2] ,5024],
[[-7, -3, 1, -5, -6] ,5116],
[[-2, -7, -6, 1, 9] ,5167],
[[-2, 11, 2, 2, 9] ,5194],
],

[
[[-7, -14, 3, -2, -5] ,30563],
[[-7, 4, 11, -1, -5] ,30590],
[[-2, 0, 4, 5, 10] ,30641],
[[-6, 5, -10, 12, 0] ,32025],
[[-2, -19, -8, -6, 0] ,32333],
[[-2, -1, 0, -5, 0] ,32360],
[[-2, 17, 8, -4, 0] ,32387]
],

[
[[-4, 5, 10, -6, 1] ,90194],
[[1, 1, 3, 0, 16] ,90245],
[[2, 0, -3, 5, -16] ,91408],
[[1, 0, -1, -10, 6] ,91964],
[[8, 2, -5, -5, -4] ,210616],
[[1, 0, 0, 0 ,0] ,214013],
[[1, 18, 8, 1 ,0] ,214040],
[[9, 0, -1, -4, -8] ,220756]
]

]

SEEDCONST = 2531011
SEEDMULT = 214013
SIZE = 4294967296
MAXINT = 4294967295
HSIZE = 65536


def list_eq(t1, t2):

    for i in range(0, len(t1)):
        if t1[i] != t2[i]:
            return False

    return True


def list_mul_conditional_to_sign(list1, list2, list3, s):

    ret = []
    for i in range(0, len(list1)):
        ret.append(list1[i ] *list2[i]) if s* list1[i] >= 0 else ret.append(list1[i] * list3[i])

    return ret


def calc_mrestrict_accept_area(multiplicator, seed_maxes, seed_mins):

    return sum_of_elements(list_mul_conditional_to_sign(multiplicator, seed_maxes, seed_mins, -1)), sum_of_elements(
        list_mul_conditional_to_sign(multiplicator, seed_maxes, seed_mins, 1))


def get_low_and_up_borders(list, bound=145):

    low = []
    up = []
    for i in range(0, len(list)):
        l, u = get_l_and_u_bounds(list[i], bound)
        low.append(l)
        up.append(u)
    return low, up


def list_mul(list1, list2):
    ret = []
    for i in range(0, len(list1)):
        ret.append(list1[i] * list2[i])

    return ret


def sum_of_elements(list):
    sum = 0
    for element in list:
        sum = (element + sum) & MAXINT

    return sum


def next(seed):
    return (seed * SEEDMULT + SEEDCONST) & MAXINT


def sequence_list(seed, length):
    list = []

    for i in range(0, length):
        seed = next(seed)
        list.append(seed)

    return list


def rand_int(seed, bound=145):
    return ((seed >> 16) * bound) >> 16


def lower_bound(val, bound=145):
    return int(HSIZE / bound * val + 1) * HSIZE


def find_next_aperiod_and_remainder_split(start_val, abound_l,
                                          abound_u, shortp_diff, interval,
                                          short_period=1, shift=0):
    distance, end_dist = abound_l - start_val, abound_u - start_val

    accepted_area = abound_u - abound_l + SIZE

    if end_dist < 0:
        end_dist += SIZE

    if distance <= 0:
        return shift, end_dist // interval + shift, -distance

    if start_val <= abound_u:

        return shift, end_dist // interval + shift, 0
    else:

        steps = distance // interval + int(distance % interval != 0)
        return steps + shift, end_dist // interval + shift, steps * interval + start_val - abound_l


def find_next_aperiod_and_remainder_rising(start_val, abound_l,
                                           abound_u, shortp_diff, interval,
                                           short_period=1, shift=0):
    f_distance, f_end_distance = SIZE, SIZE
    j = 0
    for i in range(0, short_period):

        distance, end_dist = abound_l - start_val + interval * i, abound_u - start_val + interval * i
        if (distance <= 0) & (end_dist >= 0):
            return i + shift, i + (end_dist // shortp_diff) * short_period + shift, -distance

        if end_dist < 0:
            distance, end_dist = distance + SIZE, end_dist + SIZE

        if distance < f_distance:
            f_distance, f_end_distance, j = distance, end_dist, i

    steps = j + (f_distance // shortp_diff + int(f_distance % shortp_diff != 0)) * short_period

    return steps + shift, f_end_distance // shortp_diff * short_period + j + shift, (
                (steps * interval + start_val) & MAXINT) - abound_l


def screen_sequence(sequence):
    accept_mins, accept_maxs = get_low_and_up_borders(sequence)

    for constrictor in CONSTMULTIP:

        areal, areau = calc_mrestrict_accept_area(constrictor[0], accept_maxs, accept_mins)

        if areal < areau:
            if (constrictor[1] < areal) or (constrictor[1] > areau):
                return False

        else:
            if (constrictor[1] > areal) and (constrictor[1] < areau):
                return False

    return True


def find_matching_seed(orig_sequence, lowerbound, upperbound, stage=0):
    results = []
    sequence = orig_sequence.copy()[1:]
    sequence_len = len(sequence)
    constrictors = CONSTRICTS[stage]
    curr_lbound = lowerbound
    accept_mins, accept_maxs = get_low_and_up_borders(sequence)
    next_area_lborders = [0] * len(constrictors)
    next_area_uborders = [0] * len(constrictors)

    while curr_lbound <= upperbound:
        seed_seq = sequence_list(curr_lbound, sequence_len)
        temp_shift = 0
        for i in range(0, len(constrictors)):

            if next_area_uborders[i] > curr_lbound:
                continue
            else:
                seed_areal, seed_areau = calc_mrestrict_accept_area(constrictors[i][0], accept_maxs, accept_mins)
                if seed_areau < seed_areal:
                    l, u, r = find_next_aperiod_and_remainder_split(
                        sum_of_elements(list_mul(seed_seq, constrictors[i][0]))
                        , seed_areal, seed_areau, constrictors[i][1], constrictors[i][1], shift=temp_shift)
                else:
                    l, u, r = find_next_aperiod_and_remainder_rising(
                        sum_of_elements(list_mul(seed_seq, constrictors[i][0]))
                        , seed_areal, seed_areau, constrictors[i][1], constrictors[i][1], shift=temp_shift)

                next_area_lborders[i], next_area_uborders[i] = l + curr_lbound, u + curr_lbound

        l, u = max(next_area_lborders), min(next_area_uborders)
        if l < u:
            if (u - l > 300) & (stage < MAX_STAGES):
                results += find_matching_seed(orig_sequence, l, u, stage + 1)
            else:
                result = find_matching_seed_short_interval(orig_sequence, l, u)
                results += result

        curr_lbound = min(next_area_uborders) + 1

    return results


def get_l_and_u_bounds(val, bound=145):

    if val == 0:
        return 0, lower_bound(1, bound) - 1

    elif val == bound - 1:
        return lower_bound(val, bound), MAXINT

    else:
        return lower_bound(val, bound), lower_bound(val + 1, bound) - 1


def find_matching_seed_short_interval(random_samples, low=0, up=MAXINT):

    results = []
    lowest1, uppest1 = get_l_and_u_bounds(random_samples[0], 145)

    if low > lowest1:
        lowest1 = low

    if up < uppest1:
        uppest1 = up

    one = random_samples[1]
    two = random_samples[2]
    thr = random_samples[3]
    fur = random_samples[4]

    for seed in range(lowest1, uppest1+1):

        nexts = (seed * SEEDMULT + SEEDCONST) & MAXINT
        if (((nexts >> 16) * 145) >> 16) != one:
            continue

        nexts = (nexts * SEEDMULT + SEEDCONST) & MAXINT
        if (((nexts >> 16) * 145) >> 16) != two:
            continue

        nexts = (nexts * SEEDMULT + SEEDCONST) & MAXINT
        if (((nexts >> 16) * 145) >> 16) != thr:
            continue

        nexts = (nexts * SEEDMULT + SEEDCONST) & MAXINT
        if rand_int(nexts) != random_samples[4]:
            continue

        nexts = (nexts * SEEDMULT + SEEDCONST) & MAXINT
        if rand_int(nexts) != random_samples[5]:
            continue

        results.append(previous(seed))

    return results


def previous(seed):
    return (seed * 3115528533 + 2708534849) & MAXINT


def TagRss(sequence):
    """
    Finds a list of possible matches given a 5 integer sequence of consequent tag ints. If the returned match list is
    longer than 1, then more tags are required to specify current seed. But it will be contained in the match list.

    :param sequence: List of 5 ints corresponding to sequence of ingame tags. The list length has to be exactly 5.
    :return: List of match lists. Each match list has 3 items; starting seed, list of tag ints generated from the
    starting seed, and ending seed, the seed that the sequence ends on post tag generation.
    """
    hits = []

    for i in range(0, 2):

        for j in range(0, 3):
            if j > i + 1:
                pass
            else:
                for k in range(0, 4):
                    if k > max(i, j) + 1:
                        pass
                    else:

                        for l in range(0, 5):

                            if l > max(i, j, k) + 1:
                                pass

                            elif l == 4:

                                for n in range(0, 145):
                                    vec = [sequence[0], sequence[i], sequence[j], sequence[k], sequence[l], n]
                                    if screen_sequence(vec):
                                        lowbound, upbound = get_l_and_u_bounds(vec[0])
                                        hits += find_matching_seed(vec, lowbound, upbound)



                            else:
                                for m in range(0, 5):
                                    if m > max(i, j, k, l) + 1:
                                        pass


                                    else:
                                        vec = [sequence[0], sequence[i], sequence[j], sequence[k], sequence[l],
                                               sequence[m]]
                                        if screen_sequence(vec):
                                            lowbound, upbound = get_l_and_u_bounds(vec[0])
                                            hits += find_matching_seed(vec, lowbound, upbound)

    matches = validate_hits(sequence, hits)
    return matches


def validate_hits(sequence, hits):
    valids = []

    for seed in hits:

        tag_list, post_seed = generate_tags(seed)
        if list_eq(sequence, tag_list):
            valids.append([seed, tag_list, post_seed])

    return valids


def generate_tags(seed, length=5):
    """
    Returns a list of tag ints and ending seed generated from starting point <<seed>>

    :param seed: int, starting seed from which tag ints are generated.
    :param length: int, length of the generated tag list
    :return: tags: int list, s: ending seed after list generation.
    """
    s = next(seed)
    tags = [rand_int(s)]

    for num in range(1, length):

        not_appended = True
        low_end = max(num-5, 0)

        while not_appended:
            s = next(s)
            tag = rand_int(s)
            if tag not in tags[low_end: num]:
                tags.append(tag)
                not_appended = False

    return tags, s


# type in the 5 tags that you got!
