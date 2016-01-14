# mesos-admin
Mesos admin


# dev

```sh
# run dev container
docker-compose up -d mesos-admin

# execute into container
docker exec -it mesosadmin_mesos-admin_1 bash

# makemigrations
./manage.py makemigrations

# migrate database
./manage.py migrate


# run app
./manage.py runserver 0.0.0.0:8000
```

Access:
http://127.0.0.1:8000/token-gdrive/



# TODO
1. demo data



