# Assignment 9: Seaborn

## Project purpose

This project uses Python, Pandas, Matplotlib, and Seaborn to explore two real-world datasets. The first section examines how exercise type, diet, and measurement time relate to pulse. The second section uses Seaborn's built-in `planets` dataset to demonstrate two relational plots, two distributional plots, and two categorical plots.

## Files

- `main.py` — loads and validates the data, reshapes it, creates all eight required visualizations, and prints conclusions.
- `Exercise_Data.csv` — the gym and elementary-school exercise dataset.
- `outputs/` — contains the generated PNG visualizations.
- `AI_CHAT_LOG.md` — documents the use of generative AI, as required.
- `requirements.txt` — lists the Python packages needed to run the project.

## Class design and implementation

The project is organized around the `SeabornVisualizationProject` class. This keeps data loading, validation, visualization, and interpretation in one reusable workflow rather than placing all code in the global scope.

### Attributes

- `exercise_file`: path to the exercise CSV file.
- `output_dir`: directory where graphs are saved.
- `exercise_data`: wide-format DataFrame loaded from the exercise CSV.
- `exercise_long`: long-format version used by Seaborn for grouped comparisons.
- `planets_data`: DataFrame loaded from Seaborn's built-in planets dataset.
- `REQUIRED_EXERCISE_COLUMNS`: columns that must exist for the program to continue.
- `PULSE_COLUMNS`: ordered list of the three pulse measurement columns.

### Methods

- `configure_style()`: applies consistent colors, sizing, grid styling, and resolution.
- `load_data()`: loads both datasets, checks files and columns, rejects missing pulse data, and reshapes the exercise data.
- `save_current_figure()`: saves and closes the current figure.
- `create_exercise_heatmap()`: maps each student's pulse at each recorded time.
- `create_exercise_categorical_plot()`: compares average pulse by exercise, diet, and time with standard-deviation error bars.
- `create_planets_relational_plots()`: creates a discovery trend line and mass-versus-orbit scatterplot.
- `create_planets_distribution_plots()`: creates discovery-year and orbital-period histograms.
- `create_planets_categorical_plots()`: compares method counts and detection distance by method.
- `print_conclusions()`: prints student-friendly interpretations of the results.
- `run()`: coordinates the full program from loading through output.

## Main findings

The exercise graphs show that pulse tends to be lowest at rest, increases during walking, and is highest during running. This makes sense because harder activity requires the heart to deliver oxygen more quickly. The diet groups differ in some measurements, but those differences are smaller and less consistent than the effect of exercise. Since the dataset has only 30 observations and does not describe random assignment or other health factors, it cannot prove that either diet caused a pulse difference.

For the planets data, the discovery-year plots most clearly show that exoplanet discoveries increased sharply during the 2000s and early 2010s. The categorical count plot shows that Transit and Radial Velocity account for most recorded discoveries. The log-scaled graphs are useful because orbital periods and planet masses cover extremely wide ranges.

## How to run

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Keep `Exercise_Data.csv` in the same directory as `main.py`.
3. Run:

   ```bash
   python main.py
   ```

4. Open the `outputs` directory to view all graphs.

## Limitations

- The exercise dataset is small, so the results should not be generalized to all children.
- The data does not include age, baseline fitness, medical history, or details about how diets were assigned.
- Error bars describe variation but do not prove statistical significance or causation.
- Some planets records have missing values, so each plot uses only rows containing the variables it needs.
- Seaborn may require an internet connection the first time it downloads and caches the built-in planets dataset.
