from django.core.management.base import BaseCommand

from chatgpt.consumers import MlPromptCreatedListener


class Command(BaseCommand):
    help = 'Launches Consumer for "mlmodel.prompt_created" kafka topic'

    def handle(self, *args, **options):
        td = MlPromptCreatedListener()
        td.start()
        self.stdout.write(self.help)
