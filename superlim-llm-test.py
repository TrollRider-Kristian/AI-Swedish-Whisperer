import json
import ollama

def swewic_json_test():
    # KRISTIAN_NOTE - They wrote the JSONL file in UTF-8 encoding to preserve the necessary Swedish vowels å, ä, and ö.
    with open ("SuperLim-2-2.0.4/swewic/swewic_test.jsonl", 'r', encoding = "utf8") as swewic_file:
        # KRISTIAN_NOTE - A JSONL file contains multiple JSON objects, which need to be converted to a list and read one-by-one.
        # https://stackoverflow.com/questions/50475635/loading-jsonl-file-as-json-objects
        swewic_data = list (swewic_file)
        test = json.loads (swewic_data[0])
        print (test ['first']['context'])

if __name__ == "__main__":
    swewic_json_test()
