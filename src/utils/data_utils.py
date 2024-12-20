import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import requests

ethnicity_mapping = {
    "African Ethnicities": [
        "ethnicity_African Americans", "ethnicity_African people", "ethnicity_Afro-Asians",
        "ethnicity_Afro-Cuban", "ethnicity_Berber", "ethnicity_Nigerian Americans",
        "ethnicity_Sierra Leone Creole people", "ethnicity_Somalis", "ethnicity_Sudanese Arabs",
        "ethnicity_Wolof people", "ethnicity_Xhosa people", "ethnicity_Yoruba people"
    ],
    "Indigenous Peoples": [
        "ethnicity_Apache", "ethnicity_Cherokee", "ethnicity_Choctaw", "ethnicity_Cree",
        "ethnicity_Haudenosaunee", "ethnicity_Lumbee", "ethnicity_Māori", "ethnicity_Mohawk people",
        "ethnicity_Native Hawaiians", "ethnicity_Ojibwe", "ethnicity_Omaha people",
        "ethnicity_Sámi peoples", "ethnicity_Sioux", "ethnicity_Inuit", "ethnicity_Inupiat people",
        "ethnicity_Aymara", "ethnicity_Blackfoot Confederacy"
    ],
    "Western European Ethnicities": [
        "ethnicity_Anglo-Celtic Australians", "ethnicity_Anglo-Irish people", "ethnicity_Belgians",
        "ethnicity_British Americans", "ethnicity_British Asian", "ethnicity_British Chinese",
        "ethnicity_British Indian", "ethnicity_British Jews", "ethnicity_British Pakistanis",
        "ethnicity_Dutch", "ethnicity_Dutch Americans", "ethnicity_Dutch Australian",
        "ethnicity_Dutch Canadians", "ethnicity_English Americans", "ethnicity_English Australian",
        "ethnicity_English Canadians", "ethnicity_English people", "ethnicity_French",
        "ethnicity_French Americans", "ethnicity_French Canadians", "ethnicity_Germans",
        "ethnicity_German Americans", "ethnicity_German Canadians"
    ],
    "Northern European Ethnicities": [
        "ethnicity_Danes", "ethnicity_Danish Americans", "ethnicity_Danish Canadians",
        "ethnicity_Finns", "ethnicity_Finnish Americans", "ethnicity_Icelanders",
        "ethnicity_Norwegian Americans", "ethnicity_Norwegians", "ethnicity_Swedes",
        "ethnicity_Swedish Americans", "ethnicity_Swedish Canadians"
    ],
    "Southern European Ethnicities": [
        "ethnicity_Albanians", "ethnicity_Albanian American", "ethnicity_Armenians",
        "ethnicity_Armenian American", "ethnicity_Corsicans", "ethnicity_Greek Americans",
        "ethnicity_Greek Canadians", "ethnicity_Greeks in South Africa", "ethnicity_Italians",
        "ethnicity_Italian Americans", "ethnicity_Italian Australian", "ethnicity_Italian Brazilians",
        "ethnicity_Italian Canadians", "ethnicity_Maltese", "ethnicity_Portuguese",
        "ethnicity_Portuguese Americans", "ethnicity_Sicilian Americans", "ethnicity_Spaniards",
        "ethnicity_Spanish Americans"
    ],
    "Eastern European Ethnicities": [
        "ethnicity_Baltic Russians", "ethnicity_Belarusians", "ethnicity_Bosnians",
        "ethnicity_Bulgarians", "ethnicity_Bulgarian Canadians", "ethnicity_Croats",
        "ethnicity_Croatian Americans", "ethnicity_Croatian Australians", "ethnicity_Croatian Canadians",
        "ethnicity_Czechs", "ethnicity_Czech Americans", "ethnicity_Hungarians",
        "ethnicity_Hungarian Americans", "ethnicity_Latvians", "ethnicity_Latvian American",
        "ethnicity_Lithuanian Jews", "ethnicity_Lithuanian American", "ethnicity_Poles",
        "ethnicity_Polish Americans", "ethnicity_Polish Australians", "ethnicity_Polish Canadians",
        "ethnicity_Romani people", "ethnicity_Romanian Americans", "ethnicity_Romanichal",
        "ethnicity_Russians", "ethnicity_Russian Americans", "ethnicity_Serbs in the United Kingdom",
        "ethnicity_Serbs of Croatia", "ethnicity_Serbs", "ethnicity_Serbian Americans",
        "ethnicity_Serbian Australians", "ethnicity_Serbian Canadians", "ethnicity_Slovaks",
        "ethnicity_Slovak Americans", "ethnicity_Slovenes", "ethnicity_Slovene Americans",
        "ethnicity_Tatars", "ethnicity_Ukrainians", "ethnicity_Ukrainian Americans",
        "ethnicity_Ukrainian Canadians"
    ],
    "Asian Ethnicities": [
        "ethnicity_Afro-Asians", "ethnicity_Assyrian people", "ethnicity_Bengali", "ethnicity_Bhutia",
        "ethnicity_Chinese Americans", "ethnicity_Chinese Canadians", "ethnicity_Chinese Filipino",
        "ethnicity_Chinese Jamaicans", "ethnicity_Chinese Singaporeans", "ethnicity_Filipino Americans",
        "ethnicity_Filipino Australians", "ethnicity_Filipino mestizo", "ethnicity_Filipino people",
        "ethnicity_Gujarati people", "ethnicity_Hazaras", "ethnicity_Hmong American", "ethnicity_Indian",
        "ethnicity_Indian Americans", "ethnicity_Indian diaspora in France", "ethnicity_Indo-Canadians",
        "ethnicity_Indonesian Americans", "ethnicity_Iranian peoples", "ethnicity_Japanese Brazilians",
        "ethnicity_Japanese people", "ethnicity_Kashmiri Pandit", "ethnicity_Korean American",
        "ethnicity_Koreans", "ethnicity_Malaysian Chinese", "ethnicity_Manchu", "ethnicity_Taiwanese",
        "ethnicity_Taiwanese Americans", "ethnicity_Tamil", "ethnicity_Telugu people",
        "ethnicity_Thai Americans", "ethnicity_Tibetan people"
    ],
    "Middle Eastern and Arab Ethnicities": [
        "ethnicity_Arab Americans", "ethnicity_Arabs in Bulgaria", "ethnicity_Iranian Americans",
        "ethnicity_Iranians in the United Kingdom", "ethnicity_Iraqis", "ethnicity_Iraqi Americans",
        "ethnicity_Lebanese", "ethnicity_Lebanese Americans", "ethnicity_Moroccans",
        "ethnicity_Palestinian Americans", "ethnicity_Sudanese Arabs"
    ],
    "Latin American Ethnicities": [
        "ethnicity_Afro-Cuban", "ethnicity_Argentines", "ethnicity_Brazilian Americans",
        "ethnicity_Brazilians", "ethnicity_Chilean American", "ethnicity_Chileans",
        "ethnicity_Colombian Americans", "ethnicity_Colombians", "ethnicity_Cuban Americans",
        "ethnicity_Cubans", "ethnicity_Dominican Americans", "ethnicity_Ecuadorian Americans",
        "ethnicity_Honduran Americans", "ethnicity_Hondurans", "ethnicity_Latino",
        "ethnicity_Mexican Americans", "ethnicity_Mexicans", "ethnicity_Panamanian Americans",
        "ethnicity_Puerto Ricans", "ethnicity_Salvadoran Americans", "ethnicity_Uruguayans",
        "ethnicity_Venezuelan Americans", "ethnicity_Venezuelans"
    ],
    "Jewish Communities": [
        "ethnicity_American Jews", "ethnicity_Ashkenazi Jews", "ethnicity_British Jews",
        "ethnicity_Sephardi Jews", "ethnicity_Israelis", "ethnicity_Israeli Americans",
        "ethnicity_Jewish people", "ethnicity_Lithuanian Jews", "ethnicity_History of the Jews in Morocco"
    ],
    "American Ethnicities": [
        "ethnicity_Acadians", "ethnicity_African Americans", "ethnicity_American Jews",
        "ethnicity_Anglo-Celtic Australians", "ethnicity_Apache", "ethnicity_Asian Americans",
        "ethnicity_Australian Americans", "ethnicity_Bahamian Americans", "ethnicity_Brazilian Americans",
        "ethnicity_British Americans", "ethnicity_Cajun", "ethnicity_Cherokee", "ethnicity_Chilean American",
        "ethnicity_Chinese Americans", "ethnicity_Colombian Americans", "ethnicity_Cuban Americans",
        "ethnicity_Danish Americans", "ethnicity_Dominican Americans", "ethnicity_Ecuadorian Americans",
        "ethnicity_English Americans", "ethnicity_Filipino Americans", "ethnicity_First Nations",
        "ethnicity_French Americans", "ethnicity_German Americans", "ethnicity_Greek Americans",
        "ethnicity_Haitian Americans", "ethnicity_Hmong American", "ethnicity_Indian Americans",
        "ethnicity_Irish Americans", "ethnicity_Italian Americans", "ethnicity_Korean American",
        "ethnicity_Mexican Americans", "ethnicity_Native Hawaiians"
    ],
    "Oceanian Ethnicities": [
        "ethnicity_Australian Americans", "ethnicity_Australians", "ethnicity_Filipino Australians",
        "ethnicity_Irish Australian", "ethnicity_Italian Australian", "ethnicity_Māori"
    ]
}

