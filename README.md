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

### Launch full app
In the root folder of the project, run:
```shell
git submodule update --init --recursive
docker-compose up -d --build 
```

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

### EXPORT DATABASE TO FILE
```shell
python manage.py dumpdatautf8 --output data.json --exclude contenttypes --exclude auth.permission
```
