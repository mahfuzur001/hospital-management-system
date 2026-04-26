from django.urls import path
from .views import ReviewListCreateView

urlpatterns = [
    # GET → list reviews
    # POST → create review
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
]