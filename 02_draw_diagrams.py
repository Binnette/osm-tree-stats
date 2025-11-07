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

    # Get the most recent row
    latest_row = data.iloc[-1]
    species_count = latest_row[species_col]
    no_species_count = latest_row[no_species_col]

    # Calculate percentage of trees with known species
    total = species_count + no_species_count
    percentage = round(species_count * 100 / total, 1)

    # Prepare the data for plotting
    plot_data = data[['date', species_col]].copy()

    # Ensure the 'date' column is unique and correctly formatted
    plot_data['date'] = pd.to_datetime(plot_data['date'], errors='coerce')

    # Drop rows with NaT in the 'date' column if conversion failed
    plot_data = plot_data.dropna(subset=['date'])

    # Rename category for plotting
    plot_data = plot_data.rename(columns={species_col: 'With species'})
    plot_data = plot_data.melt(id_vars='date', value_vars=['With species'],
                               var_name='Category', value_name='Number of Trees')

    # Set up the plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=plot_data, x='date', y='Number of Trees', hue='Category', palette='viridis', marker='o')

    # Adapt the Y-axis scale
    y_min = plot_data['Number of Trees'].min() - 0.001 * plot_data['Number of Trees'].max()
    y_max = plot_data['Number of Trees'].max() + 0.001 * plot_data['Number of Trees'].max()
    plt.ylim(y_min, y_max)

    # Update title with percentage
    plt.title(f'{percentage}% of trees with known species')
    plt.ylabel('Number of Trees')
    plt.xlabel('Date')
    plt.legend(title='Category')

    # Save the plot to a file in the assets folder
    plot_file_path = f'assets/{location}.png'
    plt.savefig(plot_file_path)
    plt.close()

    print(f"Plot saved to {plot_file_path}")

print("All plots generated and saved in the 'assets' directory.")
