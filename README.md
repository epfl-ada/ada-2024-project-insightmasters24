# Project Proposal: The Evolution of Gender and Ethnic Representation in Cinema


[Visit our data story website](https://epfl-ada.github.io/ada-2024-project-insightmasters24/)


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

#### Identifying Features of Interest for Our Models 

To capture the parameters most correlated with revenue, we plotted the correlation matrix with the most prominent movie genres, actor ethnicities, and genders. We created dummy variables for each of these classes, which will also be useful in training our models.

### Models and Answers to Scientific Questions (M3)

#### Revenue Prediction Model

We analyzed the relationship between movie revenue and features such as gender representation, ethnic diversity, movie genres, and character archetypes by running Ridge regressions. The analysis focused on statistically significant features with a positive effect on revenue at the 5% significance level. To address potential non-linearities caused by time, we segmented the data into 5-year periods, capturing how these features' influence evolved over time.

Key insights revealed that certain genres, like science fiction, adventure, and romance, have maintained long-term popularity, while themes like politics and war gained traction in the 1990s, reflecting societal trends like the end of the Cold War. Similarly, the late 20th century saw growing success for movies featuring LGBTQ+ themes, coinciding with cultural advocacy for inclusivity.

Ethnic representation also played a crucial role. Movies with higher "ethnic scores" (a measure of diversity) consistently performed better at the box office since 1995, highlighting the audience's growing demand for diverse storytelling. Representation trends for specific groups, like Jewish and African actors, reflect evolving societal openness to their portrayal, while European and North American ethnicities consistently dominated the screen. Additionally, the period from 1990–1999 saw notable success for romance films, where female representation and younger actors significantly influenced revenue.

These findings underline the dynamic interplay between cultural shifts and audience preferences, revealing the evolving nature of societal values reflected through cinema.


#### Temporal Representation Shift Analysis

Our analysis examined the evolution of gender, age, ethnic, and LGBTQ+ representation in cinema over time, highlighting how societal norms and cultural expectations have shifted.

- **Gender Representation**: Despite assumptions of progress, the proportion of female actresses in movie casts has remained relatively stable over the decades. We found that both too few and too many female actors negatively impacted revenue, reflecting biases that limit women's roles to secondary or stereotypical characters.

- **Age Distribution**: Actors in their 20s and 30s dominated screens across decades, with limited opportunities for older performers. However, by 2010, a more balanced age distribution emerged, indicating growing societal acceptance of older characters in cinema.

- **LGBTQ+ Representation**: LGBTQ+ themes experienced minimal visibility until the 1990s, when a sharp upward trend began, reflecting increased societal acceptance. By analyzing the percentage of movies featuring LGBTQ+ themes over time, we found steady growth, signaling the industry's move toward greater inclusivity.

- **Ethnic Representation**: The "average ethnic score," measuring cast diversity, has steadily climbed since the early 20th century, with a notable increase during the 1960s. While progress is clear, disparities persist, as some ethnic groups remain underrepresented or confined to specific genres.

These findings illustrate the gradual but uneven progress in representation across key dimensions, offering insights into how cinema reflects and drives societal change.


## Contributions

- *Omar Badri*: Plots and Notebook
- *Souhail Ed-Dlimi*: Data Story and Website
- *Amene Gafsi*: Plots and Notebook
- *Ahmed Reda Seghrouchni*: Data Story
- *Pierre Véron*: Plots and Website

## Project Structure

The directory structure of the project looks like this:

```
├── datasets                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data loading and preprocessing
│   ├── models                          <- Models directory
│   └── utils                           <- Utility directory
│
├── tests                       <- Model tests
│
├── results.ipynb               <- A well-structured notebook showing our observations
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
├── docs                        <- Website files
└── README.md
```
