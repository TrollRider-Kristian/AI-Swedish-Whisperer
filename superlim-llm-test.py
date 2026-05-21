import json
import ollama
from sklearn.metrics import confusion_matrix

SWEWIC_FILEPATH = "SuperLim-2-2.0.4/swewic/swewic_test.jsonl"
SWEANALOGY_FILEPATH = "SuperLim-2-2.0.4/sweanalogy/sweanalogy_test.jsonl"
ollama_client = ollama.Client()

def swewic_json_test():
    # KRISTIAN_NOTE - They wrote the JSONL file in UTF-8 encoding to preserve the necessary Swedish vowels å, ä, and ö.
    with open (SWEWIC_FILEPATH, 'r', encoding = "utf8") as swewic_file:
        swewic_list = load_swewic_list_from_file (swewic_file)
        # KRISTIAN_NOTE - This line of code took roughly 5-10 minutes to run and shows that the LLM is roughly 60% accurate in terms of word senses.
        # KRISTIAN_TODO - Find a way to integrate these tests and the Super-Lim files into AWS!
        print (confusion_matrix (get_target_senses (swewic_list), get_predicted_senses (swewic_list, ollama_client), labels = ['same_sense', 'different_sense']))

def load_swewic_list_from_file (swewic_file):
    # KRISTIAN_NOTE - A JSONL file contains multiple JSON objects, which need to be converted to a list and read one-by-one.
    # https://stackoverflow.com/questions/50475635/loading-jsonl-file-as-json-objects
    swewic_data = list (swewic_file)
    return [ json.loads (swewic_data[ix]) for ix in range (len (swewic_data)) ]

def get_predicted_senses (swewic_list, ollama_client):
    predictions = []
    for sentence_data in swewic_list:
        word = sentence_data ['first']['word']['text']
        first_sentence = sentence_data ['first']['context']
        second_sentence = sentence_data ['second']['context']
        prediction = eval_sentence_pair_sense (ollama_client, word, first_sentence, second_sentence)
        predictions.append (prediction)
    return predictions

def eval_sentence_pair_sense(ollama_client, given_word, first_sentence, second_sentence):
    prompt = "For each test pair, predict if the word: " + given_word + " is being used in the same sense in the following two sentences: " +\
         first_sentence + second_sentence + "  Please only answer 'same_sense' or 'different_sense'."
    # KRISTIAN_TODO - Give an example indicating what I want.  Check for nulls too.  Give the answer in a string format.  Check the data if anything is missing.
    # Instructions on how to improve my prompts.  Translator / task.  Do's and dont's.  Output structure.  Examples.  Split up into functions and merge into a large prompt.
    # Store the context as an agent.  Store the conversation log as a txt file.  S3 is good enough for now.
    return ollama_client.generate ("llama3.1", prompt).response

def get_target_senses (swewic_list):
    return [ swewic_list [ix] ['label'] for ix in range (len (swewic_list))]

def sweanalogy_json_test():
    with open (SWEANALOGY_FILEPATH, 'r', encoding = "utf8") as sweanalogy_file:
        sweanalogy_list = load_sweanalogy_list_from_file (sweanalogy_file)
        print (get_target_analogies (sweanalogy_list[0:10]))
        print (get_predicted_analogies (sweanalogy_list[0:10], ollama_client))

def load_sweanalogy_list_from_file (sweanalogy_file):
    sweanalogy_data = list (sweanalogy_file)
    return [ json.loads (sweanalogy_data [ix]) for ix in range ( len(sweanalogy_data)) ]

def get_predicted_analogies (sweanalogy_list, ollama_client):
    predictions = []
    for word_pair in sweanalogy_list:
        first_word = word_pair ['pair1_element1']
        given_analogy = word_pair ['pair1_element2']
        second_word = word_pair ['pair2_element1']
        prediction = eval_analogy_pair (ollama_client, first_word, given_analogy, second_word)
        predictions.append (prediction)
    return predictions

def eval_analogy_pair(ollama_client, first_word, given_analogy, second_word):
    prompt = "For a given word: + " + second_word + ", find a word analogous to it in the same way that " + first_word + " is analogous to " + given_analogy +\
        ".  Please respond with only a one-word answer."
    return ollama_client.generate ("llama3.1", prompt).response

def get_target_analogies (sweanalogy_list):
    return [sweanalogy_list [ix] ['label'] for ix in range (len (sweanalogy_list)) ]

if __name__ == "__main__":
    swewic_json_test()
    sweanalogy_json_test()
