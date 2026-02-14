import uuid
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from typing import Dict, Any, Optional, List, Tuple

# ── Helpers ────────────────────────────────────────────────────────────────────

def _epoca_desde_fecha(fecha_str) -> str:
    """Convierte fecha_publicacion a época legible."""
    try:
        year = int(str(fecha_str)[:4])
        if year < 1900:
            return "Clásico (antes de 1900)"
        elif year < 1970:
            return "Moderno (1900-1969)"
        elif year < 2000:
            return "Contemporáneo (1970-1999)"
        else:
            return "Reciente (2000 en adelante)"
    except Exception:
        return "Desconocido"


def _rango_estrellas(estrellas) -> str:
    """Agrupa estrellas en rangos para no ser tan restrictivo."""
    try:
        val = int(estrellas)
        if val <= 2:
            return "Cualquiera"
        elif val == 3:
            return "Bueno (3+)"
        elif val == 4:
            return "Muy bueno (4+)"
        else:
            return "Excelente (5)"
    except Exception:
        return "Cualquiera"


# ── Definición de preguntas ────────────────────────────────────────────────────

PREGUNTAS_ORDEN: List[Dict[str, str]] = [
    {
        "clave": "genero_nombre",
        "pregunta": "¿Qué género literario prefieres?",
    },
    {
        "clave": "departamento_nombre",
        "pregunta": "¿De qué área o departamento te gustaría el libro?",
    },
    {
        "clave": "epoca",
        "pregunta": "¿De qué época te gustaría que fuera el libro?",
    },
    {
        "clave": "rango_estrellas",
        "pregunta": "¿Qué calificación mínima esperas del libro?",
    },
]

# Textos amigables para la explicación final
CLAVE_LABEL: Dict[str, str] = {
    "genero_nombre":       "género",
    "departamento_nombre": "área o departamento",
    "epoca":               "época de publicación",
    "rango_estrellas":     "calificación",
}

# ── Almacén de sesiones en memoria ─────────────────────────────────────────────
_sesiones: Dict[str, Dict[str, Any]] = {}


class LibroExpertSystem:
    """
    Sistema experto basado en árbol de decisión.
    Gestiona sesiones Akinator: pregunta → respuesta → ... → top 3 libros + explicación.
    """

    def __init__(self, libros: List[Dict[str, Any]]):
        self.df_original = pd.DataFrame(libros)
        self.encoders: Dict[str, LabelEncoder] = {}
        self.model = DecisionTreeClassifier(criterion="entropy", random_state=42)
        self._features = [p["clave"] for p in PREGUNTAS_ORDEN]
        self._prepare()
        self._train()

    # ── Preparación y entrenamiento ───────────────────────────────────────────

    def _prepare(self):
        self.df = self.df_original.copy()

        # Columnas derivadas
        self.df["epoca"] = self.df_original.get(
            "fecha_publicacion", pd.Series(["Desconocido"] * len(self.df))
        ).apply(_epoca_desde_fecha)

        self.df["rango_estrellas"] = self.df_original.get(
            "estrellas", pd.Series(["Desconocido"] * len(self.df))
        ).apply(_rango_estrellas)

        # Rellenar nulos
        for col in self._features:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna("Desconocido").astype(str)
            else:
                self.df[col] = "Desconocido"

        # Encodear
        for col in self._features:
            encoder = LabelEncoder()
            self.df[col] = encoder.fit_transform(self.df[col])
            self.encoders[col] = encoder

    def _train(self):
        X = self.df[self._features]
        y = self.df_original["pk_id_libro"]
        self.model.fit(X, y)

    # ── API de sesión ─────────────────────────────────────────────────────────

    def nueva_sesion(self) -> Tuple[str, Dict[str, Any]]:
        sesion_id = str(uuid.uuid4())
        _sesiones[sesion_id] = {"respuestas": {}, "paso": 0}
        return sesion_id, self._pregunta_actual(sesion_id)

    def responder(self, sesion_id: str, clave: str, valor: str) -> Dict[str, Any]:
        if sesion_id not in _sesiones:
            raise ValueError(f"Sesión '{sesion_id}' no encontrada o expirada.")

        sesion = _sesiones[sesion_id]
        sesion["respuestas"][clave] = valor
        sesion["paso"] += 1

        if sesion["paso"] >= len(PREGUNTAS_ORDEN):
            resultado = self._predecir_top3(sesion["respuestas"])
            del _sesiones[sesion_id]
            return {"finalizado": True, **resultado}

        return {"finalizado": False, **self._pregunta_actual(sesion_id)}

    # ── Métodos internos ──────────────────────────────────────────────────────

    def _pregunta_actual(self, sesion_id: str) -> Dict[str, Any]:
        sesion = _sesiones[sesion_id]
        paso = sesion["paso"]
        info = PREGUNTAS_ORDEN[paso]
        return {
            "pregunta": info["pregunta"],
            "clave": info["clave"],
            "opciones": self._opciones_para(info["clave"]),
            "progreso": paso + 1,
            "total": len(PREGUNTAS_ORDEN),
        }

    def _opciones_para(self, clave: str) -> List[str]:
        """Devuelve valores únicos para cada clave, usando columnas derivadas si aplica."""
        if clave == "epoca":
            valores = self.df_original.get(
                "fecha_publicacion", pd.Series()
            ).apply(_epoca_desde_fecha).unique().tolist()
        elif clave == "rango_estrellas":
            valores = self.df_original.get(
                "estrellas", pd.Series()
            ).apply(_rango_estrellas).unique().tolist()
        elif clave in self.df_original.columns:
            valores = (
                self.df_original[clave]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        else:
            return []

        return sorted(set(valores))

    def _predecir_top3(self, respuestas: Dict[str, str]) -> Dict[str, Any]:
        """Devuelve top 3 libros con porcentaje de confianza, modo y explicación."""
        fila = {}
        for col in self._features:
            valor = respuestas.get(col, "Desconocido")
            encoder = self.encoders[col]
            fila[col] = (
                int(encoder.transform([valor])[0])
                if valor in encoder.classes_
                else 0
            )

        entrada = pd.DataFrame([fila])
        probas = self.model.predict_proba(entrada)[0]
        clases = self.model.classes_

        top_indices = probas.argsort()[::-1][:3]
        top3 = [
            {
                "pk_id_libro": int(clases[i]),
                "confianza": round(float(probas[i]) * 100, 1),
            }
            for i in top_indices
            if probas[i] > 0
        ]

        # Modo: exacto si el primer resultado tiene confianza >= 80%
        confianza_top = top3[0]["confianza"] if top3 else 0
        modo = "exacto" if confianza_top >= 80 else "sugerencias"

        return {
            "top3": top3,
            "modo": modo,
            "entrenado_con": len(self.df_original),
            "explicacion": self._generar_explicacion(respuestas),
        }

    def _generar_explicacion(self, respuestas: Dict[str, str]) -> str:
        """Genera texto explicando los criterios usados."""
        partes = [
            f"{CLAVE_LABEL.get(clave, clave)}: {valor}"
            for clave, valor in respuestas.items()
            if valor and valor.lower() != "desconocido"
        ]
        if not partes:
            return "Te recomendamos estos libros basándonos en nuestro catálogo."
        return f"Te recomendamos estos libros basándonos en tu preferencia de {', '.join(partes)}."