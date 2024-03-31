### Getting Started

Django Rest Framework has been used in order to build a chatgpt like application to expose prompt endpoint. 

### Environment

#### Python 3.11

Miniconda is used to create virtual environments. Check the `environment.yml` file in order to build one for your one.
You will see many dependencies that are not used in the code base but are added by default by `conda`, feel free to remove those.

#### Django 4.1

- More info: https://docs.djangoproject.com/en/4.2/releases/4.2/#dropped-support-for-mysql-5-7

### Setting up

Note: Only required if you want to contribute to the project. 

Create and activate an environment with `conda` using `environment.yml`. Can be created from the `requirements.txt` using `pip` to install dependencies.
Copy and rename `.env.example` file to `.env`.

#### Generating Secret Key

```bash
python manage.py shell

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the generated secret into `.env` to `PRIVATE_SECRET_KEY`.

### Starting the project

#### Docker compose

```bash
docker-compose -f docker-compose-mlmodel.yml up -d
```

#### MySQL

App user and DB are created with `db/init.sql`. You can connect to the mysql instance using `localhost:3306`, check
for tables `auth_*` and `chatgpt_*` after the `mlmodel-django` container has started.

#### Running tests

```bash
docker exec -it mlmodel-django bash
pytest
```

From `localhost`, change `DB_HOST=127.0.0.1` in `.env`:

```bash
pytest
```

#### Creating Django super user

Note: This is required in order to create app/api users.

From inside docker:

```bash
docker exec -it mlmodel-django bash
python manage.py createsuperuser
```

From `localhost`, change `DB_HOST=127.0.0.1` in `.env`:

```bash
python manage.py createsuperuser
```

#### Creating Django API users

Navigate to [Admin site](http://localhost:8088/admin/) and [add users](https://docs.djangoproject.com/en/dev/topics/auth/default/#id6)
Basic Auth will be used in our API.

### API docs

Navigate to:
- [Swagger YAML](http://localhost:8088/api/v1/schema/)
- [Swagger UI](http://localhost:8088/api/v1/schema/swagger-ui/)
- [Redoc UI](http://localhost:8088/api/v1/schema/redoc/)

### Ml Model endpoints

#### Prompt endpoints

The username and password send are using Basic Auth and should be created in the Django Admin site.

```bash
curl -X POST -d '{"prompt": "hello"}'  -u <USER>:<PASS> http://localhost:8088/api/v1/call_model/
```

```bash
curl -X POST -d '{"prompt": "hello"}'  -u <USER>:<PASS> http://localhost:8088/api/v1/sync_call_model/
```

```bash
curl -X GET -u <USER>:<PASS> http://localhost:8088/api/v1/sync_call_status/<job_id>
```

#### Health Endpoint

Basic Auth is not required.

```bash
curl -X GET http://localhost:8088/api/v1/health/
```

#### Kafka

Check that Kafka brokers are up and running with [Kafdrop](http://localhost:9099/) and that there is one
controller assigned and topic `mlmodel.prompt_created` is present after calling `async_call_model` endpoint.

#### References

- [Why miniconda?](https://docs.anaconda.com/free/distro-or-miniconda/)
- [Conda cheet sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
- [Comprehensive Step-by-Step Guide to Testing Django REST APIs with Pytest](https://pytest-with-eric.com/pytest-advanced/pytest-django-restapi-testing/)
- [How to Test Django REST Framework](https://apidog.com/articles/how-to-test-django-rest-framework/)
- [Testing in Django and Django REST - Useful Tools and Best Practices](https://www.rootstrap.com/blog/testing-in-django-django-rest-basics-useful-tools-good-practices)
- [DRF Dive: Embark on Your Django Rest Framework Journey](https://medium.com/@ishteaque.workplace/drf-dive-embark-on-your-django-rest-framework-journey-e7cf8ad7499d)
- [Construir un API REST con Django REST Framework y APIView](https://davidcasr.medium.com/construir-un-api-rest-con-django-rest-framework-y-apiview-5ea4b2823307)
- [Microservices in Python: Kafka and Django](https://medium.com/@mansha99/microservices-using-django-and-kafka-3776e8592ef3)
- [Dockerizing a Django and MySQL Application: A Step-by-Step Guide](https://medium.com/@akshatgadodia/dockerizing-a-django-and-mysql-application-a-step-by-step-guide-d4ba181d3de5)