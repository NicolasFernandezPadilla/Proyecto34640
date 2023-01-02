from django.shortcuts import render
from .models import Curso, Profesor, Estudiantes, Avatar
from django.http import HttpResponse

from django.urls import reverse_lazy

from AppCoder.forms import CursoForm, ProfeForm, RegistroUsuarioForm, UserEditForm, AvatarForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin #para vistas basadas en clases
from django.contrib.auth.decorators import login_required #para vistas basadas en funciones

# Create your views here.

@login_required
def curso(request):

    curso1=Curso(nombre="Python",comision=34640)

    curso.save()
    cadena_Texto="Curso guardado: "+curso.nombre+" "+str(curso.comision)
    return HttpResponse(cadena_Texto)


def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        imagen=lista[0].imagen.url
    else:
        imagen="/media/avatares/avatarpordefecto.png"
    return imagen

@login_required
def inicio(request):
    lista=Avatar.objects.filter(user=request.user)
    
    return render (request, "AppCoder/inicio.html", {"imagen":obtenerAvatar(request)})
 
@login_required
def cursos(request):
    return render(request, "AppCoder/cursos.html", {"imagen":obtenerAvatar(request)})

@login_required
def estudiantes(request):
    return render(request, "AppCoder/estudiantes.html", {"imagen":obtenerAvatar(request)})

@login_required
def profesores(request):
    
    if request.method=="POST":
        form=ProfeForm(request.POST)
        if form.is_valid():
            informacion=form.cleaned_data
            print(informacion)
            nombre=informacion["nombre"]
            apellido=informacion["apellido"]
            email=informacion["email"]
            profesion=informacion["profesion"]
            profe= Profesor(nombre=nombre, apellido=apellido, email=email, profesion=profesion)
            profe.save()
            return render(request, "AppCoder/inicio.html", {"mensaje": "PROFESOR CREADO CORRECTAMENTE!!", "imagen":obtenerAvatar(request)})
    else:
        formulario=ProfeForm()

    return render(request, "AppCoder/profesores.html", {"form": formulario, "imagen":obtenerAvatar(request)})

@login_required
def entregables(request):
    return render(request, "AppCoder/entregables.html", {"imagen":obtenerAvatar(request)})

""" def cursoFormulario(request):
    
    if request.method=="POST":
        nombrecito=request.POST["nombre"]
        comisioncita=request.POST["comision"]

        curso1=Curso (nombre=nombrecito,comision=comisioncita)
        curso1.save()
        return render (request, "AppCoder/inicio.html")

    return render (request, "AppCoder/cursoFormulario.html")"""

@login_required
def cursoFormulario(request):
    
    if request.method=="POST":
        form=CursoForm(request.POST)
        print("--------------------------------")
        print(form)
        print("--------------------------------")
        if form.is_valid():
            informacion=form.cleaned_data
            print(informacion)
            nombrecito=informacion["nombre"]
            comisioncita=informacion["comision"]

            curso1=Curso (nombre=nombrecito,comision=comisioncita)
            curso1.save()
            return render (request, "AppCoder/inicio.html", {"imagen":obtenerAvatar(request)})
        else:
            return render (request, "AppCoder/cursoFormulario.html", {"form":formulario, "imagen":obtenerAvatar(request)})

    else:    
        formulario=CursoForm()

    return render (request, "AppCoder/cursoFormulario.html", {"form":formulario, "imagen":obtenerAvatar(request)})

@login_required
def busquedaComision(request):
    return render(request, "AppCoder/busquedaComision.html", {"imagen":obtenerAvatar(request)})

@login_required
def buscar(request):

    if "comision" in request.GET:

        comision=request.GET["comision"]

        cursos=Curso.objects.filter(comision__icontains=comision)
        return render(request, "AppCoder/resultadosBusqueda.html", {"cursos":cursos, "imagen":obtenerAvatar(request)})
    else:
        return render(request, "AppCoder/busquedaComision.html", {"mensaje":"CHE: Ingresa una comision", "imagen":obtenerAvatar(request)})

@login_required
def leerProfesores(request):
    profesores=Profesor.objects.all()
    print(profesores)
    return render(request, "AppCoder/leerProfesores.html", {"profesores": profesores, "imagen":obtenerAvatar(request)})


@login_required
def eleminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    profesor.delete()
    profesores=Profesor.objects.all()
    return render(request, "AppCoder/leerProfesores.html", {"mensaje": "Profesor eliminado correctamente", "profesores":profesores, "imagen":obtenerAvatar(request)})


