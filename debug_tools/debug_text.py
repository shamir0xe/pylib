import sys


def debug_text(*texts):
    """ "
    the function for printing debug text into stderr
    usage:
        use % for extra arguments inside the string
    """
    colors = {
        "b": "\033[94m",
        "c": "\033[96m",
        "y": "\033[93m",
        "B": "\033[1m",
        "H": "\033[95m",
        "U": "\033[4m",
        "r": "\033[91m",
        "g": "\033[92m",
        "E": "\033[0m",
    }
    arr = []
    sz = len(texts)
    i = 0
    while i < sz:
        if isinstance(texts[i], str):
            res = ""
            count = 0
            j = 0
            args = []
            while j < len(texts[i]):
                char = texts[i][j]
                if char == "%":
                    if j + 1 < len(texts[i]) and texts[i][j + 1] in colors:
                        res += colors[texts[i][j + 1]]
                        j += 1
                    else:
                        res += "{}"
                        count += 1
                else:
                    res += char
                j += 1
            if count > 0:
                while count > 0:
                    i += 1
                    args.append(texts[i])
                    count -= 1
                res = res.format(*args)
            arr.append(res)
        else:
            arr.append(texts[i])
        i += 1
    sz = len(arr)
    res = ""
    for i in range(sz):
        if i > 0:
            res += ", "
        res += "[{}]"
    print(res.format(*arr), end="\r\n", flush=True, file=sys.stderr)
