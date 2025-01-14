from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Especialidad,Especialista
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import BasePermission
from mySql.utils.mongodb import MongoDBConnection
import base64
from io import BytesIO
import logging
from bson import ObjectId
logger = logging.getLogger(__name__)



# Esto te da el endpoint para obtener el token al hacer login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        logger.warning("esque te quiero wouuu")
        data = super().validate(attrs)
        data['is_superuser'] = self.user.is_superuser
        logger.warning(f"esque te quiero wouuu {data}")
        return data
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    


class AdminView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        imagenes = []
        image_data = BytesIO()


        especialidades = Especialidad.objects.all().order_by('id').values('nombre', 'owner_id')
        usuario = request.user.first_name
        db = MongoDBConnection.get_db()
        files_collection = db['fs.files']
        chunks_collection = db['fs.chunks']
        

        for especialidad in especialidades:
            owner_id = especialidad['owner_id']
            try:
                file_doc = files_collection.find_one({'_id': ObjectId(owner_id)})
            except Exception as e:
                logger.error(f"Error al convertir owner_id a ObjectId: {e}")
                continue    

            if not file_doc:
                logger.warning(f"No se encontró archivo para owner_id: {owner_id}")
                file_doc = files_collection.find_one({'_id': ObjectId('67776960474c4bd8ee017d42')})
                continue

            file_id = file_doc['_id']
            chunks = chunks_collection.find({'files_id': file_id}).sort('n', 1)
            

            image_data.truncate(0)
            image_data.seek(0)

            for chunk in chunks:
                image_data.write(chunk['data'])

            image_data.seek(0)
            encoded_image = base64.b64encode(image_data.read()).decode('utf-8')

            imagenes.append({
                'imagen': encoded_image,
                'metadatos': {
                    'filename': file_doc.get('filename', 'desconocido'),
                    'content_type': file_doc.get('contentType', 'unknown'),
                }
            })

        return Response({
            'especialidades': list(Especialidad.objects.all().order_by('id').values('nombre')),
            'imagenes': imagenes,
            'usuario': usuario,
        })
    

class AdminPostEspe(APIView):
        permission_classes = [IsSuperUser]
        def post(self, request):
            
            
            image_data = request.data.get('image')
            metadata = request.data.get('metadata', {})
            filename = metadata.get('filename', 'default_name')
            nameEspe = request.data.get('name')
            apelli = request.data.get('apellido')
            cedula = request.data.get('cedula')

            correo = request.data.get('correo')
            describe = request.data.get('describe')
            nuevas_especialidades = request.data.get('especialidades')
            list_nuevas_especialidades = [];
            service = request.data.get('servicios')

            if isinstance(nuevas_especialidades, list):
                list_nuevas_especialidades=nuevas_especialidades;
            else:
                list_nuevas_especialidades=[nuevas_especialidades];
            
            try:
                usuario = Especialista.objects.get(cedula=cedula)

                if usuario.nombre != nameEspe or usuario.apellido != apelli:
                    return Response({
                    'message': 'Datos inconsistentes.',
                    'error': 'El nombre o apellido no coincide con el registro en la base de datos.',
                    'usuario_encontrado': {
                        'cedula': usuario.cedula,
                        'nombre': usuario.nombre,
                        'apellido': usuario.apellido,
                    }
                }, status=400)


                if correo and usuario.correo.strip() != correo.strip():
                    usuario.correo = correo
                    usuario.save()  

                if describe and usuario.descripcion.strip() != describe.strip():
                    usuario.descripcion = describe 
                    usuario.save()  

                if service and usuario.servicios.strip() != service.strip():
                    usuario.servicios = service 
                    usuario.save()  

                especialidades_actuales = set(usuario.especialidades.values_list('nombre', flat=True))
                especialidades_a_agregar = [e for e in list_nuevas_especialidades if e not in especialidades_actuales]
                if not especialidades_a_agregar:
                     #buscar una logica para cuando se tenga que eliminar una especialidad
                     return Response({
                        'message': 'No se realizaron cambios.',
                        'detalle': 'Todas las especialidades ya estaban asociadas al usuario.'
                    }, status=200)
                
                
                nuevas_instancias = Especialidad.objects.filter(nombre__in=especialidades_a_agregar)
                usuario.especialidades.add(*nuevas_instancias)
                return Response({
                    'message': 'Especialidades actualizadas correctamente.',
                    'especialidades_añadidas': especialidades_a_agregar
                 }, status=200)


            except Especialista.DoesNotExist:
                 #insertar en la base si no existe el usuario
                 return Response({'message': 'Usuario no existe.'}, status=404) 






class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.user.first_name
        especialidades = Especialidad.objects.all().order_by('id').values('nombre')
        return Response({
            'username': username,
            'especialidades': list(especialidades)
        })
    



class DatosMongoView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        image_data = BytesIO()
        owner_id = request.user.last_name

        db = MongoDBConnection.get_db()
        files_collection = db['fs.files']
        chunks_collection = db['fs.chunks']

        try:
            file_doc = files_collection.find_one({'_id': ObjectId(owner_id)})
        except Exception as e:
            logger.error(f"Error al convertir owner_id a ObjectId: {e}") 


        if not file_doc:
                logger.warning(f"No se encontró archivo para owner_id: {owner_id}")
                file_doc = files_collection.find_one({'_id': ObjectId('6776235c043dda8d2809d7b6')})  


        file_id = file_doc['_id']
        chunks = chunks_collection.find({'files_id': file_id}).sort('n', 1)

        for chunk in chunks:
            image_data.write(chunk['data'])

        image_data.seek(0)
        encoded_image = base64.b64encode(image_data.read()).decode('utf-8')

        return Response({
            'imagen': encoded_image, 
            'filename': file_doc.get('filename', 'desconocido'),
        })
    



class personAdmin(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        imagenes = []
        image_data = BytesIO()
        especialistas_list = []

        especialistas = Especialista.objects.all().prefetch_related('especialidades').order_by('nombre')
        db = MongoDBConnection.get_db()
        files_collection = db['fs.files']
        chunks_collection = db['fs.chunks']
        
        for especialista in especialistas:

            especialidades = [especialidad.nombre for especialidad in especialista.especialidades.all()]
            
            especialistas_list.append({
                'nombre': especialista.nombre,
                'apellido': especialista.apellido,
                'owner_id': especialista.owner_id,
                'especialidades': especialidades
            })


        for espe in especialistas_list:
            owner_id = espe['owner_id']
            try:
                file_doc = files_collection.find_one({'_id': ObjectId(owner_id)})
            except Exception as e:
                logger.error(f"Error al convertir owner_id a ObjectId: {e}")
                continue    

            if not file_doc:
                logger.warning(f"No se encontró archivo para owner_id: {owner_id}")
                file_doc = files_collection.find_one({'_id': ObjectId('67776960474c4bd8ee017d42')})
                continue

            file_id = file_doc['_id']
            chunks = chunks_collection.find({'files_id': file_id}).sort('n', 1)
            

            image_data.truncate(0)
            image_data.seek(0)

            for chunk in chunks:
                image_data.write(chunk['data'])

            image_data.seek(0)
            encoded_image = base64.b64encode(image_data.read()).decode('utf-8')

            imagenes.append({
                'imagen': encoded_image,
                'metadatos': {
                    'filename': file_doc.get('filename', 'desconocido'),
                    'content_type': file_doc.get('contentType', 'unknown'),
                }
            })    
            

        return Response({
            'especialistas': especialistas_list,
            'imagenes':imagenes
        })

























        