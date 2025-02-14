import ctypes

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from AppTPFinal.forms import *
from AppTPFinal.models import *


def Main(request):
    return render(request, 'AppCoder/main.html')


#--------------------------------------------------------------------------------------------------------
#Modulos de Literatura
@login_required()
def literatura_crear(request):
    lit = Literatura_Form(request.POST or None, request.FILES or None)
    email = None
    email = request.user.email
    if request.method == 'POST':
        if lit.is_valid():
            lit = Literatura(
                nombre_literatura=request.POST.get('nombre_literatura'),
                autor_literatura=request.POST.get('autor_literatura'),
                editorial_literatura=request.POST.get('editorial_literatura'),
                anio_edicion_literatura=request.POST.get('anio_edicion_literatura'),
                email_usuario_literatura=email,
            )
        lit.save()

        imagen = request.FILES["imglit"]
        img = ImagenLiteratura(id_literatura=lit, imglit=imagen)
        img.save()

        ctypes.windll.user32.MessageBoxW(0, "Los datos se han cargado con exito", "mensaje", 0)

    contexto = {
        'formulariocargarliteratura': Literatura_Form()
    }
    return render(request, 'AppCoder/literatura/literatura.html', contexto)

@login_required()
def literatura_buscar(request):
    email = None
    email = request.user.email
    a_buscar = []
    if request.method == 'POST':
        nombre_literatura = request.POST.get('nombre_literatura')
        autor_literatura = request.POST.get('autor_literatura')
        editorial_literatura = request.POST.get('editorial_literatura')
        anio_edicion_literatura = request.POST.get('anio_edicion_literatura')
        if request.user.is_superuser:
            a_buscar = Literatura.objects.filter(nombre_literatura__icontains=nombre_literatura) & \
                   Literatura.objects.filter(autor_literatura__icontains=autor_literatura) & \
                   Literatura.objects.filter(editorial_literatura__icontains=editorial_literatura) & \
                   Literatura.objects.filter(anio_edicion_literatura__icontains=anio_edicion_literatura)
        else:
            a_buscar = Literatura.objects.filter(nombre_literatura__icontains=nombre_literatura) & \
                       Literatura.objects.filter(autor_literatura__icontains=autor_literatura) & \
                       Literatura.objects.filter(editorial_literatura__icontains=editorial_literatura) & \
                       Literatura.objects.filter(anio_edicion_literatura__icontains=anio_edicion_literatura) & \
                       Literatura.objects.filter(email_usuario_literatura=email)

    contexto = {
        'buscar_literatura': Buscar_Literatura_Form(),
        'literatura': a_buscar
    }
    return render(request, 'AppCoder/literatura/literaturabuscar.html', contexto)

@login_required()
def literatura_eliminar(request, id_literatura):
    lit = Literatura.objects.get(id_literatura=id_literatura)
    lit.delete()

    return redirect('TPFinalLiteraturaBuscar')

@login_required()
def literatura_modificar(request, id_literatura):
    lit = Literatura.objects.get(id_literatura=id_literatura)
    if request.method == 'POST':
        Lite = Literatura_Form(request.POST)
        if Lite.is_valid():
            data = Lite.cleaned_data
            lit.nombre_literatura= data.get('nombre_literatura')
            lit.autor_literatura= data.get('autor_literatura')
            lit.editorial_literatura= data.get('editorial_literatura')
            lit.anio_edicion_literatura= data.get('anio_edicion_literatura')
            lit.save()

            img = ImagenLiteratura.objects.filter(id_literatura=lit)
            imagen=request.FILES["imglit"]
            if img.exists():
                if imagen:
                    img = img[0]
                    img.imglit = imagen
                    img.save()

            else:
                img = ImagenLiteratura(id_literatura=lit, imglit=imagen)
                img.save()

            ctypes.windll.user32.MessageBoxW(0, "Los datos se han actualizado con exito", "mensaje", 0)
            return redirect('TPFinalLiteraturaBuscar')


    literatura_form = Literatura_Form(initial={
                'nombre_literatura': lit.nombre_literatura,
                'autor_literatura': lit.autor_literatura,
                'editorial_literatura': lit.editorial_literatura,
                'anio_edicion_literatura': lit.anio_edicion_literatura,
                'email_usuario_literatura': lit.email_usuario_literatura
                }
             )
    contexto = {
        'formulariocargarliteratura': literatura_form,
        'literatura': lit,
    }

    return render(request, 'AppCoder/literatura/literaturamodificar.html', contexto)

