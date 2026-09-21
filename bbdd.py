import os
import sqlite3
import random
from pathlib import Path

import psycopg

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    bd = psycopg.connect(DATABASE_URL)
    cursor = bd.cursor()
else:
    bd = sqlite3.connect(
        Path(__file__).resolve().parent / 'endulzada.sqlite3',
        check_same_thread=False,
    )
    cursor = bd.cursor()

AMIGOS = tuple(
    fila[0] for fila in cursor.execute("SELECT ID FROM PARTICIPANTES").fetchall()
)

# Usamos un diccionario: {id_persona: amigo_secreto}

# Y un set con los amigos ya asignados (para búsquedas rápidas)


# AMIGOS_EMPAREJADOS = cursor.execute("""SELECT * FROM AMIGOSECRETO""").fetchall()
# print(AMIGOS_EMPAREJADOS)

def obtener_amigo_secreto(id):
    # 1. Validar que la persona exista
    if id not in AMIGOS:
        return "Ese id no está en la lista de amigos."

    # 2. Validar que no tenga ya un amigo asignado
    if cursor.execute("SELECT 1 FROM AMIGOSECRETO WHERE ID = ?", (id,)).fetchone():
        return f"{id} ya tiene un amigo secreto asignado."

    asignaciones = dict(cursor.execute("SELECT ID, ID_AMIGO FROM AMIGOSECRETO").fetchall())
    personas_pendientes = [persona for persona in AMIGOS if persona not in asignaciones]
    amigos_disponibles = [
        amigo for amigo in AMIGOS
        if amigo not in asignaciones.values()
    ]

    def es_completable(personas, amigos):
        if not personas:
            return True

        opciones = {
            persona: [amigo for amigo in amigos if amigo != persona]
            for persona in personas
        }
        persona = min(personas, key=lambda item: len(opciones[item]))

        for amigo in opciones[persona]:
            personas_restantes = [item for item in personas if item != persona]
            amigos_restantes = [item for item in amigos if item != amigo]
            if es_completable(personas_restantes, amigos_restantes):
                return True

        return False

    if len(personas_pendientes) == 1:
        if amigos_disponibles and amigos_disponibles[0] != id:
            amigo = amigos_disponibles[0]
            cursor.execute(
                "INSERT INTO AMIGOSECRETO (ID, ID_AMIGO) VALUES (?, ?)",
                (id, amigo),
            )
        elif asignaciones:
            # Si se agregó un participante después de cerrar el ciclo, se inserta
            # en una arista existente para conservar un destinatario por persona.
            persona_anterior = random.choice(list(asignaciones))
            amigo_anterior = asignaciones[persona_anterior]
            cursor.execute(
                "UPDATE AMIGOSECRETO SET ID_AMIGO = ? WHERE ID = ?",
                (id, persona_anterior),
            )
            cursor.execute(
                "INSERT INTO AMIGOSECRETO (ID, ID_AMIGO) VALUES (?, ?)",
                (id, amigo_anterior),
            )
            amigo = amigo_anterior
        else:
            return "No hay amigos disponibles para asignar."
    else:
        candidatos = amigos_disponibles[:]
        random.shuffle(candidatos)
        amigo = next(
            (
                candidato for candidato in candidatos
                if candidato != id
                and es_completable(
                    [persona for persona in personas_pendientes if persona != id],
                    [disponible for disponible in amigos_disponibles if disponible != candidato],
                )
            ),
            None,
        )
        if amigo is None:
            return "No hay amigos disponibles para asignar."

        cursor.execute(
            "INSERT INTO AMIGOSECRETO (ID, ID_AMIGO) VALUES (?, ?)",
            (id, amigo),
        )

    bd.commit()

    return amigo

def registrar_deseo(id, deseo):
    DESEOS_LISTOS = [fila[0] for fila in cursor.execute("SELECT ID FROM DESEOS").fetchall()]

    if id not in DESEOS_LISTOS and deseo.strip():
        cursor.execute("""INSERT INTO DESEOS (ID, DESEO) VALUES (?, ?)""", (id, deseo,))

    bd.commit()

