import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def create_pie_dataframe(file_path):
    """
    This function reads a CSV file and create a multi-index DataFrame with sorted values.
    The expected file is a data frame containing the number of items per animal species and 
    the phylogenetic category to which each animal species belongs. 

    Args:
        file_path (str): The path to the CSV file containing the data.

    Returns:
        pandas.DataFrame: A multi-index DataFrame sorted by 'tree' and 'value', where 'tree' 
        is the phylogenetic category, and 'value' is the number of citations.
    """
    df = pd.read_csv(file_path)
    multindex_df = df.set_index(['tree', 'animal'])
    multindex_df.sort_index(inplace=True)
    inner = df.groupby(['tree', 'animal']).sum().sort_values(by=['tree', 'value'], ascending=[True, True])
    return inner

def filter_labels_and_values(inner):
    """
    Filter labels and create label-value strings based on a DataFrame.

    Args:
        inner (pandas.DataFrame): The DataFrame to extract labels and values from.

    Returns:
        list of str: A list of label-value strings for pie chart labels.
    """
    inner_labels = inner.index.get_level_values(1)
    filtered_labels = [label if value >= 5 else '' for label, value in zip(inner_labels, inner.values.flatten())]
    label_value_strings = [f'{label}: {value}' for label, value in zip(filtered_labels, inner.values.flatten())]
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
    colors = plt.get_cmap('plasma')(np.linspace(0, 1, num_colors))
    size = 0.1

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(data,
           radius=1 - size,
           textprops={'fontsize': 8},
           labels=labels,
           wedgeprops=dict(width=size, edgecolor='w'),
           colors=colors)

    plt.savefig(output_path, format="pdf", dpi=100)

if __name__ == "__main__":
    file_path = '/Volumes/ANNA_HD/DLC_AI_rec/recidency_docs/week8/fig1/df.csv'
    output_path = '/Users/annateruel/Desktop/fig1.pdf'
    inner = create_pie_dataframe(file_path)
    label_value_strings = filter_labels_and_values(inner)
    plot_pie_chart(inner.values.flatten(), label_value_strings, output_path)