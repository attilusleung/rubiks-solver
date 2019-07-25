from functools import reduce

def bit_repr(i, digits=16):
    return format(i, f'#0{digits + digits//4 - (not digits % 4) + 2}_b')

def face_repr(i):
    return bit_repr(i)

def tile_repr(i):
    return bit_repr(i, 4)

def cube_repr(i):
    return bit_repr(i, 16*6)

def ones(digits):
    return (1 << digits) - 1

def clear(i, start, end):
    return u_not(ones(end-start) << start, i.bit_length()) & i

def u_not(i, length=None):
    if length is None: length = i.bit_length()
    return ones(length) - i

def bit_roll(i, direction, start, end, bit_unit=4):
    start = start * bit_unit
    end = end * bit_unit
    direction = direction * bit_unit
    length = end - start
    j = ((ones(length) << start) & i) >> start

    if direction > 0:
        swp = (ones(direction) & j) << (length-direction)
        j = (j >> direction) & ones(length-direction)
    else:
        swp = ((ones(-direction) << length+direction) & j) >> length+direction
        j = (ones(length+direction) & j) << -direction
    return ((j | swp) << start) | clear(i, start, end)

def bit_strip(i, start, end):
    a = clear(i, 0, end) >> (end-start)
    b = ones(start) & i
    return a | b

def or_sum(it):
    return reduce(lambda x, y: x | y, it)
