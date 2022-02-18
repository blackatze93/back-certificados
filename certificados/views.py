
from rest_framework import views, viewsets
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from xml.dom import minidom
import pandas as pd
import os, magic

from .models import Certificado, Curso, Dependencia, Plantilla, Usuario, Usuario_Curso
from .serializers import CursoSerializer, DependenciaSerializer, PlantillaSerializer, Usuario_CursoSerializer, UsuarioSerializer


class DependenciaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver o editar dependencias.
    """
    queryset = Dependencia.objects.all().order_by("-nombre")
    serializer_class = DependenciaSerializer


class PlantillaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver o editar plantillas.
    """
    queryset = Plantilla.objects.all().order_by("-fecha_creacion")
    serializer_class = PlantillaSerializer


class CursoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver o editar cursos.
    """
    queryset = Curso.objects.all().order_by("-fecha_creacion")
    serializer_class = CursoSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver o editar cursos.
    """
    queryset = Usuario.objects.all().order_by("-fecha_creacion")
    serializer_class = UsuarioSerializer


class Usuario_CursoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver o editar usuario_curso.
    """
    queryset = Usuario_Curso.objects.all()
    serializer_class = Usuario_CursoSerializer


class FileUploadView(views.APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        file_obj = request.data['file']
        content_type = magic.from_buffer(file_obj.file.read(2048), mime=True)
        if content_type != 'text/csv':
            return HttpResponse('Tipo no soportado', status=406)
        else: 
            df = pd.read_csv(file_obj)
            print(request.data)
            print(df)
            # TODO: Save in the database the data from participants
            return HttpResponse(status=204)


@require_GET
def consultarCertificados(request, id):
    try:
        certificados = []
        usuario = Usuario.objects.get(numero_id=id)
        query_certificados = Certificado.objects.filter(
            usuario=usuario).values()
        for row in query_certificados:
            cert = {}
            curso = Curso.objects.get(id=row['curso_id'])
            cert['codigo_verificacion'] = row['codigo_verificacion']
            cert['fecha_generacion'] = row['fecha_generacion']
            cert['curso'] = curso.nombre
            certificados.append(cert)
        return JsonResponse({id: str(usuario), 'certificados': certificados})
    except Exception as e:
        return JsonResponse({"error": str(e)})


@require_GET
def verificarCertificado(request, codigo):
    try:
        certificado = {}
        query_certificado = Certificado.objects.get(codigo_verificacion=codigo)
        certificado['nombre'] = str(query_certificado.usuario)
        certificado['documento'] = query_certificado.usuario.numero_id
        certificado['fecha'] = query_certificado.fecha_generacion
        certificado['curso'] = str(query_certificado.curso)
        return JsonResponse({codigo: certificado})
    except Exception as e:
        return JsonResponse({"error": str(e)})


@require_GET
def consultarUsuarios(request, id):
    try:
        usuarios = []
        curso = Curso.objects.get(id=id)
        query_usuarios_curso = Usuario_Curso.objects.filter(
            curso=curso).values()
        for row in query_usuarios_curso:
            usr = {}
            usuario = Usuario.objects.get(id=row['usuario_id'])
            usr['tipo_id'] = usuario.tipo_id
            usr['numero_id'] = usuario.numero_id
            usr['nombre'] = usuario.nombre
            usr['apellido'] = usuario.apellido
            usr['correo'] = usuario.correo
            usr['fecha_inicio'] = row['fecha_inicio']
            usr['fecha_completado'] = row['fecha_completado']
            usr['estado'] = row['estado']
            usuarios.append(usr)
        return JsonResponse({id: str(curso), 'usuarios': usuarios})
    except Exception as e:
        return JsonResponse({"error": str(e)})


# TODO: Generar certificado
# https://rita.udistrital.edu.co/rita/certificados/descargar/cod_certificado
def descargarCertificado(request, codigo):
    ruta_generados = os.path.join(settings.BASE_DIR, 'media', 'generados')
    outputfile = ruta_generados + "/" + "certificado-" + codigo + ".pdf"
    if not os.path.isfile(outputfile):
        try:
            certificado = {}
            query_certificado = Certificado.objects.get(codigo_verificacion=codigo)
            certificado['codigo'] = codigo
            certificado['nombre'] = str(query_certificado.usuario)
            certificado['documento'] = query_certificado.usuario.numero_id
            certificado['fecha_generacion'] = query_certificado.fecha_generacion.date()
            certificado['nombre_curso'] = str(query_certificado.curso.nombre)
            certificado['fecha_curso'] = query_certificado.curso.fecha_lanzamiento
            certificado['template_file'] = os.path.join(settings.BASE_DIR, 'media', str(query_certificado.curso.plantilla.archivo))            
            generarCertificado(certificado)
        except Exception as e:
            return JsonResponse({"error": str(e)})
        
    with open(outputfile, 'rb') as pdf:
        response = HttpResponse(pdf.read())
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline; filename=\"'+codigo+'.pdf\"'
        
        return response
    

def generarCertificado(certificado):
    xml_documento = minidom.parse(certificado['template_file'])
    nodos = xml_documento.getElementsByTagName("tspan")
    nodosFluid = xml_documento.getElementsByTagName("flowPara")
    nodo1 = nodo2 = nodo3 = nodo4 = nodo5 = nodo6 = nodo7 = nodo8 = nodo9 = nodo10 = None
    
    #Los identificadores deben ser puestos previamente en el archivo SVG que sirve como plantilla
    ids=["nombre_miembro","cedula_miembro","nombre_evento","mes_certificacion","dia_certificacion_numeros","dia_certificacion_letras","mes_impartido","ano_certificacion_numeros","ano_impartido","codigo_verificacion"]
        
    for nodo in nodos:
        if nodo.getAttribute("id")==ids[0]:
            nodo1 = nodo
        elif nodo.getAttribute("id")==ids[1]:
            nodo2 = nodo
        elif nodo.getAttribute("id")==ids[2]:
            nodo3 = nodo
        elif nodo.getAttribute("id")==ids[3]:
            nodo4 = nodo
        elif nodo.getAttribute("id")==ids[4]:
            nodo5 = nodo
        elif nodo.getAttribute("id")==ids[5]:
            nodo6 = nodo
        elif nodo.getAttribute("id")==ids[6]:
            nodo7 = nodo
        elif nodo.getAttribute("id")==ids[7]:
            nodo8 = nodo
        elif nodo.getAttribute("id")==ids[8]:
            nodo9 = nodo
        elif nodo.getAttribute("id")==ids[9]:
            nodo10 = nodo

    for nodoFluid in nodosFluid:
        if nodoFluid.getAttribute("id")==ids[2]:
            nodo3 = nodoFluid

    ids=["nombre_miembro","cedula_miembro","nombre_evento","mes_certificacion","dia_certificacion_numeros","dia_certificacion_letras","mes_impartido","ano_certificacion_numeros","ano_impartido","codigo_verificacion"]

    [ano_curso,mes_curso,dia_curso] = str(certificado['fecha_curso']).split("-")
    [ano_generacion,mes_generacion,dia_generacion] = str(certificado['fecha_generacion']).split("-")
    
    dia_certificacion_letras = obtenerNombreNumero(dia_generacion)
    dia_certificacion_numeros = dia_generacion
    mes_certificacion = obtenerNombreMes(mes_generacion)
    ano_impartido = ano_curso
    ano_certificacion_numeros = ano_generacion
    mes_impartido = obtenerNombreMes(mes_curso)

    # nombre_miembro
    if(nodo1):
        nodo1.firstChild.replaceWholeText(certificado['nombre'])
    # cedula_miembro
    if(nodo2):
        nodo2.firstChild.replaceWholeText(certificado['documento'])
    # nombre_miembro
    if(nodo3):
        nodo3.firstChild.replaceWholeText(certificado['nombre_curso'])
    # mes_certificacion    
    if(nodo4):
        nodo4.firstChild.replaceWholeText(mes_certificacion)
    # dia_certificacion_numeros
    if(nodo5):
        nodo5.firstChild.replaceWholeText(dia_certificacion_numeros)
    # dia_certificacion_letras
    if(nodo6):
        nodo6.firstChild.replaceWholeText(dia_certificacion_letras)
    # mes_impartido
    if(nodo7):
        nodo7.firstChild.replaceWholeText(mes_impartido)
    # ano_certificacion_numeros
    if(nodo8):
        nodo8.firstChild.replaceWholeText(ano_certificacion_numeros)
    # ano_impartido
    if(nodo9):
        nodo9.firstChild.replaceWholeText(ano_impartido)
    # codigo_verificacion
    if(nodo10):
        nodo10.firstChild.replaceWholeText(certificado['codigo'])

    out_file="/tmp/output_generarpdf.svg"
    try:
        file_handle = open(out_file,"w+",encoding="utf-8")
        texto = xml_documento.toxml()
        file_handle.write(texto)
        file_handle.close()
    except Exception as e:
        return "Error SVG: " + str(e)
    
    ruta_generados = os.path.join(settings.BASE_DIR, 'media', 'generados')
    outputfile = ruta_generados + "/" + "certificado-" + certificado['codigo'] + ".pdf"

    try:
        comando = "inkscape \"%s\" --export-filename=\"%s\"" % (out_file, outputfile)
        os.system(comando.encode('utf8'))
        os.remove(out_file)
    except Exception as e:
        return "Error Inkscape: " + str(e)
    
    return outputfile

def obtenerNombreMes(mes):
	meses = {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'};
	return meses[mes]

def obtenerNombreNumero(dia):
	dias = ('','uno ', 'dos ','tres ','cuatro ','cinco ','seis ','siete ','ocho ','nueve ','diez ','once ','doce ','trece ','catorce ','quince ','dieciseis ','diecisiete ','dieciocho ','diecinueve ','veinte ','veintiún ', 'veintidos ','veintitres ', 'veinticuatro ', 'veinticinco ','veintiseis ','veintisiete ','veintiocho ','veintinueve ','treinta ','treina y un ')
	return dias[int(dia)]

def obtenerNombreAno(ano):
	anos = {'2014': 'Dos mil catorce', '2015': 'Dos mil quince', '2016': 'Dos mil dieciseis', '2017': 'Dos mil diecisiete', '2018': 'Dos mil dieciocho', '2019': 'Dos mil diecinueve', '2020': 'Dos mil veinte', '2021':'Dos mil veintiuno', '2022':'Dos mil veintidos', '2023':'Dos mil veintitres', '2024':'Dos mil veinticuatro', '2025':'Dos mil veinticinco'}
	return anos[ano.strip()]
