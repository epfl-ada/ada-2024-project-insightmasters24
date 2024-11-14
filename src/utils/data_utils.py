import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import requests

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
    print("Processing")
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

