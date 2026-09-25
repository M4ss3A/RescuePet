# Primera entrega

* [Informe presentado en PDF](./RescuePet_Primera_Entrega.pdf)
* Estado: propuesta revisada por el tutor.
* Resultado: propuesta aceptada con observaciones para mejorar la medición, la viabilidad y la planificación.

## Correcciones incorporadas

### Priorización del MVP

En caso de necesitar reducir el alcance por falta de tiempo, las funcionalidades se desarrollarán según el siguiente orden:

1. **Prioridad alta:** usuarios y roles básicos, registro de animales y rescates, actualización de estados, publicaciones, solicitudes y confirmación de adopciones.
2. **Prioridad media:** historial de salud, hogares de tránsito y seguimiento posterior.
3. **Prioridad baja:** panel de información e indicadores generales.
4. **Funcionalidades opcionales:** compatibilidad automática, estadísticas avanzadas, notificaciones y autenticación avanzada.

Las funcionalidades de prioridad alta conforman el flujo mínimo necesario para demostrar el funcionamiento principal del sistema.

### Medición del impacto

El impacto de RescuePet se evaluará comparando el proceso manual con el uso de la aplicación mediante casos de prueba equivalentes.

Se tendrán en cuenta los siguientes indicadores:

* Tiempo necesario para consultar la información completa de un animal.
* Cantidad de datos obligatorios faltantes.
* Cantidad de registros o publicaciones duplicadas.
* Porcentaje de cambios de estado que conservan fecha y responsable.
* Cantidad de adopciones con seguimiento registrado.

Antes de la validación se realizará una medición inicial utilizando registros y planillas simuladas. Luego se repetirán las mismas tareas en RescuePet para comparar los resultados.

### Objetivos medibles

* Completar al menos tres casos de prueba que recorran el proceso desde el rescate hasta la adopción y el seguimiento.
* Reducir al menos un 50 % el tiempo necesario para encontrar la información completa de un animal respecto del proceso manual simulado.
* Registrar el 100 % de los cambios de estado de los animales utilizados en las pruebas.
* Evitar registros duplicados mediante validaciones y reglas de negocio.
* Mantener completa la información obligatoria de todos los casos utilizados durante la demostración.
* Publicar una versión funcional y accesible online junto con su documentación.

### Viabilidad de conocimiento

El equipo cuenta con los conocimientos técnicos necesarios para desarrollar la aplicación utilizando Java, Spring Boot, JPA/Hibernate, MySQL y tecnologías web.

Actualmente no se dispone de contacto directo con rescatistas, protectoras u hogares de tránsito. Por este motivo, el conocimiento del dominio se obtendrá mediante fuentes públicas, análisis de plataformas existentes y casos de prueba simulados.


### Distribución de responsabilidades

* **Ayelen:** backend, base de datos, entidades y relaciones.
* **Gabriel:** frontend, pantallas, navegación e integración visual.
* **Ambos integrantes:** requisitos, reglas de negocio, integración entre frontend y backend, pruebas, despliegue y documentación final.

La distribución podrá ajustarse según las necesidades de integración y el avance real de cada etapa.

### Datos personales y privacidad

RescuePet administrará datos personales de adoptantes, rescatistas y hogares de tránsito. El sistema recopilará solamente la información necesaria para sus funciones y restringirá el acceso según el rol de cada usuario.

Durante el desarrollo y las pruebas se utilizarán datos ficticios. También se evitará exponer públicamente domicilios, teléfonos, correos electrónicos u otra información privada.

El proyecto tendrá en cuenta los principios generales de la [Ley N.º 25.326 de Protección de Datos Personales](https://www.argentina.gob.ar/aaip/datospersonales).




