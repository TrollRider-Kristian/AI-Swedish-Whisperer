from flask import Flask, render_template, request
from logging import FileHandler
import logging
import ollama

app = Flask (__name__)
ollama_client = ollama.Client()

def initialize_logger():
    logger = FileHandler ('debug.log')
    app.logger.setLevel (logging.DEBUG)
    app.logger.addHandler (logger)

@app.route('/', methods = ['GET', 'POST'])
def index():
    initialize_logger()
    if (request.method == 'GET'):
        app.logger.debug (request.args.to_dict())
        if 'user-response' in request.args.to_dict():
            response = ollama_client.generate ("llama3.1", prompt = request.args.to_dict()['user-response'])
        else:
            response = ollama_client.generate ("llama3.1", prompt = "What's the best way to learn Swedish?")
    return render_template ('index.html', prompt_response = response.response)

def main():
    app.run (debug = True)

if __name__ == "__main__":
    main()
