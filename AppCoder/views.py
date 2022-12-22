from django.shortcuts import render
from .models import Curso, Profesor, Estudiantes
from django.http import HttpResponse

from django.urls import reverse_lazy

from AppCoder.forms import CursoForm, ProfeForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.

def curso(request):

    curso1=Curso(nombre="Python",comision=34640)

    curso.save()
    cadena_Texto="Curso guardado: "+curso.nombre+" "+str(curso.comision)
    return HttpResponse(cadena_Texto)

def inicio(request):
    return render(request, "AppCoder/inicio.html")
 
def cursos(request):
    return render(request, "AppCoder/cursos.html")

def estudiantes(request):
    return render(request, "AppCoder/estudiantes.html")

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
            return render(request, "AppCoder/inicio.html", {"mensaje": "PROFESOR CREADO CORRECTAMENTE!!"})
    else:
        formulario=ProfeForm()

    return render(request, "AppCoder/profesores.html", {"form": formulario})

def entregables(request):
    return render(request, "AppCoder/entregables.html")

""" def cursoFormulario(request):
    
    if request.method=="POST":
        nombrecito=request.POST["nombre"]
        comisioncita=request.POST["comision"]

        curso1=Curso (nombre=nombrecito,comision=comisioncita)
        curso1.save()
        return render (request, "AppCoder/inicio.html")

    return render (request, "AppCoder/cursoFormulario.html")"""

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
            return render (request, "AppCoder/inicio.html")
    else:
        formulario=CursoForm()

    return render (request, "AppCoder/cursoFormulario.html", {"form":formulario})

def busquedaComision(request):
    return render(request, "AppCoder/busquedaComision.html")

def buscar(request):

    if "comision" in request.GET:

        comision=request.GET["comision"]

        cursos=Curso.objects.filter(comision__icontains=comision)
        return render(request, "AppCoder/resultadosBusqueda.html", {"cursos":cursos})
    else:
        return render(request, "AppCoder/busquedaComision.html", {"mensaje":"CHE: Ingresa una comision"})

def leerProfesores(request):
    profesores=Profesor.objects.all()
    print(profesores)
    return render(request, "AppCoder/leerProfesores.html", {"profesores": profesores})


def eleminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    profesor.delete()
    profesores=Profesor.objects.all()
    return render(request, "AppCoder/leerProfesores.html", {"mensaje": "Profesor eliminado correctamente", "profesores":profesores})


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
            return render(request, "AppCoder/inicio.html", {"mensaje": "PROFESOR CREADO CORRECTAMENTE!!"})
    else:
        formulario=ProfeForm(initial={"nombre":profesor.nombre, "apellido":profesor.apellido, "email":profesor.email, "profesion":profesor.profesion})
    return render(request, "AppCoder/editarProfesor.html", {"form":formulario, "profesor":profesor})


class EstudianteList(ListView):
    model=Estudiantes
    template_name="AppCoder/leerEstudiantes.html"

class EstudianteCreacion(CreateView):
    model = Estudiantes
    success_url = reverse_lazy('estudiante_listar')
    template_name="AppCoder/estudiante_form.html"
    fields= ['nombre', 'apellido', 'email']

class EstudianteUpdate(UpdateView):
    model= Estudiantes
    success_url = reverse_lazy('estudiante_listar')
    template_name="AppCoder/estudiante_form.html"
    fields= ['nombre', 'apellido', 'email']

class EstudianteDelete(DeleteView):
    model= Estudiantes
    success_url = reverse_lazy('estudiante_listar')
    template_name="AppCoder/estudiante_confirm_delete.html"

class EstudianteDetalle(DetailView):
    model= Estudiantes
    template_name="AppCoder/estudiante_detalle.html"