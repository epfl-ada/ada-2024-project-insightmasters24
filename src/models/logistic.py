##Logistic Regression model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import statsmodels.api as sm
from scipy import stats


def logistic_regression(df):
    # df['Movie release date'] = df['Movie release date'].astype(int)

    # First, let's create 5-year periods and count movies in each
    #df['period'] = df['Movie release date'].apply(lambda x: f"{x // 5 * 5}-{(x // 5 + 1) * 5 - 1}")
    #period_counts = df['period'].value_counts().sort_index()

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
        model_stats = sm.Logit(ytrain, xtrain).fit()
        # Create a DataFrame with coefficients and p-values
        feature_names = list(X.columns)
        coef_df = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': model_stats.params,
            'P-value': model_stats.pvalues
        })

        # Print period information
        print(period)
        print("\nModel Statistics:")
        print("F-1 Score:", f1)
        print("\nFeature Coefficients and P-values:")
        print(coef_df)

        # Store in dictionary
        features_of_interest[period] = coef_df  # Store in dictionary

    # Print the number of movies in each period
    print("\nNumber of movies in each period:")
    print(period_counts[valid_periods])
