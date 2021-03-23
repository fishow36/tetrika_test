import requests
from bs4 import BeautifulSoup
import re

def parse_ul(ul, animals_list, letter_dict):
    for tag in ul.find_all("li", recursive=True):
        animal_name = tag.text
        if not re.search('[а-яА-Я]', animal_name):
            return (-1)
        first_letter = animal_name[0]
        animals_list.append(animal_name)
        if first_letter not in letter_dict:
            letter_dict[first_letter] = 0
        letter_dict[first_letter] += 1
    return (0)

def parse_wiki_animals():
    animals_list = []
    letter_dict = {}
    url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        s = soup.find_all("div", {"class":"mw-category-group"})
        answer = parse_ul(s[0].ul, animals_list, letter_dict)
        if answer == 0:
            url = 'https://ru.wikipedia.org/' + soup.find('a', text='Следующая страница')['href']
        else:
            break
    return (animals_list, letter_dict)

if __name__ == "__main__":
    animals, letters = parse_wiki_animals()
    for key, value in sorted(letters.items(), key = lambda c: ord('Е') + 0.5 if c[0] == 'Ё' else ord(c[0])):
        print(f'{key}: {value}')