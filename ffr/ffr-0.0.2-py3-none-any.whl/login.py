"""This example demonstrates the flow for retrieving a refresh token.

In order for this example to work your application's redirect URI must be set
to http://localhost:8080.

This tool can be used to conveniently create refresh tokens for later use with
your web application OAuth2 credentials.

"""
import os
import sys
import random
import configparser

import praw


def login():
    print(
        "Go here while logged into the account you want to create a token for: "
        "https://www.reddit.com/prefs/apps/"
    )
    print(
        "Click the create an app button. Put something in the name field and select the"
        " script radio button."
    )
    print("Put http://localhost:8080 in the redirect uri field and click create app")

    print("\nEnter the client ID, it's the line just under Personal use script at the top: ", end='')
    client_id = input()

    print("Enter the client secret, it's the line next to secret: ", end='')
    client_secret = input()

    print("Enter your username: ", end='')
    username = input()
    print("Now enter your password: ", end='')
    password = input()

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8080",
        user_agent="saved_reddit_script",
    )

    state = str(random.randint(0, 65000))

    url = reddit.auth.url(["identity"], state, "permanent")
    print("\nNow open this url in your browser: " + url)

    praw_section = 'USER' if is_new_user() else username

    user_info = f"""[{praw_section}]
client_id={client_id}
client_secret={client_secret}
username={username}
password={password}\n
"""
    
    dst = get_praw_conf()
    add_to_file(dst, user_info)

    print(f"\n\nThat's it, everything's been pasted in the praw.ini file.\nYou can find it in {dst}\n"
        "\nIf this is your second account, you'll have to specify the user with the --user flag.")
    return 0


def add_to_file(dst, string):
    """Append the user config to praw.ini config file"""
    with open(dst, 'a') as f:
        f.write(string)
        f.write("\n")


def get_praw_conf():
    """Returns the path to the praw.ini config file"""
    
    # Borrowed from https://github.com/praw-dev/praw/blob/973dc8a9471a0c05e88dde9de3463b3863e6eecc/praw/settings.py#L31
    if 'APPDATA' in os.environ:  # Windows
        os_config_path = os.environ['APPDATA']
    elif 'XDG_CONFIG_HOME' in os.environ:  # Modern Linux
        os_config_path = os.environ['XDG_CONFIG_HOME']
    elif 'HOME' in os.environ:  # Legacy Linux
        os_config_path = os.path.join(os.environ['HOME'], '.config')
    else:
        os_config_path = os.path.dirname(sys.modules[__name__].__file__)
    
    return os.path.join(os_config_path, 'praw.ini')

def is_new_user():
    """Return True if there is no section in the praw.ini file
    with a USER section"""
    praw_path = get_praw_conf()
    config = configparser.ConfigParser()
    config.read(praw_path)
    sections = config.sections()

    return False if 'USER' in sections else True


if __name__ == "__main__":
    login()
