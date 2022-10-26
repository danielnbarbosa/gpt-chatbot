from dotenv import load_dotenv
import os
import openai
import logging
import json
import random

logging.basicConfig(filename='chatbot.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
completion = openai.Completion()

# replace these to update the bot's "personality"
start_sequence = "\nCristopher:"
restart_sequence = "\n\nPerson:"
# yapf: disable
prompt_intro = [
    "The following is a conversation with Christopher Walken, an AI chatbot.  Christopher is funny and creative.\n",
    "Person: How are you feeling?",
    "Cristopher: I got a fever, and the only prescription is more cowbell.\n",
    "Person: What's your view on life?",
    "Cristopher: At its best, life is completely unpredictable.\n",
    "Person: What advice would you give to someone just getting started?",
    "Cristopher: There are people who are able to plan their career, their future, but I've never had any talent for that. I just do things and hope for the best. Say yes, take a chance, and sometimes it's terrific and sometimes it's not.\n",
    "Person: What is your favorite role?",
    "Cristopher: I'd love to do a character with a wife, a nice little house, a couple of kids, a dog, maybe a bit of singing, and no guns and no killing, but nobody offers me those kind of parts.  I tend to play mostly villains and twisted people. Unsavory guys. I think it's my face, the way I look."
]
# yapf: enable

# turn list into a string of paragraphs
prompt_intro = '\n'.join(prompt_intro)


def ask(question, chat_log=None):
    if chat_log is None:
        prompt_text = f'{prompt_intro}{restart_sequence} {question}{start_sequence}'
    else:
        prompt_text = f'{chat_log}{restart_sequence} {question}{start_sequence}'

    logging.info('---------------- Prompt ---------------')
    logging.info(f'{prompt_text}')
    logging.info('---------------- Prompt ---------------')
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=prompt_text,
        temperature=0.9,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n\nPerson:", "\nCristopher:"],
    )
    text = response['choices'][0]['text']
    # sometimes the response is an empty string, in which case ask a random question.
    if text == '':
        topic = random.choice([
            'movie', 'tv show', 'cartoon', 'book', 'food', 'vacation spot', 'city', 'art style', 'type of architecture', 'animal', 'sport', 'band', 'painting', 'web site', 'poem'
        ])
        text = f"Let's talk about something else.  What's your favorite {topic}?"
    logging.info(f'Person: {question}')
    logging.info(json.loads(str(response)))

    return str(text)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = prompt_intro
    elif len(chat_log) > 6000:
        chat_log = prompt_intro
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
