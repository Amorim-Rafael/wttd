[![Build Status](https://travis-ci.org/Amorim-Rafael/wttd.svg?branch=master)](https://travis-ci.org/Amorim-Rafael/wttd)
[![Maintainability](https://api.codeclimate.com/v1/badges/1dd69179087df31db50e/maintainability)](https://codeclimate.com/github/Amorim-Rafael/wttd/maintainability)

# Eventex
Sistema de Eventos encomendado pela Morena.

## Como desenvolver?
1. Clone o repositório.
2. Crie um virtualenv com python 3.8
3. Ative o virtualenv.
4. Instale as dependências.
5. Configure a instância com o .env
6. Rode os testes.

```console
git clone git@github.com:amorim-rafael/eventex.git wttd
cd wttd
pyhton -m venv .wttd
source .wttd/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Como fazer o deploy?

1. Crie uma instância no heroku.
2. Envie as configurações para o heroku.
3. Defina uma SECRET_KEY segura para a instância.
4. Defina DEBUG=False
5. Configure o serviço de email.
6. Envie o código para o heroku.

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku congit:set DEBUG=False
# configurar o email
git push heroku master --force
```