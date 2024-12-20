from functools import wraps

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.tools as tls
import seaborn as sns
import plotly.express as px



def save_fig_to_html(func):
    """Decorator to save matplotlib figure as HTML using plotly"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the matplotlib figure from the decorated function
        fig = func(*args, **kwargs)

        # Convert Matplotlib figure to Plotly
        plotly_fig = tls.mpl_to_plotly(fig)

        # Generate filename from function name
        filename = f"{func.__name__}.html"

        # Save the Plotly figure as HTML
        pio.write_html(plotly_fig, filename)

        return fig

    return wrapper


# List of LGBTQ+ related terms
lgbtq_terms = [
    "gay",
    "lesbian",
    "homosexual",
    "homosexuality",
    "bisexual",
    "transgender",
    "queer",
    "trans",
    "transsexual",
    "transvestite",
    "transvestism",
]


@save_fig_to_html
def plot_gender_proportions(df):
    """Plot the gender proportions of actors over time"""
    # Split the comma-separated gender values and explode them into separate rows
    df_exploded = df.assign(actor_gender=df["actor_gender"].str.split(",")).explode(
        "actor_gender"
    )

    # Clean up the gender values (strip whitespace) and handle nan values
    df_exploded["actor_gender"] = df_exploded["actor_gender"].str.strip()

    # Calculate proportions by year
    proportions = (
        df_exploded.groupby("Movie release date")["actor_gender"]
        .value_counts(normalize=True)
        .unstack()
    )

    # Plot the proportions
    fig, ax = plt.subplots(figsize=(12, 6))
    proportions.plot(kind="area", stacked=True, ax=ax)
    ax.set_title("Gender Proportions of Actors Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Proportion")
    ax.legend(title="Gender", loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


@save_fig_to_html
def plot_age_proportions(df):
    """Plot the age distribution of actors over time"""

    # Create age groups
    def categorize_age(age):
        if pd.isna(age):
            return None
        elif age < 20:
            return "Under 20"
        elif age < 30:
            return "20-29"
        elif age < 40:
            return "30-39"
        elif age < 50:
            return "40-49"
        elif age < 60:
            return "50-59"
        else:
            return "60+"

    # Split the comma-separated age values and explode them into separate rows
    df_exploded = df.assign(
        actor_age=df["actor_age_at_release"].str.split(",")
    ).explode("actor_age_at_release")

    # Convert to numeric and clean up
    df_exploded["actor_age_at_release"] = pd.to_numeric(
        df_exploded["actor_age_at_release"], errors="coerce"
    )

    # Create age groups
    df_exploded["age_group"] = df_exploded["actor_age_at_release"].apply(categorize_age)

    # Remove rows where age_group is None
    df_exploded = df_exploded.dropna(subset=["age_group"])

    # Calculate proportions by year
    proportions = (
        df_exploded.groupby("Movie release date")["age_group"]
        .value_counts(normalize=True)
        .unstack()
    )

    # Plot the distribution
    fig, ax = plt.subplots(figsize=(12, 6))
    proportions.plot(kind="area", stacked=True, ax=ax)
    ax.set_title("Age Distribution of Actors Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Proportion")
    ax.legend(title="Age Groups", bbox_to_anchor=(1.05, 1))
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


@save_fig_to_html
def plot_age_proportions_by_gender(df: pd.DataFrame):
    """Plot the age distribution of actors over time by gender"""

    # Create age groups
    def categorize_age(age):
        if pd.isna(age):
            return None
        elif age < 20:
            return "Under 20"
        elif age < 30:
            return "20-29"
        elif age < 40:
            return "30-39"
        elif age < 50:
            return "40-49"
        elif age < 60:
            return "50-59"
        else:
            return "60+"

    # Split and explode both age and gender columns
    df_exploded = df.assign(
        actor_age=df["actor_age_at_release"].str.split(","),
        actor_gender=df["actor_gender"].str.split(","),
    )
    df_exploded = df_exploded.explode("actor_age")
    df_exploded = df_exploded.explode("actor_gender")

    # Convert age to numeric and clean up
    df_exploded["actor_age"] = pd.to_numeric(df_exploded["actor_age"], errors="coerce")

    # Clean up gender values
    df_exploded["actor_gender"] = df_exploded["actor_gender"].str.strip()

    # Create age groups
    df_exploded["age_group"] = df_exploded["actor_age"].apply(categorize_age)

    # Filter for just M and F genders and remove rows with missing age groups
    df_exploded = df_exploded[
        (df_exploded["actor_gender"].isin(["M", "F"]))
        & (df_exploded["age_group"].notna())
    ]

    # Create separate plots for each gender
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

    for gender, ax, title in zip(["F", "M"], [ax1, ax2], ["Female", "Male"]):
        gender_data = df_exploded[df_exploded["actor_gender"] == gender]

        proportions = (
            gender_data.groupby("Movie release date")["age_group"]
            .value_counts(normalize=True)
            .unstack()
        )

        proportions.plot(kind="area", stacked=True, ax=ax)
        ax.set_title(f"Age Distribution of {title} Actors Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Proportion")
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis="x", rotation=45)
        ax.legend(title="Age Groups")

    plt.tight_layout()
    return fig


@save_fig_to_html
def plot_top_languages(df):
    """Plot the top 20 movie released languages"""
    language_counts = df["Movie languages"].str.split(", ").explode().value_counts()
    # remove the languages with less than 2 character
    language_counts = language_counts[language_counts.index.str.len() > 1]
    fig = plt.figure(figsize=(15, 6))
    language_counts[:20].plot(
        kind="bar", title="Top 20 languages", ylabel="Count", alpha=0.75
    )
    return fig


@save_fig_to_html
def plot_top_genres(df):
    """Plot the movie genres of our entire dataset"""
    genre_counts = (
        df["Movie genres"]
        .str.split(", ")
        .explode()
        .loc[lambda x: x != ""]
        .value_counts()
    )

    fig, ax = plt.subplots(figsize=(15, 6))
    genre_counts.plot(
        kind="bar",
        title="Top genres",
        ylabel="Count",
        xlabel="Movie Genre",
        alpha=0.75,
        ax=ax,
    )
    return fig


@save_fig_to_html
def plot_movies_by_year(df):
    """Plot the number of movies in the last 50 years"""
    year_counts = df["Movie release date"].value_counts()
    # Drop non numeric years
    year_counts = year_counts[year_counts.index.str.isnumeric()]
    year_counts.sort_index(ascending=False, inplace=True)

    fig, ax = plt.subplots(figsize=(20, 6))
    year_counts[:50].plot(
        kind="bar",
        title="Number of movies in last 50 years",
        ylabel="Count",
        xlabel="Year",
        alpha=0.75,
        ax=ax,
    )
    return fig


@save_fig_to_html
def plot_gender_distribution(df):
    """Plot the total distribution of female and male actors"""
    # Extract the 'Actor gender' column, split it by commas, and count the occurrences of 'F' and 'M'
    gender_counts = df["actor_gender"].str.split(", ").explode().value_counts()

    # Create the Matplotlib figure
    fig, ax = plt.subplots(figsize=(5, 5))
    gender_counts[["F", "M"]].plot(
        kind="pie",
        colors=["pink", "blue"],
        autopct="%1.1f%%",
        labels=["Female", "Male"],
        ax=ax,
    )
    ax.set_title("Distribution of Female vs Male Actors")
    ax.set_ylabel("")  # Remove y-label as it's not needed for pie charts

    return fig


@save_fig_to_html
def plot_gender_distribution_pie(df):
    """Plot the total distribution of female and male actors as a pie chart"""
    # Extract the 'Actor gender' column, split it by commas, and count the occurrences of 'F' and 'M'
    gender_counts = df["actor_gender"].str.split(", ").explode().value_counts()

    fig, ax = plt.subplots(figsize=(8, 8))
    gender_counts[["F", "M"]].plot(
        kind="pie",
        colors=["#FF6B6B", "#4ECDC4"],  # Coral red and Turquoise
        autopct="%1.1f%%",  # Show percentages with 1 decimal
        labels=["Female", "Male"],
        ax=ax,
    )
    plt.title("Distribution of Female vs Male Actors")
    plt.ylabel("")  # Remove y-label as it's not needed for pie charts
    return fig


@save_fig_to_html
def plot_top_genres_by_year(df):
    """Plot the top 3 movie genres for the last 10 years of our dataset"""
    # Convert 'Movie release date' to numeric without modifying the original dataset
    recent_years = (
        pd.to_numeric(df["Movie release date"], errors="coerce")
        .dropna()
        .astype(int)
        .sort_values(ascending=False)
        .unique()[:20]
    )

    top_genres_per_year = pd.DataFrame()

    for year in recent_years:
        # Get movies in the year
        movies_in_year = df[
            pd.to_numeric(df["Movie release date"], errors="coerce") == year
        ]

        # Count the genres for movies in this year
        genre_counts = (
            movies_in_year["Movie genres"]
            .str.split(", ")
            .explode()
            .loc[lambda x: x != ""]
            .value_counts()
        )

        # Get the top 3 genres and their counts
        top_genres = genre_counts.head(5)

        # Add the data to the DataFrame
        top_genres_per_year = pd.concat(
            [top_genres_per_year, pd.DataFrame({year: top_genres})], axis=1
        )

    # Transpose and clean up the DataFrame for plotting
    top_genres_per_year = top_genres_per_year.T.fillna(0)

    # Plotting the top 3 genres per year for the last 10 years
    fig, ax = plt.subplots(figsize=(15, 8))
    top_genres_per_year.plot(kind="bar", stacked=True, width=0.8, ax=ax)
    ax.set_title("Top 5 Movie Genres Per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Genres", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    return fig


@save_fig_to_html
def plot_mean_revenue_per_year(df):
    """Plot the mean movie box office revenue per year"""
    mean_revenue_per_year = df.groupby("Movie release date")[
        "Movie box office revenue"
    ].mean()
    mean_revenue_per_year = mean_revenue_per_year.dropna()
    mean_revenue_per_year = mean_revenue_per_year[mean_revenue_per_year.index != "nan"]

    fig, ax = plt.subplots(figsize=(25, 7))
    ax.plot(
        mean_revenue_per_year.index,
        mean_revenue_per_year.values,
        color="b",
        marker=".",
        linestyle="solid",
        markersize=12,
        markerfacecolor="white",
    )
    ax.set_title("Mean Movie Box Office Revenue Per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Mean Revenue")
    ax.grid(True)
    ax.tick_params(axis="x", rotation=45)
    plt.draw()
    return fig


@save_fig_to_html
def plot_ethnicity_proportions(df):
    """Plot the ethnicity distribtution of actors in our dataset"""
    # Plot the ethnicities proportions
    ethnicity_counts = df["ethnicity"].str.split(", ").explode().value_counts()

    # Count the non nan values and get top 8
    ethnicity_counts = ethnicity_counts[ethnicity_counts.index != "nan"]
    top_10_ethnicities = ethnicity_counts[1:9]
    others = pd.Series({"Others": ethnicity_counts[8:].sum()})
    ethnicity_counts_final = pd.concat([top_10_ethnicities, others])

    fig, ax = plt.subplots()
    ethnicity_counts_final.plot(kind="pie", autopct="%1.1f%%", ax=ax)
    plt.title("Ethnicity Proportions (Top 8 + Others)")
    return fig


@save_fig_to_html
def plot_lgbtq_movies_per_year(df):
    """Plot the total number of movies with LGBTQ+ related themes per year considering mentions in plot summaries and genres"""
    # Create boolean masks for plots and genres containing LGBTQ+ terms
    lgbtq_mentions = (
        df["plot"].str.lower().str.contains("|".join(lgbtq_terms), na=False)
    )
    lgbtq_genres = df["Movie genres"].str.lower().str.contains("lgbt", na=False)

    # Combine masks to find movies with either LGBTQ+ mentions in plot or genres
    lgbtq_movies = lgbtq_mentions | lgbtq_genres

    # Group by year and count occurrences, excluding 'nan' years
    lgbtq_counts = df[lgbtq_movies].groupby("Movie release date").size()
    lgbtq_counts = lgbtq_counts[lgbtq_counts.index != "nan"]

    fig, ax = plt.subplots(figsize=(25, 7))
    ax.plot(
        lgbtq_counts.index,
        lgbtq_counts.values,
        color="purple",
        marker="o",
        markersize=8,
    )
    ax.set_title(
        "Number of Movies with LGBTQ+ Themes (Plot Mentions or Genres) Per Year"
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    ax.grid(True)
    ax.tick_params(axis="x", rotation=45)
    return fig


@save_fig_to_html
def plot_lgbtq_movies_percentage_per_period(data):
    """Plot the proportion of movies with LGBTQ+ related themes per year with respect to the total number of movies released per year"""
    df = data.copy()

    # Convert years to 5-year periods for smoothing
    df["Period"] = pd.to_numeric(df["Movie release date"], errors="coerce") // 5 * 5

    # Create boolean masks for plots and genres containing LGBTQ+ terms
    lgbtq_mentions = (
        df["plot"].str.lower().str.contains("|".join(lgbtq_terms), na=False)
    )
    lgbtq_genres = df["Movie genres"].str.lower().str.contains("lgbt", na=False)

    # Combine masks to find movies with either LGBTQ+ mentions in plot or genres
    lgbtq_movies = lgbtq_mentions | lgbtq_genres

    # Calculate percentage of LGBTQ+ movies per 5-year period
    lgbtq_counts = df[lgbtq_movies].groupby("Period").size()
    movies_per_period = df.groupby("Period").size()
    lgbtq_percentage = (lgbtq_counts / movies_per_period * 100).dropna()

    fig, ax = plt.subplots(figsize=(25, 7))
    ax.plot(
        lgbtq_percentage.index,
        lgbtq_percentage.values,
        color="purple",
        marker="o",
        markersize=8,
    )
    ax.set_title("Mean Percentage of Movies with LGBTQ+ Themes Per 5-Year Period")
    ax.set_xlabel("Year")
    ax.set_ylabel("Percentage of Movies")
    ax.grid(True)
    ax.tick_params(axis="x", rotation=45)

    return fig


def create_feature_matrix(df):
    """Create a feature matrix from the dataframe"""
    # Create gender representation difference feature (M-F) for each movie
    gender_splits = (
        df["actor_gender"]
        .str.split(", ")
        .apply(
            lambda x: pd.Series(
                [len([g for g in x if g == "M"]), len([g for g in x if g == "F"])]
            )
        )
    )
    gender_difference = gender_splits[0] - gender_splits[1]

    # Get top 5 ethnicities
    top_ethnicities = (
        df["ethnicity"].str.split(", ").explode().value_counts().iloc[1:6].index
    )

    # Create dummy variables for top 5 ethnicities only
    ethnicity_dummies = (
        df["ethnicity"]
        .str.get_dummies(sep=", ")
        .reindex(columns=top_ethnicities, fill_value=0)
    )

    df["Movie genres"] = df["Movie genres"].str.replace(", ,", ",").str.strip(", ")
    top_5_genres = (
        df["Movie genres"]
        .str.split(", ")
        .explode()
        .loc[lambda x: x != ""]
        .value_counts()
        .head(5)
        .index
    )

    # Create dummy variables for only top 5 genres
    genre_dummies = (
        df["Movie genres"]
        .str.get_dummies(sep=", ")
        .reindex(columns=top_5_genres, fill_value=0)
    )

    # Combine all features
    feature_matrix = pd.concat(
        [
            pd.DataFrame(
                {
                    "revenue": df["Movie box office revenue"],
                    "release_year": pd.to_numeric(
                        df["Movie release date"], errors="coerce"
                    ),
                    "gender_difference": gender_difference,
                }
            ),
            genre_dummies,
            ethnicity_dummies,
        ],
        axis=1,
    )
    return feature_matrix


# @save_fig_to_html
# def plot_correlation_matrix(df):
#     """Plot the correlation matrix of the feature matrix using Plotly"""
#     # Assuming create_feature_matrix is already defined
#     feature_matrix = create_feature_matrix(df)

#     # Compute correlation matrix
#     correlation_matrix = feature_matrix.corr("spearman")

#     # Reset the index to prepare for Plotly heatmap
#     correlation_matrix = correlation_matrix.reset_index().melt(id_vars="index")
#     correlation_matrix.columns = ["Feature1", "Feature2", "Correlation"]

#     # Create the heatmap using Plotly
#     fig = px.imshow(
#         feature_matrix.corr("spearman"),
#         color_continuous_scale="coolwarm",
#         title="Correlation Matrix of Movie Features",
#         labels={"color": "Correlation"},
#         zmin=-1,
#         zmax=1
#     )
#     fig.update_layout(
#         xaxis_title="Features",
#         yaxis_title="Features",
#         title_x=0.5,
#     )

#     # Print the top correlations with revenue
#     revenue_correlations = feature_matrix.corr("spearman")["revenue"].sort_values(ascending=False)
#     print("\nTop 5 positive correlations with revenue:")
#     print(revenue_correlations.head(5))
#     print("\nTop 5 negative correlations with revenue:")
#     print(revenue_correlations.tail(5))

#     return fig


def plot_ethnicity_and_genre_influence_on_revenue(df):
    """Plot the influence of ethnicity and genre on movie revenue"""
    ethnicities = {
        "European": [
            "Western European Ethnicities",
            "Northern European Ethnicities",
            "Southern European Ethnicities",
            "Eastern European Ethnicities",
        ],
        "American / Oceanian": ["American Ethnicities", "Oceanian Ethnicities"],
        "African Ethnicities": ["African Ethnicities"],
        "Indigenous Peoples": ["Indigenous Peoples"],
        "Asian Ethnicities": ["Asian Ethnicities"],
        "Middle Eastern and Arab": ["Middle Eastern and Arab Ethnicities"],
        "Latin American Ethnicities": ["Latin American Ethnicities"],
        "Jewish Communities": ["Jewish Communities"],
    }
    genre_columns = [
        "Action",
        "Adventure",
        "Comedy",
        "Drama",
        "Fantasy and Science Fiction",
        "Horror",
        "Romance",
        "Documentary",
        "Crime and Mystery",
        "Musicals and Dance",
        "War and Political",
        "Family and Children",
        "Animation",
        "Sports",
        "Experimental and Independent",
        "LGBT and Gender Issues",
        "Erotic and Adult",
    ]

    # Ethnicity Data
    avg_revenue_per_ethnicity = {}
    std_error_per_ethnicity = {}
    for group, columns in ethnicities.items():
        group_revenue = []
        for column in columns:
            if column in df.columns:
                revenue = df[df[column] != 0]["Movie box office revenue"]
                group_revenue.extend(revenue)
        if group_revenue:
            avg_revenue_per_ethnicity[group] = np.mean(group_revenue)
            std_error_per_ethnicity[group] = np.std(group_revenue) / np.sqrt(
                len(group_revenue)
            )
    sorted_ethnicities = sorted(
        avg_revenue_per_ethnicity.items(), key=lambda x: x[1], reverse=True
    )
    ethnicity_groups = [group for group, _ in sorted_ethnicities]
    avg_revenues_ethnicity = [
        avg_revenue_per_ethnicity[group] for group in ethnicity_groups
    ]
    std_errors_ethnicity = [
        std_error_per_ethnicity[group] for group in ethnicity_groups
    ]

    # Genre Data
    avg_revenue_per_genre = {}
    std_error_per_genre = {}
    for genre in genre_columns:
        if genre in df.columns:
            genre_revenue = df[df[genre] == 1]["Movie box office revenue"]
            if not genre_revenue.empty:
                avg_revenue_per_genre[genre] = genre_revenue.mean()
                std_error_per_genre[genre] = genre_revenue.std() / np.sqrt(
                    len(genre_revenue)
                )
    sorted_genres = sorted(
        avg_revenue_per_genre.items(), key=lambda x: x[1], reverse=True
    )
    genres = [genre for genre, _ in sorted_genres]
    avg_revenues_genre = [avg_revenue_per_genre[genre] for genre in genres]
    std_errors_genre = [std_error_per_genre[genre] for genre in genres]

    # Plot side by side
    fig, axes = plt.subplots(1, 2, figsize=(20, 8), sharey=True)

    # Plot Ethnicity Influence
    axes[0].bar(
        ethnicity_groups,
        avg_revenues_ethnicity,
        yerr=std_errors_ethnicity,
        capsize=5,
        color="lightcoral",
        edgecolor="black",
    )
    axes[0].set_title(
        "Average Revenue per Ethnic Group", fontsize=14, fontweight="bold"
    )
    axes[0].set_xlabel("Ethnic Group", fontsize=12)
    axes[0].set_ylabel("Average Revenue", fontsize=12)
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].set_xticks(range(len(ethnicity_groups)))
    axes[0].set_xticklabels(ethnicity_groups, ha="right", rotation_mode="anchor")

    # Plot Genre Influence
    axes[1].bar(
        genres,
        avg_revenues_genre,
        yerr=std_errors_genre,
        capsize=5,
        color="skyblue",
        edgecolor="black",
    )
    axes[1].set_title("Average Revenue per Movie Genre", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Movie Genre", fontsize=12)
    axes[1].tick_params(axis="x", rotation=45)
    axes[1].set_xticks(range(len(genres)))
    axes[1].set_xticklabels(genres, ha="right", rotation_mode="anchor")

    # Final adjustments
    plt.tight_layout()
    plt.show()


@save_fig_to_html
def plot_mean_revenue_by_f_ratio(df):
    """Plot the mean box office revenue per F ratio interval with error bars"""
    # Ensure F-ratio and revenue columns exist in the DataFrame
    # Drop missing values
    df_filtered = df[["F ratio", "Movie box office revenue"]].dropna()
    f_ratios = df_filtered["F ratio"]
    revenues = df_filtered["Movie box office revenue"]

    # Create bins with 0.05 intervals
    bins = np.arange(0, 1.05, 0.05)  # Adjust range as needed
    bin_labels = [f"{bins[i]:.2f}-{bins[i+1]:.2f}" for i in range(len(bins) - 1)]
    df_filtered["F ratio bin"] = pd.cut(
        f_ratios, bins=bins, labels=bin_labels, include_lowest=True
    )

    # Calculate mean revenue and standard error for each bin
    mean_revenue_per_bin = df_filtered.groupby("F ratio bin", observed=False)[
        "Movie box office revenue"
    ].mean()
    std_error_per_bin = df_filtered.groupby("F ratio bin", observed=False)[
        "Movie box office revenue"
    ].sem()

    # Plot the mean revenue per bin as a line plot with dots and error bars
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.errorbar(
        mean_revenue_per_bin.index.astype(str),
        mean_revenue_per_bin.values,
        yerr=std_error_per_bin.values,
        fmt="o-",
        color="#1f77b4",
        ecolor="darkred",
        capsize=6,
        linewidth=2.5,
        markersize=8,
        label="Mean Revenue with Error Bars",
    )

    # Enhancing aesthetics
    ax.set_xlabel(
        "F ratio Interval (0.05)", fontsize=14, labelpad=10, fontweight="bold"
    )
    ax.set_ylabel(
        "Mean Box Office Revenue", fontsize=14, labelpad=10, fontweight="bold"
    )
    ax.set_title(
        "Impact of Female Representation on Movie Revenue",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="both", labelsize=12)
    ax.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.8, color="gray")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=12, loc="upper left", frameon=False)
    plt.tight_layout()
    return fig


@save_fig_to_html
def plot_avg_ethnic_score_evolution(df):
    """Plot the average ethnic score per period"""

    # Calculate the average ethnic score per period
    average_ethnic_score_per_period = df.groupby("period")["ethnic_score"].mean()

    # Plot the average ethnic score per period
    fig, ax = plt.subplots(figsize=(12, 6))
    average_ethnic_score_per_period.plot(kind="bar", ax=ax)
    ax.set_title("Average Ethnic Score per Period")
    ax.set_xlabel("Period")
    ax.set_ylabel("Average Ethnic Score")
    return fig


@save_fig_to_html
def plot_female_ratio_distribution(df):
    """
    Creates a bar plot showing the distribution of female actor ratios over time periods.

    Parameters:
    df (pandas.DataFrame): DataFrame containing 'Movie release date' and 'F ratio' columns

    Returns:
    None (displays plot and prints percentages)
    """
    df["period"] = pd.to_datetime(df["Movie release date"], format="%Y").dt.year.apply(
        lambda x: f"{(x//5)*5}-{(x//5)*5+4}"
    )

    period_f_ratios = df.groupby("period")["F ratio"].mean() * 100

    # Select only the periods we're interested in
    periods_of_interest = [
        "1985-1989",
        "1990-1994",
        "1995-1999",
        "2000-2004",
        "2005-2009",
        "2010-2014",
    ]
    f_ratios = period_f_ratios[periods_of_interest]

    # Plot with Seaborn for better aesthetics
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=f_ratios.values,
        y=f_ratios.index,
        hue=f_ratios.index,  # Set hue to the y variable
        palette="coolwarm",
        dodge=False,
        legend=False,
        ax=ax,
    )

    # Add plot details
    ax.set_title("Average Percentage of Female Actors by Period", fontsize=16)
    ax.set_xlabel("Percentage of Female Actors (%)", fontsize=12)
    ax.set_ylabel("Period", fontsize=12)
    for index, value in enumerate(f_ratios.values):
        ax.text(value + 0.5, index, f"{value:.1f}%", va="center", fontsize=10)

    plt.tight_layout()
    return fig


@save_fig_to_html
def plot_female_ratio_heatmap(df):
    """
    Creates a heatmap showing the percentage of female actors across different periods and genres.

    Parameters:
    df (pandas.DataFrame): DataFrame containing 'Movie release date', 'F ratio' and genre columns

    Returns:
    None (displays heatmap and prints averages)
    """
    genres = df.columns[
        df.columns.get_loc("Action") : df.columns.get_loc("Erotic and Adult") + 1
    ].tolist()

    # Define periods of interest
    periods_of_interest = [
        "1985-1989",
        "1990-1994",
        "1995-1999",
        "2000-2004",
        "2005-2009",
        "2010-2014",
    ]

    heatmap_data = []

    # For each period and genre, we calculate average F ratio for movies of that genre
    for period in periods_of_interest:
        period_data = df[df["period"] == period]
        row_data = []
        for genre in genres:
            genre_movies = period_data[period_data[genre] == 1]
            if len(genre_movies) > 0:
                f_ratio = genre_movies["F ratio"].mean() * 100
                row_data.append(f_ratio)
            else:
                row_data.append(0)
        heatmap_data.append(row_data)

    heatmap_df = pd.DataFrame(heatmap_data, index=periods_of_interest, columns=genres)

    fig, ax = plt.subplots(figsize=(15, 8))
    sns.heatmap(
        heatmap_df,
        annot=True,
        fmt=".1f",
        cmap="RdYlBu_r",
        center=30,
        vmin=0,
        vmax=60,
        ax=ax,
    )

    ax.set_title("Percentage of Female Actors by Period and Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Period")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


@save_fig_to_html
def plot_male_ratio_heatmap(df):
    """
    Creates a heatmap showing the percentage of male actors across different periods and genres.

    Parameters:
    df (pandas.DataFrame): DataFrame containing 'Movie release date', 'F ratio' and genre columns

    Returns:
    None (displays heatmap and prints averages)
    """
    genres = df.columns[
        df.columns.get_loc("Action") : df.columns.get_loc("Erotic and Adult") + 1
    ].tolist()

    # Define periods of interest
    periods_of_interest = [
        "1985-1989",
        "1990-1994",
        "1995-1999",
        "2000-2004",
        "2005-2009",
        "2010-2014",
    ]

    heatmap_data = []

    # For each period and genre, calculate average male proportion (1 - F ratio) for movies of that genre
    for period in periods_of_interest:
        period_data = df[df["period"] == period]
        row_data = []
        for genre in genres:
            genre_movies = period_data[period_data[genre] == 1]
            if len(genre_movies) > 0:
                m_ratio = (1 - genre_movies["F ratio"]).mean() * 100
                row_data.append(m_ratio)
            else:
                row_data.append(0)
        heatmap_data.append(row_data)

    heatmap_df = pd.DataFrame(heatmap_data, index=periods_of_interest, columns=genres)

    fig, ax = plt.subplots(figsize=(15, 8))
    sns.heatmap(
        heatmap_df,
        annot=True,
        fmt=".1f",
        cmap="RdYlBu",
        center=50,
        vmin=40,
        vmax=100,
        ax=ax,
    )
    ax.set_title("Percentage of Male Actors by Period and Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Period")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


@save_fig_to_html
def plot_ethnic_score_heatmap(df):
    """
    Creates a heatmap showing the average ethnic score across different periods and genres.

    Parameters:
    df (pandas.DataFrame): DataFrame containing 'Movie release date', 'ethnic_score' and genre columns

    Returns:
    None (displays heatmap and prints averages)
    """
    genres = df.columns[
        df.columns.get_loc("Action") : df.columns.get_loc("Erotic and Adult") + 1
    ].tolist()

    # Define periods of interest
    periods_of_interest = [
        "1985-1989",
        "1990-1994",
        "1995-1999",
        "2000-2004",
        "2005-2009",
        "2010-2014",
    ]

    heatmap_data = []

    # For each period and genre, calculate average ethnic_score for movies of that genre
    for period in periods_of_interest:
        period_data = df[df["period"] == period]
        row_data = []
        for genre in genres:
            genre_movies = period_data[period_data[genre] == 1]
            if len(genre_movies) > 0:
                avg_score = genre_movies["ethnic_score"].mean()
                row_data.append(avg_score)
            else:
                row_data.append(0)
        heatmap_data.append(row_data)

    heatmap_df = pd.DataFrame(heatmap_data, index=periods_of_interest, columns=genres)

    fig, ax = plt.subplots(figsize=(15, 8))
    sns.heatmap(
        heatmap_df, annot=True, fmt=".1f", cmap="YlOrRd", center=None, vmin=0, ax=ax
    )

    ax.set_title("Average Ethnic Score by Period and Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Period")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig
