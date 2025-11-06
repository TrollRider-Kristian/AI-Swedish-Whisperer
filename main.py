from flask import Flask, render_template
from logging import FileHandler
import logging

app = Flask (__name__)

def initialize_logger():
    logger = FileHandler ('debug.log')
    app.logger.setLevel (logging.DEBUG)
    app.logger.addHandler (logger)

@app.route('/', methods = ['GET', 'POST'])
def index():
    initialize_logger()
    app.logger.debug ('hello')
    return render_template ('index.html', prompt_response = 'some response')

def main():
    app.run (debug = True)

if __name__ == "__main__":
    main()
