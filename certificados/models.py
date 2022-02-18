from random import randint
import magic
from django.db import models
from django.core.exceptions import ValidationError


def validate_svg(value):
    content_type = magic.from_buffer(value.file.read(2048), mime=True)
    if content_type != 'image/svg+xml':
        raise ValidationError(u'Tipo no soportado')


class Dependencia(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50)
    pagina_web = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.nombre


class Plantilla(models.Model):
    nombre = models.CharField(max_length=50)
    archivo = models.FileField(upload_to='plantillas', validators=[validate_svg])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nombre


class Curso(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=50)
    fecha_lanzamiento = models.DateField()
    fecha_cierre = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nombre


class Usuario(models.Model):
    TIPOS_ID = [
        ('CC', 'Cédula de ciudadanía'),
        ('CE', 'Cédula de extranjería'),
        ('TI', 'Tarjeta de identidad '),
        ('NIT', 'NIT'),

    ]
    tipo_id = models.CharField(max_length=3, choices=TIPOS_ID, default='CC')
    numero_id = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=50, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cursos = models.ManyToManyField(Curso, through='Usuario_Curso')

    def __str__(self) -> str:
        return self.nombre + ' ' + self.apellido


class Usuario_Curso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_completado = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'curso'], name='unico usuario_curso')
        ]


class Certificado(models.Model):
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    codigo_verificacion = models.CharField(max_length=50, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'curso'], name='unico certificado')
        ]

    def obtenerCodigo(self, curso_id, usuario_id):
        aleatorio = str(randint(100, 999))
        curso = str(curso_id).zfill(3)
        usuario = str(usuario_id).zfill(5)
        codigoNumero = int(aleatorio+curso+usuario)
        codigoHex = hex(codigoNumero)
        return str(codigoHex).upper()

    def save(self, *args, **kwargs):        
        super().save(*args, **kwargs)
        if not self.codigo_verificacion:
            self.codigo_verificacion = self.obtenerCodigo(self.curso.id, self.usuario.id)
            self.save()

    def __str__(self) -> str:
        return self.codigo_verificacion


class Sesion(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nombre


class Encuesta(models.Model):
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    contenido = models.IntegerField(blank=True, null=True)
    utilidad = models.IntegerField(blank=True, null=True)
    desempeno = models.IntegerField(blank=True, null=True)
    claridad = models.IntegerField(blank=True, null=True)
    mejoras = models.TextField(blank=True, null=True)
    otras_capacitaciones = models.TextField(blank=True, null=True)
