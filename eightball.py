#!/usr/bin/python3
'''
magic 8 ball questions and answers module
this runs on port 80 and answers REST requests
for a predefined set of questions

this is a toy for local testing of OpenAPI stuffs only,
and if you ever expose it to other users, that
is Very Bad. Do Not Do That.
'''
import argparse
import json
import random
import sys
from ssl import PROTOCOL_TLS_SERVER, SSLContext
from urllib import parse
from http.server import BaseHTTPRequestHandler, HTTPServer


class EightBallRequestHandler(BaseHTTPRequestHandler):
    '''
    process an incoming HTTP request for a query to the magic 8 ball.
    '''
    API_BASE = '/8ball/v1/'
    TOPICS = {'romance': 'Will I have a great date within the next 2 weeks?',
              'puppy': 'Will a wonderful puppy enter my life within the next 4 weeks?',
              'kitty': 'Will a wonderful kitty enter my life within the next 4 weeks?',
              'Bug1': 'Will Bug 1 be completely fixed within the next 6 months?',
              'singularity': 'Will The Singularity(TM) happen within the next 6 months?',
              'movie': 'Will the next movie I see be worth the price?',
              'wwu': 'Will the WMF voluntarily recognize the WWU US branch?'}
    ANSWERS = ['It is certain', 'It is decidedly so', 'Without a doubt',
               'Yes definitely', 'You may rely on it', 'As I see it, yes',
               'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
               'Reply hazy, try again', 'Ask again later', 'Better not tell you now',
               'Cannot predict now', 'Concentrate and ask again', "Don't count on it",
               'My reply is no', 'My sources say no', 'Outlook not so good',
               'Very doubtful']
    HELP = {'help': 'example: curl "http[s]://host:port/8ball/v1/help"',
            'topics': 'example: curl "http[s]://host:port/8ball/v1/topics',
            'question': 'example: curl "http[s]://host:port/8ball/v1/question/puppy'}

    def get_ball_answer(self):
        '''
        get an 8 ball random answer, independently of whatever question is asked.
        random seed is the default (time)
        '''
        return self.ANSWERS[random.randrange(0, len(self.ANSWERS)-1)]

    def get_answer(self, topic):
        '''
        given a topic (question short form), return the full text of the question
        and the 8 ball answer
        '''
        ball_answer = self.get_ball_answer()
        return json.dumps({'question': self.TOPICS[topic],
                           'answer': ball_answer})

    def path_invalid(self, components, query):
        '''
        check prefix, number of components, and expect no query string
        '''
        if len(components) == 4:
            return self.topic_invalid(components[3])
        return len(components) != 3 or not self.path.startswith(self.API_BASE) or query

    def topic_invalid(self, topic):
        '''
        check that topic is a known query or one of the defined topics
        '''
        return topic not in self.TOPICS and topic != 'topics' and topic != 'help'

    def get_response(self):
        '''
        get the body of the response for q request for the list of questions
        or the request for an answer to a specific questions
        '''
        url_fields = parse.urlsplit(self.path.lstrip('/'))
        # url_fields[2] is the path up to the ? if any
        path_components = url_fields[2].split('/')
        if self.path_invalid(path_components, query=url_fields[3]):
            self.send_error(404, message='Not Found',
                            explain='No such content available: ' + path_components[2])
            return ''
        if path_components[2] == 'topics':
            return json.dumps(self.TOPICS)
        if path_components[2] == 'help':
            return json.dumps(self.HELP)
        if path_components[2] == 'question':
            return self.get_answer(path_components[3])
        self.send_error(404, message='Not Found',
                        explain='No such content available: ' + path_components[2])
        return ''


    def do_GET(self):   # pylint: disable=invalid-name
        '''
        override the GET method handler for the parent class
        '''
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))

    def do_POST(self):  # pylint: disable=invalid-name
        '''
        override the POST method handler for the parent class
        in our case, we just don't support POST requests at all
        '''
        self.send_error(405, message="POST method unsupported", explain="")


def whine(message):
    '''
    minimal error message handler
    '''
    sys.stderr.write(message + "\n")
    sys.exit(1)

def do_main():
    '''
    entry point
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--cert", type=str, default="")
    parser.add_argument("--keyfile", type=str, default="")
    args = parser.parse_args()

    if (args.cert and not args.keyfile) or (args.keyfile and not args.cert):
        whine("both --cert and --keyfile must be provided or omitted together")

    if args.cert:
        ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(args.cert, args.keyfile)
        ssl_context.load_default_certs()
    server = HTTPServer((args.host, args.port), EightBallRequestHandler)
    if args.cert:
        server.socket = ssl_context.wrap_socket(server.socket, server_side=True)
    server.serve_forever()


if __name__ == "__main__":
    do_main()
