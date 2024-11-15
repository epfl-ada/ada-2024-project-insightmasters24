# Project Proposal: The Evolution of Gender and Ethnic Representation in Cinema

## Abstract

The evolution of gender, ethnic, and other apparent physical features representation in cinema serves as a lens reflecting societal values and cultural shifts over decades. This project seeks to explore these dynamics by analyzing the physical characteristics of main actors—gender, ethnicity, sexual orientation, height, and age—across decades and genres, using the CMU movie summary corpus as our main data source. We find this project idea very compelling because it allows us to investigate how specific archetypes emerge, evolve, and influence genre conventions and movie revenues, shedding light on diversity’s role in shaping audience engagement and the movie industry in general. By examining shifts in societal norms, we aim to contribute to the understanding of cinema’s role in mirroring and potentially driving cultural changes, thus offering valuable insights into the power of representation in media.

## Research Questions

- What is the evolution of the main actors' physical characteristics (gender, ethnicity, sexual orientation, height, and age) throughout the years?
- How do archetype distributions vary across genres (which kinds of actors tend to be preferred for specific movie genres) and correlate with movie revenues? How does this evolve with time?
- If new archetype tendencies are emerging, how do they reflect societal changes? How do these archetypes correlate with movie revenue?

## Additional Datasets

- **Freebase to Wikidata Mapping Dataset**:  
  The CMU dataset contains Freebase IDs, but Freebase is no longer accessible through a website or API. We used an additional dataset that maps these IDs to corresponding Wikidata IDs and labels. [Dataset on Kaggle](https://www.kaggle.com/datasets/latebloomer/freebase-wikidata-mapping/data)

- **Movie Revenue Dataset**:  
  To enhance our movie dataset, we integrated box office revenue data sourced from Wikidata, using unique movie identifiers for direct access. Initially, our dataset included revenue data for 8168 movies; after augmentation, this increased to 9062 movies, enabling us to have more data for our prediction of the movie revenue.

- **TMDB Movie Dataset**:  
  To fill missing values for the release date and additional revenue data of the movies, we used the TMDB movie dataset. [Dataset on Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)

## Methods

### Data Preprocessing

#### Data Loading and Initial Processing

Data is loaded from TSV files into Pandas DataFrames. For character data, unnecessary columns are removed, and Freebase IDs for characters, actors, and movies are mapped to Wikidata IDs. JSON-encoded columns in movie data (e.g., languages, countries, genres) are parsed into lists, and release dates are simplified to the year.

#### Data Merging and Aggregation

Movie and character data are merged on "wikipedia_movie_id," with character attributes consolidated into comma-separated lists by movie. Plot summaries are also added by merging on "wikipedia_movie_id."

#### Handling Data

For movies with missing revenue values, data is retrieved from Wikidata using unique Wikidata IDs obtained from our updated dataset. To handle rows with NaN values in revenue, each movie’s information is requested via its specific Wikidata ID. Given the substantial dataset size of approximately 64,000 samples, this process can be time-intensive. Therefore, we implemented parallel processing, allowing multiple requests to be handled simultaneously. This parallelization drastically reduced runtime from over 4 hours to just 20 minutes, enabling faster data completion.

Notice that we did not remove remaining NaN values of movie box office revenue at this stage because we still wanted to observe the other parameters that were given for exploratory data distribution purposes. We decided not to clean the columns that we are not using at this stage of the project, and we will manage missing values for those columns if required in the future. We also decided not to drop these columns in case we need them later. We used the Freebase-to-Wikidata Mapping Dataset to map Freebase ethnicity IDs to their corresponding Wikidata IDs and retrieve the labels.

We also used the TMDB movie dataset to fill missing values for the release date and additional revenue data of the movies. We merge the datasets on the title column.

We cleaned the actor age data by removing actors that had a negative age (indicating they were born after the movie release date) and actors with unrealistic ages (over 100 years old at the time of movie release) to ensure data quality.

### Exploratory Data Analysis

#### Preliminary Data Distribution Visualization

We decided to plot the number of movies released each year. We noticed an outlier data point with a movie release date of 1010, which was a typo in the initial dataset that we corrected.  
We observed the global distribution of movie revenue from 1920 to 2015 and the mean movie revenue over time. We noticed significant revenue differences between distinct time periods, stressing the need for standardizing the revenue per year for more consistent comparison across different periods.

Furthermore, the annual and global distributions of movie genres revealed temporal trends. We also observed actor gender distribution across all movies and across years, providing initial insights into how gender representation in movies has changed over time.

The distribution of age among actors by gender over time highlighted trends regarding age group distribution among female and male actors, reflecting the roles and representation of male and female characters in cinema.  
The distribution of movie release languages was mainly dominated by English, so we decided to focus our study primarily on these movies to avoid a significant data imbalance.

#### Identifying Features of Interest for Our Models in Milestone 3

To capture the parameters most correlated with revenue, we plotted the correlation matrix with the most prominent movie genres, actor ethnicities, and genders. We created dummy variables for each of these classes, which will also be useful in training our models. More statistical analysis for causal inference is expected for Project M3.

### Models and Answers to Scientific Questions (M3)

#### Revenue Prediction Model

We plan to build a model to predict movie revenue using character archetypes, actor attributes (e.g., gender, ethnicity, age, height), and movie-specific features like genre, release year, and archetype distribution. We’ll test linear regression, random forest regression, and neural networks, adjusting revenue for inflation to account for changing baselines across decades. Model accuracy will be evaluated using metrics such as Mean Absolute Error (MAE) or Root Mean Square Error (RMSE) to assess prediction effectiveness.

#### Genre-Archetype Association Model

We will model the relationship between movie genres and character archetypes to identify genre-specific archetype preferences over time. Using actor attributes, genres, and time periods as inputs, we’ll apply clustering (e.g., k-means, hierarchical) to group movies by genre-specific archetype patterns, or association rule learning to uncover these patterns. The output will be a distribution of archetypes per genre over time, that could show shifts in character type prevalence across genres.

#### Temporal Representation Shift Analysis

The Temporal Representation Shift Analysis model will focus on capturing changes in the representation of gender, ethnicity, and other attributes over time. We will apply time series analysis techniques to capture trends in archetype distribution over the years, using methods like linear or polynomial regression to quantify representation shifts. We will visualize these results to illustrate temporal trends and for interpretation.

## Proposed Timeline

**Week by week until the last milestone:**

- **15.11.2023**: Step 1 and 2
- **29.11.2023**: Homework 2
- **06.12.2023**: Step 3.a, Step 3.b
- **13.12.2023**: Step 3.b, Step 3.c
- **20.12.2023**: Project review and Data Story

## Project Structure

The directory structure of new project looks like this:

```
├── datasets                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data loading and preprocessing
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing our observations
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```
