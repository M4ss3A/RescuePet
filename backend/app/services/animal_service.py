from app.core.errors import NoEncontrado
from app.core.uow import UnitOfWork
from app.models import Animal, FotoAnimal
from app.models.enums import EstadoAnimal
from app.schemas.animal import AnimalCreate, AnimalRead, AnimalUpdate


class AnimalService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    #Funciones auxiliares (se usan dentro de un bloque `with self.uow`)

    def _a_respuesta(self, animal: Animal) -> AnimalRead:
        """Convierte el modelo en la respuesta de la API, agregando la URL de la foto principal."""
        respuesta = AnimalRead.model_validate(animal)
        foto = self.uow.animales.obtener_foto_principal(respuesta.id)
        respuesta.foto_url = foto.url if foto else None
        return respuesta

    def _obtener_o_error(self, animal_id: int) -> Animal:
        animal = self.uow.animales.obtener_por_id(animal_id)
        if animal is None:
            raise NoEncontrado("Animal no encontrado")
        return animal

    def _guardar_foto_principal(self, animal_id: int, url: str) -> None:
        """Crea la foto principal del animal o actualiza su URL si ya existía."""
        foto = self.uow.animales.obtener_foto_principal(animal_id)
        if foto is None:
            foto = FotoAnimal(animal_id=animal_id, url=url, es_principal=True)
        else:
            foto.url = url
        self.uow.animales.guardar_foto(foto)

    #Casos de uso 

    def listar(self, estado: EstadoAnimal | None = None) -> list[AnimalRead]:
        with self.uow:
            return [self._a_respuesta(animal) for animal in self.uow.animales.listar(estado)]

    def obtener(self, animal_id: int) -> AnimalRead:
        with self.uow:
            return self._a_respuesta(self._obtener_o_error(animal_id))

    def crear(self, datos: AnimalCreate) -> AnimalRead:
        with self.uow:
            animal = self.uow.animales.agregar(Animal(**datos.model_dump(exclude={"foto_url"})))
            respuesta = AnimalRead.model_validate(animal)
            if datos.foto_url:
                self._guardar_foto_principal(respuesta.id, datos.foto_url)
            return self._a_respuesta(animal)

    def actualizar(self, animal_id: int, datos: AnimalUpdate) -> AnimalRead:
        with self.uow:
            animal = self._obtener_o_error(animal_id)
            animal.sqlmodel_update(datos.model_dump(exclude_unset=True, exclude={"foto_url"}))
            self.uow.animales.agregar(animal)
            if datos.foto_url:
                self._guardar_foto_principal(animal_id, datos.foto_url)
            return self._a_respuesta(animal)

    def dar_de_baja(self, animal_id: int) -> None:
        """Baja lógica: el animal no se borra, pasa a INACTIVO para conservar su historial."""
        with self.uow:
            animal = self._obtener_o_error(animal_id)
            animal.estado = EstadoAnimal.INACTIVO
            self.uow.animales.agregar(animal)
