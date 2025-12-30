from app.pb_clients.departamento import *
from app.pb_clients.libros import *
from app.pb_clients.copias_libros import *
from app.pb_clients.tipo_usuario import *
from app.pb_clients.usuarios import *
from app.pb_clients.prestamos import *
from app.pb_clients.generos import *
from app.core.auth import db_get_client

from app.models.db_models import *
from datetime import date

# TOKEN

def test_get_token():
    client = db_get_client()
    book = client.collection("Libros").get_one("u963eez24adx58f")
    print(book.titulo)
    assert client

#Querys

def test_db_get_total_prestamos():
    total = db_get_total_prestamos()
    print(total)
    assert total

def test_get_metrics():
    metrics = get_metrics()
    print(metrics)
    assert metrics

def test_top_libros():
    top = top_libros()
    print(top)
    assert top

def test_get_prestamos_ultimos_siete_dias():
    prestamos = get_prestamos_ultimos_siete_dias()
    print(prestamos)
    assert prestamos

def test_db_get_estadisticas_admin_panel_a():
    estadisticas = db_get_estadisticas_admin_panel_a()
    print(estadisticas)
    assert estadisticas

#Libros

def test_db_create_libro():
    fecha = datetime.today()
    fecha_hoy = fecha.strftime("%Y-%m-%d %H:%M:%S")

    pk_id_departamento = 1
    departamento = db_get_departamento(pk_id_departamento)

    pk_id_genero = 2
    genero = db_get_genero(pk_id_genero)

    new_libro = Libro(
        id= None,
        pk_id_libro=48,
        titulo="Dune",
        autor="Frank Herbert",
        fecha_publicacion=fecha_hoy,
        ruta_img="blob:http://localhost:3000/2d1369c8-4a7d-4721-8c8f-d841141a6bdd",
        fk_id_departamento= departamento.id,
        fk_id_genero=genero.id,
        created_at=fecha_hoy,
        updated_at=fecha_hoy
    )

    response = db_create_libro(new_libro)
    assert response

def test_db_get_libro():
    pk_id_libro = 1
    libro = db_get_libro(pk_id_libro)
    print(libro)
    assert libro.pk_id_libro == pk_id_libro

def test_db_update_libro():
    # Asumimos que el libro existe y que se va a enviar a actualizar, si no es asi, se evalua desde los servicios
    pk_id_libro = 1
    libro = db_get_libro(pk_id_libro)
    libro.ruta_img = "C:/Users/USUARIO/Desktop/MODULAR/informacion/user.png"
    response = db_update_libro(libro)
    print(libro)
    assert response.titulo == "New Title"

def test_db_delete_libro():
    # Asumimos que el libro existe y que se va a enviar a eliminar, si no es asi, se evalua desde los servicios
    pk_id_libro = 1
    response = db_delete_libro(pk_id_libro)
    assert response

def test_db_get_last_id_libro():
    response = db_get_last_id_libro()
    print(response)
    assert response

def test_db_get_all_libros():
    libros = db_get_all_libros(10)
    print(libros)
    assert libros

## Departamentos

#id: str
#pk_id_departamento: int
#numero: int
#nombre: str
#created_at: Optional[date]
#updated_at: Optional[date]

def test_db_create_departamento():
    fecha = datetime.today()
    fecha_hoy = fecha.strftime("%Y-%m-%d %H:%M:%S")
    new_departamento = Departamento(
        id= None,
        pk_id_departamento=1,
        numero= 522,
        nombre="Ciencias de la salud",
        created_at=fecha_hoy,
        updated_at=fecha_hoy
    )
    response = db_create_departamento(new_departamento)
    print(response)
    assert response

def test_db_get_all_dptos():
    response = db_get_all_dptos()
    print(response)
    assert response


def test_db_get_departamento():
    pk_id_departamento = 1
    departamento = db_get_departamento(pk_id_departamento)
    assert departamento.nombre == "Ciencias de la salud"

def test_db_update_departamento():
    # Asumimos que el departamento existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    departamento = db_get_departamento(1)
    departamento.nombre = "Ciencias Salud"
    departamento_json = departamento.model_dump(mode="json")
    response = db_update_departamento(departamento_json)
    assert response.nombre == "Ciencias Salud"

def test_db_delete_departamento():
    pk_id_departamento = 1
    response = db_delete_departamento(pk_id_departamento)
    assert response


## Departamentos

#id: str
#pk_id_departamento: int
#numero: int
#nombre: str
#created_at: Optional[date]
#updated_at: Optional[date]

def test_db_create_genero():
    fecha = datetime.today()
    fecha_hoy = fecha.strftime("%Y-%m-%d %H:%M:%S")
    new_genero = Generos(
        id=None,
        pk_id_genero=6,
        genero="Terror",
        icon="C:/Users/USUARIO/Desktop/MODULAR/informacion/generos/terror.png",
        created_at=fecha_hoy,
        updated_at=fecha_hoy
    )
    response = db_create_genero(new_genero)
    print(response)
    assert response

def test_db_get_genero():
    pk_id_genero = 1
    genero = db_get_genero(pk_id_genero)
    print(genero)
    assert genero.genero == "Terror"

