from django.db import models


class ColumnEncodingTypeChoices(models.TextChoices):
    NONE = 'NONE', 'None'
    ONE_HOT = 'ONE_HOT', 'One Hot'
    LABEL = 'LABEL', 'Label'


class ColumnScalingTypeChoices(models.TextChoices):
    NONE = 'NONE', 'None'
    STANDARD = 'STANDARD', 'Standard'
    MIN_MAX = 'MIN_MAX', 'Min Max'
    MAX_ABS = 'MAX_ABS', 'Max Abs'
    ROBUST = 'ROBUST', 'Robust'
    NORMALIZER = 'NORMALIZER', 'Normalizer'


class TrainModelTypeChoices(models.TextChoices):
    LINEAR_REGRESSION = 'LINEAR_REGRESSION', 'Linear Regression'
    LOGISTIC_REGRESSION = 'LOGISTIC_REGRESSION', 'Logistic Regression'
    DECISION_TREE = 'DECISION_TREE', 'Decision Tree'
    RANDOM_FOREST = 'RANDOM_FOREST', 'Random Forest'
    SUPPORT_VECTOR_MACHINE = 'SUPPORT_VECTOR_MACHINE', 'Support Vector Machine'
    K_NEAREST_NEIGHBORS = 'K_NEAREST_NEIGHBORS', 'K Nearest Neighbors'
    NAIVE_BAYES = 'NAIVE_BAYES', 'Naive Bayes'
    K_MEANS = 'K_MEANS', 'K Means'
