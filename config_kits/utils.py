def get_value(ba, offset, shift, mask):
    j = (ba[offset]) << 8 | (ba[(offset - 1)])
    j = zero_fill_right_shift(j,shift)
    j &= mask
    return j

def set_value(ba, offset, shift, mask, new_value):
    j = (ba[offset]) << 8 | (ba[(offset - 1)])
    k = 0xFFFF & (mask << shift ^ 0xFFFFFFFF)
    j &= k
    new_value &= mask
    new_value <<= shift
    new_value = j | new_value
    ba[(offset - 1)] = (new_value & 0xFF)
    ba[offset] = (zero_fill_right_shift(new_value,8))

def zero_fill_right_shift(val, n):
    return (val % 0x100000000) >> n

def hex_to_rgb(value):
    # desde ask color para escribir en memoria
    value = value.lstrip('#')
    lv = len(value)
    return [int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)]

def rgb_to_hex(rgb):
    # desde memoria a valor aceptable para ask color
    return '#%02x%02x%02x' % tuple(rgb)

def check_value(min_value,value,max_value):
    return min_value <= value <= max_value
