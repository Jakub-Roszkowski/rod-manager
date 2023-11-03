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
```shell
docker-compose up -d --build 
```

### Rebuild
```shell
docker-compose down
docker-compose up -d --build 
```

### Production (almost) version with nginx

```shell
docker-compose -f docker-compose.prod.yml up -d --build  
```

### Rebuild production version
```shell
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build  
```
