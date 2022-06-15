# Check whether execution is faster in a separate .py file

# Imports 

import pandas as pd 
import numpy as np 
import time

from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

def modeltraining():
    # Read df
    full_df = pd.read_pickle('../data/finalized/full_df.pkl')

    # Delete NAs
    full_df = full_df.dropna(how = 'any')

    # Creating dummy variables for all categorical variables
    # Note: Onehotencoder is the better solution, however for simplicity let's use pandas for the moment

    # Get object columns
    full_df_objectcolumns = full_df.select_dtypes(include = 'object')
    varlist = full_df_objectcolumns.columns.values.tolist()

    # get dummies
    full_df_encoded = pd.get_dummies(full_df, columns = varlist, drop_first = True)

    # We split the forecast in two different forecasts - one for ground delay and one for block delay

    X_train_blockdelay_encoded, X_test_blockdelay_encoded, y_train_blockdelay_encoded, y_test_blockdelay_encoded = train_test_split(
        full_df_encoded.drop(['block_delay'], axis = 1), full_df_encoded['block_delay'], test_size=0.33, random_state=42)

    # Filtering out rows which are skewing ground delay prediction
    full_df_encoded_grounddelay = full_df_encoded[full_df_encoded['rows_to_drop_grounddelay']<1]

    X_train_grounddelay_encoded, X_test_grounddelay_encoded, y_train_grounddelay_encoded, y_test_grounddelay_encoded = train_test_split(
        full_df_encoded_grounddelay.drop(['ground_delay'], axis = 1), full_df_encoded_grounddelay['ground_delay'], test_size=0.33, random_state=42)



    # Initialize estimators
    #reg1 = LinearRegression()
    reg2 = Lasso()
    #reg3 = Ridge()
    #reg4 = GradientBoostingRegressor()
    #reg5 = SVR()

    # Initialize hyperparameters for each dictionary
    #param1 = {}

    param2 = {}
    param2['regressor__alpha'] = [x for x in np.logspace(0.05,20,20)]
    #param2['normalize'] = [True, False]

    # Create Pipeline
    pipeline = Pipeline([('regressor', reg2)])
    params = [param2]

    # Train grid search model
    gs = GridSearchCV(pipeline, params, cv=5, n_jobs=-1, scoring='neg_root_mean_squared_error').fit(X_train_blockdelay_encoded,y_train_blockdelay_encoded)
    print(gs.best_params_)

if __name__ == "__main__":
    start_time = time.time()
    modeltraining()
    print("--- %s seconds ---" % (time.time() - start_time))