genre_mapping = {
    "Action": [
        "Movie genres_Action", "Movie genres_Action Comedy", "Movie genres_Action Thrillers",
        "Movie genres_Action/Adventure", "Movie genres_Biker Film", "Movie genres_Buddy cop",
        "Movie genres_Chase Movie", "Movie genres_Disaster", "Movie genres_Martial Arts Film",
        "Movie genres_Ninja movie", "Movie genres_Superhero", "Movie genres_Superhero movie",
        "Movie genres_Swashbuckler films", "Movie genres_Sword and sorcery", "Movie genres_Spy"
    ],
    "Adventure": [
        "Movie genres_Action/Adventure", "Movie genres_Adventure", "Movie genres_Adventure Comedy",
        "Movie genres_Costume Adventure", "Movie genres_Fantasy Adventure",
        "Movie genres_Family-Oriented Adventure", "Movie genres_Sci-Fi Adventure",
        "Movie genres_Sword and Sandal", "Movie genres_Archaeology", "Movie genres_Space western"
    ],
    "Comedy": [
        "Movie genres_Action Comedy", "Movie genres_Black comedy", "Movie genres_Camp",
        "Movie genres_Comedy", "Movie genres_Comedy Thriller", "Movie genres_Comedy Western",
        "Movie genres_Comedy horror", "Movie genres_Comedy-drama", "Movie genres_Comedy of Errors",
        "Movie genres_Comedy of manners", "Movie genres_Domestic Comedy", "Movie genres_Heavenly Comedy",
        "Movie genres_Musical comedy", "Movie genres_Parody", "Movie genres_Romantic comedy",
        "Movie genres_Screwball comedy", "Movie genres_Stand-up comedy", "Movie genres_Sex comedy",
        "Movie genres_Stoner film", "Movie genres_Workplace Comedy"
    ],
    "Drama": [
        "Movie genres_Addiction Drama", "Movie genres_Biographical film", "Movie genres_Biopic [feature]",
        "Movie genres_Childhood Drama", "Movie genres_Coming-of-age film", "Movie genres_Courtroom Drama",
        "Movie genres_Costume drama", "Movie genres_Family Drama", "Movie genres_Historical drama",
        "Movie genres_Melodrama", "Movie genres_Political drama", "Movie genres_Romantic drama",
        "Movie genres_Social problem film", "Movie genres_Tragedy"
    ],
    "Fantasy and Science Fiction": [
        "Movie genres_Alien Film", "Movie genres_Alien invasion", "Movie genres_Apocalyptic and post-apocalyptic fiction",
        "Movie genres_Fairy tale", "Movie genres_Fantasy", "Movie genres_Fantasy Adventure",
        "Movie genres_Fantasy Comedy", "Movie genres_Fantasy Drama", "Movie genres_Mythological Fantasy",
        "Movie genres_Science Fiction", "Movie genres_Space opera", "Movie genres_Steampunk",
        "Movie genres_Supernatural", "Movie genres_Sword and sorcery", "Movie genres_Time travel"
    ],
    "Horror": [
        "Movie genres_Comedy horror", "Movie genres_Creature Film", "Movie genres_Costume Horror",
        "Movie genres_Demonic child", "Movie genres_Doomsday film", "Movie genres_Horror",
        "Movie genres_Haunted House Film", "Movie genres_Horror Comedy", "Movie genres_Natural horror films",
        "Movie genres_Period Horror", "Movie genres_Psychological horror", "Movie genres_Slasher",
        "Movie genres_Splatter film", "Movie genres_Road-Horror", "Movie genres_Vampire movies",
        "Movie genres_Werewolf fiction", "Movie genres_Zombie Film"
    ],
    "Romance": [
        "Movie genres_Romance Film", "Movie genres_Romantic comedy", "Movie genres_Romantic drama",
        "Movie genres_Romantic fantasy", "Movie genres_Heaven-Can-Wait Fantasies", "Movie genres_Tragicomedy"
    ],
    "Documentary": [
        "Movie genres_Docudrama", "Movie genres_Documentary", "Movie genres_Educational",
        "Movie genres_Environmental Science", "Movie genres_Film & Television History",
        "Movie genres_Journalism", "Movie genres_News", "Movie genres_Rockumentary",
        "Movie genres_Social issues", "Movie genres_Culture & Society", "Movie genres_History"
    ],
    "Crime and Mystery": [
        "Movie genres_Caper story", "Movie genres_Crime", "Movie genres_Crime Comedy",
        "Movie genres_Crime Drama", "Movie genres_Crime Fiction", "Movie genres_Crime Thriller",
        "Movie genres_Detective", "Movie genres_Detective fiction", "Movie genres_Film noir",
        "Movie genres_Heist", "Movie genres_Master Criminal Films", "Movie genres_Mystery",
        "Movie genres_Neo-noir", "Movie genres_Political thriller", "Movie genres_Psychological thriller",
        "Movie genres_Suspense", "Movie genres_Whodunit"
    ],
    "Musicals and Dance": [
        "Movie genres_Animated Musical", "Movie genres_Backstage Musical", "Movie genres_Breakdance",
        "Movie genres_Jukebox musical", "Movie genres_Musical", "Movie genres_Musical Drama",
        "Movie genres_Musical comedy", "Movie genres_Rockumentary", "Movie genres_Dance"
    ],
    "War and Political": [
        "Movie genres_Anti-war", "Movie genres_Anti-war film", "Movie genres_Cold War",
        "Movie genres_Combat Films", "Movie genres_Glamorized Spy Film", "Movie genres_Gulf War",
        "Movie genres_Historical Epic", "Movie genres_Political cinema", "Movie genres_Political drama",
        "Movie genres_Political satire", "Movie genres_Political thriller", "Movie genres_Propaganda film",
        "Movie genres_War film", "Movie genres_The Netherlands in World War II"
    ],
    "Family and Children": [
        "Movie genres_Children's", "Movie genres_Children's Fantasy", "Movie genres_Children's/Family",
        "Movie genres_Family Film", "Movie genres_Family Drama", "Movie genres_Family-Oriented Adventure",
        "Movie genres_Family & Personal Relationships", "Movie genres_Christmas movie", "Movie genres_Animated Musical"
    ],
    "Animation": [
        "Movie genres_Animated cartoon", "Movie genres_Animation", "Movie genres_Anime",
        "Movie genres_Computer Animation", "Movie genres_Stop motion", "Movie genres_Supermarionation"
    ],
    "Sports": [
        "Movie genres_Auto racing", "Movie genres_Baseball", "Movie genres_Boxing",
        "Movie genres_Extreme Sports", "Movie genres_Horse racing", "Movie genres_Sports"
    ],
    "Experimental and Independent": [
        "Movie genres_Absurdism", "Movie genres_Avant-garde", "Movie genres_Art film",
        "Movie genres_Experimental film", "Movie genres_Indie", "Movie genres_Mockumentary",
        "Movie genres_Mumblecore"
    ],
    "LGBT and Gender Issues": [
        "Movie genres_Feminist Film", "Movie genres_Gay", "Movie genres_Gay Interest",
        "Movie genres_Gay Themed", "Movie genres_Gender Issues", "Movie genres_LGBT"
    ],
    "Erotic and Adult": [
        "Movie genres_Adult", "Movie genres_Erotica", "Movie genres_Erotic Drama",
        "Movie genres_Erotic thriller", "Movie genres_Gay pornography", "Movie genres_Hardcore pornography",
        "Movie genres_Sexploitation", "Movie genres_Softcore Porn"
    ]
}

