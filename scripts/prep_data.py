import shutil
import os

import pandas as pd

data_dir = "./data/"

train_data = pd.read_csv(f"{data_dir}train_classes.csv")
test_data = pd.read_csv(f"{data_dir}test_classes.csv")

train_rust = train_data[
    (train_data["rust"] == 1) & (train_data["miner"] != 1) & (train_data["phoma"] != 1)
]
train_rust_ids = train_rust["id"].to_list()

other_train_ids = train_data[(train_data["rust"] == 0)]["id"].to_list()

test_rust = test_data[
    (test_data["rust"] == 1) & (test_data["miner"] != 1) & (test_data["phoma"] != 1)
]
test_rust_ids = test_rust["id"].to_list()

other_test_ids = test_data[(test_data["rust"] == 0)]["id"].to_list()

print(f"Number of train rust images: {len(train_rust_ids)}")
print(f"Number of test rust images: {len(test_rust_ids)}")

train_dir = f"{data_dir}/coffee-leaf-diseases/train/images"

os.mkdir(f"{train_dir}/rust")
os.mkdir(f"{train_dir}/other")

test_dir = f"{data_dir}/coffee-leaf-diseases/test/images"

os.mkdir(f"{test_dir}/rust")
os.mkdir(f"{test_dir}/other")

for n in train_rust_ids:
    shutil.move(f"{train_dir}/{n}.jpg", f"{train_dir}/rust/")

for n in test_rust_ids:
    shutil.move(f"{test_dir}/{n}.jpg", f"{test_dir}/rust/")

for n in other_train_ids:
    shutil.move(f"{train_dir}/{n}.jpg", f"{train_dir}/other/")

for n in other_test_ids:
    shutil.move(f"{test_dir}/{n}.jpg", f"{test_dir}/other/")
