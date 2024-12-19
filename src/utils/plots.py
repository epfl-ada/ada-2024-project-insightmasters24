from functools import wraps

import matplotlib.pyplot as plt
import pandas as pd
import plotly.io as pio
import plotly.tools as tls
import seaborn as sns


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
lgbtq_terms = ['gay', 'lesbian', 'homosexual', 'homosexuality', 'bisexual', 'transgender', 'queer', 'trans', 'transsexual', 'transvestite', 'transvestism']


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
    plt.figure(figsize=(12, 6))
    proportions.plot(kind="area", stacked=True)
    plt.title("Gender Proportions of Actors Over Time")
    plt.xlabel("Year")
    plt.ylabel("Proportion")
    plt.legend(title="Gender", loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

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
    plt.figure(figsize=(12, 6))
    proportions.plot(kind="area", stacked=True)
    plt.title("Age Distribution of Actors Over Time")
    plt.xlabel("Year")
    plt.ylabel("Proportion")
    plt.legend(title="Age Groups", bbox_to_anchor=(1.05, 1))
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

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
    plt.show()

def plot_top_languages(df):
    """Plot the top 20 movie released languages"""
    language_counts = (
        df["Movie languages"].str.split(", ").explode().value_counts()
    )
    # remove the languages with less than 2 character
    language_counts = language_counts[language_counts.index.str.len() > 1]
    plt.figure(figsize=(15, 6))
    language_counts[:20].plot(kind="bar", title="Top 20 languages", ylabel="Count", alpha=0.75)
    plt.show()

def plot_top_genres(df):
    """Plot the top 20 movie genres of our entire dataset"""
    genre_counts = (
        df["Movie genres"].str.split(", ").explode().value_counts()
    )

    plt.figure(figsize=(15, 6))
    genre_counts[:20].plot(
        kind="bar", title="Top 20 genres", ylabel="Count", xlabel="Movie Genre", alpha=0.75
    )
    plt.show()

def plot_movies_by_year(df):
    """Plot the number of movies in the last 50 years"""
    year_counts = df["Movie release date"].value_counts()
    # Drop non numeric years
    year_counts = year_counts[year_counts.index.str.isnumeric()]
    year_counts.sort_index(ascending=False, inplace=True)
    plt.figure(figsize=(20, 6))
    year_counts[:50].plot(
        kind="bar",
        title="Number of movies in last 50 years", 
        ylabel="Count",
        xlabel="Year",
        alpha=0.75,
    )
    plt.show()


@save_fig_to_html
def plot_gender_distribution(df):
    """Plot the total distribution of female and male actors"""
    # Extract the 'Actor gender' column, split it by commas, and count the occurrences of 'F' and 'M'
    gender_counts = df["actor_gender"].str.split(", ").explode().value_counts()

    # Create the Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 6))
    gender_counts[["F", "M"]].plot(kind="bar", color=["pink", "blue"], ax=ax)
    ax.set_title("Number of Female vs Male Actors")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Number of Actors")
    ax.set_xticks(range(len(gender_counts[["F", "M"]])))
    ax.set_xticklabels(["F", "M"], rotation=0)

    return fig


@save_fig_to_html
def plot_gender_distribution_pie(df):
    """Plot the total distribution of female and male actors as a pie chart"""
    # Extract the 'Actor gender' column, split it by commas, and count the occurrences of 'F' and 'M'
    gender_counts = df["actor_gender"].str.split(", ").explode().value_counts()

    plt.figure(figsize=(8, 8))
    gender_counts[["F", "M"]].plot(
        kind="pie",
        colors=["#FF6B6B", "#4ECDC4"],  # Coral red and Turquoise
        autopct="%1.1f%%",  # Show percentages with 1 decimal
        labels=["Female", "Male"],
    )
    plt.title("Distribution of Female vs Male Actors")
    plt.ylabel("")  # Remove y-label as it's not needed for pie charts
    plt.show()


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
            pd.to_numeric(df["Movie release date"], errors="coerce")
            == year
        ]

        # Count the genres for movies in this year
        genre_counts = (
            movies_in_year["Movie genres"].str.split(", ").explode().value_counts()
        )

        # Get the top 3 genres and their counts
        top_genres = genre_counts.head(3)

        # Add the data to the DataFrame
        top_genres_per_year = pd.concat(
            [top_genres_per_year, pd.DataFrame({year: top_genres})], axis=1
        )

    # Transpose and clean up the DataFrame for plotting
    top_genres_per_year = top_genres_per_year.T.fillna(0)

    # Plotting the top 3 genres per year for the last 10 years
    plt.figure(figsize=(15, 8))
    top_genres_per_year.plot(kind="bar", stacked=True, figsize=(15, 8), width=0.8)
    plt.title("Top 3 Movie Genres Per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Movies")
    plt.xticks(rotation=45)
    plt.legend(title="Genres", bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()

def plot_mean_revenue_per_year(df):
    """Plot the mean movie box office revenue per year"""
    mean_revenue_per_year = df.groupby("Movie release date")[
        "Movie box office revenue"
    ].mean()
    mean_revenue_per_year = mean_revenue_per_year.dropna()
    mean_revenue_per_year = mean_revenue_per_year[mean_revenue_per_year.index != "nan"]

    plt.figure(figsize=(25, 7))
    plt.plot(
        mean_revenue_per_year.index,
        mean_revenue_per_year.values,
        color="b",
        marker=".",
        linestyle="solid",
        markersize=12,
        markerfacecolor="white",
    )

    plt.title("Mean Movie Box Office Revenue Per Year")
    plt.xlabel("Year")
    plt.ylabel("Mean Revenue")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

def plot_ethnicity_proportions(df):
    """Plot the ethnicity distribtution of actors in our dataset"""
    # Plot the ethnicities proportions
    ethnicity_counts = (
        df["ethnicity"].str.split(", ").explode().value_counts()
    )

    # Count the non nan values and get top 8
    ethnicity_counts = ethnicity_counts[ethnicity_counts.index != "nan"]
    top_10_ethnicities = ethnicity_counts[1:9]
    others = pd.Series({'Others': ethnicity_counts[8:].sum()})
    ethnicity_counts_final = pd.concat([top_10_ethnicities, others])

    ethnicity_counts_final.plot(kind="pie", autopct='%1.1f%%')
    plt.title("Ethnicity Proportions (Top 8 + Others)")
    plt.show()

def plot_lgbtq_movies_per_year(df):
    """Plot the total number of movies with LGBTQ+ related themes per year considering mentions in plot summaries and genres"""
    # Create boolean masks for plots and genres containing LGBTQ+ terms
    lgbtq_mentions = df['plot'].str.lower().str.contains('|'.join(lgbtq_terms), na=False)
    lgbtq_genres = df['Movie genres'].str.lower().str.contains('lgbt', na=False)
    
    # Combine masks to find movies with either LGBTQ+ mentions in plot or genres
    lgbtq_movies = lgbtq_mentions | lgbtq_genres

    # Group by year and count occurrences, excluding 'nan' years
    lgbtq_counts = df[lgbtq_movies].groupby('Movie release date').size()
    lgbtq_counts = lgbtq_counts[lgbtq_counts.index != 'nan']

    plt.figure(figsize=(25, 7))
    plt.plot(lgbtq_counts.index, lgbtq_counts.values, color='purple', marker='o', markersize=8)
    plt.title('Number of Movies with LGBTQ+ Themes (Plot Mentions or Genres) Per Year')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

def plot_lgbtq_movies_percentage_per_period(df):
    """Plot the proportion of movies with LGBTQ+ related themes per year with respect to the total number of movies released per year"""

    # Convert years to 5-year periods for smoothing
    df['Period'] = pd.to_numeric(df['Movie release date'], errors='coerce') // 5 * 5

    # Create boolean masks for plots and genres containing LGBTQ+ terms
    lgbtq_mentions = df['plot'].str.lower().str.contains('|'.join(lgbtq_terms), na=False)
    lgbtq_genres = df['Movie genres'].str.lower().str.contains('lgbt', na=False)
    
    # Combine masks to find movies with either LGBTQ+ mentions in plot or genres
    lgbtq_movies = lgbtq_mentions | lgbtq_genres

    # Calculate percentage of LGBTQ+ movies per 5-year period
    lgbtq_counts = df[lgbtq_movies].groupby('Period').size()
    movies_per_period = df.groupby('Period').size()
    lgbtq_percentage = (lgbtq_counts / movies_per_period * 100).dropna()

    plt.figure(figsize=(25, 7))
    plt.plot(lgbtq_percentage.index, lgbtq_percentage.values, color='purple', marker='o', markersize=8)
    plt.title('Mean Percentage of Movies with LGBTQ+ Themes Per 5-Year Period')
    plt.xlabel('Year')
    plt.ylabel('Percentage of Movies')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

def create_feature_matrix(df):
    """Create a feature matrix from the dataframe"""
    # Create gender representation difference feature (M-F) for each movie
    gender_splits = df['actor_gender'].str.split(', ').apply(lambda x: 
        pd.Series([
            len([g for g in x if g == 'M']),
            len([g for g in x if g == 'F'])
        ])
    )
    gender_difference = gender_splits[0] - gender_splits[1]
    
    # Get top 5 ethnicities
    top_ethnicities = (
        df['ethnicity'].str.split(', ')
        .explode()
        .value_counts()
        .iloc[1:6]
        .index
    )
    
    # Create dummy variables for top 5 ethnicities only
    ethnicity_dummies = (
        df['ethnicity'].str.get_dummies(sep=', ')
        .reindex(columns=top_ethnicities, fill_value=0)
    )
    
    # Create dummy variables for genres
    top_5_genres = (
        df['Movie genres'].str.split(", ")
        .explode()
        .value_counts()
        .head(5)
        .index
    )
    
    # Create dummy variables for only top 5 genres
    genre_dummies = (
        df['Movie genres'].str.get_dummies(sep=', ')
        .reindex(columns=top_5_genres, fill_value=0)
    )
        
    # Combine all features
    feature_matrix = pd.concat([
        pd.DataFrame({
            'revenue': df['Movie box office revenue'],
            'release_year': pd.to_numeric(df['Movie release date'], errors='coerce'),
            'gender_difference': gender_difference
        }),
        genre_dummies,
        ethnicity_dummies
    ], axis=1)
    return feature_matrix

def plot_correlation_matrix(df):
    """Plot the correlation matrix of the feature matrix"""
    feature_matrix = create_feature_matrix(df)

    # Compute and plot correlation matrix
    plt.figure(figsize=(20, 16))
    correlation_matrix = feature_matrix.corr()

    # Plot heatmap and showing the correlation coefficients
    sns.heatmap(correlation_matrix, 
                cmap='coolwarm', 
                center=0,
                annot=True,  
                fmt='.2f',
                square=True)

    plt.title('Correlation Matrix of Movie Features')
    plt.tight_layout()
    plt.show()

    # Printing the top correlations with revenue
    revenue_correlations = correlation_matrix['revenue'].sort_values(ascending=False)
    print("\nTop 5 positive correlations with revenue:")
    print(revenue_correlations.head(5))
    print("\nTop 5 negative correlations with revenue:")
    print(revenue_correlations.tail(5))