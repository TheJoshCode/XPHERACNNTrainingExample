import os
import tarfile
import urllib.request
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split

# CHATGPT WAS USED FOR ORGANIZATION, BLOCKOUT FUNCTION NAMES/PLACEMENT BY ME

# DOWNLOADING DATASET
def download_cifar10(url, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    filename = url.split('/')[-1]
    file_path = os.path.join(download_path, filename)
    
    # CHECK IF THE DATASET EXISTS, IF NOT, DOWNLOAD FROM LINK
    if not os.path.exists(file_path):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded {filename}.")

    return file_path

# UNPACK DATASET
def extract_cifar10(file_path, extract_to):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    print(f"Extracting {file_path}...")
    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(path=extract_to)
    print(f"Extracted to {extract_to}.")

# lOAD DATASET
def load_cifar10_data(data_dir):
    def unpickle(file):
        with open(file, 'rb') as fo:
            data_dict = pickle.load(fo, encoding='bytes')
        return data_dict

    # LOAD DATASET FOR TRAINING
    X_train, y_train = [], []
    for batch_num in range(1, 6):
        batch_file = os.path.join(data_dir, f"data_batch_{batch_num}")
        batch_data = unpickle(batch_file)
        X_train.append(batch_data[b"data"])
        y_train.append(batch_data[b"labels"])

    X_train = np.concatenate(X_train)
    y_train = np.concatenate(y_train)

    # LOAD TEST DATA FOR COMPARISON
    test_batch_file = os.path.join(data_dir, "test_batch")
    test_data = unpickle(test_batch_file)
    X_test = test_data[b"data"]
    y_test = test_data[b"labels"]

    # CONVERT TRAINING MATRIX FORMAT
    X_train = X_train.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
    X_test = X_test.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)

    # NORMALIZE COLOR DATA TO 255 BAND
    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0

    return X_train, y_train, X_test, y_test

# MODEL DEFINING
def create_model():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')  # 10 classes for CIFAR-10
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

# TRAINING
def train_model(model, X_train, y_train, X_test, y_test):
    # SPLIT TRAINING DATA INTO AXIS
    X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(X_train, y_train, test_size=0.1, random_state=42)

    # TRAIN
    model.fit(X_train_split, y_train_split, epochs=10, batch_size=64, validation_data=(X_val_split, y_val_split))

    # EVAL/TEST MODEL
    test_loss, test_acc = model.evaluate(X_test, y_test)
    
    # READOUT FOR MODEL ACCURACY
    print(f"Test accuracy: {test_acc * 100:.2f}%")

# MAIN EXEC FUNCTION
def main():

    # LINK TO TRAINING DATASET
    url = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
    download_path = "data/cifar-10"
    extract_path = "data/cifar-10-extracted"

    # DOWNLOAD/EXTRACT DATASET
    file_path = download_cifar10(url, download_path)
    extract_cifar10(file_path, extract_path)

    # LOAD DATASET & SPLIT INTO AXIS FOR ANALYSIS
    X_train, y_train, X_test, y_test = load_cifar10_data(extract_path)

    # MAKE AND TRAIN MODEL
    model = create_model()
    train_model(model, X_train, y_train, X_test, y_test)

# EXEC MAIN FUNCTION
if __name__ == "__main__":
    main()
