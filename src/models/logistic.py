from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import statsmodels.api as sm
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def logistic_regression(df, show_details=False):
    period_counts = df['period'].value_counts().sort_index()

    # Print periods with more than 500 movies
    valid_periods = period_counts[period_counts > 500].index

    features_of_interest = {}  

    # For each valid period, run a separate regression
    for period in valid_periods:
        # Filter data for this period
        period_data = df[df['period'] == period]
        
        # Split data
        X = period_data.drop(["Movie box office revenue", "period", "Movie release date"], axis=1)
        y = period_data["Movie box office revenue"]
        xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=0.1, random_state=42, shuffle=True)
        
        # Scale features
        x_scaler = StandardScaler()
        xtrain = x_scaler.fit_transform(xtrain)
        xtest = x_scaler.transform(xtest)
        
        # Convert to binary for logistic regression
        ytrain = ytrain > 300000000
        ytest = ytest > 300000000
        
        # Fit model
        model = LogisticRegression()
        model.fit(xtrain, ytrain)
        
        # Predict
        ypred = model.predict(xtest)
        ypred_2 = model.predict(xtrain)

        # Calculate F-1 score
        f1 = f1_score(ytest, ypred)
        
        # Statistical Summary
        if show_details:  
            model_stats = sm.Logit(ytrain, xtrain).fit()
        else:
            model_stats = sm.Logit(ytrain, xtrain).fit(disp=0)
        # Create a DataFrame with coefficients and p-values
        feature_names = list(X.columns)
        coef_df = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': model_stats.params,
            'P-value': model_stats.pvalues
        })

        if show_details:
        # Print period information
            print(period)
            print("\nModel Statistics:")
            print("F-1 Score:", f1)
            print("\nFeature Coefficients and P-values:")
            print(coef_df)

        # Store in dictionary
        features_of_interest[period] = coef_df  # Store in dictionary

    if show_details:
        # Print the number of movies in each period
        print("\nNumber of movies in each period:")
        print(period_counts[valid_periods])
    return features_of_interest

def plot_important_features(features_of_interest):
    """Plot the most important features from our logistic regression analysis"""
    # Create DataFrames for character and genre features
    character_df = pd.DataFrame()
    genre_df = pd.DataFrame()

    for period, features in features_of_interest.items():
        if len(features) == 0:  # Skip if no significant features for this period
            continue
        # Extract feature names and coefficients
        period_features = pd.DataFrame({
            'Feature': features['Feature'],
            'Coefficient': features['Coefficient']
        })
        
        # Split into character and genre features
        character_features = period_features[
            period_features['Feature'].str.contains('actor|ethnicities|F ratio|people|communities', case=False, regex=True)
        ].copy()
        
        # Genre features are everything that's not a character feature
        genre_features = period_features[
            ~period_features['Feature'].str.contains('actor|ethnicities|F ratio|people|communities', case=False, regex=True)
        ].copy()
        
        # Keep only top 5 genre features by coefficient magnitude
        genre_features = genre_features.sort_values('Coefficient', ascending=True).head(5)
        character_features = character_features.sort_values('Coefficient', ascending=True).head(5)

        #if not character_features.empty:
        character_features['Period'] = period
        character_df = pd.concat([character_df, character_features])
            
        #if not genre_features.empty:
        genre_features['Period'] = period
        genre_df = pd.concat([genre_df, genre_features])


    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(25, 20))

    # Define distinct color palettes for each plot with more vibrant colors
    char_colors = plt.cm.tab20(np.linspace(0, 1, len(character_df['Feature'].unique())))
    genre_colors = plt.cm.tab20(np.linspace(0, 1, len(genre_df['Feature'].unique())))

    # Plot character features if we have any
    char_plot_data = character_df.pivot_table(
        index='Period', 
        columns='Feature',
        values='Coefficient',
        fill_value=0
    )
    char_plot_data.plot(kind='bar', stacked=True, width=0.8, ax=ax1, color=char_colors)
    ax1.set_title("Character-Related Features Across Time Periods", fontsize=20)
    ax1.set_xlabel("Time Period", fontsize=16)
    ax1.set_ylabel("Coefficient Value", fontsize=16)
    ax1.tick_params(axis='x', rotation=0, labelsize=16)
    ax1.tick_params(axis='y', labelsize=16)
    ax1.legend(title="Character Features", bbox_to_anchor=(1.2, 1), fontsize=14, title_fontsize=16)
    # Plot genre features if we have any
    genre_plot_data = genre_df.pivot_table(
        index='Period',
        columns='Feature', 
        values='Coefficient',
        fill_value=0
    )
    genre_plot_data.plot(kind='bar', stacked=True, width=0.8, ax=ax2, color=genre_colors)
    ax2.set_title("Genre Features Across Time Periods", fontsize=20)
    ax2.set_xlabel("Time Period", fontsize=16)
    ax2.set_ylabel("Coefficient Value", fontsize=16)
    ax2.tick_params(axis='x', rotation=0, labelsize=16)
    ax2.tick_params(axis='y', labelsize=16)
    legend = ax2.legend(title="Genre Features", bbox_to_anchor=(1.0, 1), fontsize=14, title_fontsize=16)

    plt.show()