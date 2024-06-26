from django.db import models
from json import JSONEncoder

class MlModel(models.Model):
    user = models.ForeignKey('auth.User', related_name = 'mlmodels', on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    prompt = models.TextField()
    response = models.TextField()
    duration = models.DurationField()

    class Meta:
        ordering = ['timestamp']


class MlJobStatus(models.TextChoices):
    PENDING = ('PENDING', 'pending')
    DONE = ('DONE', 'done')


class MlJob(models.Model):
    user = models.ForeignKey('auth.User', related_name = 'mljobs', on_delete = models.CASCADE)
    mlmodel = models.ForeignKey(
        'chatgpt.MlModel',
        related_name = 'mljob',
        on_delete = models.CASCADE,
        blank = True,
        null = True,
    )
    created_on = models.DateTimeField(auto_now_add = True)
    start_time = models.DateTimeField()
    prompt = models.TextField()
    status = models.CharField(
        max_length = 32,
        choices = MlJobStatus.choices,
        default = MlJobStatus.PENDING,
    )

    class Meta:
        ordering = ['created_on']

    class MlJobEncoder(JSONEncoder):
        def default(self, o):
            return { 'job_id': o.id }
