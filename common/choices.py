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
    POLYNOMIAL_REGRESSION = 'POLYNOMIAL_REGRESSION', 'Polynomial Regression'
    RIDGE_REGRESSION = 'RIDGE_REGRESSION', 'Ridge Regression'
    LASSO_REGRESSION = 'LASSO_REGRESSION', 'Lasso Regression'
    ELASTIC_NET = 'ELASTIC_NET', 'Elastic Net'
    DECISION_TREE = 'DECISION_TREE', 'Decision Tree'
    RANDOM_FOREST = 'RANDOM_FOREST', 'Random Forest'
    SUPPORT_VECTOR_MACHINE = 'SUPPORT_VECTOR_MACHINE', 'Support Vector Machine'
    K_NEAREST_NEIGHBORS = 'K_NEAREST_NEIGHBORS', 'K Nearest Neighbors'
    NAIVE_BAYES = 'NAIVE_BAYES', 'Naive Bayes'
    K_MEANS = 'K_MEANS', 'K Means'


class ModelDefaultHyperParameterChoices(models.TextChoices):
    LINEAR_REGRESSION = 'LINEAR_REGRESSION', {
        'fit_intercept': True, # Whether to calculate the intercept for this model. If set to False, no intercept will be used in calculations (i.e. data is expected to be centered).
        'normalize': False, # This parameter is ignored when fit_intercept is set to False. If True, the regressors X will be normalized before regression by subtracting the mean and dividing by the l2-norm. If you wish to standardize, please use sklearn.preprocessing.StandardScaler before calling fit on an estimator with normalize=False.
        'copy_X': True, # If True, X will be copied; else, it may be overwritten. We set this to True by default so that it is safe to call fit(X, y) more than once.
        'n_jobs': None, # The number of jobs to use for the computation. This will only provide speedup for n_targets > 1 and sufficient large problems. None means 1 unless in a joblib.parallel_backend context. -1 means using all processors. See Glossary for more details.
    }
    LOGISTIC_REGRESSION = 'LOGISTIC_REGRESSION', {
        'penalty': 'l2', # Used to specify the norm used in the penalization. The ‘newton-cg’, ‘sag’ and ‘lbfgs’ solvers support only l2 penalties. ‘elasticnet’ is only supported by the ‘saga’ solver. If ‘none’ (not supported by the liblinear solver), no regularization is applied.
        'dual': False, # Dual or primal formulation. Dual formulation is only implemented for l2 penalty with liblinear solver. Prefer dual=False when n_samples > n_features.
        'tol': 0.0001, # Tolerance for stopping criteria.
        'C': 1.0, # Inverse of regularization strength; must be a positive float. Like in support vector machines, smaller values specify stronger regularization.
        'fit_intercept': True, # Specifies if a constant (a.k.a. bias or intercept) should be added to the decision function.
        'intercept_scaling': 1, # Useful only when the solver ‘liblinear’ is used and self.fit_intercept is set to True. In this case, x becomes [x, self.intercept_scaling], i.e. a “synthetic” feature with constant value equal to intercept_scaling is appended to the instance vector. The intercept becomes intercept_scaling * synthetic_feature_weight.
        'class_weight': None,
        'random_state': None,
        'solver': 'lbfgs',
        'max_iter': 100,
        'multi_class': 'auto',
        'verbose': 0,
        'warm_start': False,
        'n_jobs': None,
        'l1_ratio': None,
    }
    POLYNOMIAL_REGRESSION = 'POLYNOMIAL_REGRESSION', {
        'degree': 2,
        'interaction_only': False,
        'include_bias': True,
        'order': 'C',
    }
    RIDGE_REGRESSION = 'RIDGE_REGRESSION', {
        'alpha': 1.0,
        'fit_intercept': True,
        'normalize': False,
        'copy_X': True,
        'max_iter': None,
        'tol': 0.001,
        'solver': 'auto',
        'random_state': None,
    }
    LASSO_REGRESSION = 'LASSO_REGRESSION', {
        'alpha': 1.0,
        'fit_intercept': True,
        'normalize': False,
        'precompute': False,
        'copy_X': True,
        'max_iter': 1000,
        'tol': 0.0001,
        'warm_start': False,
        'positive': False,
        'random_state': None,
        'selection': 'cyclic',
    }
    ELASTIC_NET = 'ELASTIC_NET', {
        'alpha': 1.0,
        'l1_ratio': 0.5,
        'fit_intercept': True,
        'normalize': False,
        'precompute': False,
        'max_iter': 1000,
        'copy_X': True,
        'tol': 0.0001,
        'warm_start': False,
        'positive': False,
        'random_state': None,
        'selection': 'cyclic',
    }
    DECISION_TREE = 'DECISION_TREE', {
        'criterion': 'gini',
        'splitter': 'best',
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
        'min_weight_fraction_leaf': 0.0,
        'max_features': None,
        'random_state': None,
        'max_leaf_nodes': None,
        'min_impurity_decrease': 0.0,
        'min_impurity_split': None,
        'class_weight': None,
        'presort': False,
    }
    RANDOM_FOREST = 'RANDOM_FOREST', {
        'n_estimators': 100,
        'criterion': 'gini',
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
        'min_weight_fraction_leaf': 0.0,
        'max_features': 'auto',
        'max_leaf_nodes': None,
        'min_impurity_decrease': 0.0,
        'min_impurity_split': None,
        'bootstrap': True,
        'oob_score': False,
        'n_jobs': None,
        'random_state': None,
        'verbose': 0,
        'warm_start': False,
        'class_weight': None,
    }
    SUPPORT_VECTOR_MACHINE = 'SUPPORT_VECTOR_MACHINE', {
        'C': 1.0,
        'kernel': 'rbf',
        'degree': 3,
        'gamma': 'scale',
        'coef0': 0.0,
        'shrinking': True,
        'probability': False,
        'tol': 0.001,
        'cache_size': 200,
        'class_weight': None,
        'verbose': False,
        'max_iter': -1,
        'decision_function_shape': 'ovr',
        'break_ties': False,
        'random_state': None,
    }
    K_NEAREST_NEIGHBORS = 'K_NEAREST_NEIGHBORS', {
        'n_neighbors': 5,
        'weights': 'uniform',
        'algorithm': 'auto',
        'leaf_size': 30,
        'p': 2,
        'metric': 'minkowski',
        'metric_params': None,
        'n_jobs': None,
    }
    NAIVE_BAYES = 'NAIVE_BAYES', {
        'priors': None,
        'var_smoothing': 1e-09,
    }
    K_MEANS = 'K_MEANS', {
        'n_clusters': 8,
        'init': 'k-means++',
        'n_init': 10,
        'max_iter': 300,
        'tol': 0.0001,
        'precompute_distances': 'auto',
        'verbose': 0,
        'random_state': None,
        'copy_x': True,
        'n_jobs': None,
        'algorithm': 'auto',
    }
