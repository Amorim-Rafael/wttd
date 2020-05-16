from django.test import TestCase
from django.core import mail

class InscreverPostValid(TestCase):
    def setUp(self):
        data = dict(name='Rafael Amorim', cpf='12345678901', 
                    email='rafael@amorim.net', phone='00-99999-9090')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]
    
    def test_inscricao_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_inscricao_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_inscricao_email_to(self):
        expect = ['contato@eventex.com.br', 'rafael@amorim.net']

        self.assertEqual(expect, self.email.to)

    def test_inscricao_email_body(self):
        contents = ['Rafael Amorim',
                    '12345678901',
                    'rafael@amorim.net',
                    '00-99999-9090']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)