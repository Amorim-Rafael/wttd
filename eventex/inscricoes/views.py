from django.shortcuts import render
from eventex.inscricoes.forms import InscricaoForm
from django.http import HttpResponseRedirect
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings


def inscricao(request):
    if request.method == 'POST':
        return criar(request)
    else:
        return novo(request)


def criar(request):
    form = InscricaoForm(request.POST)

    if not form.is_valid():
        return render(request, 'inscricoes/inscricao_form.html', 
                      { 'form': form })

    enviar_email('Confirmação de inscrição', 
                 settings.DEFAULT_FROM_EMAIL,
                 form.cleaned_data['email'],
                 'inscricoes/inscricao_email.txt',
                 form.cleaned_data)

    messages.success(request, 'Inscrição realizada com sucesso!')
    
    return HttpResponseRedirect('/inscricao/')


def novo(request):
    return render(request, 'inscricoes/inscricao_form.html', {'form': InscricaoForm()})


def enviar_email(subject, from_, to, template_name, content):
    body = render_to_string(template_name, content)
    mail.send_mail(subject, body, from_, [from_, to])