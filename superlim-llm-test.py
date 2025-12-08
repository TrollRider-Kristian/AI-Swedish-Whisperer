import json
import ollama

def swewic_json_test():
    ollama_client = ollama.Client()
    # KRISTIAN_NOTE - They wrote the JSONL file in UTF-8 encoding to preserve the necessary Swedish vowels å, ä, and ö.
    with open ("SuperLim-2-2.0.4/swewic/swewic_test.jsonl", 'r', encoding = "utf8") as swewic_file:
        swewic_list = load_swewic_list_from_file (swewic_file)
        print (get_predicted_senses (swewic_list, ollama_client))
        print (get_target_senses (swewic_list))

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
    return ollama_client.generate ("llama3.1", prompt).response

def get_target_senses (swewic_list):
    return [ swewic_list [ix] ['label'] for ix in range (len (swewic_list))]

if __name__ == "__main__":
    swewic_json_test()
