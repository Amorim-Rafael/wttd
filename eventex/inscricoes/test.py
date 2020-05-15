from django.test import TestCase
from eventex.inscricoes.forms import InscricaoForm
from django.core import mail

class InscreverTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use inscricoes/inscricao_form.html"""
        self.assertTemplateUsed(self.response, 'inscricoes/inscricao_form.html')

    def test_html(self):
        "Html must contains input tags"
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"')
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """Html must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have inscricao form"""
        form = self.response.context['form']
        self.assertIsInstance(form, InscricaoForm)

    def test_has_fields(self):
        """Form must have 4 fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class InscreverPostTest(TestCase):
    def setUp(self):
        data = dict(name='Rafael Amorim', cpf='12345678901', 
                    email='rafael@amorim.net', phone='00-99999-9090')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_inscrever_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_inscricao_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    def test_inscricao_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_inscricao_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'rafael@amorim.net']

        self.assertEqual(expect, email.to)

    def test_inscricao_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Rafael Amorim', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('rafael@amorim.net', email.body)
        self.assertIn('00-99999-9090', email.body)


class InscriverInvalidPostTest(TestCase):
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