## Herramienta para Acelerar consultas legales

El presente directorio contiene los archivos para solucionar la segunda prueba técnica propuesta:

- La carpeta `data` contiene la base de datos jurídica suministrada, y en esta se generan además los datos para persistir la base de datos vectorial generada.
- La carpeta `scripts` contiene código para la generación de la base de datos vectorial, para la instanciación del sistema RAG, y un notebook mostrando las preguntas propuestas para la validación con sus respuestas. En caso de querer replicar los resultados, es necesario correr nuevamente el código para la generación de la BD, y además, dado que se usan modelos de OpenAI, es necesario crear un archivo `.env` con `OPENAI_API_KEY` válida.
- El informe requerido como entregable para la prueba se encuentra en `Informe.md`