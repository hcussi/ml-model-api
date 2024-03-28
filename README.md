### Getting Started

Django Rest Framework has been used in order to build a chatgpt like application to expose prompt endpoint. 

### Environment

- Python 3.11

Miniconda is used to create virtual environments. Check the `requirements.txt` file in order to build one for your one.
You will see many dependencies that are not used in the code base but are added by default by `conda`, feel free to remove those.

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

#### Running Django Server

````bash
python manage.py runserver
````

##### Prompt endpoint

```bash
curl -X POST -d '{"prompt": "hello"}' http://localhost:8000/api/v1/call_model/
```

##### Health Endpoint

```bash
curl -X GET http://localhost:8000/api/v1/health/
```

#### References

- [Why miniconda?](https://docs.anaconda.com/free/distro-or-miniconda/)
- [Conda cheet sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
