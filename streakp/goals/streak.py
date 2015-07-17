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
    return get_streak(values)