def test_db_update_genero():
    # Asumimos que el departamento existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    pk_id_genero = 1
    genero_item = db_get_genero(pk_id_genero)
    genero_item.icon = "C:/Users/USUARIO/Desktop/MODULAR/informacion/click.png"

    response = db_update_genero(genero_item)
    print(response)
    assert response.pk_id_genero == pk_id_genero

def test_db_delete_genero():
    pk_id_genero = 1
    response = db_delete_genero(pk_id_genero)
    assert response

def test_db_get_all_generos():
    response = db_get_all_generos()
    print(response)
    assert response

# ---------- CopiasLibro ----------
#CopiaLibro(BaseModel):
#    id: str
#    pk_id_copia: int
#    fk_id_libro: int
#    rfid_tag: str
#    disponibilidad: bool
#    created_at: Optional[date]
#    updated_at: Optional[date]

def test_db_create_copia_libro():
    fecha = datetime.today()
    fecha_hoy = fecha.strftime("%Y-%m-%d %H:%M:%S")
    pk_id_libro = 4
    libro = db_get_libro(pk_id_libro)

    new_copia_libro = CopiaLibro(
        id= None,
        pk_id_copia=6,
        fk_id_libro= libro.id,
        isbn="54a5sdas6d5a",
        rfid_tag="0000000008",
        disponibilidad=True,
        created_at=fecha_hoy,
        updated_at=fecha_hoy
    )

    response = db_create_copia_libro(new_copia_libro)
    assert response

def test_db_update_stat_copia_libro():
    pk_id_copia_libro = 1
    copia_libro = db_update_stat_copia_libro(pk_id_copia_libro)
    print(copia_libro)
    assert copia_libro

def test_db_get_copia_libro():
    pk_id_copia_libro = 1
    copia_libro = db_get_copia_libro(pk_id_copia_libro)
    print(copia_libro)
    assert copia_libro.rfid_tag == "0000000001"

def test_db_get_copia_libro_rfid():
    rfid = "0000000001"
    copia_libro_rfid = db_get_copia_libro_rfid(rfid)
    print(copia_libro_rfid)
    assert copia_libro_rfid

def test_db_update_copia_libro():
    # Asumimos que el copia_libro existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    pk_id_copia_libro = 1
    copia_libro = db_get_copia_libro(pk_id_copia_libro)
    copia_libro.rfid_tag = "0000000002"
    response = db_update_copia_libro(copia_libro)
    assert response.rfid_tag == "0000000002"

def test_db_delete_copia_libro():
    # Asumimos que el copia_libro existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    pk_id_copia = 1
    response = db_delete_copia_libro(pk_id_copia)
    assert response

def test_db_get_all_copies():
    response = db_get_all_copies()
    print(response)
    assert response

# ---------- TipoUsuario ----------
#class TipoUsuario(BaseModel):
#    id: str
#    pk_id_tipo_usuario: int
#    rol: str
#    created_at: Optional[datetime]
#    updated_at: Optional[datetime]

def test_db_create_tipo_usuario():
    fecha = datetime.today()
    fecha_hoy = fecha.strftime("%Y-%m-%d %H:%M:%S")
    new_tipo_usuario = TipoUsuario(
        id=None,
        pk_id_tipo_usuario=3,
        rol="Dummy",
        created_at=fecha_hoy,
        updated_at=fecha_hoy,
    )
    response = db_create_tipo_usuario(new_tipo_usuario)
    assert response.rol == "Dummy"

def test_db_get_tipo_usuario():
    pk_id_tipo_usuario = 1
    tipo_usuario = db_get_tipo_usuario(pk_id_tipo_usuario)
    assert tipo_usuario.rol == "Administrador"

def test_db_get_all_tipo_usuario():
    tipo_usuario = db_get_all_tipo_usuario()
    print(tipo_usuario)
    assert tipo_usuario

def test_db_update_tipo_usuario():
    # Asumimos que el copia_libro existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    pk_id_tipo_usuario = 3
    tipo_usuario = db_get_tipo_usuario(pk_id_tipo_usuario)
    tipo_usuario.rol = "Dummie"
    response = db_update_tipo_usuario(tipo_usuario)
    assert response.rol == "Dummie"

def test_db_delete_tipo_usuario():
    # Asumimos que el copia_libro existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    pk_id_tipo_usuario = 3
    response = db_delete_tipo_usuario(pk_id_tipo_usuario)
    assert response

# ---------- Usuario ----------
#class Usuario(BaseModel):
#    id: str
#    pk_id_usuario: int
#    nombre_usuario: str
#    password: str  # NOTE: consider hashing this in production
#    email: str
#    fk_id_rol: int
#    created_at: Optional[date]
#    updated_at: Optional[date]

def test_db_get_all_usuarios():
    usuarios = db_get_all_usuarios()
    print(usuarios)
    assert usuarios

