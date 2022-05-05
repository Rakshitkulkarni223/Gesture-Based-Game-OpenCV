import random

import requests
import json

from bs4 import BeautifulSoup


def load(type):
    catergory_list = {"General Knowledge": 9, "Books": 10, "Film": 11, "Music": 12,
                      "Television": 14, "Video Games": 15, "Science and Nature": 17, "Science and Computer": 18,
                      "Science and Mathematics": 19, "Mythology": 20, "Sports": 21, "Geography": 22,
                      "History": 23, "Politics": 24, "Art": 25, "Celebrities": 26, "Animals": 27,
                      "Vehicles": 28, "Comics": 29, "Gadgets": 30}

    catergory_list_values = list(catergory_list.values())

    catergory_list_values = random.sample(catergory_list_values, 5)

    questions_list = {}

    for i in catergory_list_values:
        response_API = requests.get(
            "https://opentdb.com/api.php?amount=1&category={}&difficulty={}&type=multiple".format(i, type))
        data = response_API.text

        data = json.loads(data)

        result = data['results'][0]

        question = BeautifulSoup(result['question'], 'html.parser')

        correct_option = result["correct_answer"]
        correct_option = BeautifulSoup(correct_option, 'html.parser')

        correct_answer = [correct_option]

        incorrect_options = []

        for incorrect_option in result["incorrect_answers"]:
            incorrect_options.append(BeautifulSoup(incorrect_option, 'html.parser'))

        correct_answer.extend(incorrect_options)

        questions_list[question] = correct_answer

    return questions_list