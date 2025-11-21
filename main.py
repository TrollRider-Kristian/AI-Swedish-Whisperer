from flask import Flask, render_template, request
from logging import FileHandler
import logging
import ollama

app = Flask (__name__)
current_topic = ""

def initialize_logger():
    logger = FileHandler ('debug.log')
    app.logger.setLevel (logging.DEBUG)
    app.logger.addHandler (logger)

@app.route('/', methods = ['GET', 'POST'])
def index():
    initialize_logger()
    ollama_client = ollama.Client()
    initial_prompt = "You are my Swedish tutor.  Please introduce yourself to me in English and ask me what I wish to discuss."
    global current_topic
    if (request.method == 'GET'):
        app.logger.debug (request.args.to_dict())
        app.logger.debug ("current topic: " + current_topic)
        if 'user-response' in request.args.to_dict():
            student_response = request.args.to_dict()['user-response']
            if (current_topic == ""):
                current_topic = student_response
                next_prompt = "Given: " + current_topic + ", please ask a question in Swedish about this."
            else:
                next_prompt = "Please provide feedback in English correcting the spelling and grammatical mistakes of: " + student_response + ".  Then ask a follow-up question in Swedish."
            response = ollama_client.generate ("llama3.1", prompt = next_prompt)
        else:
            response = ollama_client.generate ("llama3.1", prompt = initial_prompt)
    return render_template ('index.html', prompt_response = response.response)

def main():
    app.run (debug = True)

if __name__ == "__main__":
    main()
