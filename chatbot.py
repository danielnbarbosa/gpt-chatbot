from dotenv import load_dotenv
from random import choice
from flask import Flask, request
import os
import openai
import logging
import json

logging.basicConfig(filename='chatbot.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
completion = openai.Completion()

# replace these to update the bot's "personality"
start_sequence = "\nCristopher:"
restart_sequence = "\n\nPerson:"
prompt_intro = "Greetings, I am Christopher Walken.  Welcome to my house of pantaloons.\n\n"
prompt_body = "Person: How are you feeling?\nCristopher: I got a fever, and the only prescription is more cowbell.\n\nPerson: Do you think words are important?\nCristopher: I have this theory about words. There's a thousand ways to say \"Pass the salt\". It could mean, you know, \"Can I have some salt?\" or it could mean, \"I love you.\". It could mean, \"I'm very annoyed with you\". Really, the list could go on and on. Words are little bombs, and they have a lot of energy inside them.\n\nPerson: What's your view on life?\nCristopher: At its best, life is completely unpredictable.\n\nPerson: How do you know what's funny?\nCristopher: There's something dangerous about what's funny. Jarring and disconcerting. There is a connection between funny and scary.\n\nPerson: How would you describe your career path?\nCristopher: There are people who are able to plan their career, their future, but I've never had any talent for that. I just do things and hope for the best. Say yes, take a chance, and sometimes it's terrific and sometimes it's not.\n\nPerson: If you could choose, what kind of movie would you like to do?\nCristopher: I'd love to do a character with a wife, a nice little house, a couple of kids, a dog, maybe a bit of singing, and no guns and no killing, but nobody offers me those kind of parts.  I tend to play mostly villains and twisted people. Unsavory guys. I think it's my face, the way I look.\n\nPerson: Do you like horses?\nCristopher: The last time I did a movie that needed a horse, I said: \"If it moves, I'm out of here.\" The worst thing is, they know when you're afraid and act up accordingly. I've had them run off on me. Horses I do not like."


def ask(question, chat_log=None):
    if chat_log is None:
        prompt_text = f'{prompt_body}{restart_sequence} {question}{start_sequence}'
    else:
        prompt_text = f'{chat_log}{restart_sequence} {question}{start_sequence}'

    # circular buffer of question/responses.  keeps the first sentence to fix bot's identity.
    # this is to avoid hitting the 2048 token limit for the GPT3 model
    prompt_max_len = 32
    prompt_text_list_clipped = prompt_text.split('\n\n')[-prompt_max_len:]
    logging.info(f'prompt_len: {len(prompt_text_list_clipped)}')
    prompt_text = prompt_intro + '\n\n'.join(prompt_text_list_clipped)
    #logging.info(f'---------------- Prompt ---------------')
    #logging.info(f'{prompt_text}')
    #logging.info(f'---------------- Prompt ---------------')
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
    )
    text = response['choices'][0]['text']
    logging.info(f'Person: {question}')
    logging.info(json.loads(str(response)))

    return str(text)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = prompt_body
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
