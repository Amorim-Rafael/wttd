from django.test import TestCase
from eventex.inscricoes.forms import InscricaoForm

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

    