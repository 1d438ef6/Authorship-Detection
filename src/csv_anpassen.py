import pandas as pd

def find_replace(csv_path, search_characters, replace_with):
    text = open(csv_path, "r")
    text = ''.join([i for i in text]).replace(
        search_characters, replace_with)
    x = open(csv_path, "w")
    x.writelines(text)
    x.close()


if __name__ == '__main__':
    csv_path = 'feature_save4_1.csv'
    search_characters = 'A'
    replace_with = ''

    find_replace(csv_path, search_characters, replace_with)