import kagglehub
import os
import shutil

path = kagglehub.dataset_download("shakilrana/octdl-retinal-oct-images-dataset")

print("Path to dataset files:", path)


cwd = os.getcwd()
target_path = os.path.join(cwd, "octdl_dataset")

if os.path.exists(target_path):
    shutil.rmtree(target_path)

shutil.copytree(path, target_path)

print("Dataset copied to:", target_path)