import json
import random


"""
with open ("qs.txt", "r") as myfile:

    text = myfile.read()
import re



splittext= re.split('\d+\.', text)
print(splittext)
lines=[]
for block in splittext:
    block =block.split("\n")[0]
    
    lines.append(block)
print(lines)
questions=lines

with open('conversation_data.json') as json_file:
    data = json.load(json_file)

data['lots of questions'] = questions
with open('conversation_data.json', 'w') as jsonfile:
    json.dump(data, jsonfile)
exit()
"""



'''
data = {}
data['initial'] = []
data['initial'].append('Hello')
data['initial'].append('Hi')
data['questions'] = []
data['answers'] = []
data['questions'].append('What did you do today?')
data['answers'].append("It's been flat out all day.")
with open('conversation_data.json', 'w') as jsonfile:
    json.dump(data, jsonfile)
'''
def save_data(data):
    with open('market_garden/conversation_data.json', 'w') as jsonfile:
        json.dump(data, jsonfile)


def get_phrases():
    with open('market_garden/conversation_data.json') as json_file:
        data = json.load(json_file)
        return data


data = get_phrases()
initial_greeting = data['initial']
questions = data['questions']
answers = data['answers']



def first_greeting():
    data = get_phrases()
    initial_greeting = data['initial']
    return random.choice(initial_greeting)

def save_initial_greeting(reply):
    if reply not in initial_greeting:
        initial_greeting.append(reply)
        data['initial'] = initial_greeting
        save_data(data)



def lots_of_questions():
    lots_of_questions = data["lots of questions"]
    return random.choice(lots_of_questions)

"""
print("What's your name?")
reply = input("... ")
name = reply.split()[0]
print(random.choice(initial_greeting) + " " + name + "\n\tMy name's " + name + " too!")
"""
def save_question(reply):
    if reply not in questions:
        questions.append(reply)
        data['questions'] = questions
        save_data(data)

def save_answer(reply):
    if reply not in answers:
        answers.append(reply)
        data['answers'] = answers
        save_data(data)
"""
while True:

    reply = input("... ")
    split_reply = reply.split(". ")
    if len(split_reply)>1:
        for r in split_reply[0:-1]:
            save_answer(r)
        reply = split_reply[-1]



    if reply.endswith("?"):
        save_question(reply)
        print(random.choice(data['answers']))
        print(random.choice(data['questions']))
    else:
        save_answer(reply)
        print(random.choice(data['questions']))
"""