from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo de Especialidad
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    owner_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'especialidad'

    def __str__(self):
        return self.nombre


# Modelo de Especialista
class Especialista(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)
    descripcion = models.TextField(blank=True, null=True)
    servicios = models.TextField(blank=True, null=True)
    especialidades = models.ManyToManyField(Especialidad, related_name="especialistas")
    owner_id = models.CharField(max_length=50, blank=True, null=True) 

    class Meta:
        db_table = 'especialista'

    def __str__(self):
        especialidades = ", ".join([especialidad.nombre for especialidad in self.especialidades.all()])
        return f"{self.nombre} {self.apellido} - {self.cedula} - {self.correo} - Especialidades: {especialidades}"


# Modelo de Horario
class Horario(models.Model):
    horas_disponibles = models.TimeField()
    horas_citas = models.TimeField()
    fecha = models.DateField()
    especialistas = models.ManyToManyField(Especialista, related_name="horarios")

    class Meta:
        db_table = 'horario'

    def __str__(self):
        especialistas = ", ".join([especialista.nombre + " " + especialista.apellido for especialista in self.especialistas.all()])
        return f"{self.horas_disponibles} - {self.horas_citas} - {self.fecha} - Especialistas: {especialistas}"
    
    

# Modelo de Usuario (heredado de AbstractUser)
class Usuario(AbstractUser):
    cedula = models.CharField(max_length=20, unique=True)
    owner_id = models.CharField(max_length=255, null=True, blank=True)  
    
    # Relacionar los grupos con un related_name único
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="usuarios_set",  # Cambié el nombre del accesor inverso
        blank=True
    )
    
    # Relacionar los permisos con un related_name único
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="usuarios_permissions_set",  # Cambié el nombre del accesor inverso
        blank=True
    )

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"

    

    

# Modelo de Cita
class Cita(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    correo = models.EmailField()
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name="citas")
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE, related_name="citas")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="citas", null=True, blank=True)
    edificio = models.CharField(max_length=100)
    consultorio = models.CharField(max_length=100)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()

    class Meta:
        db_table = 'cita'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula} - {self.correo} - Especialidad: {self.especialidad.nombre}"
