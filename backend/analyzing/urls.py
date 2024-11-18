from django.urls import path

from analyzing.views import SalesDataUploadView, GetSalesDataResultView

app_name = 'analyzing'

urlpatterns = [
    path('upload/', SalesDataUploadView.as_view(), name='upload-sales-data'),
    path('result/<uuid:uuid>/', GetSalesDataResultView.as_view(), name='get-sales-data-result'),
]
