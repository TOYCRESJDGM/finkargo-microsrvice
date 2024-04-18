# Microservicio de Gestión NPS (Net Promoters Score)

Este microservicio tiene como objetivo gestionar los datos de empresas en LATAM, como pueden ser proveedores, beneficiarios, partners, fiduciarias, bancos, entre otros. Además, permite administrar los diferentes tipos de cargos asociadas a cada empresa, como accionistas, contactos, consultores y gestores de cuentas. También proporciona información sobre la puntuación NPS (Net Promoter Score) que cada persona nos ha otorgado.

## Características Principales

- Gestión completa de datos de empresas y cargos asociados.
- Registro y Autenticación de usuarios.
- Seguimiento detallado de las calificaciones NPS.

Todo esto se realiza por medio de Operaciones CRUD para empresas, cargos, personas y calificaciones NPS.

## Requisitos del Proyecto

Para implementar esta funcionalidad se utilizo:

1. **Base de Datos**: Una base de datos relacional para almacenar la información de empresas, cargos, personas y calificaciones NPS.

2. **API REST**: Una API RESTful para exponer los endpoints necesarios para la gestión de datos.

3. **Seguridad**: Asegurar que la API requiera autenticación para acceder a los datos sensibles. 

4. **Documentación**: Generar una documentación clara y completa de la API para facilitar su uso. 

5. **Despliegue**: Digrama de como desplegar el microservicio en un entorno de producción para su uso continuo. 

## Tecnologías Utilizadas

- **Base de Datos**: PostgreSQL
- **Framework Web**: FastAPI (Python)
- **Autenticación**: JWT (JSON Web Tokens)
- **Documentación**: Swagger UI
- **Despliegue**: Docker, Kubernetes

## Apectos relevantes
El proyecto puede correrse atraves del dockerfile, especificado en el mismo o por medio del comando (tener en cuenta el archivo requirements.txt)

```bash
uvicorn main:app
```

### Documentación
Toda la documentación relacionada al microservicio se encuentra en un archivo yaml (openapi.yaml) o tambien al momento de desplegar el app en la ruta /docs.

![image](https://github.com/TOYCRESJDGM/finkargo-microsrvice/assets/69774985/b9bb4a8c-bafa-41bc-85fb-1f8df2bc7481)

### Diagramas

Se trato de incluir Diagramas que tratasen de explicar, la forma en la que se podria desplegar a produccion y que tecnologias utilizar en cada momento, asi como tambien la relacion entre las entidades (clases) y ha rasgo general el funcionamiento del microservicio. Estos se encuentran en la carpeta diagrams

![image](https://github.com/TOYCRESJDGM/finkargo-microsrvice/assets/69774985/a41d3c09-d50a-4524-8984-9ea6fe0bd7ee)

### Data

La carga de paises, se realiza por medio del api <a href="https://restcountries.com/v2/all" target="blank"> "Rest Countries" V2. </a> y se realiza al momento de inicializar el servicio.
Mientras que para las demas tablas tambien se incluyeron algunos datos de prueba ubicados en la carpeta data (data.sql)

### Reportes 
Para los reportes se tienen la ruta nps/general/reports en el cual se trato de dar solucion al item2 de Reportes, esta requiere del query param "option" que va de 1 a 4 para mostrar diferentes reportes, en caso de no tenerlo sera 1. :

- Clasificar las encuestas por mes dentro indicando cual es el detractor vs promotor mas alto de cada país (Option 1)
- Muestreo del NPS por país clasificándolos un top 3 de de los países con más encuestas con detractores (Option 2 - 3)
- Clasificar los tipos de personas con mayor calificación de promotor (Option 4)

  ![image](https://github.com/TOYCRESJDGM/finkargo-microsrvice/assets/69774985/74d8edb9-a4d0-4373-8d77-a682b27e81ef)

Para el requisito:

- Un usuario logueado puede ver los datos de todos los clientes que calificaron a la empresa por debajo de 4 puntos, y la posibilidad de enviar un registro de log de que fue contactado.
- 
Se hace uso de la ruta nps/reports/lower_score/{entity_id}

![image](https://github.com/TOYCRESJDGM/finkargo-microsrvice/assets/69774985/c285747f-e06d-4364-aba0-ecbc21767877)

