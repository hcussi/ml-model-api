from django.test import SimpleTestCase
from chatgpt.ml_model import super_chat_gpt_like_model


class TestModels(SimpleTestCase):

    def test_ml_model(self) -> None:
        """
        Test success super_chat_gpt_like_model with 'hello' prompt
        :return: None
        """
        response = super_chat_gpt_like_model('hello')
        self.assertEqual(response, 'dummy response from prompt: hello')
