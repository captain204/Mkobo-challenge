from random import randrange


"""Function to generate 10 digit account numbers"""
def account():
    arr = [0] * 10
    i = 0
    while i < 10:
        num = randrange(9)
        arr[i] = num
        i += 1   
    return convert(arr)

    

"""Function to convert a list into an integer"""

def convert(lst):
    s = [str(i) for i in lst]
    result = int("".join(s))
    return result


