"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
from boto_functions import *

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    boto_values['user_message'] = request.POST.get('msg')
    boto_logic(boto_values['user_message'])
    return json.dumps({"animation": boto_values['animation'], "msg": boto_values['answer']})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7001)

if __name__ == '__main__':
    main()