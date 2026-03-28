# FTIR Transmission and Absorbance Plotter

A Python script that reads multi-sample FTIR data from an Excel file and generates interactive plots of either transmission or absorbance spectra, with outputs saved as an HTML plot and an Excel file.

---

## Author

**Nitish Kapur**<br>
GitHub: [github.com/nitish-kapur](https://github.com/nitish-kapur)

---

## Expected Input Format

The script expects an `.xls` or `.xlsx` Excel file structured as follows:

| Wavenumber | Sample 1 | Sample 2 | Sample 3 | ... |
|---|---|---|---|---|
| 400.296851 | 85.17 | 97.12 | 97.78 | ... |
| 401.731607 | 84.71 | 97.60 | 97.99 | ... |
| ... | ... | ... | ... | ... |

- **Column 1** — Wavenumber values (cm⁻¹)
- **Columns 2 onwards** — Transmission (%) for each sample; column headers are used as legend labels

---

## Requirements
```bash
pip install pandas numpy plotly openpyxl xlrd
```

> `tkinter` is included with most standard Python installations. On some Linux systems you may need to install it separately (e.g. `sudo apt install python3-tk`).

---

## Usage

Run the script directly:
```bash
python ftir-transmision-absorbance-excel-stacked.py
```

1. A file dialog will open — select your Excel file
2. Enter `T` for Transmission or `A` for Absorbance when prompted in the terminal
3. The plot will open in your browser and outputs will be saved automatically

---

## Output

All outputs are saved in subdirectories created automatically in the working directory:

| Location | File | Description |
|---|---|---|
| `Graphs/` | `<filename>_Transmission/Absorbance_<timestamp>.html` | Interactive Plotly HTML plot |
| `Plotted Excel/` | `<filename>_Transmission/Absorbance_<timestamp>.xlsx` | Plotted data as Excel file |

---

## Notes

- If `A` (Absorbance) is selected, transmission values are converted using: **A = −log₁₀(T / 100) × 100**
- The X-axis is inverted as per FTIR convention
- Up to 13 distinct colours are assigned to traces automatically; additional samples cycle through the same colours
- Hovering over a trace displays the wavenumber and transmission/absorbance value
