import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Read the Excel file
file_path = '/Users/annateruel/Desktop/fig1/animal_counts_with_taxonomic_class.xlsx'
df = pd.read_excel(file_path)

# Step 2: Convert the DataFrame to dictionaries
animal_counts = df.set_index('Animal')['Count'].to_dict()
taxonomic_classes = df.set_index('Animal')['Taxonomic Class'].to_dict()

def filter_labels_and_values(data, threshold=5):
    filtered_labels = [label if value >= threshold else '' for label, value in data.items()]
    label_value_strings = [f'{label}: {value}' if label else '' for label, value in zip(filtered_labels, data.values())]
    return label_value_strings

def plot_pie_chart(data, labels, categories, output_path, threshold=5):
    """
    Create and save a donut-style pie chart based on data and labels.
                                                                                                                          
    Args:
        data (array-like): The data values for the pie chart.
        labels (list of str): Labels for each pie slice.
        categories (list of str): Categories for each pie slice.
        output_path (str): The path to save the generated pie chart image.
        threshold (int): The threshold for aggregating small categories.
    """
    # Aggregate small categories into 'Other'
    aggregated_data = {}
    aggregated_categories = {}
    for i, (label, value) in enumerate(zip(labels, data)):
        if value < threshold:
            if 'Other' not in aggregated_data:
                aggregated_data['Other'] = 0
                aggregated_categories['Other'] = 'Other'
            aggregated_data['Other'] += value
        else:
            aggregated_data[label.split(":")[0]] = value
            aggregated_categories[label.split(":")[0]] = categories[i]

    # Ensure no missing taxonomic classes
    aggregated_categories = {k: (v if v else 'Unknown') for k, v in aggregated_categories.items()}

    # Sort aggregated data by taxonomic categories first and then by value
    aggregated_data = {k: v for k, v in sorted(aggregated_data.items(), key=lambda item: (str(aggregated_categories[item[0]]), item[1]), reverse=True)}
    aggregated_categories = {k: aggregated_categories[k] for k in aggregated_data.keys()}

    # Update labels and categories
    labels = filter_labels_and_values(aggregated_data, threshold=threshold)
    categories = [aggregated_categories[label.split(":")[0]] for label in aggregated_data.keys()]

    # Define unique colors for each category using the plasma colormap
    unique_categories = list(set(categories))
    cmap = plt.get_cmap('plasma')
    category_colors = {category: cmap(i / len(unique_categories)) for i, category in enumerate(unique_categories)}
    
    # Assign colors to data based on categories
    colors = [category_colors[category] for category in categories]

    fig, ax = plt.subplots(figsize=(10, 10))
    size = 0.3  # Size of the ring
    wedges, texts = ax.pie(aggregated_data.values(),  # Use actual values for the plot
                           radius=1,
                           textprops={'fontsize': 10},
                           labels=labels,
                           wedgeprops=dict(width=size, edgecolor='w'),
                           colors=colors)

    # Add a white circle in the middle to create the donut effect
    centre_circle = plt.Circle((0, 0), 1 - size, fc='white')
    fig.gca().add_artist(centre_circle)

    # Add counts to the labels
    for i, text in enumerate(texts):
        if labels[i]:
            text.set_text(f"{labels[i].split(': ')[0]}: {list(aggregated_data.values())[i]}")
    
    plt.savefig(output_path, format="svg", dpi=100)
    plt.show()

    return category_colors

def plot_other_category(data, categories, output_path, category_colors):
    """
    Create a bar plot for the "Other" category with taxonomic color coding and labels.

    Args:
        data (dict): Dictionary with animal counts for the "Other" category.
        categories (dict): Dictionary with taxonomic categories for the animals.
        output_path (str): The path to save the generated bar plot image.
        category_colors (dict): Colors used in the pie chart.
    """
    pdf_animals = [
        'gecko', 'leaf', 'mouse', 'rat', 'monkey', 'macaque', 'dog', 'cat', 'pig', 'stick',
        'rabbit', 'horse', 'bat', 'zebra', 'bear', 'cow', 'chimpanzee', 'worm', 'spider',
        'fly', 'ant', 'bee', 'cricket', 'moth', 'beetle', 'fish', 'bird', 'chicken'
    ]
    
    other_animals = {k: v for k, v in data.items() if k not in pdf_animals and v < 5}

    # Create DataFrame for the "Other" category
    other_df = pd.DataFrame(list(other_animals.items()), columns=['Animal', 'Count'])
    other_df['Taxonomic Class'] = other_df['Animal'].map(categories)

    # Sort by Taxonomic Class and then by Count
    other_df = other_df.sort_values(by=['Taxonomic Class', 'Count'], ascending=[True, False])

    # Define unique colors for each taxonomic class
    taxonomic_classes = other_df['Taxonomic Class'].unique()
    cmap = plt.get_cmap('plasma')
    color_map = {taxonomic_class: cmap(i / len(taxonomic_classes)) for i, taxonomic_class in enumerate(taxonomic_classes)}
    
    # Assign colors to taxonomic classes
    other_df['Color'] = other_df['Taxonomic Class'].map(color_map)

    # Plot
    fig, ax = plt.subplots(figsize=(4, 10))
    bottom = 0

    for _, row in other_df.iterrows():
        ax.bar('Other', row['Count'], bottom=bottom, color=row['Color'], edgecolor='black', width=0.3)
        ax.text(0.35, bottom + row['Count'] / 2, f"{row['Animal']}: {row['Count']}", va='center', ha='left')
        bottom += row['Count']

    # Remove axes
    ax.axis('off')

    ax.set_title('Count Distribution in "Other" Category')
    plt.savefig(output_path, format="svg", dpi=100)
    plt.show()

# Example usage
sorted_animal_counts = dict(sorted(animal_counts.items(), key=lambda item: item[1], reverse=True))

categories_list = [taxonomic_classes.get(animal, 'Other') for animal in sorted_animal_counts.keys()]
label_value_strings = filter_labels_and_values(sorted_animal_counts)

output_path_pie = '/Users/annateruel/Desktop/fig1_sorted.svg'
category_colors = plot_pie_chart(list(sorted_animal_counts.values()), label_value_strings, categories_list, output_path_pie)

# Plot the "Other" category
output_path_other = '/Users/annateruel/Desktop/fig2_other_category.svg'
plot_other_category(animal_counts, taxonomic_classes, output_path_other, category_colors)
