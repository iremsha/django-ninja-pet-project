# Docker
## Install docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/

## Install docker-compose
https://docs.docker.com/compose/install/


# Nginx
## http NGINX (host machine)
```
server {
    listen 80;
    server_name is.doubletapp.ai;

    location / {
        proxy_pass http://localhost:1345;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

## https NGINX (host machine)
https://certbot.eff.org/lets-encrypt/ubuntuxenial-nginx
```
server {
    listen 80;
    server_name is.doubletapp.ai;
    return 301 https://is.doubletapp.ai$request_uri;
}

server {
    listen 443 ssl;
    server_name is.doubletapp.ai;

    ssl_certificate /etc/letsencrypt/live/is.doubletapp.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/is.doubletapp.ai/privkey.pem;

    location / {
        proxy_pass http://localhost:1345;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

### Local .env images example
```
IMAGE_DB=dt-is-backend_db
IMAGE_APP=dt-is-backend_app
IMAGE_NGINX=dt-is-backend_nginx
IMAGE_SWAGGER=dt-is-backend_swagger
