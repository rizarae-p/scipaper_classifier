import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

animal_counts = {'mouse': 651, 'rat': 148, 'fly': 50, 'ant': 24, 'macaque': 18, 'dolphin': 2, 'bird': 29, 'fish': 72, 'rabbit': 10, 'pig': 17, 'dog': 19, 'cobra': 1, 'monkey': 37, 'insect': 23, 'bug': 3, 'beetle': 4, 'rodent': 30, 'primate': 30, 'snake': 2, 'elephant': 3, 'turkey': 1, 'cricket': 6, 'spider': 5, 'worm': 11, 'zebra': 8, 'salamander': 1, 'larva': 13, 'frog': 1, 'jellyfish': 1, 'cat': 17, 'bat': 8, 'cheetah': 4, 'octopus': 4, 'chimpanzee': 5, 'bee': 11, 'cow': 6, 'mosquito': 3, 'hamster': 1, 'squirrel': 2, 'gecko': 6, 'lizard': 4, 'zooplankton': 1, 'chicken': 8, 'eel': 1, 'goat': 3, 'tiger': 2, 'moth': 2, 'hedgehog': 1, 'wolf': 1, 'shrimp': 2, 'otter': 1, 'pupa': 1, 'cockroach': 2, 'sheep': 2, 'horse': 11, 'caterpillar': 1, 'bear': 7, 'baboon': 1, 'mite': 1, 'duck': 1, 'crab': 2, 'cuttlefish': 1, 'sloth': 1, 'goose': 1, 'butterfly': 1, 'camel': 1, 'sea urchin': 1, 'caribou': 1, 'flea': 1, 'snail': 1, 'alligator': 1, 'crocodile': 1, 'termite': 1, 'wasp': 1}


# def create_pie_dataframe(file_path):
#     """
#     This function reads a CSV file and create a multi-index DataFrame with sorted values.
#     The expected file is a data frame containing the number of items per animal species and 
#     the phylogenetic category to which each animal species belongs. 

#     Args:
#         file_path (str): The path to the CSV file containing the data.

#     Returns:
#         pandas.DataFrame: A multi-index DataFrame sorted by 'tree' and 'value', where 'tree' 
#         is the phylogenetic category, and 'value' is the number of citations.
#     """
#     df = pd.read_csv(file_path)
#     multindex_df = df.set_index(['tree', 'animal'])
#     multindex_df.sort_index(inplace=True)
#     inner = df.groupby(['tree', 'animal']).sum().sort_values(by=['tree', 'value'], ascending=[True, True])
#     return inner

def filter_labels_and_values(data):
    """
    Filter labels and create label-value strings based on a dictionary.

    Args:
        data (dict): The dictionary to extract labels and values from.

    Returns:
        list of str: A list of label-value strings for pie chart labels.
    """
    filtered_labels = [label if value >= 5 else '' for label, value in data.items()]
    label_value_strings = [f'{label}: {value}' if label else '' for label, value in zip(filtered_labels, data.values())]
    return label_value_strings

def plot_pie_chart(data, labels, output_path):
    """
    Create and save a pie chart based on data and labels.

    Args:
        data (array-like): The data values for the pie chart.
        labels (list of str): Labels for each pie slice.
        output_path (str): The path to save the generated pie chart image.

    Returns:
        None
    """
    num_colors = len(labels)
    colors = plt.get_cmap('Set1')(np.linspace(0, 1, num_colors))
    size = 0.1

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(data,
           radius=1 - size,
           textprops={'fontsize': 8},
           labels=labels,
           wedgeprops=dict(width=size, edgecolor='w'),
           colors=colors)

    plt.savefig(output_path, format="pdf", dpi=100)
    plt.show()


if __name__ == "__main__":
    sorted_animal_counts = dict(sorted(animal_counts.items(), key=lambda item: item[1], reverse=True))
    output_path = '/Users/annateruel/Desktop/fig1.pdf'
    label_value_strings = filter_labels_and_values(sorted_animal_counts)
    plot_pie_chart(list(sorted_animal_counts.values()), label_value_strings, output_path)