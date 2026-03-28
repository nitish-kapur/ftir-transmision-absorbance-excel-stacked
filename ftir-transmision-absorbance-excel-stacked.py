"""
FTIR Transmission and Absorbance Plots
Copyright (C) 2026 Nitish Kapur
GitHub: [github.com/nitish-kapur](https://github.com/nitish-kapur)
Licensed under GNU GPLv3
"""

"""
    This script was made as a part of a biofuel research project.

    1.  Opens a file dialog for the user to select an Excel file containing
        multi-sample FTIR transmission data; the first column must be
        wavenumbers and each subsequent column one sample's spectrum.
    2.  Prompts the user in the terminal to choose between Transmission ('T')
        or Absorbance ('A') mode.
    3.  If Absorbance is selected, converts all transmission values using:
            A = −log₁₀(T / 100) × 100
        If Transmission is selected, data is used as-is.
    4.  Generates an interactive Plotly line chart with:
            - X-axis: Wavenumber (cm⁻¹), inverted as per FTIR convention
            - Y-axis: Transmission (%) or Absorbance (%)
            - One coloured trace per sample, labelled by column header
            - Hover tooltips showing wavenumber and spectral value
    5.  Saves the interactive plot as a timestamped HTML file inside a
        'Graphs/' subfolder in the working directory.
    6.  Saves the plotted data (wavenumbers + spectra) as a timestamped
        Excel file inside a 'Plotted Excel/' subfolder.
    7.  Opens the interactive plot in the default web browser.
"""



import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# --- Set up tkinter root for file dialog ---
root = tk.Tk()
root.withdraw()  # Hide the main tkinter window

# Open file dialog to select the Excel file, set initial directory to current working directory
current_folder = os.getcwd()  # Get current working directory
file_path = filedialog.askopenfilename(
    title="Select an Excel File",
    initialdir=current_folder,  # Set initial directory to current folder
    filetypes=[("Excel Files", "*.xls;*.xlsx")]
)

if not file_path:
    print("No file selected. Exiting program.")
    exit()

# --- Load Excel file ---
df = pd.read_excel(file_path)

# Extract wavenumber values (first column)
wavenumber = df.iloc[:, 0]

# --- Timestamp for filenames ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- Ask user whether they want transmission or absorbance ---
graph_type = input("Do you want to plot Transmission or Absorbance? (Enter 'T' for Transmission or 'A' for Absorbance): ").strip().upper()

if graph_type not in ['T', 'A']:
    print("Invalid input. Please enter 'T' for Transmission or 'A' for Absorbance.")
    exit()

# --- If the user wants absorbance, convert transmission values to absorbance ---
if graph_type == 'A':
    df_plot = df.copy()
    for col in df.columns[1:]:  # Skip the first column (wavenumber)
        df_plot[col] = -np.log10(df[col] / 100) * 100  # Convert to absorbance and multiply by 100 to show percentage
    y_axis_label = 'Absorbance (%)'
    plot_title = "Averaged Absorbance Spectra"
    plot_filename_suffix = "_Absorbance"
else:
    df_plot = df.copy()
    y_axis_label = 'Transmission (%)'
    plot_title = "Averaged Transmission Spectra"
    plot_filename_suffix = "_Transmission"

# --- Create a plotly figure ---
fig = go.Figure()

# Define colors for the plot
colors = [
    '#000000',  # Black
    '#ff7f0e',  # Orange
    '#2ca02c',  # Green
    '#d62728',  # Red
    '#9467bd',  # Purple
    '#8c564b',  # Brown
    '#e377c2',  # Pink
    '#7f7f7f',  # Gray
    '#bcbd22',  # Yellow-Green
    '#17becf',  # Cyan
    '#f9a825',  # Yellow
    '#1f77b4',  # Blue
    '#9c27b0'   # Violet
]

# Add traces for each column (except the first one which is wavenumber)
for i, col in enumerate(df_plot.columns[1:]):
    fig.add_trace(go.Scatter(
        x=wavenumber,
        y=df_plot[col],
        mode='lines',
        marker=dict(size=2),
        name=col,
        line=dict(color=colors[i % len(colors)]),
        hovertemplate='%{x} cm<sup>-1</sup><br>' +  # Display wavenumber value inside hover box
                      '<b>%{y:.2f}</b>',  # Display transmission/absorbance value inside hover box
        hoverlabel=dict(bgcolor="yellow", font_size=16, font_family="Arial"),
        opacity=1  # Default opacity for all lines
    ))

# Update layout to include hover effects and invert x-axis
fig.update_layout(
    title=plot_title,
    xaxis_title=r'Wavenumber (cm<sup>-1</sup>)',
    yaxis_title=y_axis_label,
    hovermode="closest",  # Enable hover interaction
    xaxis=dict(
        autorange="reversed"  # Invert x-axis
    ),
)

# Add hover interaction to dim all lines except the one being hovered
fig.update_traces(
    opacity=1,  # Dim all traces by default
    selected=dict(marker=dict(color='black', opacity=1))  # Make hovered trace bold
)

# --- Save the plot ---
output_folder = os.path.join(os.getcwd(), "Graphs")
os.makedirs(output_folder, exist_ok=True)

plot_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}{plot_filename_suffix}_{timestamp}.html"
plot_path = os.path.join(output_folder, plot_filename)

fig.write_html(plot_path)

print(f"Processed and saved plot to {plot_path}")

# --- Save the plotted data as an Excel file ---
plotted_excel_folder = os.path.join(os.getcwd(), "Plotted Excel")
os.makedirs(plotted_excel_folder, exist_ok=True)

plotted_excel_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}{plot_filename_suffix}_{timestamp}.xlsx"
plotted_excel_path = os.path.join(plotted_excel_folder, plotted_excel_filename)

# Save the plotted data (including wavenumber and corresponding transmission/absorbance)
df_plot.to_excel(plotted_excel_path, index=False)

print(f"Saved plotted data as Excel file to {plotted_excel_path}")

# --- Show the plot ---
fig.show()
