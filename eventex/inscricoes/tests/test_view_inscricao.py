from django.test import TestCase
from eventex.inscricoes.forms import InscricaoForm
from django.core import mail

class InscreverGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use inscricoes/inscricao_form.html"""
        self.assertTemplateUsed(self.response, 'inscricoes/inscricao_form.html')

    def test_html(self):
        """Html must contains input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)
        

    def test_csrf(self):
        """Html must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have inscricao form"""
        form = self.response.context['form']
        self.assertIsInstance(form, InscricaoForm)


class InscreverPostValid(TestCase):
    def setUp(self):
        data = dict(name='Rafael Amorim', cpf='12345678901', 
                    email='rafael@amorim.net', phone='00-99999-9090')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_inscrever_email(self):
        self.assertEqual(1, len(mail.outbox))
    

class InscriverPostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})
    
    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'inscricoes/inscricao_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, InscricaoForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)


class InscreverSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Rafael Amorim', cpf='12345678901',
                    email='rafael@amorim.net', phone='00-99999-9090')
        
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')