def test_db_create_usuario():
    #Notas: contraseña minimo 8, debe enviarse la confirmacion de la contraseña, verificacion obligatoria
    pk_id_tipo_usuario= 2
    tipo_usuario = db_get_tipo_usuario(pk_id_tipo_usuario)

    new_usuario = Usuario(
        id = None,
        pk_id_usuario = 1,
        nombre_usuario = "Jesus Ruiz Hernández",
        password= "1q2e3r4t",
        passwordConfirm= "1q2e3r4t",
        verified=True,
        email= "jesus.ruiz0216@alumnos.udg.mx",
        fk_id_tipo_usuario= tipo_usuario.id,
        created_at= datetime.today(),
        updated_at = datetime.today()
    )

    response = db_create_usuario(new_usuario)
    assert response.nombre_usuario == "Jesus Ruiz Hernández"


def test_db_get_usuario():
    pk_id_usuario = 1
    usuario = db_get_usuario(pk_id_usuario)
    print(usuario)
    assert usuario.pk_id_usuario == 1

def test_db_get_last_id_usuario():
    last_usuario_id = db_get_last_id_usuario()
    print(last_usuario_id)
    assert last_usuario_id >= 0

def test_db_auth_usuario():
    email = "jesus.ruiz0216@alumnos.udg.mx"
    password = "1q2e3r4t"
    usuario = db_auth_usuario(email, password)
    print(usuario)
    assert usuario.pk_id_usuario == 1

def test_db_update_usuario():
    # Asumimos que el usuario existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    pk_id_usuario = 1
    usuario = db_get_usuario(pk_id_usuario)
    usuario.nombre_usuario = "Jesus Ruiz Peréz"
    usuario.password = "12345678"
    usuario.passwordConfirm = "12345678"
    response = db_update_usuario(usuario)
    assert response.nombre_usuario == "Jesus Ruiz Peréz"

def test_db_delete_usuario():
    # Asumimos que el usuario existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    pk_id_usuario = 1
    response = db_delete_usuario(pk_id_usuario)
    assert response

def test_db_get_historial_libros():
    pk_id_usuario = 1
    historial_libros = db_get_historial_libros(pk_id_usuario)
    print(historial_libros)
    assert historial_libros

# ---------- Prestamo ----------
#class Prestamo(BaseModel):
#    id: str
#    pk_id_prestamo: int
#    fk_id_usuario: int
#    fk_id_copia: int
#    fecha_prestamo: date
#    fecha_entrega: Optional[date]
#    dias_restantes: Optional[int]
#    estatus_entrega: Optional[bool]
#    created_at: Optional[date]
#    updated_at: Optional[date]

def test_db_create_prestamo():
    #Notas: contraseña minimo 8, debe enviarse la confirmacion de la contraseña, verificacion obligatoria
    pk_id_usuario = 1
    usuario = db_get_usuario(pk_id_usuario)
    pk_id_copia_libro = 6
    copia_libro = db_get_copia_libro(pk_id_copia_libro)

    print("usuario id",usuario.id ,"copia libro",copia_libro.id)

    new_prestamo = Prestamo(
        id = None,
        pk_id_prestamo = 6,
        fk_id_copia= copia_libro.id,
        fk_id_usuario= usuario.id,
        fecha_prestamo= datetime.today(),
        fecha_entrega=None,
        dias_restantes=None,
        estatus_entrega = False,
        created_at= datetime.today(),
        updated_at = datetime.today()
    )

    response = db_create_prestamo(new_prestamo)
    assert response

def test_db_get_top():
    lista_top = db_get_top_libros(10)
    print(lista_top)
    assert lista_top

def test_db_get_last_id_prestamos():
    last_prestamo_id = db_get_last_id_prestamos()
    print(last_prestamo_id)
    assert last_prestamo_id >= 0

def test_db_get_mis_prestamos():
    pk_id_usuario = 1
    events = db_get_mis_prestamos_pendientes(pk_id_usuario)
    print(events)
    assert events

def test_db_get_historial_prestamos():
    pk_id_usuario = 1
    historial = db_get_historial_prestamos(pk_id_usuario)
    print(historial)
    assert historial

def test_db_get_generos_leidos():
    pk_id_usuario = 1
    conteo_generos_leidos = db_get_generos_leidos(pk_id_usuario)
    print(conteo_generos_leidos)
    assert conteo_generos_leidos

def test_db_get_prestamos_por_mes():
    pk_id_usuario = 1
    libros_por_mes = db_get_prestamos_por_mes(pk_id_usuario)
    print(libros_por_mes)
    assert libros_por_mes

def test_db_get_prestamo():
    pk_id_prestamo = 1
    prestamo = db_get_prestamo(pk_id_prestamo)
    assert prestamo.pk_id_prestamo == 1

def test_db_update_prestamo():
    # Asumimos que el prestamo existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    pk_id_prestamo = 1
    prestamo = db_get_prestamo(pk_id_prestamo)
    prestamo.dias_restantes = 5
    response = db_update_prestamo(prestamo)
    assert response.dias_restantes == 5

def test_db_delete_prestamo():
    # Asumimos que el prestamo existe y que se va a enviar a actualizar, si no es asi,
    # se evalua desde los servicios
    pk_id_prestamo = 1
    response = db_delete_prestamo(pk_id_prestamo)
    assert response
