from django.shortcuts import redirect, render

from bbdd import (
    AMIGOS,
    obtener_amigo_secreto,
    obtener_clave,
    obtener_deseo,
    obtener_nombre,
    obtener_participantes,
    registrar_deseo,
    verificar_amigo_asignado,
)

from .forms import DeseoForm, GenerarClaveForm, LoginParticipanteForm


def login_participante(request):
    form = LoginParticipanteForm(request.POST or None)
    participante = None

    if request.method == 'POST' and form.is_valid():
        request.session['participante_id'] = form.participante_id
        return redirect('pagina_principal')

    return render(
        request,
        'index.html',
        {'form': form},
    )


def generar_clave(request):
    form = GenerarClaveForm(request.POST or None)
    clave_generada = None

    if request.method == 'POST' and form.is_valid():
        clave_generada = obtener_clave(
            form.cleaned_data['nombre'],
            form.cleaned_data['codigo'],
        )
        if clave_generada in ('Código incorrecto', 'Contraseña ya reclamada'):
            form.add_error(None, clave_generada)
            clave_generada = None

    return render(
        request,
        'generar_clave.html',
        {'form': form, 'clave_generada': clave_generada},
    )


def pagina_principal(request):
    participante_id = request.session.get('participante_id')
    if participante_id not in AMIGOS:
        return redirect('login')

    mensaje = None
    deseo_existente = obtener_deseo(participante_id)
    tiene_deseo = deseo_existente != 'Su amigo aún no ha registrado su deseo. ¡Paciencia!'
    deseo_form = DeseoForm(request.POST or None)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'sortear':
            obtener_amigo_secreto(participante_id)
        elif accion == 'deseo' and not tiene_deseo and deseo_form.is_valid():
            registrar_deseo(participante_id, deseo_form.cleaned_data['deseo'])
            deseo_existente = deseo_form.cleaned_data['deseo']
            tiene_deseo = True
            mensaje = 'Su deseo quedó registrado.'

    amigo_id = verificar_amigo_asignado(participante_id)
    amigo_asignado = amigo_id if amigo_id in AMIGOS else None
    deseo_amigo = obtener_deseo(amigo_id) if amigo_asignado else None
    nombres = dict(obtener_participantes())

    return render(
        request,
        'pagina_principal.html',
        {
            'nombre': obtener_nombre(participante_id),
            'amigo_asignado': nombres.get(amigo_asignado),
            'deseo_amigo': deseo_amigo,
            'deseo_form': deseo_form,
            'deseo_existente': deseo_existente if tiene_deseo else None,
            'tiene_deseo': tiene_deseo,
            'mensaje': mensaje,
        },
    )


def cerrar_sesion(request):
    request.session.flush()
    return redirect('login')