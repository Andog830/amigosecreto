from django import forms

from bbdd import obtener_participantes, validar_ingreso


class NombreSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value == '':
            option['attrs']['disabled'] = True
        return option


class LoginParticipanteForm(forms.Form):
    nombre = forms.ChoiceField(choices=(), label='Nombre')
    clave = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [('', 'Escoja su nombre')] + obtener_participantes()
        self.fields['nombre'].choices = choices
        self.fields['nombre'].widget = NombreSelect(choices=choices)

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        clave = cleaned_data.get('clave')

        if nombre and clave:
            if not validar_ingreso(nombre, clave):
                raise forms.ValidationError('El nombre o la contraseña no son correctos.')

            self.participante_id = nombre

        return cleaned_data


class GenerarClaveForm(forms.Form):
    nombre = forms.ChoiceField(choices=(), label='Nombre')
    codigo = forms.CharField(label='Código de 4 dígitos', max_length=4, min_length=4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [('', 'Escoja su nombre')] + obtener_participantes()
        self.fields['nombre'].choices = choices
        self.fields['nombre'].widget = NombreSelect(choices=choices)

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if not codigo.isdigit():
            raise forms.ValidationError('El código debe tener cuatro dígitos.')
        return codigo


class DeseoForm(forms.Form):
    deseo = forms.CharField(
        label='Mi deseo',
        max_length=500,
        required=True,
        error_messages={'required': 'Aún no ha registrado su deseo, su amigo secreto no podrá conseguirlo a tiempo.'},
        widget=forms.Textarea(attrs={'rows': 4}),
    )