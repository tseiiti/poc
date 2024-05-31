# POC

## Virtual Env
sudo apt install python3-virtualenv
virtualenv .venv
source .venv/bin/activate

## PIP install
pip install -r requirements.txt

## Tesseract
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev

## migrate runserver
python manage.py migrate
python manage.py runserver

## Para usar o banco de dados na nuvem
export HOST='url_de_conexao_cloud_mongodb'

## Para usar o banco local via docker
docker compose up --build -d

## Para usar funcionalidades gpt3.5
export OPENAI_API_KEY='chave_de_acesso_api_openai'
