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
    start *= bit_unit
    end *= bit_unit
    direction *= bit_unit
    length = end - start
    j = ((ones(length) << start) & i) >> start

    if direction > 0:
        swp = (ones(direction) & j) << (length-direction)
        j = (j >> direction) & ones(length-direction)
    else:
        swp = ((ones(-direction) << length+direction) & j) >> length+direction
        j = (ones(length+direction) & j) << -direction
    return ((j | swp) << start) | clear(i, start, end)

def bit_strip(i, start, end, bit_unit=4):
    start *= bit_unit
    end *= bit_unit
    a = clear(i, 0, end) >> (end-start)
    b = ones(start) & i
    return a | b

def bit_swap(i, start_1, end_1, start_2, end_2, bit_unit=4):
    start_1 *= bit_unit
    start_2 *= bit_unit
    end_1 *= bit_unit
    end_2 *= bit_unit
    swp = ((ones(end_1 - start_1) << start_1) & i) >> start_1
    # print(bit_repr(swp, bit_unit))
    i = ((((ones(end_2 - start_2) << start_2) & i) >> start_2) << start_1) | clear(i, start_1, end_1)
    # print(bit_repr(i, 16*6))
    # print(bit_repr(swp << start_2, 16*6))
    # print(bit_repr(clear(i, start_2, end_2), 16*6))
    return (swp << start_2) | clear(i, start_2, end_2)

def or_sum(it):
    return reduce(lambda x, y: x | y, it)
