from django.test import TestCase
from eventex.inscricoes.forms import InscricaoForm

class InscricaoFormTest(TestCase):
    def setUp(self):
        self.form = InscricaoForm()

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(self.form.fields))