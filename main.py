"""Assignment 9: Seaborn data visualization project.

Run this file from the project directory with:
    python main.py

The script creates all required exercise and planets visualizations in the
``outputs`` directory and prints the main conclusions to the terminal.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class SeabornVisualizationProject:
    """Load, validate, reshape, and visualize the assignment datasets."""

    REQUIRED_EXERCISE_COLUMNS = {
        "id", "1 min", "15 min", "30 min", "diet", "kind"
    }
    PULSE_COLUMNS = ["1 min", "15 min", "30 min"]

    def __init__(self, exercise_file="Exercise_Data.csv", output_dir="outputs"):
        """Store file locations and initialize empty DataFrame attributes."""
        self.exercise_file = Path(exercise_file)
        self.output_dir = Path(output_dir)
        self.exercise_data = pd.DataFrame()
        self.exercise_long = pd.DataFrame()
        self.planets_data = pd.DataFrame()

    def configure_style(self):
        """Apply one consistent, readable visual style to every graph."""
        sns.set_theme(style="whitegrid", context="notebook", palette="colorblind")
        plt.rcParams.update({
            "figure.dpi": 120,
            "savefig.dpi": 200,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "axes.titlesize": 14,
            "figure.titlesize": 16,
        })

    def load_data(self):
        """Load both datasets and raise useful errors if data are unavailable."""
        if not self.exercise_file.exists():
            raise FileNotFoundError(
                f"Could not find {self.exercise_file}. Place Exercise_Data.csv "
                "in the same folder as main.py."
            )

        self.exercise_data = pd.read_csv(self.exercise_file)
        missing = self.REQUIRED_EXERCISE_COLUMNS - set(self.exercise_data.columns)
        if missing:
            raise ValueError(f"Exercise data is missing columns: {sorted(missing)}")

        if self.exercise_data[list(self.PULSE_COLUMNS)].isna().any().any():
            raise ValueError("Pulse columns contain missing values.")

        self.exercise_long = self.exercise_data.melt(
            id_vars=["id", "diet", "kind"],
            value_vars=self.PULSE_COLUMNS,
            var_name="time",
            value_name="pulse",
        )
        self.exercise_long["time"] = pd.Categorical(
            self.exercise_long["time"],
            categories=self.PULSE_COLUMNS,
            ordered=True,
        )

        try:
            self.planets_data = sns.load_dataset("planets")
        except Exception as error:
            raise RuntimeError(
                "Seaborn could not load its built-in planets dataset. "
                "Connect to the internet once so Seaborn can cache it."
            ) from error

        if self.planets_data.empty:
            raise ValueError("The planets dataset loaded but contains no rows.")

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_current_figure(self, filename):
        """Save the active Matplotlib figure and close it to conserve memory."""
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, bbox_inches="tight")
        plt.close()

    def create_exercise_heatmap(self):
        """Create a participant-by-time heatmap of all pulse measurements."""
        pulse_matrix = self.exercise_data.set_index("id")[self.PULSE_COLUMNS]
        plt.figure(figsize=(8, 10))
        sns.heatmap(
            pulse_matrix,
            cmap="YlOrRd",
            annot=True,
            fmt=".0f",
            linewidths=0.4,
            cbar_kws={"label": "Pulse (beats per minute)"},
        )
        plt.title("Pulse Readings for Each Student Over Time", pad=14)
        plt.xlabel("Time of Measurement")
        plt.ylabel("Student ID")
        self.save_current_figure("exercise_pulse_heatmap.png")

    def create_exercise_categorical_plot(self):
        """Compare pulse by exercise and diet at each measurement time."""
        graph = sns.catplot(
            data=self.exercise_long,
            x="kind",
            y="pulse",
            hue="diet",
            col="time",
            kind="bar",
            errorbar="sd",
            order=["rest", "walking", "running"],
            hue_order=["low fat", "no fat"],
            palette="Set2",
            height=4.5,
            aspect=0.85,
        )
        graph.set_axis_labels("Type of Exercise", "Average Pulse (beats per minute)")
        graph.set_titles("{col_name}")
        graph.set(ylim=(75, 150))
        graph.legend.set_title("Diet")
        graph.figure.subplots_adjust(top=0.82)
        graph.figure.suptitle("Average Pulse by Exercise, Diet, and Time", fontweight="bold")
        graph.savefig(
            self.output_dir / "exercise_categorical_comparison.png",
            dpi=200,
            bbox_inches="tight",
        )
        plt.close(graph.figure)

    def create_planets_relational_plots(self):
        """Create two relational plots: discovery trend and mass-orbit relation."""
        yearly = (
            self.planets_data.dropna(subset=["year"])
            .groupby("year")
            .size()
            .reset_index(name="discoveries")
        )
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=yearly,
            x="year",
            y="discoveries",
            marker="o",
            color="#3066BE",
            linewidth=2.5,
        )
        plt.title("Exoplanet Discoveries Increased Sharply Over Time")
        plt.xlabel("Discovery Year")
        plt.ylabel("Number of Planets Discovered")
        self.save_current_figure("planets_relational_discoveries_by_year.png")

        mass_orbit = self.planets_data.dropna(subset=["mass", "orbital_period"])
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=mass_orbit,
            x="orbital_period",
            y="mass",
            hue="method",
            size="number",
            sizes=(35, 180),
            alpha=0.75,
            palette="tab10",
        )
        plt.xscale("log")
        plt.yscale("log")
        plt.title("Planet Mass and Orbital Period by Discovery Method")
        plt.xlabel("Orbital Period (days, log scale)")
        plt.ylabel("Planet Mass (Jupiter masses, log scale)")
        plt.legend(title="Method / Planets in System", bbox_to_anchor=(1.02, 1), loc="upper left")
        self.save_current_figure("planets_relational_mass_vs_orbit.png")

    def create_planets_distribution_plots(self):
        """Create two distribution plots for year and orbital period."""
        plt.figure(figsize=(10, 6))
        sns.histplot(
            data=self.planets_data,
            x="year",
            bins=25,
            kde=True,
            color="#00A6A6",
            edgecolor="white",
        )
        plt.title("Distribution of Exoplanet Discovery Years")
        plt.xlabel("Discovery Year")
        plt.ylabel("Number of Planets")
        self.save_current_figure("planets_distribution_discovery_year.png")

        orbit = self.planets_data.dropna(subset=["orbital_period"]).query("orbital_period > 0")
        plt.figure(figsize=(10, 6))
        sns.histplot(
            data=orbit,
            x="orbital_period",
            bins=45,
            log_scale=True,
            color="#F28E2B",
            edgecolor="white",
        )
        plt.title("Distribution of Planet Orbital Periods")
        plt.xlabel("Orbital Period (days, log scale)")
        plt.ylabel("Number of Planets")
        self.save_current_figure("planets_distribution_orbital_period.png")

    def create_planets_categorical_plots(self):
        """Create two categorical plots comparing major discovery methods."""
        method_order = self.planets_data["method"].value_counts().index
        plt.figure(figsize=(11, 7))
        sns.countplot(
            data=self.planets_data,
            y="method",
            order=method_order,
            hue="method",
            palette="viridis",
            legend=False,
        )
        plt.title("Exoplanets Found by Each Discovery Method")
        plt.xlabel("Number of Planets")
        plt.ylabel("Discovery Method")
        self.save_current_figure("planets_categorical_method_counts.png")

        top_methods = self.planets_data["method"].value_counts().head(4).index
        distance_data = self.planets_data[
            self.planets_data["method"].isin(top_methods)
        ].dropna(subset=["distance"])
        plt.figure(figsize=(11, 7))
        sns.boxplot(
            data=distance_data,
            x="method",
            y="distance",
            hue="method",
            order=top_methods,
            palette="mako",
            legend=False,
            showfliers=False,
        )
        plt.title("Detection Distance for the Four Most Common Methods")
        plt.xlabel("Discovery Method")
        plt.ylabel("Distance (parsecs)")
        plt.xticks(rotation=15, ha="right")
        self.save_current_figure("planets_categorical_distance_by_method.png")

    def print_conclusions(self):
        """Print concise interpretations required by the assignment."""
        exercise_means = (
            self.exercise_long.groupby(["kind", "diet"], observed=True)["pulse"]
            .mean()
            .round(1)
        )
        print("\nEXERCISE DATA CONCLUSIONS")
        print(exercise_means.to_string())
        print(
            "\nPulse is lowest while resting, higher while walking, and highest "
            "while running. This shows students that the heart beats faster to "
            "move more oxygen through the body during harder activity. Differences "
            "between the two diet groups are smaller and less consistent than the "
            "differences caused by exercise, so this small experiment does not prove "
            "that one diet alone caused a change in pulse."
        )

        print("\nPLANETS DATA CONCLUSIONS")
        print(
            "The discovery-year line and histogram most clearly demonstrate a "
            "notable pattern: recorded exoplanet discoveries rose dramatically in "
            "the 2000s and early 2010s. The method count plot also shows that Transit "
            "and Radial Velocity produced most observations. Log scales make the "
            "very wide ranges in orbital period and mass readable without allowing "
            "a few extreme values to flatten the rest of the graph."
        )

    def run(self):
        """Execute the complete project workflow."""
        self.configure_style()
        self.load_data()
        self.create_exercise_heatmap()
        self.create_exercise_categorical_plot()
        self.create_planets_relational_plots()
        self.create_planets_distribution_plots()
        self.create_planets_categorical_plots()
        self.print_conclusions()
        print(f"\nSaved all visualizations in: {self.output_dir.resolve()}")


if __name__ == "__main__":
    project = SeabornVisualizationProject()
    project.run()
