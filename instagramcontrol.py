import json
import sys
from instagram.InstagramAPI import InstagramAPI


def eprint(*args, **kwargs):
    """
    Prints to standard error.
    :param args: 
    :param kwargs: 
    :return: 
    """
    print(*args, file=sys.stderr, **kwargs)


def get_credentials(file):
    """
    Loads username and password from json file. 
    :param file: JSON file containing username and password.
    :return: username and password fields.
    """
    try:
        data = json.load(open(file))
    except Exception as e:
        eprint("Error attempting to load JSON from credentials file {}".format(file))
        print(str(e))
        return None, None
    try:
        user = data["username"]
        password = data["password"]
    except KeyError as e:
        eprint("Missing data from file {}".format(file))
        print(str(e))
        return None, None
    return user, password


if __name__ == '__main__':
    user, password = get_credentials("credentials.json")
    instagram_api = InstagramAPI(user, password)
    instagram_api.login()  # login

    photo_file = "photos/weddingshots-2017-12-31-15:40:50.jpg"
    print("Uploading photo {}", photo_file)
    caption = "Sample photo"
    instagram_api.uploadPhoto(photo_file, caption=caption)