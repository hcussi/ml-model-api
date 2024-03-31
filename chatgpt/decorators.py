from typing import Callable

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from chatgpt.models import MlJob, MlJobStatus, MlModel


def rate_limited(rate_limit: int) -> Callable | Response:
    def decorator(func) -> Callable:
        """
        Check the rate limit for the ml model
        :param func: The function to decorate
        :return: Too many request response if the limit is exceeded
        """
        def wrapper(*args, **kwargs) -> Callable | Response:
            request: Request = args[1]
            user_id: int = request.user.id

            job_count: int = MlJob.objects.filter(user_id = user_id, status = MlJobStatus.PENDING).count()
            model_count: int = MlModel.objects.filter(user_id = user_id).count()

            if (job_count + model_count) >= rate_limit:
                return Response(status = status.HTTP_429_TOO_MANY_REQUESTS)

            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__

        return wrapper
    return decorator