def reorder_column(df: pd.DataFrame, col_name: str, index: int) -> pd.DataFrame:
    """Move a column to the specified position in a dataframe"""
    cols = df.columns.tolist()
    cols.remove(col_name)
    cols.insert(index, col_name)
    return df[cols]

def get_revenue(wikidata_id):
    """Get the movie revenue from the wikidata id"""
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": wikidata_id,
        "format": "json",
        "languages": "en",
    }
    try:
        # Request the data from the wikidata API
        response = requests.get(url, params=params)
        data = response.json()
        if "entities" in data and wikidata_id in data["entities"]:
            claims = data["entities"][wikidata_id]["claims"]
            # Get the box office revenue claim stored in the wikidata item P2142
            if "P2142" in claims:
                box_office_claim = claims["P2142"][0]["mainsnak"]["datavalue"]["value"]
                return float(box_office_claim["amount"])
            else:
                return None
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def update_movie_revenue(movie_df):
    """Update the movie revenue for movies having a missing revenue"""
    def process_row(index, row):
        """Process a row to update the movie revenue"""
        if pd.notna(row["Movie box office revenue"]):
            return index, row["Movie box office revenue"]

        revenue = get_revenue(row["wikidata_movie_id"])
        if revenue == 0:
            revenue = None
        return index, revenue

    # Create a thread pool executor
    with ThreadPoolExecutor() as executor:
        # Submit tasks to the thread pool
        futures = {
            executor.submit(process_row, index, row): index
            for index, row in movie_df.iterrows()
        }

        # Wait for each future to complete and update the DataFrame
        for future in futures:
            index, revenue = future.result()
            movie_df.at[index, "Movie box office revenue"] = revenue

    return movie_df

