from tm import tm
from tm import jsonConverter

if __name__ == "__main__":
    f = open("text.txt", "r", encoding="utf8")
    text3 = f.read()
    f.close()
    print(text3)
    text3 = tm.remove_special_characters(text3)
    print(tm.get_number_of_words(text3))
