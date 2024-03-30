from django.db import models


class MlModel(models.Model):
    user = models.ForeignKey('auth.User', related_name = 'mlmodels', on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    prompt = models.TextField()
    response = models.TextField()
    duration = models.DurationField()

    class Meta:
        ordering = ['timestamp']
