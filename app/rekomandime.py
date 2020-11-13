import ast
import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Liber, Cache


@login_required(login_url='/accounts/login/')
def rekomandime(request):
    while True:
        time.sleep(1.1)
        if Cache.objects.filter(perdorues=request.user).last():
            break
    libra_te_rekomaduar_ids = ast.literal_eval(Cache.objects.filter(perdorues=request.user).last().librat_to_string)
    data = {
        'titulli_i_faqes': 'Librat e Sygjeruar',
        'librat': [lib.as_dict() for lib in Liber.objects.filter(iid__in=libra_te_rekomaduar_ids)],
        'edit': False
    }
    return render(request, 'libratemi.html', data)