#--------------------------------------------------------------------------------------------------------
#Modulos de Musica
@login_required()
def musica_crear(request):
    mus = Musica_Form(request.POST)
    email = None
    email = request.user.email
    if request.method == 'POST':
        if mus.is_valid():
            mus = Musica(
                nombre_artista_musica=request.POST.get('nombre_artista_musica'),
                nombre_disco_musica=request.POST.get('nombre_disco_musica'),
                anio_lanzamiento_musica=request.POST.get('anio_lanzamiento_musica'),
                email_usuario_musica=email,
            )
        mus.save()

        imagen = request.FILES["imgmus"]
        img = ImagenMusica(id_musica=mus, imgmus=imagen)
        img.save()
        ctypes.windll.user32.MessageBoxW(0, "Los datos se han cargado con exito", "mensaje", 0)

    contexto = {
        'formulariomusica': Musica_Form()
    }
    return render(request, 'AppCoder/musica/musica.html', contexto)

@login_required()
def musica_buscar(request):
    email = None
    email = request.user.email
    a_buscar = []
    if request.method == 'POST':
        nombre_artista_musica = request.POST.get('nombre_artista_musica')
        nombre_disco_musica = request.POST.get('nombre_disco_musica')
        anio_lanzamiento_musica = request.POST.get('anio_lanzamiento_musica')
        if request.user.is_superuser:
            a_buscar = Musica.objects.filter(nombre_artista_musica__icontains=nombre_artista_musica) & \
                   Musica.objects.filter(nombre_disco_musica__icontains=nombre_disco_musica) & \
                   Musica.objects.filter(anio_lanzamiento_musica__icontains=anio_lanzamiento_musica)
        else:
            a_buscar = Musica.objects.filter(nombre_artista_musica__icontains=nombre_artista_musica) & \
                       Musica.objects.filter(nombre_disco_musica__icontains=nombre_disco_musica) & \
                       Musica.objects.filter(anio_lanzamiento_musica__icontains=anio_lanzamiento_musica) & \
                    Musica.objects.filter(email_usuario_musica=email)
    contexto = {
        'buscar_musica': Buscar_Musica_Form(),
        'musica': a_buscar
    }
    return render(request, 'AppCoder/musica/musicabuscar.html', contexto)

@login_required()
def musica_eliminar(request, id_musica):
    musica = Musica.objects.get(id_musica=id_musica)
    musica.delete()

    return redirect('TPFinalMusicaBuscar')

@login_required()
def musica_modificar(request, id_musica):
    mus = Musica.objects.get(id_musica=id_musica)

    if request.method == 'POST':
        Musi = Musica_Form(request.POST)
        if Musi.is_valid():
            data = Musi.cleaned_data
            mus.nombre_artista_musica= data.get('nombre_artista_musica')
            mus.nombre_disco_musica= data.get('nombre_disco_musica')
            mus.anio_lanzamiento_musica= data.get('anio_lanzamiento_musica')
            mus.save()

            img = ImagenMusica.objects.filter(id_musica=mus)
            imagen=request.FILES["imgmus"]
            if img.exists():
                if imagen:
                    img = img[0]
                    img.imgmus = imagen
                    img.save()

            else:
                img = ImagenMusica(id_musica=mus, imgmus=imagen)
                img.save()

            ctypes.windll.user32.MessageBoxW(0, "Los datos se han actualizado con exito", "mensaje", 0)
            return redirect('TPFinalMusicaBuscar')


    musica_form = Musica_Form(initial={
                'nombre_artista_musica': mus.nombre_artista_musica,
                'nombre_disco_musica': mus.nombre_disco_musica,
                'anio_lanzamiento_musica': mus.anio_lanzamiento_musica,
                'email_usuario_musica': mus.email_usuario_musica,
                }
             )
    contexto = {
        'formulariomusica': musica_form,
        'musica': mus,
    }

    return render(request, 'AppCoder/musica/musicamodificar.html', contexto)

