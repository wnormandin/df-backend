import requests
from df_backend.api.models import NameLanguage


def populate_languages():
    url = 'https://www.searchify.ca/wp-content/uploads/2018/07/List-of-languages-txt.txt'

    resp = requests.get(url)
    languages = [name.replace('"', '') for name in resp.content.decode().split('\n')]

    NameLanguage.objects.bulk_create([NameLanguage(name=lang, description='Retrieved from https://www.searchify.ca/wp-content/uploads/2018/07/List-of-languages-txt.txt') for lang in languages])


if __name__ == '__main__':
    populate_languages()