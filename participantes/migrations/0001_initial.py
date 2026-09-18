from django.db import migrations, models
from django.contrib.auth.hashers import make_password


NOMBRES = [
    ('belen', 'Ana Belen'),
    ('sergio', 'Sergio'),
    ('nicolas', 'Nicolás'),
    ('cristhian', 'Christian'),
    ('karen', 'Karen'),
    ('fabian', 'Fabián'),
    ('ricaurte', 'Ricaurte'),
    ('valentina', 'Valsita'),
]


def crear_participantes(apps, schema_editor):
    participante = apps.get_model('participantes', 'Participante')
    participante.objects.bulk_create(
        [
            participante(
                nombre=nombre,
                clave=make_password('prueba123'),
                registro_generado=False,
            )
            for nombre, _ in NOMBRES
        ]
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=NOMBRES, max_length=30, unique=True)),
                ('clave', models.CharField(max_length=128)),
                ('registro_generado', models.BooleanField(default=False)),
            ],
        ),
        migrations.RunPython(crear_participantes, migrations.RunPython.noop),
    ]