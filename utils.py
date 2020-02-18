def online():
    """
    Check if user is online, False if not
    """
    import requests as r
    try:
        r = r.get('https://www.example.com')
    except ConnectionError:
        print("Probably no internet, can't even connect to Example.com")
        return False
    return True
