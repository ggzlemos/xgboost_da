import os 
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
        for file in files:                
            file_path = os.path.join(subdir, file)
            file_content = pd.read_csv(file_path)

            if TARGET_FILE_NAME in file_path:          
                y = pd.concat([y, file_content])
            else:
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