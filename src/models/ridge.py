from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def ridge_regression1(df, show_details=False):
    period_counts = df['period'].value_counts().sort_index()

    # Print periods with more than 500 movies
    valid_periods = period_counts[period_counts > 500].index

    features_of_interest = {}  # Initialize as dictionary 

    # For each valid period, run a separate regression
    for period in valid_periods:
        # Filter data for this period
        period_data = df[df['period'] == period]
        
        # Split data
        X = period_data.drop(["Movie box office revenue", "period", "Movie release date", "African Ethnicities","Indigenous Peoples", "Western European Ethnicities", 
                            "Northern European Ethnicities", "Southern European Ethnicities", "Eastern European Ethnicities",
                            "Asian Ethnicities", "Middle Eastern and Arab Ethnicities","Latin American Ethnicities", "Jewish Communities", "American Ethnicities",
                                "Oceanian Ethnicities"], axis=1)
        y = period_data["Movie box office revenue"]
        xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=0.1, random_state=42, shuffle=True)
        
        # Scale features
        x_scaler = StandardScaler()
        xtrain = x_scaler.fit_transform(xtrain)
        xtest = x_scaler.transform(xtest)
        
        y_scaler = StandardScaler()
        ytrain = y_scaler.fit_transform(ytrain.values.reshape(-1, 1)).ravel()
        
        # Fit model
        model = Ridge(alpha=100.0)
        model.fit(xtrain, ytrain)
        
        # Predict and inverse transform
        ypred = model.predict(xtest)
        ypred = y_scaler.inverse_transform(ypred.reshape(-1, 1)).ravel()
        ypred_2 = model.predict(xtrain)
        #ypred_2 = y_scaler.inverse_transform(ypred_2.reshape(-1, 1)).ravel()

        if show_details:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

            # Create subplot
            ax1.scatter(ytest, ypred, alpha=0.6, label="Revenue", color="blue")
            ax1.plot([ytest.min(), ytest.max()], [ytest.min(), ytest.max()], 'r--', label="Perfect Prediction Line")
            ax1.set_xscale('log')
            ax1.set_yscale("log")
            ax1.set_xlabel("Actual Values")
            ax1.set_ylabel("Predicted Values")
            ax1.set_title(f"Period {period} : Test data")
            ax1.legend()

            ax2.scatter(ytrain, ypred_2, alpha=0.6, label="Revenue", color="blue")
            ax2.plot([ytrain.min(), ytrain.max()], [ytrain.min(), ytrain.max()], 'r--', label="Perfect Prediction Line")
            ax2.set_xscale('log')
            ax2.set_yscale("log")
            ax2.set_xlabel("Actual Values")
            ax2.set_ylabel("Predicted Values")
            ax2.set_title(f"Period {period} : Train data")
            ax2.legend()

        # Statistical Summary
        X_with_const = sm.add_constant(xtrain)
        model_stats = sm.OLS(ytrain, X_with_const).fit()
        # Create a DataFrame with coefficients and p-values
        feature_names = ['const'] + list(X.columns)
        coef_df = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': model_stats.params,
            'P-value': model_stats.pvalues
        })

        # Sort by absolute coefficient value
        coef_df['Abs_Coefficient'] = coef_df['Coefficient']
        coef_df = coef_df.sort_values('Abs_Coefficient', ascending=False)
        coef_df = coef_df.drop('Abs_Coefficient', axis=1)

        # Filter for p-value < 0.05 and display
        significant_features = coef_df[coef_df['P-value'] < 0.05]
        significant_features = significant_features[significant_features['Feature'] != 'const']
        # Inverse transform the coefficients to get them back to original scale
        # Corrected to use x_scaler for inverse transform
        significant_features['Coefficient'] = y_scaler.inverse_transform(significant_features['Coefficient'].values.reshape(-1, 1)).ravel()
        features_of_interest[period] = significant_features  # Store in dictionary

        if show_details:
            # Display period information
            print(period)
            print("\nModel Statistics:")
            print("R-squared:", model_stats.rsquared)
            print("\nFeature Coefficients and P-values:")
            print(significant_features)

            plt.tight_layout()
            plt.show()

    if show_details:
        # Print the number of movies in each period
        print("\nNumber of movies in each period:")
        print(period_counts[valid_periods])
    return features_of_interest

def plot_most_important_features_generated_by_ridge_regression(features_of_interest):
    # Create DataFrames for character and genre features
    character_df = pd.DataFrame()
    genre_df = pd.DataFrame()
    for period, features in features_of_interest.items():
        if len(features) == 0:  # Skip if no significant features for this period
            continue

        # Extract feature names and coefficients (retain original values)
        period_features = pd.DataFrame({
            'Feature': features['Feature'],
            'Coefficient': features['Coefficient']
        })
        
        # Split into character and genre features
        character_features = period_features[
            period_features['Feature'].str.contains('actor|ethnicities|F ratio|people|communities|score', case=False, regex=True)
        ].copy()
        
        genre_features = period_features[
            ~period_features['Feature'].str.contains('actor|ethnicities|F ratio|people|communities|score', case=False, regex=True)
        ].copy()

        # Keep only top 5 genre and character features based on absolute coefficient value
        genre_features = genre_features.nlargest(5, 'Coefficient')
        character_features = character_features.nlargest(5, "Coefficient")

        # Add period column
        character_features['Period'] = period
        genre_features['Period'] = period
        
        # Append to the respective DataFrames
        character_df = pd.concat([character_df, character_features])
        genre_df = pd.concat([genre_df, genre_features])

    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(25, 20))

    # Define distinct color palettes for each plot
    char_colors = plt.cm.tab20(np.linspace(0, 1, len(character_df['Feature'].unique())))
    genre_colors = plt.cm.tab20(np.linspace(0, 1, len(genre_df['Feature'].unique())))

    # Plot character features (signed values)
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

    # Plot genre features (signed values)
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

    plt.tight_layout()
    plt.show()

