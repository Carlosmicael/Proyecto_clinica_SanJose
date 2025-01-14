from django.contrib import admin
from .models import Usuario
from .models import Especialidad
from .models import Especialista
from .models import Horario
from .models import Cita

admin.site.register(Usuario)
admin.site.register(Especialidad)
admin.site.register(Especialista)
admin.site.register(Horario)
admin.site.register(Cita)