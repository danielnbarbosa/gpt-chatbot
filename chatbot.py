from dotenv import load_dotenv
from random import choice
from flask import Flask, request
import os
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
completion = openai.Completion()


start_sequence = "\nEliza:"
restart_sequence = "\n\nPerson:"
session_prompt="How do you do?  Please tell me your problem.\n\nPerson: I am unhappy.\nEliza: How do you feel about being unhappy?\n\nPerson: I need some help, that much seems certain.\nEliza: Would it really help you to get some help?\n\nPerson: Perhaps I could learn to get along with my mother.\nEliza: Good family relations are important.\n\nPerson: My mother takes care of me.\nEliza: Why do you think your mother takes care of you?",


def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
    engine='davinci',
    prompt=prompt_text,
    temperature=0.8,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.3,
    stop=["\n"],
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'


if __name__ == '__main__':
    chat_log = None
    answer = 'How do you do?  Please tell me your problem.'

    while True:
        print('\n')
        question = input(f'{answer}\n')
        #print(f'% question is {question}')
        answer = ask(question, session_prompt)
        #print(answer)
        #print(f'% answer is {answer}')
        #print(f'% chat_log B4 is {chat_log}')
        chat_log = append_interaction_to_chat_log(question, answer, chat_log)
        print(f'----- chat_log is {chat_log}')