def obtener_clave(id, codigo):

    sustantivos = [
        "gato", "perro", "pato", "pollo", "gallo", "cerdo", "burro", "caballo",
        "toro", "carnero", "chivo", "mono", "gorila", "ardilla", "mapache", "rata",
        "ratón", "hámster", "conejo", "camello", "llamero", "alce", "pingüino",
        "gecko", "nutria", "castor", "ornitorrinco", "cocodrilo", "lagarto",
        "iguano", "serpiente", "tortugo", "sapo", "mosquito", "moscardón",
        "cucaracho", "escarabajo", "mariposón", "abejorro", "avispero", "pulpo",
        "calamar", "cangrejo", "camarón", "meduso", "tiburón", "balleno",
        "dinosaurio", "dragón", "palomo", "búho", "águila", "cuervo", "loro",
        "canario", "melón", "banano", "mango", "papayo", "piñón", "coco",
        "aguacate", "tomate", "cebollín", "papa", "zanahorio", "arepazo", "empanadón",
        "chicharrón", "buñuelo", "tamal", "salchichón", "hamburguesón", "pizza",
        "galletón", "panqueque", "churro", "helado", "yogur", "queso", "frijol",
        "lentejo", "arroz", "espagueti", "palillo", "tenedor", "cucharón",
        "espátulo", "sartén", "caldero", "balde", "escobón", "trapero", "recogedor",
        "esponjón", "cepillo", "peine", "sombrero", "paraguas", "almohadón",
        "colchón", "cobertor", "pantuflo", "calcetín", "zapato", "arepuelo",
        "pantalón", "camisón", "corbatón", "sombrero", "monóculo", "mochilón", "maletón",
        "carterón", "monedero", "billete", "llavero", "candado", "martillo", "tornillo",
        "clavo", "taladro", "destornillador", "serrucho", "ladrillo", "cemento",
        "carretillo", "escalón", "semáforo", "poste", "banco", "sillón", "butaco",
        "sofá", "televisor", "neverón", "microondas", "ventilador", "computador",
        "teclado", "ratón", "impresor", "celular", "audífono", "cargador",
        "control", "cable", "enchufe", "bombillo", "reloj", "espejo", "cuadro",
        "florero", "macetero", "planto", "cactus", "árbol", "pedrusco", "ladrillo",
        "charco", "pantano", "volcán", "monte", "río", "trueno", "relámpago",
        "huracán", "tornado", "bigote", "barbón", "argentino", "peruano", "orejón", "ombligo",
        "rodillo", "codo", "panza", "cachete", "ceño", "moco", "pedo", "eructo",
        "culo", "huevo", "pene", "teto", "mierdo", "pendejo", "huevón",
        "gonorrea", "marica", "pirobo", "malparido", "payaso", "mamarracho",
        "pelmazo", "zoquete", "imbécil", "idiota", "baboso", "lambón", "sapoperro", "guámbito", "negro"
    ]

    adjetivos = [
        "absurdo", "ridículo", "torpe", "tonto",
        "bobo", "bobazo", "lento", "despistado",
        "confundido", "chiflado", "loco", "pirado",
        "alocado", "distraído", "curioso", "extraño",
        "raro", "peculiar", "ridiculón", "patoso",
        "torpón", "grandote", "pequeñajo", "enano",
        "gigantesco", "minúsculo", "enorme", "gordito",
        "panzón", "culón", "peludo", "greñudo",
        "bigotudo", "narigón", "orejón", "cachetón",
        "despeinado", "mugroso", "sucio", "cochino",
        "desastroso", "desordenado", "caótico", "escandaloso",
        "ruidoso", "silencioso", "dramático", "exagerado",
        "melodramático", "nervioso", "tranquilo", "sospechoso",
        "misterioso", "siniestro", "tenebroso", "espantoso",
        "terrorífico", "vergonzoso", "bochornoso", "penoso",
        "patético", "lamentable", "desgraciado", "malhumorado",
        "amargado", "gruñón", "quejumbroso", "fastidioso",
        "intenso", "cansón", "mamón", "pegajoso",
        "baboso", "pedorro", "mocoso", "apestoso",
        "hediondo", "grasiento", "picosito", "degenerado",
        "asqueroso", "repugnante", "viscoso", "gelatinoso",
        "esponjoso", "fofo", "flaco", "escuálido",
        "chueco", "torcido", "bizco", "patizambo",
        "cabezón", "calvo", "pelón", "barbudo",
        "ciego", "sordo", "ronco", "chillón",
        "tartamudo", "perezoso", "vago", "haragán",
        "holgazán", "inútil", "inservible", "mediocre",
        "chapucero", "improvisado", "cutre", "barato",
        "destartalado", "oxidado", "viejo", "viejuno",
        "anticuado", "prehistórico", "jurásico", "pendejo",
        "huevón", "no heterosexual", "gonorrea", "pirobo",
        "malparido", "jodido", "hijueputa", "gulumbo", "espantalavirgen"
    ]

    credenciales = [(i[0], i[1]) for i in cursor.execute("""SELECT ID, CODIGO FROM PARTICIPANTES""").fetchall()]
    registrados = [fila[0] for fila in cursor.execute("SELECT ID FROM CREDENCIALES").fetchall()]

    if id not in registrados:
        for j in credenciales:
            if j == (id, codigo):
                sust = random.choice(sustantivos)
                adj = random.choice(adjetivos)
                password = f"{sust} {adj}"
                cursor.execute("""INSERT INTO CREDENCIALES (ID, CLAVE) VALUES (?, ?)""", (id, password))
                bd.commit()
                return password
        return "Código incorrecto"
    else:
        return "Contraseña ya reclamada"

def validar_ingreso(id, clave):
    credenciales = [(i[0], i[1]) for i in cursor.execute("""SELECT ID, CLAVE FROM CREDENCIALES""").fetchall()]

    return (id, clave) in credenciales


def obtener_participantes():
    return cursor.execute("SELECT ID, NOMBRE FROM PARTICIPANTES ORDER BY NOMBRE").fetchall()


def obtener_nombre(id):
    participante = cursor.execute("SELECT NOMBRE FROM PARTICIPANTES WHERE ID = ?", (id,)).fetchone()
    return participante[0] if participante else id

def verificar_amigo_asignado(id):
    amigo = cursor.execute("""SELECT ID_AMIGO FROM AMIGOSECRETO WHERE ID = ?""", (id,)).fetchone()
    if amigo:
        return amigo[0]
    else:
        return "Debes sortear un amigo secreto primero."

def obtener_deseo(id):
    deseo = cursor.execute("""SELECT DESEO FROM DESEOS WHERE ID = ?""", (id,)).fetchone()
    if deseo:
        return deseo[0]
    else:
        return "Su amigo aún no ha registrado su deseo. ¡Paciencia!"
