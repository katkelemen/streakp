__author__ = 'fox'


def get_streak(values):
    if values:
        cons = [values[0]]
        for val in values[1:]:
            if cons[-1] == val-1:
                cons.append(val)
            else:
                cons = [val]
        return len(cons)
    else:
        return 0

def dates_to_ints(datelist):
    return map(lambda x: x.toordinal(), datelist)

def cons_dates(datelist):
    values = dates_to_ints(datelist)
    values_unique = list(set(values))
    values = sorted(values_unique)
    return get_streak(values)


def longest_streak(datelist):
    longest = 1
    ls = [0]
    values = sorted(dates_to_ints(datelist))
    for i in range(len(values)-1):
        if values[i]+1 == values[i+1]:
            longest += 1
        else:
            ls.append(longest)
            longest = 1
    ls.append(longest)
    return max(ls)