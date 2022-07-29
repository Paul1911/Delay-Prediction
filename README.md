Landing Delay Prediction of Airline Flights
==============================

This is a project for the prediction of landing times of aircraft, which is, in its core, a supervised regression for delay prediction. I used the Cookiecutter template for overall structuring, however not leveraging all of its features. 

The main idea is to predict all landing times for a given day and aircraft at the start of the day. We are provided with the schedule, so the landing time for a flight event can be broken down to

$$ 
LandingTime_i = \left\{\begin{array}{lr}
    ScheduledDeparture_i + ScheduledBlockTime_i + Delay_i & \text{for } i=1\\
    LandingTime_{i-1}+ScheduledGroundTime_i+ScheduledBlockTime_i+Delay_i & \text{for } i > 1\\
    \end{array}\right\}
$$

where $i$ is the number of the flight event. 

Overall, the data is very messy and required a lot of data cleaning and feature engineering. The final RMSE for arrival delay is 6.03 minutes, archived by using a Gradient Boosted tree, but the ridge regression model only performs only slightly worse with an RMSE of 6.18, so it might be preferable due to its easier explainablity. 
The notebooks and important files can be found in /notebooks. A detailed project description can also be found in the first and second workbook. 


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── finalized      <- The finalized dat
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- Processed data, but not yet final. 
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
