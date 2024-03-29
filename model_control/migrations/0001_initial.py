# Generated by Django 4.2.4 on 2024-01-29 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('dataset', models.FileField(upload_to='datasets/')),
                ('dataset_size', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'Dataset Model',
                'verbose_name_plural': 'Dataset Models',
                'db_table': 'dataset_model',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_models', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Project Model',
                'verbose_name_plural': 'Project Models',
                'db_table': 'project_model',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TrainModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('model_type', models.CharField(choices=[('LINEAR_REGRESSION', 'Linear Regression'), ('LOGISTIC_REGRESSION', 'Logistic Regression'), ('POLYNOMIAL_REGRESSION', 'Polynomial Regression'), ('RIDGE_REGRESSION', 'Ridge Regression'), ('LASSO_REGRESSION', 'Lasso Regression'), ('ELASTIC_NET', 'Elastic Net'), ('DECISION_TREE', 'Decision Tree'), ('RANDOM_FOREST', 'Random Forest'), ('SUPPORT_VECTOR_MACHINE', 'Support Vector Machine'), ('K_NEAREST_NEIGHBORS', 'K Nearest Neighbors'), ('NAIVE_BAYES', 'Naive Bayes'), ('K_MEANS', 'K Means')], max_length=100)),
                ('test_size', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('model', models.FileField(upload_to='models/')),
                ('hyperparameters', models.JSONField(blank=True, null=True)),
                ('metrics', models.JSONField(blank=True, null=True)),
                ('plots', models.JSONField(blank=True, null=True)),
                ('is_training', models.BooleanField(default=False)),
                ('is_complete', models.BooleanField(default=False)),
                ('dataset_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='train_models', to='model_control.datasetmodel')),
                ('project_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='train_models', to='model_control.projectmodel')),
            ],
            options={
                'verbose_name': 'Train Model',
                'verbose_name_plural': 'Train Models',
                'db_table': 'train_model',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='datasetmodel',
            name='project_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataset_models', to='model_control.projectmodel'),
        ),
        migrations.CreateModel(
            name='ColumnModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('encoding_type', models.CharField(blank=True, choices=[('NONE', 'None'), ('ONE_HOT', 'One Hot'), ('LABEL', 'Label')], max_length=100, null=True)),
                ('scaling_type', models.CharField(blank=True, choices=[('NONE', 'None'), ('STANDARD', 'Standard'), ('MIN_MAX', 'Min Max'), ('MAX_ABS', 'Max Abs'), ('ROBUST', 'Robust'), ('NORMALIZER', 'Normalizer')], max_length=100, null=True)),
                ('is_numeric', models.BooleanField(default=False)),
                ('is_feature', models.BooleanField(default=False)),
                ('is_target', models.BooleanField(default=False)),
                ('dataset_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='column_models', to='model_control.datasetmodel')),
            ],
            options={
                'verbose_name': 'Column Model',
                'verbose_name_plural': 'Column Models',
                'db_table': 'column_model',
                'ordering': ['created_at'],
            },
        ),
    ]
