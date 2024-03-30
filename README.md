### Getting Started

Django Rest Framework has been used in order to build a chatgpt like application to expose prompt endpoint. 

### Environment

#### Python 3.11

Miniconda is used to create virtual environments. Check the `requirements.txt` file in order to build one for your one.
You will see many dependencies that are not used in the code base but are added by default by `conda`, feel free to remove those.

#### Django 4.1

- More info: https://docs.djangoproject.com/en/4.2/releases/4.2/#dropped-support-for-mysql-5-7

#### Setting up

Create and activate an environment with `conda` or other. Can be created from the `requirements.txt` or directly and then use `pip` to install dependencies.
Copy and rename `.env.example` file to `.env`.

#### Generating Secret Key

Copy the generated secret into `.env` to `PRIVATE_SECRET_KEY`.

```bash
python manage.py shell

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### Starting docker compose

```bash
docker-compose -f docker-compose-mlmodel.yml up -d
```

##### MySQL

Create user for the DB.

```bash
docker exec -it mlmodel-mysql bash
mysql -u root -p
CREATE USER 'mlModelUser'@'%' IDENTIFIED BY 's3c3rTpaZZ';
GRANT ALL PRIVILEGES ON usersdb.* TO 'mlModelUser'@'%';
CREATE SCHEMA testsdb;
GRANT ALL PRIVILEGES ON testsdb.* TO 'mlModelUser'@'%';
```

#### Initializing DB and creating Django super user

```bash
python manage.py makemigrations chatgpt
python manage.py migrate
python manage.py createsuperuser
```

#### Kafka

Check that Kafka brokers are up and running with [Kafdrop](http://localhost:9099/) and that there is one
controller assigned.
Create a topic: `mlmodel.prompt_created` with replication factor of 2 and number of partitions of 3.

#### Running Django Server

````bash
python manage.py runserver
````

##### API docs

Navigate to:
- [Swagger YAML](http://localhost:8000/api/v1/schema/)
- [Swagger UI](http://localhost:8000/api/v1/schema/swagger-ui/)
- [Redoc UI](http://localhost:8000/api/v1/schema/redoc/)

##### Running tests

```bash
pytest
```

#### Creating Django API users

Navigate to [Admin site](http://localhost:8000/admin/) and [add users](https://docs.djangoproject.com/en/dev/topics/auth/default/#id6)
Basic Auth will be used in our API.

##### Prompt endpoints

The username and password send are using Basic Auth and should be created in the Django Admin site.

```bash
curl -X POST -d '{"prompt": "hello"}'  -u <USER>:<PASS> http://localhost:8000/api/v1/call_model/
```

```bash
curl -X POST -d '{"prompt": "hello"}'  -u <USER>:<PASS> http://localhost:8000/api/v1/sync_call_model/
```

```bash
curl -X GET -u <USER>:<PASS> http://localhost:8000/api/v1/sync_call_status/<job_id>
```

##### Health Endpoint

Basic Auth is not required.

```bash
curl -X GET http://localhost:8000/api/v1/health/
```

#### References

- [Why miniconda?](https://docs.anaconda.com/free/distro-or-miniconda/)
- [Conda cheet sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