def reduce_genres_and_ethnicities(df, genre_mapping=genre_mapping, ethnicity_mapping=ethnicity_mapping):
    """Reduce the number of genres and ethnicities columns in the DataFrame using a mapping dictionary to more general categories"""
    df = create_dummies_from_list_column(df, 'ethnicity')
    df = create_dummies_from_list_column(df, 'Movie genres')
    ethnicity_columns = [col for col in df.columns if col.lower().startswith('ethnicity')]
    genre_columns = [col for col in df.columns if col.lower().startswith('movie genres')]

    # Create new columns for each category
    for category, columns in ethnicity_mapping.items():
        existing_columns = [col for col in columns if col in df.columns]
        if existing_columns:
            df[category] = df[existing_columns].sum(axis=1)

    for category, genres in genre_mapping.items():
        existing_columns = [col for col in genres if col in df.columns]
        if existing_columns:
            df[category] = df[existing_columns].sum(axis=1)
            df[category] = df[category].apply(lambda x: 1 if x > 1 else x)

    df['Movie genres'] = df[genre_mapping.keys()].apply(
        lambda row: ', '.join([category for category in genre_mapping.keys() if row[category] == 1]), axis=1
    )
    df['ethnicity'] = df[ethnicity_mapping.keys()].apply(
        lambda row: ', '.join([category for category in ethnicity_mapping.keys() if row[category] > 0]), axis=1
    )

    # Drop the grouped ethnicity and genre columns used for intermediate calculations
    df = df.drop(columns=list(ethnicity_mapping.keys()) + list(genre_mapping.keys()), axis=1)

    # Drop the original ethnicity columns
    df = df.drop(columns=ethnicity_columns, axis=1)
    df = df.drop(columns=genre_columns, axis=1)
    return df

