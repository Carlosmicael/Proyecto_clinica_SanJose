from django.urls import path
from .views import CustomTokenObtainPairView,UserInfoView,AdminView,DatosMongoView,AdminPostEspe,personAdmin # Asegúrate de importar EspecialidadesView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user-info/', UserInfoView.as_view(), name='user_info'),
    path('admin/', AdminView.as_view(), name='admin_view'),
    path('mongo/', DatosMongoView.as_view(), name='datos_mongo'),
    path('postEspe/', AdminPostEspe.as_view(), name='datos_mongo'),
    path('personAdmin/', personAdmin.as_view(), name='datos_mongo'),
]
