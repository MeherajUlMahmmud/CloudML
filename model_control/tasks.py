from __future__ import absolute_import, unicode_literals

import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from celery import shared_task
import logging
from joblib import dump
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split

from common.choices import TrainModelTypeChoices
from model_control.models import TrainModel, DatasetModel, ColumnModel
from model_control.utils import get_numeric_columns, get_categorical_columns, validate_columns, \
    drop_unnecessary_columns, encode_dataset, save_plots

matplotlib.use('agg')


@shared_task
def preprocess_and_train_model(train_model_instance_id):
    logger = logging.getLogger(__name__)
    logger.info('---------preprocess_and_train_model----------')
    logger.info(train_model_instance_id)
    train_model_instance = TrainModel.objects.get(id=train_model_instance_id)
    logger.info(train_model_instance)
    dataset = DatasetModel.objects.get(id=train_model_instance.dataset_model.id).dataset
    columns = ColumnModel.objects.filter(dataset_model=train_model_instance.dataset_model)

    try:
        dataframe = pd.read_csv(dataset)
    except pd.errors.EmptyDataError:
        raise ValueError('The dataset is empty or could not be read.')

    numeric_columns = get_numeric_columns(dataframe)
    categorical_columns = get_categorical_columns(dataframe)

    is_valid = validate_columns(dataframe, columns, numeric_columns, categorical_columns)

    if not is_valid:
        raise Exception('Invalid columns')

    try:
        os.makedirs(f'media/data/{train_model_instance.id}', exist_ok=True)
        dataframe.to_csv(f'media/data/{train_model_instance.id}/dataset.csv', index=False)
    except OSError:
        logger.info('Creation of the directory failed for dataset')

    dataframe = drop_unnecessary_columns(dataframe, columns)

    encoded_dataframe = encode_dataset(dataframe, columns)
    try:
        encoded_dataframe.to_csv(f'media/data/{train_model_instance.id}/encoded_dataset.csv', index=False)
    except OSError:
        logger.info('Creation of the directory failed for encoded dataset')

    # save all the plots
    plots = save_plots(dataframe, columns, train_model_instance)

    target_column = [column.name for column in columns if column.is_target][0]
    X_data = encoded_dataframe.drop(columns=target_column)
    y_data = encoded_dataframe[target_column]

    # Split the data into train and test
    logger.info("Splitting the data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_data,
        y_data,
        test_size=float(train_model_instance.test_size),
        random_state=42,
        shuffle=True,
    )

    # train the model
    logger.info("Training the model...")
    trained_model = None
    if train_model_instance.model_type == TrainModelTypeChoices.LINEAR_REGRESSION:
        from sklearn.linear_model import LinearRegression
        trained_model = LinearRegression()
        trained_model.fit(X_train, y_train)
    # elif train_model_instance.model_type == TrainModelTypeChoices.LOGISTIC_REGRESSION:
    #     from sklearn.linear_model import LogisticRegression
    #     trained_model = LogisticRegression()
    #     trained_model.fit(X_train, y_train)
    else:
        raise ValueError('Unsupported model type')

    # save the hyperparameters
    train_model_instance.hyperparameters = {
        'test_size': float(train_model_instance.test_size),
    }

    # save the metrics
    logger.info("Calculating the metrics...")
    if train_model_instance.model_type == TrainModelTypeChoices.LINEAR_REGRESSION:
        y_pred = trained_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        train_model_instance.metrics = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
        }
    # elif train_model_instance.model_type == TrainModelTypeChoices.LOGISTIC_REGRESSION:
    #     y_pred = trained_model.predict(X_test)
    #     accuracy = accuracy_score(y_test, y_pred)
    #     train_model_instance.metrics = {
    #         'accuracy': accuracy,
    #     }

    # residual plot
    logger.info("Saving the residual plot...")
    plt.figure()
    plt.title('Residual Plot')
    plt.xlabel('Predicted')
    plt.ylabel('Residual')
    plt.scatter(y_pred, y_test - y_pred, alpha=0.5, label='x', color='blue', edgecolor='black')
    plt.savefig(f'media/data/{train_model_instance.id}/residual_plot.png')
    plots['residual plot'] = f'media/data/{train_model_instance.id}/residual_plot.png'
    plt.close()

    # save the model
    logger.info("Saving the model...")
    path = f'media/datasets/models'
    short_path = f'datasets/models'
    os.makedirs(path, exist_ok=True)
    model_save_path = f'{path}/{train_model_instance.id}_{train_model_instance.model_type}_model.joblib'
    dump(trained_model, model_save_path)

    logger.info("Saving the train model instance...")
    train_model_instance.model = short_path + f'/{train_model_instance.id}_{train_model_instance.model_type}_model.joblib'
    train_model_instance.plots = plots
    train_model_instance.is_training = False
    train_model_instance.is_complete = True
    train_model_instance.save()