#--------------------------------------------------------------------------------------------------------
#Modulos de Cine
@login_required()
def cine_crear(request):
    cine = Cine_Form(request.POST)
    email = None
    email = request.user.email
    if request.method == 'POST':
        if cine.is_valid():
            cine = Cine(
                nombre_pelicula_cine=request.POST.get('nombre_pelicula_cine'),
                nombre_director_cine=request.POST.get('nombre_director_cine'),
                anio_lanzamiento_cine=request.POST.get('anio_lanzamiento_cine'),
                email_usuario_cine=email,
            )
        cine.save()

        imagen = request.FILES["imgcin"]
        img = ImagenCine(id_cine=cine, imgcin=imagen)
        img.save()
        ctypes.windll.user32.MessageBoxW(0, "Los datos se han cargado con exito", "mensaje", 0)
    contexto = {
        'formulariocine': Cine_Form()
    }
    return render(request, 'AppCoder/cine/cine.html', contexto)

@login_required()
def cine_buscar(request):
    email = None
    email = request.user.email
    a_buscar = []
    if request.method == 'POST':
        nombre_pelicula_cine = request.POST.get('nombre_pelicula_cine')
        nombre_director_cine = request.POST.get('nombre_director_cine')
        anio_lanzamiento_cine = request.POST.get('anio_lanzamiento_cine')
        if request.user.is_superuser:
            a_buscar = Cine.objects.filter(nombre_pelicula_cine__icontains=nombre_pelicula_cine) & \
                   Cine.objects.filter(nombre_director_cine__icontains=nombre_director_cine) & \
                   Cine.objects.filter(anio_lanzamiento_cine__icontains=anio_lanzamiento_cine)
        else:
            a_buscar = Cine.objects.filter(nombre_pelicula_cine__icontains=nombre_pelicula_cine) & \
                       Cine.objects.filter(nombre_director_cine__icontains=nombre_director_cine) & \
                       Cine.objects.filter(anio_lanzamiento_cine__icontains=anio_lanzamiento_cine) & \
                    Cine.objects.filter(email_usuario_cine=email)

    contexto = {
        'buscar_cine': Buscar_Cine_Form(),
        'cine': a_buscar
    }
    return render(request, 'AppCoder/cine/cinebuscar.html', contexto)

@login_required()
def cine_eliminar(request, id_cine):
    cine = Cine.objects.get(id_cine=id_cine)
    cine.delete()

    return redirect('TPFinalCineBuscar')

@login_required()
def cine_modificar(request, id_cine):
    cine = Cine.objects.get(id_cine=id_cine)

    if request.method == 'POST':
        cine_temp = Cine_Form(request.POST)
        if cine_temp.is_valid():
            data = cine_temp.cleaned_data
            cine.nombre_pelicula_cine= data.get('nombre_pelicula_cine')
            cine.nombre_director_cine= data.get('nombre_director_cine')
            cine.anio_lanzamiento_cine= data.get('anio_lanzamiento_cine')
            cine.save()

            img = ImagenCine.objects.filter(id_cine=cine)
            imagen=request.FILES["imgcin"]
            if img.exists():
                if imagen:
                    img = img[0]
                    img.imgcin = imagen
                    img.save()

            else:
                img = ImagenCine(id_cine=cine, imgcin=imagen)
                img.save()

            ctypes.windll.user32.MessageBoxW(0, "Los datos se han actualizado con exito", "mensaje", 0)
            return redirect('TPFinalCineBuscar')


    cine_form = Cine_Form(initial={
                'nombre_pelicula_cine': cine.nombre_pelicula_cine,
                'nombre_director_cine': cine.nombre_director_cine,
                'anio_lanzamiento_cine': cine.anio_lanzamiento_cine,
                'email_usuario_cine': cine.email_usuario_cine,
                }
             )
    contexto = {
        'formulariocine': cine_form,
        'cine': cine,
    }

    return render(request, 'AppCoder/cine/cinemodificar.html', contexto)