@login_required
def editarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    if request.method=="POST":
        form=ProfeForm(request.POST)
        if form.is_valid():
            informacion=form.cleaned_data
            print(informacion)
            
            profesor.nombre=informacion["nombre"]
            profesor.apellido=informacion["apellido"]
            profesor.email=informacion["email"]
            profesor.profesion=informacion["profesion"]
            profesor.save()
            return render(request, "AppCoder/inicio.html", {"mensaje": "PROFESOR CREADO CORRECTAMENTE!!", "imagen":obtenerAvatar(request)})
    else:
        formulario=ProfeForm(initial={"nombre":profesor.nombre, "apellido":profesor.apellido, "email":profesor.email, "profesion":profesor.profesion})
    return render(request, "AppCoder/editarProfesor.html", {"form":formulario, "profesor":profesor, "imagen":obtenerAvatar(request)})


class EstudianteList(LoginRequiredMixin, ListView):
    model=Estudiantes
    template_name="AppCoder/leerEstudiantes.html"

class EstudianteCreacion(LoginRequiredMixin, CreateView):
    model = Estudiantes
    success_url = reverse_lazy('estudiante_listar')
    template_name="AppCoder/estudiante_form.html"
    fields= ['nombre', 'apellido', 'email']

class EstudianteUpdate(LoginRequiredMixin, UpdateView):
    model= Estudiantes
    success_url = reverse_lazy('estudiante_listar')
    template_name="AppCoder/estudiante_form.html"
    fields= ['nombre', 'apellido', 'email']

class EstudianteDelete(LoginRequiredMixin, DeleteView):
    model= Estudiantes
    success_url = reverse_lazy('estudiante_listar')
    template_name="AppCoder/estudiante_confirm_delete.html"

class EstudianteDetalle(LoginRequiredMixin, DetailView):
    model= Estudiantes
    template_name="AppCoder/estudiante_detalle.html"

#---- seccion de login

def login_request(request):
    if request.method == "POST":
        form= AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usu=form.cleaned_data.get("username")
            clave=form.cleaned_data.get("password")

            usuario=authenticate(username=usu, password=clave)#crea un usuario de la base, que tenga ese usuario y ese pass, si existe lo trae y sino nada.
            if usuario is not None:
                login(request, usuario)
                return render(request, 'AppCoder/inicio.html', {'mensaje':f"Bienvenido {usuario}"})
            else:
                return render(request, 'AppCoder/login.html', {'mensaje':"Usuario o contraseña inconrrectos", 'form':form})
        else:
            return render(request, 'AppCoder/login.html', {'mensaje': "Usuario o contraseña inconrrectos", 'form':form})
    
    else:
        form=AuthenticationForm()
    return render(request, "AppCoder/login.html", {"form":form})


def register(request):
    if request.method =="POST":
        form=RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            form.save()
            #aca se podria loguear el usuario,con authenticate y login...
            return render(request, "AppCoder/inicio.html", {"mensaje": f"Usuario {username} creado correctamente"})
        else:
            return render(request, "AppCoder/register.html", {"form":form, "mensaje":"Error al crear el usuario"})


    else:
        form=RegistroUsuarioForm()
    return render(request, "AppCoder/register.html", {"form":form})

@login_required
def editarPerfil(request):
    usuario=request.user
    if request.method=="POST":
        form=UserEditForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usuario.email=info["email"]
            usuario.password1=info["password1"]
            usuario.password2=info["password2"]
            usuario.first_name=info["first_name"]
            usuario.last_name=info["last_name"]
            usuario.save()
            return render(request, "AppCoder/inicio.html",{"mensaje":"Perfil editado correctamente", "imagen":obtenerAvatar(request)})
        else:
            return render(request, "AppCoder/editarUsuario.html", {"form":form, "nombreusuario":usuario.username, "mensaje":"Error al editar el perfil", "imagen":obtenerAvatar(request)})
    else:
        form=UserEditForm(instance=usuario)
        return render(request, "AppCoder/editarUsuario.html", {"form":form,  "nombreusuario":usuario, "imagen":obtenerAvatar(request)})

@login_required
def agregarAvatar(request):
    if request.method=="POST":
        form=AvatarForm(request.POST, request.FILES)#Ademas del post, como trae archivos (yo se que trae archivos porque conozco el form, tengo que usar request.files)
        if form.is_valid():
            avatarViejo=Avatar.objects.filter(user=request.user)
            if len(avatarViejo)>0:
                avatarViejo[0].delete()
            avatar=Avatar(user=request.user, imagen=request.FILES["imagen"])
            avatar.save()
            return render(request, "AppCoder/inicio.html",{"mensaje": "Avatar agregado correctamente", "imagen":obtenerAvatar(request)})
    else:
        form=AvatarForm()
        return render(request, "AppCoder/agregarAvatar.html", {"formulario":form, "usuario":request.user, "imagen":obtenerAvatar(request)})
