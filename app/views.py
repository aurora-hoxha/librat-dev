from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from . import models
from .forms import HiqLiberForm, ShtoLiberForm
from .models import Vlersim, Liber


@require_http_methods(["GET"])
def libra(request, id):
    # "get_object_or_404"
    # Browserit / klientit i kthehet 404
    libri = get_object_or_404(models.Liber, pk=id)

    shto_form = ShtoLiberForm(initial={'liber_id': libri.iid})
    hiq_form = HiqLiberForm(initial={'liber_id': libri.iid})

    data = {
        'liber': libri,
        'titulli_i_faqes': 'Libra (id: {})'.format(id),
        'shto_form': shto_form,
        'hiq_form': hiq_form,
        'edit': True
    }

    return render(request, 'libra.html', data)


@require_http_methods(["GET"])
def autore(request, id):
    autori = get_object_or_404(models.Autor, pk=id)
    data = {
        'titulli_i_faqes': '{}: {}'.format(id, autori.emri),
        'autori': autori.as_dict(),
        'librat': [lib.as_dict() for lib in autori.librat.all()],
        'edit': False
    }
    return render(request, 'autore.html', data)


@login_required(login_url='/accounts/login/')
@require_http_methods(["GET"])
def librat_e_mi(request):
    user = request.user
    data = {
        'titulli_i_faqes': 'Librat e Mi',
        'librat': [lib.as_dict() for lib in user.profil.librat.all()],
        'edit': False
    }
    return render(request, 'libratemi.html', data)


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def shto_liber(request):
    form = ShtoLiberForm(request.POST)

    if not form.is_valid():
        # mund te cohet nje mesazh qe dicka shkoi keq, etj etj
        return

    user = request.user
    libri = models.Liber.objects.get(pk=form.cleaned_data['liber_id'])

    #
    user.profil.librat.add(libri)
    user.save()

    # redirect(<url>, <arg0>, <arg1>, ...)
    return redirect('libra', id=form.cleaned_data['liber_id'])


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def hiq_liber(request):
    form = HiqLiberForm(request.POST)

    if not form.is_valid():
        return

    user = request.user
    libri = models.Liber.objects.get(pk=form.cleaned_data['liber_id'])

    user.profil.librat.remove(libri)
    user.save()

    return redirect('libra', id=form.cleaned_data['liber_id'])


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def vlerso_liber(request):
    liber_id = None
    if request.method == 'POST':
        perdorues = request.user
        vlersimi = request.POST.get('vlerso')
        liber_id = request.POST.get('liber')

        vlersimi_pare = perdorues.vlersimet.filter(liber_id=liber_id)
        if vlersimi_pare.exists():
            vlersim_ri = vlersimi_pare.first()
            vlersim_ri.vlersimi = vlersimi
            vlersim_ri.save()
        else:
            vlersim = Vlersim.objects.create(perdorues_id=request.user.id, liber_id=liber_id, vlersimi=vlersimi)
    liber = Liber.objects.get(iid=liber_id)
    vlersimi_mesatar = liber.vlersimet.aggregate(Avg('vlersimi'))
    liber.vlersimi_avg = round(vlersimi_mesatar['vlersimi__avg'], 4)
    liber.save()
    return redirect('/app/libratemi/')
