from itertools import product

def check(key: str) -> bool:
    raw = key.split("-")

    one = int(raw[0], 16)
    two = int(raw[1], 16)
    three = int(raw[2], 16)

    if (one * two) <= three:
        if abs(one - two) >= three:
            if three % 2 != 0:
                
                if (one + two) > three:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def generate(count = 1) -> list:
    tmp = []
    tmp_count = 0

    for tmp_one in product("0123456789abcdef", repeat=4):
        for tmp_two in product("0123456789abcdef", repeat=4):
            for tmp_three in product("0123456789abcdef", repeat=4):

                    one = "".join(tmp_one)
                    two = "".join(tmp_two)
                    three = "".join(tmp_three)

                    try:
                        if tmp_count < count:
                            if check(f"{one}-{two}-{three}") == True:
                                tmp.append(f"{one}-{two}-{three}")
                                tmp_count += 1
                        else:
                            return tmp
                        
                    except ZeroDivisionError:
                        continue