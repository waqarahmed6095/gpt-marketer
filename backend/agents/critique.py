import sys
from pathlib import Path
from datetime import datetime
from langchain_community.adapters.openai import convert_openai_messages
from langchain_anthropic import ChatAnthropic
from .models.spam_model import SpamClassifier
import os

model_path = os.path.join(Path(__file__).parent, 'models/email_spam_model.pkl')
vectorizer_path = os.path.join(Path(__file__).parent, 'models/vectorizer.pkl')


class CritiqueAgent:

    def __init__(self):
        self.spam_classifier = SpamClassifier(model_path=model_path,
                                              vectorizer_path=vectorizer_path)

    def critique(self, article: dict):
        email_content = article['email_content']
        critique_result = self.spam_classifier.classify_email(email_content)
        if critique_result <= 0.2:

            prompt = [{
                "role": "system",
                "content": "You are a marketing email writing critique. Your sole purpose is to provide feedback on "
                           "a written article so the writer will know what to fix to increase the chances of their "
                           "target reader interacting with the email.\n"
                           "Write less than 150 words, and add new line tagging so the text would be styled for HTML\n"
            }, {
                "role": "user",
                "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                           f"{str(article['email_content'])}\n"
                           f"Your task is to provide a short feedback on the email only if necessary.\n"
                           f"if you think the email is good, please return None.\n"
                           f"if you noticed the field 'message' in the article, it means the writer has revised the article"
                           f"based on your previous critique. you can provide feedback on the revised email or just "
                           f"return None if "
                           f"you think the email is good.\n"
                           f"Please return a string of your critique or None.\n"
            }]

        else:
            prompt = [{
                "role": "system",
                "content": "You are a marketing email writing critique. Your sole purpose is to provide feedback on "
                           "a written article so the writer will know what to fix to increase the chances of their "
                           f"target reader interacting with the email. Additionally, the likelihood of this email "
                           f"being classified as spam is {critique_result * 100}, make additional recommendations to "
                           f"the writer to reduce this likelihood to under 40%. \n"
                           f"Write less than 150 words, and add new line tagging so the text would be styled for HTML\n"
            }, {
                "role": "user",
                "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                           f"{str(article['email_content'])}\n"
                           f"Your task is to provide a really short feedback on the email only if necessary.\n"
                           f"if you think the email is good, please return None.\n"
                           f"if you noticed the field 'message' in the article, it means the writer has revised the article"
                           f"based on your previous critique. you can provide feedback on the revised email or just "
                           f"return None if "
                           f"you think the email is good.\n"
                           f"Please return a string of your critique or None.\n"
            }]

        lc_messages = convert_openai_messages(prompt)
        response = ChatAnthropic(model='claude-3-5-sonnet-20240620', max_retries=1, api_key=os.getenv("ANTHROPIC_API_KEY")).invoke(lc_messages).content
        number_of_revisions = article.get('number_of_revisions')
        if response == 'None' or number_of_revisions == "1" or number_of_revisions == 1: # deterministic approach
            return {'critique': None}
        else:
            print(f"For article: {article['title']}")
            print(f"Feedback: {response}\n")
            return {'critique': response, 'message': None}

    def run(self, article: dict):
        article.update(self.critique(article))
        return article

