def isnumber(string):
    try:
        float(string)
    except ValueError:
        return False
    return True
