import pandas as pd
import pickle
import json
import pdb
import warnings

from pathlib import Path
from utils import FeatureTools
from sklearn.preprocessing import MinMaxScaler

warnings.filterwarnings("ignore")


def load_new_training_data(path):
	data = []
	with open (path, "r") as f:
		for line in f:
			data.append(json.loads(line))
	return pd.DataFrame(data)


def build_train(PATH_1, results_path, dataprocessor_id=0, PATH_2=None):
	target = 'income_label'
	df = pd.read_csv(PATH_1)
	if PATH_2:
		df_tmp = load_new_training_data(PATH_2)
		df_tmp = df_tmp[df.columns]
		df = pd.concat([df, df_tmp], ignore_index=True)
		df.to_csv(PATH_1, index=False)
	df[target] = (df['income_bracket'].apply(lambda x: '>50K' in x)).astype(int)
	df.drop('income_bracket', axis=1, inplace=True)
	categorical_columns = list(df.select_dtypes(include=['object']).columns)
	numerical_columns = [c for c in df.columns if c not in categorical_columns+[target]]
	crossed_columns = (['education', 'occupation'], ['native_country', 'occupation'])
	preprocessor = FeatureTools()
	dataprocessor = preprocessor.fit(df,
		target,
		numerical_columns,
		categorical_columns,
		crossed_columns,
		sc=MinMaxScaler())
	dataprocessor_fname = 'dataprocessor_{}_.p'.format(dataprocessor_id)
	pickle.dump(dataprocessor, open(results_path/dataprocessor_fname, "wb"))
	return dataprocessor


if __name__ == '__main__':

	PATH = Path('data/')
	TRAIN_PATH = PATH/'train'
	DATAPROCESSORS_PATH = PATH/'dataprocessors'

	dataprocessor = build_train(TRAIN_PATH/'train.csv', DATAPROCESSORS_PATH)

