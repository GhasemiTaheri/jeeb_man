# intro
"Jeeb man" is a service for personal financial management implemented with Django Rest Framework.

# 1- Create environment variables

1. rename .example-env file to .env
2. generate new secret key with django framework and insert it into .env file

# 2- Run in docker and run

1. run command in project base directory
    ```CMD
    docker-compose  up -d --build
    ```
2. run this to create database tables
    ```CMD
    docker-compose exec web python manage.py migrate --noinput
    ```
3. run this to create superuser
    ```CMD
    docker-compose exec web python manage.py createsuperuser
    ```
4. run this to execute test
    ```CMD
    docker-compose exec web python manage.py test
    ```
5. run this to initial public categories
    ```CMD
    docker-compose exec web python manage.py create_categories
    ```
