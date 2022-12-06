import numpy as np
import pandas as pd
from sklearn.decomposition import FastICA
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from tpot.export_utils import set_param_recursive

kstrTrainFile = "../dat/train_df.csv"
kstrTargetCol = 'Purchase'

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
#tpot_data = pd.read_csv(kstrTrainFile, sep=',', dtype=np.float64)
#tpot_data = pd.read_csv(kstrTrainFile, compression='gzip')
tpot_data = pd.read_csv(kstrTrainFile, sep=',', dtype=np.float64)

features = tpot_data.drop(kstrTargetCol, axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data[kstrTargetCol], random_state=42)

# Average CV score on the training set was: 1.0
exported_pipeline = make_pipeline(
    MinMaxScaler(),
    FastICA(tol=0.35000000000000003),
    GradientBoostingClassifier(learning_rate=0.01, max_depth=4, max_features=0.9000000000000001, min_samples_leaf=20, min_samples_split=6, n_estimators=100, subsample=0.4)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
