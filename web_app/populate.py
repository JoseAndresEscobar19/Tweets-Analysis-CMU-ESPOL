# source: https://www.tangowithdjango.com/book17/chapters/models.html
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analisistweets.settings')

import django
django.setup()

from analisis.models import *

from django.contrib.auth.models import User
import csv
import json

def random_password(length=10):
    from string import digits, ascii_letters
    from random import choices, shuffle
    chars = list(f"{digits}{ascii_letters}!#$%&'*+-<=>?@^_|~")
    shuffle(chars)
    result = choices(chars, k=length)
    return ''.join(result)

def add_annotators():
    with open('data/Lista_anotadores.csv', encoding="ISO-8859-1") as csv_file:            
        rows = list(csv.reader(csv_file, delimiter=','))
        for row in rows:
            username = row[1] #same as email
            password = row[2]
            u, _ = User.objects.get_or_create(username=username)
            u.set_password(password)
            u.save()
            print(u)

            #Mirror an annotator with same id as user
            name = row[0]
            name = name.strip('"').replace(',',' ')
            a, _ = Annotator.objects.get_or_create(id=u.id, name=name)
            print(a)


def add_tweet_and_tweet_relations():
    # Load tweet_texts in memory
    data = []
    with open('data/main_pair_database.json') as f:
        for line in f:
            data.append(json.loads(line))

    #for info in data[:10]: #<-- a little limit for test and debugging
    for info in data:
        tweet_target_id = int(info['tweet_target_id'])
        tweet_target_text = info['tweet_target_text']

        tweet_response_id = int(info['tweet_response_id'])
        tweet_response_text = info['tweet_response_text']

        interaction_type = info['interaction_type']

        t, _ = Tweet.objects.get_or_create(
            id = tweet_target_id,
            text = tweet_target_text
        )
        print(t)

        t, _ = Tweet.objects.get_or_create(
            id = tweet_response_id,
            text = tweet_response_text
        )
        print(t)

        tr, _ = TweetRelation.objects.get_or_create(
            tweet_target_id = tweet_target_id,
            tweet_response_id = tweet_response_id,
            relation_type = interaction_type
        )
        print(tr)


def add_questions():
    sections = [
        {
            "name" : "Identificación del Evento",
            "questions" : [
                {
                    "value" :  "¿De qué país se habla en el tweet original?",
                    "type" :  "Checkbox",
                    "options" : ["Bolivia","Chile","Colombia","Ecuador","Otros","No es claro"]
                },
                {
                    "value" :  "¿El tweet original está relacionado con las protestas que ocurrieron en el (los) país(es) identificado(s) en la pregunta anterior?",
                    "type" : "Choice",
                    "options" : ["Si", "No", "No es claro"]
                }
            ]
        },
        {
            "name" : "Postura del original con respecto a las protestas",
            "questions" : [
                {
                    "value" :  "¿Cuál es la postura del original con respecto al gobierno?",
                    "type" : "Choice",
                    "options" : ["A favor","En contra","Neutro","No es claro","No Aplica"]
                },
                {
                    "value" :  "¿Cuál es la postura del original con respecto a las protestas?",
                    "type" : "Choice",                    
                    "options" : ["A favor","En contra","Neutro","No es claro","No Aplica"]
                },
            ]
        },
        {
            "name" : "Postura de la respuesta con respecto a las protestas",
            "questions" : [
                {
                    "value" :  "¿Cuál es la postura de la respuesta con respecto al gobierno?",
                    "type" : "Choice",                    
                    "options" : ["A favor","En contra","Neutro","No es claro","No Aplica"]
                },
                {
                    "value" :  "¿Cuál es la postura de la respuesta con respecto a las protestas?",
                    "type" : "Choice",                    
                    "options" : ["A favor","En contra","Neutro","No es claro","No Aplica"]
                }
            ]
        },
        {
            "name" : "Postura de la respuesta con respecto al original",
            "questions" : [
                {
                    "value" :  "¿Cuál es la postura del tweet respuesta al contenido del tweet original?",
                    "type" : "Choice",
                    "options" : [
                        "Soporte Explícito", 
                        "Soporte Implícito", 
                        "Comentario", 
                        "Pregunta por más información",                        
                        "Negación Explícita",
                        "Negación Implícita",
                        "Respuesta/Original No disponible"
                    ]
                },
                {
                    "value" :  "¿Qué tan seguro está de su respuesta?",
                    "type" : "Choice",
                    "options" : ["Inseguro", "Algo Seguro", "Seguro"]
                },
                {
                    "value" :  "¿La respuesta expresa que el original contiene información verdadera?",
                    "type" : "Choice",
                    "options" : ["Si" , "No", "No Aplica"]
                },
                {
                    "value" :  "¿La respuesta expresa que el original contiene información falsa?",
                    "type" : "Choice",                    
                    "options" : ["Si" , "No", "No Aplica"]
                },
                {                    
                    "value" :  "¿Qué tipo de evidencia presenta la respuesta para soportar esto?",
                    "type" : "Choice",
                    "options" : [
                        "Experiencia de primera mano",
                        "URL direccionando a la evidencia",
                        "Cita verificable de terceros",
                        "Cita no verificable de terceros",
                        "Aplica razonamiento",
                        "Ninguna"
                    ]
                }
            ]
        },        
    ]
    for section in sections:
        section_name = section['name']        
        for question in section['questions']:
            question['value']
            question['type'] 
            #print(dumps(question['options'], ensure_ascii=False))
            q, _ = Question.objects.get_or_create(
                section=section_name,
                value=question['value'],
                type=question['type'],
                options=json.dumps(question['options'], ensure_ascii=False)
            )
            print(q)

if __name__ == '__main__':
    print("Starting population script...")    
    add_tweet_and_tweet_relations()
    add_questions()
    add_annotators()
