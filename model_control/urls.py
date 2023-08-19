from django.urls import path, include
from rest_framework import routers

from model_control.views.column import ColumnModelViewSet, UpdateColumnModelAPIView
from model_control.views.dataset import DatasetModelViewSet
from model_control.views.project import ProjectModelViewSet
from model_control.views.train_model import TrainModelViewSet

router = routers.DefaultRouter()
router.register(r'project', ProjectModelViewSet, basename='project')
router.register(r'dataset', DatasetModelViewSet, basename='dataset')
router.register(r'column', ColumnModelViewSet, basename='column')
router.register(r'trained-model', TrainModelViewSet, basename='train-model')


urlpatterns = [
    path('', include(router.urls)),
    path('column/update-columns/<str:dataset_id>', UpdateColumnModelAPIView.as_view()),
]
