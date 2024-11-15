import json
import os

import pandas as pd

from src.utils.data_utils import reorder_column


class DataLoader:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(
            os.path.dirname(os.path.dirname(current_dir)), "datasets"
        )
        self.paths = {
            "character": os.path.join(data_dir, "character.metadata.tsv"),
            "movie": os.path.join(data_dir, "movie.metadata.tsv"),
            "name": os.path.join(data_dir, "name.clusters.tsv"),
            "plot": os.path.join(data_dir, "plot_summaries.tsv"),
            "tvtropes": os.path.join(data_dir, "tvtropes.clusters.tsv"),
            "fb_wiki": os.path.join(data_dir, "freebase_wikidata_mapping.tsv"),
            "tmdb_movies": os.path.join(data_dir, "tmdb/movies_metadata.csv"),
        }

    def _load_tsv(self, path: str, names: list = None) -> pd.DataFrame:
        """Generic TSV loader"""
        return pd.read_csv(path, sep="\t", names=names)

    def load_characters(self) -> pd.DataFrame:
        """Load character metadata"""
        df = self._load_tsv(self.paths["character"])

        # Drop "Movie release date" column
        df.drop(
            columns=["Movie release date", "Freebase character/actor map ID"],
            inplace=True,
        )

        # Get mapping once
        fb_wiki_mapping = self.load_fb_wiki_mapping()

        # Map ethnicity
        df = df.merge(
            fb_wiki_mapping[["freebase_id", "label"]],
            how="left",
            left_on="Actor ethnicity (Freebase ID)",
            right_on="freebase_id",
        )
        df.drop(columns=["freebase_id", "Actor ethnicity (Freebase ID)"], inplace=True)
        df.rename(columns={"label": "ethnicity"}, inplace=True)

        # Map character ID
        df = df.merge(
            fb_wiki_mapping[["freebase_id", "wikidata_id"]],
            how="left",
            left_on="Freebase character ID",
            right_on="freebase_id",
        )
        df.drop(columns=["freebase_id", "Freebase character ID"], inplace=True)
        df.rename(columns={"wikidata_id": "wikidata_character_id"}, inplace=True)

        # Map actor ID
        df = df.merge(
            fb_wiki_mapping[["freebase_id", "wikidata_id"]],
            how="left",
            left_on="Freebase actor ID",
            right_on="freebase_id",
        )
        df.drop(columns=["freebase_id", "Freebase actor ID"], inplace=True)
        df.rename(columns={"wikidata_id": "wikidata_actor_id"}, inplace=True)

        # Map Freebase movie ID
        df = df.merge(
            fb_wiki_mapping[["freebase_id", "wikidata_id"]],
            how="left",
            left_on="Freebase movie ID",
            right_on="freebase_id",
        )
        df.drop(columns=["freebase_id", "Freebase movie ID"], inplace=True)
        df.rename(columns={"wikidata_id": "wikidata_movie_id"}, inplace=True)

        # Rename columns with underscores
        df.rename(
            columns={
                "Wikipedia movie ID": "wikipedia_movie_id",
                "Character name": "character_name",
                "Actor date of birth": "actor_date_of_birth",
                "Actor gender": "actor_gender",
                "Actor height (in meters)": "actor_height_meters",
                "Actor name": "actor_name",
                "Actor age at movie release": "actor_age_at_release",
            },
            inplace=True,
        )

        # Reorder columns to put wikidata_movie_id in second place
        df = reorder_column(df, "wikidata_movie_id", 1)

        # Add this in case we want to use the 500 TV tropes
        # df = pd.merge(
        #     df,
        #     self.load_tvtropes()[["trope", "Freebase character/actor map ID"]],
        #     on="Freebase character/actor map ID",
        #     how="left",
        # )

        return df

    def load_movies(self) -> pd.DataFrame:
        """Load and process movie metadata"""
        df = self._load_tsv(self.paths["movie"])

        # Process JSON columns
        json_columns = {
            "Movie languages (Freebase ID:name tuples)": "Movie languages",
            "Movie countries (Freebase ID:name tuples)": "Movie countries",
            "Movie genres (Freebase ID:name tuples)": "Movie genres",
        }

        for old_col, new_col in json_columns.items():
            # Convert JSON string of {id: name} pairs into comma-separated string of names
            # e.g. '{"m/123": "Action", "m/456": "Drama"}' -> "Action, Drama"
            df[new_col] = df[old_col].apply(
                lambda x: ", ".join(json.loads(x).values()) if pd.notnull(x) else x
            )
            df.drop(columns=[old_col], inplace=True)

        df.rename(columns={"Wikipedia movie ID": "wikipedia_movie_id"}, inplace=True)

        print(
            "Number of movies with missing release date:",
            df["Movie release date"].isna().sum(),
        )
        print(
            "Number of movies with missing revenue:",
            df["Movie box office revenue"].isna().sum(),
        )

        # Add TMDB release dates and revenue for movies with missing data
        tmdb_df = pd.read_csv(self.paths["tmdb_movies"])
        tmdb_df = tmdb_df[["title", "release_date", "revenue"]]
        tmdb_df["release_date"] = tmdb_df["release_date"].str[:4]  # Keep only year

        # Merge with TMDB data
        df = df.merge(tmdb_df, left_on="Movie name", right_on="title", how="left")

        # Fill missing dates and revenue with TMDB data
        df["Movie release date"] = df["Movie release date"].fillna(df["release_date"])
        df["Movie box office revenue"] = df["Movie box office revenue"].fillna(
            df["revenue"]
        )
        df.drop(columns=["title", "release_date", "revenue"], inplace=True)

        print(
            "Number of movies with missing release date:",
            df["Movie release date"].isna().sum(),
        )
        print(
            "Number of movies with missing revenue:",
            df["Movie box office revenue"].isna().sum(),
        )

        # Keep only the year from the release date
        # e.g. "2024-01-01" -> "2024"
        df["Movie release date"] = df["Movie release date"].astype(str).str[:4]

        # Fix outlier movie release date
        df["Movie release date"] = df["Movie release date"].replace("1010", "2010")

        # Remove movies outside the 1910-2012 range
        df = df[
            (pd.to_numeric(df["Movie release date"], errors="coerce") >= 1910)
            & (pd.to_numeric(df["Movie release date"], errors="coerce") <= 2012)
        ]

        # Drop movie runtime column
        df.drop(columns=["Movie runtime"], inplace=True)

        return df

    def load_movies_with_characters(self) -> pd.DataFrame:
        """Load movies with characters"""
        df = self.load_movies()
        df = df.merge(
            self.load_characters(),
            on="wikipedia_movie_id",
            how="inner",
        )

        df = (
            df.groupby(["wikipedia_movie_id"])
            .agg(
                {
                    "wikidata_movie_id": lambda x: x.dropna().iloc[0]
                    if not x.dropna().empty
                    else None,
                    "Movie name": lambda x: x.dropna().iloc[0]
                    if not x.dropna().empty
                    else None,
                    "Movie release date": lambda x: x.dropna().iloc[0]
                    if not x.dropna().empty
                    else None,
                    "Movie box office revenue": lambda x: x.dropna().iloc[0]
                    if not x.dropna().empty
                    else None,
                    "Movie languages": lambda x: x.dropna().iloc[0]
                    if not x.dropna().empty
                    else None,
                    "Movie countries": lambda x: x.dropna().iloc[0]
                    if not x.dropna().empty
                    else None,
                    "Movie genres": lambda x: x.dropna().iloc[0]
                    if not x.dropna().empty
                    else None,
                    "character_name": lambda x: ", ".join(x[~x.isna()].astype(str)),
                    "actor_gender": lambda x: ", ".join(x[~x.isna()].astype(str)),
                    "actor_height_meters": lambda x: ", ".join(
                        x[~x.isna()].astype(str)
                    ),
                    "actor_age_at_release": lambda x: ", ".join(
                        x[~x.isna()].astype(str)
                    ),
                    "ethnicity": lambda x: ", ".join(x[~x.isna()].astype(str)),
                }
            )
            .reset_index()
        )

        df = pd.merge(
            df, self.load_plot_summaries(), on="wikipedia_movie_id", how="left"
        )

        # df = df.merge(
        #     self.load_fb_wiki_mapping()[["freebase_id", "wikidata_id"]],
        #     how="left",
        #     left_on="Freebase movie ID",
        #     right_on="freebase_id",
        # )

        return df

    def load_name_clusters(self) -> pd.DataFrame:
        """Load name clusters"""
        return self._load_tsv(
            self.paths["name"],
            names=["Character name", "Freebase character/actor map ID"],
        )

    def load_plot_summaries(self) -> pd.DataFrame:
        """Load plot summaries"""
        df = self._load_tsv(self.paths["plot"], names=["wikipedia_movie_id", "plot"])
        return df

    def load_tvtropes(self) -> pd.DataFrame:
        """Load and process TV tropes data"""
        df = self._load_tsv(self.paths["tvtropes"], names=["trope", "details"])
        df = pd.concat(
            [df["trope"], df["details"].apply(json.loads).apply(pd.Series)], axis=1
        )
        df.rename(columns={"id": "Freebase character/actor map ID"}, inplace=True)
        return df

    def load_fb_wiki_mapping(self) -> pd.DataFrame:
        """Load Freebase to Wikipedia mapping"""
        return self._load_tsv(self.paths["fb_wiki"])
