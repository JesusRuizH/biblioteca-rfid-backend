from app.pb_clients.departamento import *
from app.pb_clients.libros import *
from app.pb_clients.copias_libros import *
from app.pb_clients.tipo_usuario import *
from app.pb_clients.usuarios import *
from app.pb_clients.prestamos import *
from app.pb_clients.generos import *
from app.core.auth import db_get_client
from app.models.db_models import *

def test_agregar_libros():
  fecha = datetime.today()
  fecha_hoy = fecha.strftime("%Y-%m-%d %H:%M:%S")
  libros_json = [
    {
      "id": 1,
      "titulo": "Cien años de soledad",
      "autor": "Gabriel García Márquez",
      "isbn": "9788497592208",
      "fecha_publicacion": "1967-05-30",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/cien_anos_de_soledad.webp",
      "copias": 1,
      "genero": "Realismo mágico",
      "categoria": "Ficción"
    },
    {
      "id": 2,
      "titulo": "1984",
      "autor": "George Orwell",
      "isbn": "9780451524935",
      "fecha_publicacion": "1949-06-08",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/1984.webp",
      "copias": 1,
      "genero": "Distopía",
      "categoria": "Ficción"
    },
    {
      "id": 3,
      "titulo": "Don Quijote de la Mancha",
      "autor": "Miguel de Cervantes",
      "isbn": "9788491050292",
      "fecha_publicacion": "1605-01-16",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/don_quijote_de_la_mancha.webp",
      "copias": 1,
      "genero": "Novela clásica",
      "categoria": "Ficción"
    },
    {
      "id": 4,
      "titulo": "Orgullo y prejuicio",
      "autor": "Jane Austen",
      "isbn": "9780141439518",
      "fecha_publicacion": "1813-01-28",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/orgullo_y_prejuicio.webp",
      "copias": 1,
      "genero": "Romance",
      "categoria": "Ficción"
    },
    {
      "id": 5,
      "titulo": "Crimen y castigo",
      "autor": "Fiódor Dostoyevski",
      "isbn": "9780140449136",
      "fecha_publicacion": "1866-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/crimen_y_castigo.webp",
      "copias": 1,
      "genero": "Ficción psicológica",
      "categoria": "Ficción"
    },
    {
      "id": 6,
      "titulo": "Matar a un ruiseñor",
      "autor": "Harper Lee",
      "isbn": "9780060935467",
      "fecha_publicacion": "1960-07-11",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/matar_a_un_ruisenor.webp",
      "copias": 1,
      "genero": "Drama social",
      "categoria": "Ficción"
    },
    {
      "id": 7,
      "titulo": "El Gran Gatsby",
      "autor": "F. Scott Fitzgerald",
      "isbn": "9780743273565",
      "fecha_publicacion": "1925-04-10",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_gran_gatsby.webp",
      "copias": 1,
      "genero": "Ficción clásica",
      "categoria": "Ficción"
    },
    {
      "id": 8,
      "titulo": "En busca del tiempo perdido",
      "autor": "Marcel Proust",
      "isbn": "9782070401903",
      "fecha_publicacion": "1913-11-14",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/en_busca_del_tiempo_perdido.webp",
      "copias": 1,
      "genero": "Modernismo",
      "categoria": "Ficción"
    },
    {
      "id": 9,
      "titulo": "Ulises",
      "autor": "James Joyce",
      "isbn": "9780141182803",
      "fecha_publicacion": "1922-02-02",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/ulises.webp",
      "copias": 1,
      "genero": "Modernismo",
      "categoria": "Ficción"
    },
    {
      "id": 10,
      "titulo": "La Odisea",
      "autor": "Homero",
      "isbn": "9780140268867",
      "fecha_publicacion": "0800-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/la_odisea.webp",
      "copias": 1,
      "genero": "Épica",
      "categoria": "Poesía"
    },
    {
      "id": 11,
      "titulo": "El retrato de Dorian Gray",
      "autor": "Oscar Wilde",
      "isbn": "9780141439570",
      "fecha_publicacion": "1890-06-20",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_retrato_de_dorian_gray.webp",
      "copias": 1,
      "genero": "Gótica",
      "categoria": "Terror"
    },
    {
      "id": 12,
      "titulo": "Fahrenheit 451",
      "autor": "Ray Bradbury",
      "isbn": "9781451673319",
      "fecha_publicacion": "1953-10-19",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/fahrenheit_451.webp",
      "copias": 1,
      "genero": "Ciencia ficción",
      "categoria": "Ficción"
    },
    {
      "id": 13,
      "titulo": "El extranjero",
      "autor": "Albert Camus",
      "isbn": "9780679720201",
      "fecha_publicacion": "1942-04-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_extranjero.webp",
      "copias": 1,
      "genero": "Existencialismo",
      "categoria": "Filosofía"
    },
    {
      "id": 14,
      "titulo": "Rayuela",
      "autor": "Julio Cortázar",
      "isbn": "9788437604947",
      "fecha_publicacion": "1963-06-28",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/rayuela.webp",
      "copias": 1,
      "genero": "Experimental",
      "categoria": "Ficción"
    },
    {
      "id": 15,
      "titulo": "Pedro Páramo",
      "autor": "Juan Rulfo",
      "isbn": "9788426404681",
      "fecha_publicacion": "1955-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/pedro_paramo.webp",
      "copias": 1,
      "genero": "Realismo mágico",
      "categoria": "Ficción"
    },
    {
      "id": 16,
      "titulo": "La metamorfosis",
      "autor": "Franz Kafka",
      "isbn": "9780140184785",
      "fecha_publicacion": "1915-10-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/la_metamorfosis.webp",
      "copias": 1,
      "genero": "Ficción surrealista",
      "categoria": "Ficción"
    },
    {
      "id": 17,
      "titulo": "Los hermanos Karamazov",
      "autor": "Fiódor Dostoyevski",
      "isbn": "9780140449242",
      "fecha_publicacion": "1880-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/los_hermanos_karamazov.webp",
      "copias": 1,
      "genero": "Filosófica",
      "categoria": "Filosofía"
    },
    {
      "id": 18,
      "titulo": "Madame Bovary",
      "autor": "Gustave Flaubert",
      "isbn": "9780140449129",
      "fecha_publicacion": "1857-04-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/madame_bovary.webp",
      "copias": 1,
      "genero": "Realismo",
      "categoria": "Ficción"
    },
    {
      "id": 19,
      "titulo": "Hamlet",
      "autor": "William Shakespeare",
      "isbn": "9780451526922",
      "fecha_publicacion": "1603-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/hamlet.webp",
      "copias": 1,
      "genero": "Tragedia",
      "categoria": "Teatro"
    },
    {
      "id": 20,
      "titulo": "Macbeth",
      "autor": "William Shakespeare",
      "isbn": "9780451526779",
      "fecha_publicacion": "1606-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/macbeth.webp",
      "copias": 1,
      "genero": "Tragedia",
      "categoria": "Teatro"
    },
    {
      "id": 21,
      "titulo": "Romeo y Julieta",
      "autor": "William Shakespeare",
      "isbn": "9780451526861",
      "fecha_publicacion": "1597-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/romeo_y_julieta.webp",
      "copias": 1,
      "genero": "Tragedia romántica",
      "categoria": "Teatro"
    },
    {
      "id": 22,
      "titulo": "Drácula",
      "autor": "Bram Stoker",
      "isbn": "9780486411095",
      "fecha_publicacion": "1897-05-26",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/dracula.webp",
      "copias": 1,
      "genero": "Terror gótico",
      "categoria": "Terror"
    },
    {
      "id": 23,
      "titulo": "Frankenstein",
      "autor": "Mary Shelley",
      "isbn": "9780141439471",
      "fecha_publicacion": "1818-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/frankenstein.webp",
      "copias": 1,
      "genero": "Ciencia ficción gótica",
      "categoria": "Terror"
    },
    {
      "id": 24,
      "titulo": "El lobo estepario",
      "autor": "Hermann Hesse",
      "isbn": "9788497593828",
      "fecha_publicacion": "1927-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_lobo_estepario.webp",
      "copias": 1,
      "genero": "Existencialismo",
      "categoria": "Filosofía",
    },
    {
      "id": 25,
      "titulo": "Siddhartha",
      "autor": "Hermann Hesse",
      "isbn": "9780142437186",
      "fecha_publicacion": "1922-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/siddhartha.webp",
      "copias": 1,
      "genero": "Filosofía espiritual",
      "categoria": "Filosofía"
    },
    {
      "id": 26,
      "titulo": "La náusea",
      "autor": "Jean-Paul Sartre",
      "isbn": "9788497930616",
      "fecha_publicacion": "1938-04-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/la_nausea.webp",
      "copias": 1,
      "genero": "Existencialismo",
      "categoria": "Filosofía"
    },
    {
      "id": 27,
      "titulo": "El Principito",
      "autor": "Antoine de Saint-Exupéry",
      "isbn": "9780156013987",
      "fecha_publicacion": "1943-04-06",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_principito.webp",
      "copias": 1,
      "genero": "Fábula filosófica",
      "categoria": "Ficción"
    },
    {
      "id": 28,
      "titulo": "Alicia en el país de las maravillas",
      "autor": "Lewis Carroll",
      "isbn": "9788491050402",
      "fecha_publicacion": "1865-11-26",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/alicia_en_el_pais_de_las_maravillas.webp",
      "copias": 1,
      "genero": "Fantasía",
      "categoria": "Fantasía"
    },
    {
      "id": 29,
      "titulo": "La divina comedia",
      "autor": "Dante Alighieri",
      "isbn": "9780142437223",
      "fecha_publicacion": "1320-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/la_divina_comedia.webp",
      "copias": 1,
      "genero": "Épica religiosa",
      "categoria": "Poesía"
    },
    {
      "id": 30,
      "titulo": "El arte de la guerra",
      "autor": "Sun Tzu",
      "isbn": "9781590302255",
      "fecha_publicacion": "-0500-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_arte_de_la_guerra.webp",
      "copias": 1,
      "genero": "Filosofía militar",
      "categoria": "Filosofía"
    },
    {
      "id": 31,
      "titulo": "El código Da Vinci",
      "autor": "Dan Brown",
      "isbn": "9780307474278",
      "fecha_publicacion": "2003-03-18",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_codigo_da_vinci.webp",
      "copias": 1,
      "genero": "Thriller",
      "categoria": "Suspenso"
    },
    {
      "id": 32,
      "titulo": "Los juegos del hambre",
      "autor": "Suzanne Collins",
      "isbn": "9780439023481",
      "fecha_publicacion": "2008-09-14",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/los_juegos_del_hambre.webp",
      "copias": 1,
      "genero": "Distopía juvenil",
      "categoria": "Fantasía"
    },
    {
      "id": 33,
      "titulo": "Harry Potter y la piedra filosofal",
      "autor": "J.K. Rowling",
      "isbn": "9788478884452",
      "fecha_publicacion": "1997-06-26",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/harry_potter_y_la_piedra_filosofal.webp",
      "copias": 1,
      "genero": "Fantasía",
      "categoria": "Fantasía"
    },
    {
      "id": 34,
      "titulo": "El Hobbit",
      "autor": "J.R.R. Tolkien",
      "isbn": "9780261102217",
      "fecha_publicacion": "1937-09-21",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_hobbit.webp",
      "copias": 1,
      "genero": "Fantasía",
      "categoria": "Fantasía"
    },
    {
      "id": 35,
      "titulo": "El señor de los anillos",
      "autor": "J.R.R. Tolkien",
      "isbn": "9780261103252",
      "fecha_publicacion": "1954-07-29",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_senor_de_los_anillos.webp",
      "copias": 1,
      "genero": "Fantasía épica",
      "categoria": "Fantasía"
    },
    {
      "id": 36,
      "titulo": "It",
      "autor": "Stephen King",
      "isbn": "9780450411434",
      "fecha_publicacion": "1986-09-15",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/it.webp",
      "copias": 1,
      "genero": "Terror",
      "categoria": "Terror"
    },
    {
      "id": 37,
      "titulo": "Cementerio de animales",
      "autor": "Stephen King",
      "isbn": "9780451172419",
      "fecha_publicacion": "1983-11-14",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/cementerio_de_animales.webp",
      "copias": 1,
      "genero": "Terror",
      "categoria": "Terror"
    },
    {
      "id": 38,
      "titulo": "El resplandor",
      "autor": "Stephen King",
      "isbn": "9780307743657",
      "fecha_publicacion": "1977-01-28",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_resplandor.webp",
      "copias": 1,
      "genero": "Terror psicológico",
      "categoria": "Terror"
    },
    {
      "id": 39,
      "titulo": "El nombre del viento",
      "autor": "Patrick Rothfuss",
      "isbn": "9788401337208",
      "fecha_publicacion": "2007-03-27",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_nombre_del_viento.webp",
      "copias": 1,
      "genero": "Fantasía épica",
      "categoria": "Fantasía"
    },
    {
      "id": 40,
      "titulo": "La sombra del viento",
      "autor": "Carlos Ruiz Zafón",
      "isbn": "9788408172178",
      "fecha_publicacion": "2001-04-12",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/la_sombra_del_viento.webp",
      "copias": 1,
      "genero": "Misterio histórico",
      "categoria": "Suspenso"
    },
    {
      "id": 41,
      "titulo": "La catedral del mar",
      "autor": "Ildefonso Falcones",
      "isbn": "9788401336942",
      "fecha_publicacion": "2006-09-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/la_catedral_del_mar.webp",
      "copias": 1,
      "genero": "Ficción histórica",
      "categoria": "Ficción"
    },
    {
      "id": 42,
      "titulo": "El alquimista",
      "autor": "Paulo Coelho",
      "isbn": "9780061122415",
      "fecha_publicacion": "1988-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_alquimista.webp",
      "copias": 1,
      "genero": "Ficción espiritual",
      "categoria": "Ficción"
    },
    {
      "id": 43,
      "titulo": "Cometas en el cielo",
      "autor": "Khaled Hosseini",
      "isbn": "9781594631931",
      "fecha_publicacion": "2003-05-29",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/cometas_en_el_cielo.webp",
      "copias": 1,
      "genero": "Drama",
      "categoria": "Ficción"
    },
    {
      "id": 44,
      "titulo": "Mil soles espléndidos",
      "autor": "Khaled Hosseini",
      "isbn": "9781594483851",
      "fecha_publicacion": "2007-05-22",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/mil_soles_esplendidos.webp",
      "copias": 1,
      "genero": "Drama",
      "categoria": "Ficción"
    },
    {
      "id": 45,
      "titulo": "Ensayo sobre la ceguera",
      "autor": "José Saramago",
      "isbn": "9788483462036",
      "fecha_publicacion": "1995-10-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/ensayo_sobre_la_ceguera.webp",
      "copias": 1,
      "genero": "Ficción alegórica",
      "categoria": "Ficción"
    },
    {
      "id": 46,
      "titulo": "La tregua",
      "autor": "Mario Benedetti",
      "isbn": "9789500406342",
      "fecha_publicacion": "1960-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/la_tregua.webp",
      "copias": 1,
      "genero": "Romance",
      "categoria": "Ficción"
    },
    {
      "id": 47,
      "titulo": "El túnel",
      "autor": "Ernesto Sabato",
      "isbn": "9788437601786",
      "fecha_publicacion": "1948-01-01",
      "rfid": None,
      "imagen": "C:/Users/USUARIO/Desktop/MODULAR/informacion/imagenes_libros/el_tunel.webp",
      "copias": 1,
      "genero": "Psicológica",
      "categoria": "Otros"
    }
  ]

  for libro_json in libros_json:
    pk_id_genero = None
    if libro_json["categoria"] == "Fantasía":
      pk_id_genero = 0
      genero = db_get_genero(pk_id_genero)
    elif libro_json["categoria"] == "Ficción":
      pk_id_genero = 1
      genero = db_get_genero(pk_id_genero)
    elif libro_json["categoria"] == "Filosofía":
      pk_id_genero = 2
      genero = db_get_genero(pk_id_genero)
    elif libro_json["categoria"] == "Poesía":
      pk_id_genero = 3
      genero = db_get_genero(pk_id_genero)
    elif libro_json["categoria"] == "Suspenso":
      pk_id_genero = 4
      genero = db_get_genero(pk_id_genero)
    elif libro_json["categoria"] == "Teatro":
      pk_id_genero = 5
      genero = db_get_genero(pk_id_genero)
    elif libro_json["categoria"] == "Terror":
      pk_id_genero = 6
      genero = db_get_genero(pk_id_genero)
    else:
      pk_id_genero = 1
      genero = db_get_genero(pk_id_genero)

    libro = Libro(
      id = None,
      pk_id_libro = libro_json["id"],
      titulo= libro_json["titulo"],
      autor= libro_json["autor"],
      isbn= libro_json["isbn"],
      fecha_publicacion= libro_json["fecha_publicacion"],
      ruta_img= libro_json["imagen"],
      copias= libro_json["copias"],
      fk_id_departamento= None,
      fk_id_genero= genero.id,
      created_at= fecha_hoy,
      updated_at= fecha_hoy
    )
    response = db_create_libro(libro)
    print(libro)