def ridge_regression2(df, show_details=False):
    period_counts = df['period'].value_counts().sort_index()

    # Print periods with more than 500 movies
    valid_periods = period_counts[period_counts > 500].index
    features_of_interest = {}  # Initialize as dictionary 

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
        
        y_scaler = StandardScaler()
        ytrain = y_scaler.fit_transform(ytrain.values.reshape(-1, 1)).ravel()
        
        # Fit model
        model = Ridge(alpha=100.0)
        model.fit(xtrain, ytrain)
        
        # Predict and inverse transform
        ypred = model.predict(xtest)
        ypred = y_scaler.inverse_transform(ypred.reshape(-1, 1)).ravel()
        ypred_2 = model.predict(xtrain)
        #ypred_2 = y_scaler.inverse_transform(ypred_2.reshape(-1, 1)).ravel()

        if show_details:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

            # Create subplot
            ax1.scatter(ytest, ypred, alpha=0.6, label="Revenue", color="blue")
            ax1.plot([ytest.min(), ytest.max()], [ytest.min(), ytest.max()], 'r--', label="Perfect Prediction Line")
            ax1.set_xscale('log')
            ax1.set_yscale("log")
            ax1.set_xlabel("Actual Values")
            ax1.set_ylabel("Predicted Values")
            ax1.set_title(f"Period {period} : Test data")
            ax1.legend()

            ax2.scatter(ytrain, ypred_2, alpha=0.6, label="Revenue", color="blue")
            ax2.plot([ytrain.min(), ytrain.max()], [ytrain.min(), ytrain.max()], 'r--', label="Perfect Prediction Line")
            ax2.set_xscale('log')
            ax2.set_yscale("log")
            ax2.set_xlabel("Actual Values")
            ax2.set_ylabel("Predicted Values")
            ax2.set_title(f"Period {period} : Train data")
            ax2.legend()

        # Statistical Summary
        X_with_const = sm.add_constant(xtrain)
        model_stats = sm.OLS(ytrain, X_with_const).fit()
        # Create a DataFrame with coefficients and p-values
        feature_names = ['const'] + list(X.columns)
        coef_df = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': model_stats.params,
            'P-value': model_stats.pvalues
        })

        ###Change code snippet because we dont sort by absolute value anymore
        coef_df['Abs_Coefficient'] = coef_df['Coefficient']
        coef_df = coef_df.sort_values('Abs_Coefficient', ascending=False)
        coef_df = coef_df.drop('Abs_Coefficient', axis=1)

        # Filter for p-value < 0.05 and display
        significant_features = coef_df[coef_df['P-value'] < 0.05]
        significant_features = significant_features[significant_features['Feature'] != 'const']
        # Inverse transform the coefficients to get them back to original scale
        # Corrected to use x_scaler for inverse transform
        significant_features['Coefficient'] = y_scaler.inverse_transform(significant_features['Coefficient'].values.reshape(-1, 1)).ravel()
        features_of_interest[period] = significant_features  # Store in dictionary

        if show_details:
            # Display period information
            print(period)
            print("\nModel Statistics:")
            print("R-squared:", model_stats.rsquared)
            print("\nFeature Coefficients and P-values:")
            print(significant_features)

            plt.tight_layout()
            plt.show()

    if show_details:
        # Print the number of movies in each period
        print("\nNumber of movies in each period:")
        print(period_counts[valid_periods])
    return features_of_interest

def plot_most_important_features_generated_by_ridge_regression_only_considering_ethnic_score(features_of_interest):
    # Create DataFrames for character and genre features
    character_df = pd.DataFrame()
    genre_df = pd.DataFrame()

    for period, features in features_of_interest.items():
        if len(features) == 0:  # Skip if no significant features for this period
            continue

        # Extract feature names and coefficients (retain original values)
        period_features = pd.DataFrame({
            'Feature': features['Feature'],
            'Coefficient': features['Coefficient']
        })
        
        # Split into character and genre features
        character_features = period_features[
            period_features['Feature'].str.contains('actor|ethnicities|F ratio|people|communities|score', case=False, regex=True)
        ].copy()
        
        genre_features = period_features[
            ~period_features['Feature'].str.contains('actor|ethnicities|F ratio|people|communities|score', case=False, regex=True)
        ].copy()

        # Keep only top 5 genre and character features based on absolute coefficient value
        genre_features = genre_features.nlargest(5, 'Coefficient')
        character_features = character_features.nlargest(5, "Coefficient")

        # Add period column
        character_features['Period'] = period
        genre_features['Period'] = period
        
        # Append to the respective DataFrames
        character_df = pd.concat([character_df, character_features])
        genre_df = pd.concat([genre_df, genre_features])

    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(25, 20))

    # Define distinct color palettes for each plot
    char_colors = plt.cm.tab20(np.linspace(0, 1, len(character_df['Feature'].unique())))
    genre_colors = plt.cm.tab20(np.linspace(0, 1, len(genre_df['Feature'].unique())))

    # Plot character features (signed values)
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

    # Plot genre features (signed values)
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

    plt.tight_layout()
    plt.show()