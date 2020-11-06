from django.contrib.auth.models import User
from django.db.models import Avg

from app.models import Liber


# Gjenerohet vetem nje here per perdorues
def sinkronizo_librat_e_mi(user_id):
    user = User.objects.get(id=user_id)
    Profil = user.profil
    librat = user.vlersimet.all().values_list('liber__iid', flat=True)
    librat = Liber.objects.filter(iid__in=list(librat))
    Profil.librat.add(*librat)


def sinkronizo_mesataret():
    librat = Liber.objects.all()

    for liber in librat:
        vlersimi_mesatar = liber.vlersimet.aggregate(Avg('vlersimi'))
        liber.vlersimi_avg = round(vlersimi_mesatar['vlersimi__avg'], 4)
        liber.save()
