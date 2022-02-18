# serializers.py
from django.db.models import fields
from rest_framework import serializers, permissions

from .models import *

class DependenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dependencia
        fields = ['id', 'nombre', 'descripcion', 'pagina_web', 'fecha_creacion']


class PlantillaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plantilla
        fields = ['id', 'nombre', 'archivo', 'dependencia', 'fecha_creacion']


class CursoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Curso
        fields = ['id', 'nombre', 'descripcion', 'fecha_lanzamiento', 'fecha_cierre', 'dependencia', 'fecha_creacion', 'plantilla']
        

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'tipo_id', 'numero_id', 'nombre', 'apellido', 'correo', 'fecha_creacion', 'cursos']


class Usuario_CursoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario_Curso
        fields = ['id', 'usuario', 'curso', 'fecha_inicio', 'fecha_completado', 'estado']
