import math


millnames = [
    "", "k", "m", "b", "t", "big"
]


def millify_num(number):
    n = float(number)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
    result = ('%.3f' % (n / 10 ** (3 * millidx))).rstrip('0').rstrip('.')
    return '{0}{dx}'.format(result, dx=millnames[millidx])