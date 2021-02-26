from django.urls import path
from api.views import ImageView, Base64ImageView

urlpatterns = [
    # path('predict-breed',PredictBreed.as_view()),
    path('image-view',ImageView.as_view(),),
    path('base64image-view',Base64ImageView.as_view(),)
]