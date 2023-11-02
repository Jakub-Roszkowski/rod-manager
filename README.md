# rod-manager
### SETUP 
## Setup venv and install requirements:
(Windows)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### LAUNCH
```
venv\Scripts\activate
python manage.py runserver
```

## Setup with docker compose
### Requirements
- Install docker desktop: https://www.docker.com/products/docker-desktop
- Have docker deamon running

### Launch
In the root folder of the project, run:
```
docker-compose build
docker-compose up
```

### Alternative with Jetbrains IDE
- install docker plugin
- open the project with the IDE
- go to the docker-compose.yml file
- right click on the green arrow next to "services"

