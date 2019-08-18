import django
import json
from df_backend.utils import setup_logging

logger = setup_logging()


def main():
    from df_backend.api import models, resources, serializers

    rc = models.EntityRace.objects.first()
    pf = models.EntityProfession.objects.first()

    cb = models.User.objects.get(id=1)
    pl = models.User.objects.get(username='df_user')
    go = models.Game.objects.filter(player=pl, created_by=cb).first()
    gm = models.GameMap.objects.filter(game=go).first()

    while True:
        e = resources.generate_entity(gender='male', race=rc, prof=pf,
                                      created_by=cb, game_map=gm)

        print(json.dumps(serializers.EntitySerializer(e).data, sort_keys=True, indent=2))

        ch = input('Another? (y/n)> ')
        if ch.upper() != 'Y':
            break


if __name__ == '__main__':
    django.setup()
    main()
