from django.urls import include, path, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'dependencias', views.DependenciaViewSet)
router.register(r'plantillas', views.PlantillaViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'usuarios_cursos', views.Usuario_CursoViewSet)

from . import views

urlpatterns = [
    path('', include(router.urls)),
    path('cursos/<str:id>/usuarios', views.consultarUsuarios, name="usuarios_curso"),
    path('consultar/<str:id>', views.consultarCertificados, name="consultar"),
    path('verificar/<str:codigo>', views.verificarCertificado, name="verificar"),
    path('descargar/<str:codigo>', views.descargarCertificado, name="descargar"),
    re_path(r'^upload/$', views.FileUploadView.as_view(), name="subir")
]
