def replace_char_in_string(string, newChar, index):
    """Replaces char in a string with another char at specified index."""

    string = string[:index] + newChar + string[index + 1:]
    return string


def list_to_string(changeList):
    """Converts a list to a string (works on int as well)"""

    changeList = [str(i) for i in changeList]
    string = ''.join(changeList)
    return string


def to_list(string):
    """Converts to list (works on int as well)"""

    number = True if type(string) == int else False
    string = str(string)
    newList = list(string)
    if number:
        for i in newList:
            if i.isnumeric():
                newList[newList.index(i)] = int(i)
    return newList


def list_to_2d_list(changeList):
    """Converts list to a list of lists (works on int as well)"""

    for i in changeList:
        changeList[changeList.index(i)] = to_list(i)
    return changeList


def get_key(dictionary, value):
    """Gets the first key found of a value in a dictionary"""

    for i, j in dictionary.items():
        if value == j:
            return i


def is_vowel(string):
    """Checks if all chars in string is vowel."""

    vowels = 'aeiou'
    return True if string.lower() in vowels else False


def remove_char_in_string(string, index):
    """Removes char at specified index."""

    string = string[:index] + string[index + 1:]
    return string


def get_divisors(number):
    """Gets list of divisors of number."""

    divisors = []
    for i in range(1, number + 1):
        if number % i == 0:
            divisors.append(i)

    return divisors


def is_palindrome(toCheck):
    """Checks if string or number is a palindrome (Doesn't work on palindromes with spaces)"""

    list1 = to_list(toCheck)
    list2 = to_list(toCheck)
    list2.reverse()
    return True if list1 == list2 else False


def is_even(number):
    """Checks if number is even"""

    return True if number % 2 == 0 else False


def is_prime(number):
    """Checks if number is prime."""

    if number <= 3:
        return number > 1
    elif number % 2 == 0 or number % 3 == 0:
        return False

    i = 5

    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True
