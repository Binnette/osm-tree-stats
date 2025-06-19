import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the data from the CSV file
file_path = 'trees_data.csv'
data = pd.read_csv(file_path)

# Create the assets directory if it doesn't exist
os.makedirs('assets', exist_ok=True)

# Iterate over each pair of columns and generate a plot
for i in range(1, len(data.columns) - 1, 2):
    species_col = data.columns[i]
    no_species_col = data.columns[i + 1]

    # Extract the location name from the column name
    location = species_col.replace('_species', '')

    # Prepare the data for plotting
    #plot_data = data[['date', species_col, no_species_col]].copy()
    plot_data = data[['date', species_col]].copy()

    # Ensure the 'date' column is unique and correctly formatted
    plot_data['date'] = pd.to_datetime(plot_data['date'], errors='coerce')

    # Drop rows with NaT in the 'date' column if conversion failed
    plot_data = plot_data.dropna(subset=['date'])

    plot_data = plot_data.melt(id_vars='date', value_vars=[species_col], #, no_species_col],
                               var_name='Category', value_name='Number of Trees')

    # Set up the plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=plot_data, x='date', y='Number of Trees', hue='Category', palette='viridis', marker='o')


    # Adapt the Y-axis scale
    # Dynamically set the Y-axis scale based on the data range
    y_min = plot_data['Number of Trees'].min() - 0.001 * plot_data['Number of Trees'].max()
    y_max = plot_data['Number of Trees'].max() + 0.001 * plot_data['Number of Trees'].max()
    plt.ylim(y_min, y_max)

    plt.title(f'Number of Trees with Known Species') # vs Unknown Species in {location} Over Time')
    plt.ylabel('Number of Trees')
    plt.xlabel('Date')
    plt.legend(title='Category')

    # Save the plot to a file in the assets folder
    plot_file_path = f'assets/{location}.png'
    plt.savefig(plot_file_path)
    plt.close()
