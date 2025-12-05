import json
import ollama

def swewic_json_test():
    ollama_client = ollama.Client()
    # KRISTIAN_NOTE - They wrote the JSONL file in UTF-8 encoding to preserve the necessary Swedish vowels å, ä, and ö.
    with open ("SuperLim-2-2.0.4/swewic/swewic_test.jsonl", 'r', encoding = "utf8") as swewic_file:
        # KRISTIAN_NOTE - A JSONL file contains multiple JSON objects, which need to be converted to a list and read one-by-one.
        # https://stackoverflow.com/questions/50475635/loading-jsonl-file-as-json-objects
        swewic_data = list (swewic_file)
        test = json.loads (swewic_data[3]) # KRISTIAN_TODO - loop through this.  For each json object in the list -> measure accuracy -> make graphs
        print (test ['first']['context'])
        print ("The LLM evaluates:")
        print (eval_llm_for_sentence_pair (ollama_client, test['first']['word']['text'], test['first']['context'], test['second']['context']))
        print ("But the actual answer is:")
        print (test['label'])

def eval_llm_for_sentence_pair(ollama_client, given_word, first_sentence, second_sentence):
    prompt = "For each test pair, predict if the word: " + given_word + " is being used in the same sense in the following two sentences: " +\
         first_sentence + second_sentence + "  Please answer 'Yes' or 'No'."
    return ollama_client.generate ("llama3.1", prompt).response

if __name__ == "__main__":
    swewic_json_test()
