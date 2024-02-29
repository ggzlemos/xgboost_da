import os 
import numpy as np
import pandas as pd
from tqdm import tqdm
from utils.constants import TARGET_FILE_NAME, TARGET_COLUMN, INPUT_COLUMNS


def generate_unique_file(filename: str, path: str) -> None:
    """Generates a unique file with the data in the given path and saves it in the data folder. 

    Keywords arguments:
    filename -- name of the output file
    path -- path of the data folder
    """
    X = pd.DataFrame()
    y = pd.DataFrame()

    print(f"Extracting files from {path}...")
    
    for subdir, dirs, files in os.walk(path):
        split_string_ano = subdir.split('/')
        for file in files:                
            file_path = os.path.join(subdir, file)

            file_content = pd.read_csv(file_path) 

            if TARGET_FILE_NAME in file_path:

                y = pd.concat([y, file_content])
            else:
                file_content['dia'] = split_string_ano[-1][2:]
                file_content['mes'] = split_string_ano[-1][:2]
                file_content['ano'] = split_string_ano[-2]
                X = pd.concat([X, file_content])

    #add the columns names to both dataframes
    X.columns = INPUT_COLUMNS
    y.columns = [TARGET_COLUMN]

    #unify both dataframes
    data = pd.concat([X, y], axis=1)

    data.reset_index(inplace=True)    
    none_days = data[data[TARGET_COLUMN].isna()]
    data = data.drop(none_days.index)        

    if not os.path.isdir(f"{os.getcwd()}/data"):
        os.mkdir(f"{os.getcwd()}/data")


    data = data.drop(columns=['index'])
    data.to_csv(f"{os.getcwd()}/data/{filename}", index=False)

def expand_data(dataframe: pd.DataFrame, column: str, variable: str) -> dict:
    """Expandas the column shape of the data to an actual n X m grid

    Keywords arguments:
    dataframe -- data to be expanded
    column -- column that will be used to expand the dataframe
    variable -- column (variable) that will be part of the grid
    """
    result = []
    for i in dataframe[variable].unique():
        coluna_resutl = dataframe.loc[dataframe[variable] == i][column].to_numpy()
        result.append(coluna_resutl)

    return np.array(result)

