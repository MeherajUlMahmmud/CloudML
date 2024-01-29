import os

import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common.choices import ColumnEncodingTypeChoices, ColumnScalingTypeChoices


def validate_columns(df, columns, numeric_columns, categorical_columns):
    df_columns = df.columns

    for column in columns:
        if column.name not in df_columns:
            # raise Exception('Invalid column name: ' + column.name)
            return False

        if column.is_numeric and column.name not in numeric_columns:
            # raise Exception('Invalid column type: ' + column.name + ' is not numeric')
            return False

        if not column.is_numeric and column.name not in categorical_columns:
            # raise Exception('Invalid column type: ' + column.name + ' is not categorical')
            return False

        if column.is_target and column.is_feature:
            # raise Exception('Invalid column type: ' + column.name + ' is both target and feature')
            return False

    return True


def drop_unnecessary_columns(df, columns):
    columns_to_drop = [column.name for column in columns if not column.is_feature and not column.is_target]
    df.drop(columns=columns_to_drop, inplace=True)

    return df


def encode_dataset(df, columns):
    columns_to_encode = []

    for column in columns:
        if not column.is_numeric:
            if column.encoding_type == ColumnEncodingTypeChoices.ONE_HOT.value:
                columns_to_encode.append(column.name)

    if columns_to_encode:
        encoded_df = pd.get_dummies(df, columns=columns_to_encode, prefix=columns_to_encode)
        df = pd.concat([df, encoded_df], axis=1)
        df.drop(columns=columns_to_encode, inplace=True)

    for column in columns:
        if column.is_numeric:
            if column.scaling_type == ColumnScalingTypeChoices.MIN_MAX.value:
                df[column.name] = (df[column.name] - df[column.name].min()) / (
                        df[column.name].max() - df[column.name].min())
            elif column.scaling_type == ColumnScalingTypeChoices.STANDARD.value:
                df[column.name] = (df[column.name] - df[column.name].mean()) / df[column.name].std()

    return df


def save_plots(df, columns, train_model_instance):
    plots_directory = f'media/data/{train_model_instance.id}/plots'

    # Create the directory if it doesn't exist
    os.makedirs(plots_directory, exist_ok=True)

    print(columns)
    print(df.columns)
    print(df.shape)
    plots = {}
    for column in columns:
        plt.figure()

        if not column.is_feature and not column.is_target:
            continue
        if column.is_numeric:
            plt.title(column.name)
            plt.xlabel(column.name)
            plt.ylabel('Count')
            plt.hist(df[column.name], bins=20, alpha=0.5, label='x', color='blue', edgecolor='black')
        else:
            plt.title(column.name)
            plt.xlabel(column.name)
            plt.ylabel('Count')
            df[column.name].value_counts().plot(kind='bar', color='blue', edgecolor='black', label='x')

        plt.savefig(f'{plots_directory}/{column.name}.png')
        plots[column.name] = f'{plots_directory}/{column.name}.png'
        plt.close()

    target_column = columns.get(is_target=True)
    feature_columns = columns.filter(is_feature=True)

    if target_column:
        print(target_column.name)
        for i in range(len(feature_columns)):
            print(feature_columns[i].name)
            plt.figure()
            plt.title(f'{feature_columns[i].name} vs {target_column.name}')
            plt.xlabel(target_column.name)
            plt.ylabel(feature_columns[i].name)
            plt.scatter(df[target_column.name], df[feature_columns[i].name], alpha=0.5, label='x', color='blue',
                        edgecolor='black')
            plt.savefig(f'{plots_directory}/{feature_columns[i].name} vs {target_column.name}.png')
            plots[
                f'{feature_columns[i].name} vs {target_column.name}'] = f'{plots_directory}/{feature_columns[i].name} vs {target_column.name}.png'
            plt.close()

    correlation_matrix = df.corr()
    plt.figure(figsize=(12, 9))
    sns.heatmap(correlation_matrix, cmap='YlGnBu', annot=True, linewidths=.5)
    plt.savefig(f'{plots_directory}/correlation_matrix.png')
    plots['correlation matrix'] = f'{plots_directory}/correlation_matrix.png'
    plt.close()

    return plots


def get_numeric_columns(df):
    columns = df.columns
    numeric_columns = []
    for column in columns:
        if df[column].dtype == 'int64' or df[column].dtype == 'float64':
            numeric_columns.append(column)
    return numeric_columns


def get_categorical_columns(df):
    columns = df.columns
    categorical_columns = []
    for column in columns:
        if df[column].dtype == 'object':
            categorical_columns.append(column)
    return categorical_columns
