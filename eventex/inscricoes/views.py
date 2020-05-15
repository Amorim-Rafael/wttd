from django.shortcuts import render
from eventex.inscricoes.forms import InscricaoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages


def inscricao(request):
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        
        if form.is_valid():
            body = render_to_string('inscricoes/inscricao_email.txt', 
                                    form.cleaned_data)

            mail.send_mail('Confirmação de inscrição', 
                            body, 
                            'contato@eventex.com.br', 
                            ['contato@eventex.com.br', form.cleaned_data['email']])
            
            messages.success(request, 'Inscrição realizada com sucesso!')
            
            return HttpResponseRedirect('/inscricao/')
        else :
            return render(request, 'inscricoes/inscricao_form.html', 
                          { 'form': form })
    else:
        context = {'form': InscricaoForm()}
        return render(request, 'inscricoes/inscricao_form.html', context)
