def connected():
    try:
        __import__('urllib.request').request.urlopen('https://www.google.com')
    except:
        return False
    else:
        return True
