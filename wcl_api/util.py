import re

def parse_int_else_zero(string):
    filtered = re.sub('[^0-9]', '', string)
    return int(filtered) if filtered else 0