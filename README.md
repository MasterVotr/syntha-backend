# SynthA! | A Modular Synth for the Web Generation | Backend
## Francesco Colotti, Jakub Votrubec, Roos Zoutman
## CS-E4400 - Design of WWW Services (23/24)

[Frontend repo](https://github.com/thepihen/syntha)

### Key challenges and learning moments:
- learning new technologies (Vue js, Tone js, Flask)
- learing how and where to deploy out webapp (frontend - github io, backend - Heroku)

## Recommended IDE Setup
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Python venv](https://docs.python.org/3/library/venv.html)
- command line
- Python libraries (in `requirements.txt`)

## Project Setup

### Development environment
```
apt install python3.10
apt install python3.10-venv
python3 -m venv venv 
source venv/bin/activate
pip3 install -r requirements.txt
```

### Run project
#### production
```sh
gunicorn 'app:create_app()'
```
#### development
```sh
flask run
```
