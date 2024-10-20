import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('ver05.csv')

# Drop rows with NaN values in the DateTime column
df = df.dropna(subset=['DateTime'])

# Ensure DateTime column is in the correct datetime format
df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y:%m:%d %H:%M:%S')

# Extract hour and day of the week
df['Hour'] = df['DateTime'].dt.hour
df['DayOfWeek'] = df['DateTime'].dt.day_name()  # Get the name of the day of the week

# Create a pivot table for the heatmap
pivot_table = df.pivot_table(index='DayOfWeek', columns='Hour', aggfunc='size', fill_value=0)

# Plot the heatmap using Plotly
fig = px.imshow(pivot_table, 
                labels=dict(x="Hour of the Day", y="Day of the Week", color="Counts"),
                x=pivot_table.columns,
                y=pivot_table.index,
                aspect="auto")

fig.update_layout(title='Heatmap of Photos taken in October, by Hour and Day of the Week')

# Save the plot as an HTML file
fig.write_html("heatmap.html")

print("Heatmap saved as heatmap.html. Open this file in your browser to view the plot.")