def create_dummies_from_list_column(df, column_name):
    """Create dummy variables from a column containing lists of comma separated values"""
    # Split the string entries into lists
    split_series = df[column_name].str.split(', ')
    # Create a new DataFrame with dummy variables
    dummy_df = pd.get_dummies(split_series.apply(pd.Series).stack(), prefix=column_name).groupby(level=0).sum()
    # Merge the dummy variables into the original DataFrame
    df = pd.concat([df, dummy_df], axis=1)
    # Drop the original column
    df = df.drop(column_name, axis=1)
    return df

def replace_with_min_max(df, column_name):
    """Replace a column containing lists of comma separated values with the minimum and maximum values"""
    # Split the ages into lists, cleaning up any whitespace or invalid entries
    df[column_name] = df[column_name].str.split(', ').apply(
        lambda x: [float(age.strip()) for age in x if age.strip().replace('.', '', 1).isdigit()]
    )
    df[f'{column_name}_min'] = df[column_name].apply(
        lambda x: min(x) if len(x) > 0 else None
    )
    df[f'{column_name}_max'] = df[column_name].apply(
        lambda x: max(x) if len(x) > 0 else None
    )
    # Drop the original column
    df = df.drop(column_name, axis=1)
    return df

def preprocess_data_for_model(df):
    """
    Preprocess the dataset for machine learning by cleaning, encoding, and engineering features.

    Steps:
    1. Drop irrelevant columns (e.g., identifiers, names, plot) and rows with missing or invalid data.
    2. One-hot encode categorical variables (`actor_gender`, `Movie genres`, `ethnicity`, etc.) and compute `F ratio`.
    3. Filter for English-language movies produced in the USA.
    4. Replace features (`actor_age_at_release`, `actor_height_meters`) with min-max scaled values.
    5. Adjust actor heights relative to 160 cm.
    6. Sort by release date and group into periods (e.g., "2000-2004").
    7. Compute `ethnic_score` from ethnicity indicators.

    Parameters:
    ----------
    df : Input dataframe containing movie and actor details.

    Returns:
    -------
    Transformed dataframe ready for modeling.
    """
    df = df.drop(["wikipedia_movie_id", "wikidata_movie_id", "Movie name", "character_name", "plot"], axis=1)
    df = df.dropna()
    df = df[df["Movie box office revenue"] != 0]
    
    df = create_dummies_from_list_column(df, 'actor_gender')
    df = df.drop("actor_gender_", axis=1)
    df["F ratio"] = df["actor_gender_F"] / (df["actor_gender_M"]+df["actor_gender_F"])

    df = replace_with_min_max(df, 'actor_age_at_release')
    df = replace_with_min_max(df, 'actor_height_meters')

    df_with_countries = create_dummies_from_list_column(df, 'Movie countries')
    df = df[df_with_countries["Movie countries_United States of America"] == 1]

    df_with_countries = create_dummies_from_list_column(df, 'Movie languages')
    df = df[df_with_countries["Movie languages_English Language"] == 1]

    df = create_dummies_from_list_column(df, 'Movie genres')
    df = create_dummies_from_list_column(df, 'ethnicity')

    df = df.rename(columns=lambda col: col.replace('Movie genres_', '') if col.startswith('Movie genres') else col)
    df = df.rename(columns=lambda col: col.replace('ethnicity_', '') if col.startswith('ethnicity') else col)
    df = df.drop(["Movie languages", "Movie countries"], axis=1)
    df.dropna(inplace=True)
    
    #We compare heights wrt a reference of 160 cm :
    df['actor_height_meters_min'] = df['actor_height_meters_min'] * 100 - 160 
    df['actor_height_meters_max'] = df['actor_height_meters_max'] * 100 - 160

    df = df.sort_values(by="Movie release date")
    df['Movie release date'] = df['Movie release date'].astype(int)
    df['period'] = df['Movie release date'].apply(lambda x: f"{x // 5 * 5}-{(x // 5 + 1) * 5 - 1}")
    df['ethnic_score'] = df[['African Ethnicities', 'American Ethnicities', 'Asian Ethnicities', 'Eastern European Ethnicities', 'Indigenous Peoples',
    'Jewish Communities', 'Latin American Ethnicities', 'Middle Eastern and Arab Ethnicities',
    'Northern European Ethnicities', 'Oceanian Ethnicities', 'Southern European Ethnicities',
   'Western European Ethnicities']].sum(axis=1)
    return df
