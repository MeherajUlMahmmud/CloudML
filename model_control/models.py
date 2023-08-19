from django.db import models

from common.choices import ColumnScalingTypeChoices, ColumnEncodingTypeChoices, TrainModelTypeChoices
from common.models import BaseModel
from user_control.models import UserModel


class ProjectModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='project_models')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        db_table = 'project_model'

        verbose_name = 'Project Model'
        verbose_name_plural = 'Project Models'


class DatasetModel(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    dataset = models.FileField(upload_to='datasets/')
    dataset_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    project_model = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, related_name='dataset_models')

    def __str__(self):
        return self.project_model.name + ' - ' + self.name

    class Meta:
        ordering = ['-created_at']
        db_table = 'dataset_model'

        verbose_name = 'Dataset Model'
        verbose_name_plural = 'Dataset Models'


class ColumnModel(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    dataset_model = models.ForeignKey(DatasetModel, on_delete=models.CASCADE, related_name='column_models')
    encoding_type = models.CharField(
        max_length=100, null=True, blank=True,
        choices=ColumnEncodingTypeChoices.choices,
    )
    scaling_type = models.CharField(
        max_length=100, null=True, blank=True,
        choices=ColumnScalingTypeChoices.choices,
    )
    is_numeric = models.BooleanField(default=False)
    is_feature = models.BooleanField(default=False)
    is_target = models.BooleanField(default=False)

    def __str__(self):
        return self.dataset_model.name + ' - ' + self.name

    class Meta:
        ordering = ['created_at']
        db_table = 'column_model'

        verbose_name = 'Column Model'
        verbose_name_plural = 'Column Models'


class TrainModel(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    dataset_model = models.ForeignKey(DatasetModel, on_delete=models.CASCADE, related_name='train_models')
    project_model = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, related_name='train_models')
    model_type = models.CharField(max_length=100, choices=TrainModelTypeChoices.choices)
    test_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    model = models.FileField(upload_to='models/')
    # Hyperparameters are the parameters that are set before training the model
    hyperparameters = models.JSONField(null=True, blank=True)
    # Metrics are the result of model evaluation
    metrics = models.JSONField(null=True, blank=True)
    plots = models.JSONField(null=True, blank=True)
    is_training = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.project_model.name + ' - ' + self.dataset_model.name + ' - ' + self.name

    class Meta:
        ordering = ['-created_at']
        db_table = 'train_model'

        verbose_name = 'Train Model'
        verbose_name_plural = 'Train Models'
