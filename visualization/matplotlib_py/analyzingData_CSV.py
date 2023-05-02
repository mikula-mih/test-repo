import numpy as np
import pandas as pd
import csv
from collections import Counter
from matplotlib import pyplot as plt

plt.style.use("fivethirtyeight")

def open_data_with_csv_module():
    with open('./matplotlib_py/data.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        language_counter = Counter()

        for row in csv_reader:
            language_counter.update(row['LanguagesWorkedWith'].split(';'))

    for item in language_counter.most_common(15):
        languages.append(item[0])
        popularity.append(item[1])


def loading_csv_with_pandas():
    data = pd.read_csv('./matplotlib_py/data.csv')
    ids = data['Responder_id']
    lang_responses = data['LanguagesWorkedWith']

    language_counter = Counter()

    for response in lang_responses:
        language_counter.update(response.split(';'))

    for item in language_counter.most_common(15):
        languages.append(item[0])
        popularity.append(item[1])




if __name__ == '__main__':
    languages = []
    popularity = []

    # open_data_with_csv_module()
    loading_csv_with_pandas()

    languages.reverse()
    popularity.reverse()

    plt.barh(languages, popularity)

    # plt.ylabel('Programming Language')
    plt.xlabel('Number of People Who Use')
    plt.title('Most Popular Language')

    plt.tight_layout()

    plt.show()
