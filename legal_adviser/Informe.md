# Prueba Técnica Científico de datos DataKnow - Caso 2 - 
## Carolina Rojas Duque - 19 de octubre de 2025

## Explicación del caso

El presente caso aborda el desarrollo de un sistema para la aceleración de consultas legales sobre una base de datos de casos previos. Se propone la creación de una Prueba de Concepto (PoC) que permita dar respuesta a preguntas específicas con base en un conjunto de demandas relacionadas con redes sociales.

Se contempla además la evaluación de la implementación propuesta mediante la respuesta a un conjunto de preguntas predefinidas, con el objetivo de validar las capacidades y limitaciones de la solución desarrollada.

## Supuestos

Para la Prueba de Concepto se considera pertinente la utilización de recursos de bajo costo y rápida implementación, con el fin de validar la viabilidad técnica y económica de la alternativa propuesta tan rápido como sea posible. Por tal motivo, se opta por:

- Utilizar bases de datos vectoriales locales en lugar de soluciones cloud empresariales.
- Emplear modelos de lenguaje de bajo costo y requisitos computacionales moderados.
- Prescindir de la implementación de una interfaz de usuario (UI) en esta etapa inicial.

Esta decisión permite enfocar los esfuerzos en validar la arquitectura del sistema de Retrieval-Augmented Generation (RAG) y la calidad de las respuestas generadas, dejando la interfaz de usuario para fases posteriores del desarrollo, una vez demostrada la viabilidad del enfoque técnico.

Se asume además que el conjunto de datos proporcionado es representativo de las características de las consultas reales que el sistema deberá atender en producción.

## Formas para resolver el caso y la opción tomada en esta prueba

La consulta eficiente sobre fuentes de información es un problema clásico de los sistemas de Information Retrieval (IR). Esta disciplina ha mantenido relevancia desde hace varias décadas, y sus avances fundamentan el funcionamiento de motores de búsqueda como Google, donde cada consulta busca recuperar información relevante de una base de conocimiento (Knowledge Base).

En el contexto de los avances tecnológicos recientes, y considerando las directrices del ejercicio respecto al uso de IA generativa y la respuesta automática de preguntas en lenguaje natural, se identifica que los sistemas de IR clásicos pueden resultar insuficientes para este caso de uso. El problema puede abordarse de manera más satisfactoria mediante un patrón de Generación Aumentada por Recuperación (Retrieval-Augmented Generation - RAG), donde un modelo de lenguaje grande (LLM) responde preguntas tras enriquecer su contexto con documentos específicos recuperados dinámicamente de la base de casos.

### Alternativas evaluadas

**1. Contexto extendido con toda la base de datos**

Actualmente existen modelos con ventanas de contexto superiores a dos millones de tokens, lo que teóricamente permitiría incluir la totalidad de la base de casos en cada consulta. Sin embargo, esta aproximación presenta limitaciones significativas:

- Degradación del rendimiento en contextos extensos, con pérdida de precisión en la recuperación de información relevante.
- Costos operacionales elevados debido al alto volumen de tokens de entrada por llamada.
- Escalabilidad limitada ante el crecimiento esperado de la base de conocimiento.

**2. Fine-tuning de modelos especializados**

El entrenamiento especializado de modelos con conocimiento específico del dominio legal constituye una alternativa técnicamente viable. No obstante, se descarta por las siguientes razones:

- Mayor complejidad y tiempo de implementación.
- Costos significativamente superiores en infraestructura y recursos computacionales.
- Menor flexibilidad para incorporar nuevos casos, requiriendo reentrenamiento periódico.
- El conocimiento del modelo queda "congelado" en el momento del entrenamiento, sin capacidad de actualización dinámica.

**3. Sistema RAG (seleccionado)**

La arquitectura RAG se selecciona como la solución óptima por combinar las siguientes ventajas:

- Capacidad de enfoque contextual en información específicamente relevante para cada consulta.
- Escalabilidad natural mediante la adición de nuevos documentos a la base vectorial sin modificar el modelo. 
- Relación costo-beneficio favorable al utilizar modelos base sin necesidad de entrenamiento adicional.
- Flexibilidad para actualizar y expandir la base de conocimiento de forma continua.
- Trazabilidad de las fuentes utilizadas para generar cada respuesta, aspecto crítico en aplicaciones legales.


## Resultados del análisis de los datos y los modelos

### Análisis exploratorio de datos

Se inició el proceso con una exploración manual del archivo Excel conteniendo la información de las demandas. Esta revisión preliminar permitió examinar la estructura de campos, verificar el volumen total de casos (número exacto de demandas) y estimar el tamaño de información asociada a cada registro. Este análisis confirmó la pertinencia de implementar un sistema RAG dada la extensión y complejidad del dataset.

Una decisión arquitectónica clave fue garantizar que la información de **cada demanda permaneciera en un mismo chunk durante el proceso de embebimiento**, evitando así la fragmentación de casos individuales entre múltiples vectores. Esta estrategia preserva la integridad contextual de cada demanda y mejora la coherencia de las respuestas generadas.

### Implementación técnica

**Base de datos vectorial**

Se seleccionó ChromaDB como gestor de la base de datos vectorial por las siguientes características:

- Facilidad de implementación y configuración mínima
- Capacidad de persistencia local sin dependencias externas
- Acceso gratuito y open-source

Para la estrategia de retrieval se implementó el enfoque más directo: embebimiento semántico seguido de recuperación de los *k=3* chunks más similares mediante búsqueda por similitud. Se utilizó el modelo de embebimiento de OpenAI (`text-embedding-3-small`) junto con el modelo de lenguaje `gpt-4o-mini` para la generación de respuestas, con un costo total de implementación inferior a $0.01 USD mediante API key personal.

**Pipeline RAG**

La implementación del sistema de pregunta-respuesta se desarrolló utilizando LangChain, framework seleccionado por su madurez en el ecosistema de aplicaciones LLM y su amplia documentación. El pipeline consiste en una cadena secuencial de pregunta-retrieval-respuesta que aprovecha las abstracciones predefinidas de LangChain para simplificar significativamente el código y acelerar el desarrollo.

### Evaluación de resultados

Con la infraestructura funcional, se procedió a evaluar el sistema mediante un conjunto de preguntas de prueba. Los resultados obtenidos se presentan a continuación:

**PREGUNTA 1 y 2: ¿Cuáles son las sentencias de 3 demandas? Y de qué trataron?**

Claro, aquí te resumo las sentencias de tres demandas:

1. **Sentencia T-242/22**:
   - **Fecha**: 10 de noviembre de 2022.
   - **Tema**: Se trató de una solicitud de nulidad presentada por Marcel Dousse y Daniel Mendoza Leal, quienes argumentaron que la sentencia anterior había vulnerado su derecho al debido proceso. Sin embargo, la Corte Constitucional rechazó estas solicitudes porque no presentaron argumentos claros que demostraran que la decisión original tenía errores significativos. En resumen, la Corte decidió que no había razones suficientes para anular la sentencia.


2. **Sentencia T-452/22**:
   - **Fecha**: 12 de diciembre de 2022.
   - **Tema**: En este caso, un director de cine, Ciro Alfonso Guerra Picón, alegó que sus derechos al buen nombre y a la presunción de inocencia fueron violados por dos periodistas que publicaron un reportaje sobre acusaciones de acoso sexual en su contra. La Corte decidió no proteger sus derechos, argumentando que las periodistas actuaron dentro de su derecho a la libertad de expresión y que el reportaje era de interés público. Además, se consideró que el director estaba abusando del sistema judicial al presentar múltiples demandas.
   

3. **Sentencia C-487/23**:
   - **Fecha**: 15 de noviembre de 2023.
   - **Tema**: Esta sentencia se ocupó de la constitucionalidad de las penas de prisión por los delitos de injuria y calumnia. La Corte analizó si las penas eran compatibles con la libertad de expresión. Al final, la Corte declaró que las normas que establecen penas de prisión para estos delitos eran válidas y no violaban la Constitución, ya que no se dirigían específicamente a periodistas y ofrecían alternativas para resolver conflictos sin necesidad de prisión.

Si necesitas más detalles sobre alguno de estos casos, ¡dímelo!

**PREGUNTA 3: ¿Cuál fue la sentencia del caso que habla de acoso escolar?**

Hay varios casos que tratan sobre acoso escolar. Aquí te resumo dos de ellos:

1. **Caso de Paola (Sentencia T-249/24)**: En este caso, la madre de Paola denunció que su hija sufrió acoso escolar y que esto le causó problemas de salud mental, como depresión y ansiedad. La corte decidió que la institución educativa no hizo lo suficiente para proteger a Paola y no respondió adecuadamente a sus solicitudes. Como resultado, se ordenó que la escuela ofreciera disculpas públicas y que implementara una estrategia para prevenir y manejar el acoso escolar. También se le garantizó a Paola el acceso a una educación adecuada y se le permitió hacer una nivelación de materias.


2. **Caso de Sara (Sentencia T-449/23)**: Aquí, se trató el caso de Sara, quien fue víctima de ciberacoso en su colegio. La corte determinó que el colegio no investigó adecuadamente los hechos de ciberacoso y, por lo tanto, vulneró los derechos de Sara a la educación y al debido proceso. Se ordenó que el colegio realizara una investigación sobre el ciberacoso y que ofreciera disculpas públicas si así lo deseaba Sara. Además, se le aseguró a Sara la posibilidad de continuar su educación en otra institución.

Ambos casos resaltan la importancia de que las escuelas actúen de manera efectiva para proteger a los estudiantes del acoso y garantizar su derecho a una educación segura y digna.

**PREGUNTA 4: ¿Diga el detalle de la demanda relacionada con acoso escolar?**

Claro, aquí te explico algunos casos de demandas relacionadas con acoso escolar de manera sencilla:

1. **Caso de Camila y Paola (T-249/24)**:
   - **Contexto**: Camila, como madre, demandó a la Institución Educativa Sol porque su hija Paola fue víctima de acoso escolar (matoneo) y esto le causó problemas de salud mental, incluyendo depresión y ansiedad.
   - **Problema**: La escuela no tomó medidas para proteger a Paola ni para ayudarla con su educación, lo que llevó a que reprobara el año escolar.
   - **Decisión**: La corte decidió que la escuela había violado los derechos de Paola y ordenó que se hicieran disculpas públicas, se implementaran estrategias para ayudar a Paola y se revisara el manual de convivencia de la escuela para prevenir futuros casos de acoso.


2. **Caso de Sara (T-449/23)**:
   - **Contexto**: Sara fue víctima de ciberacoso en su colegio, y la escuela no investigó adecuadamente lo sucedido.
   - **Problema**: Esto afectó su dignidad y su derecho a la educación, ya que no pudo continuar en la escuela donde sufrió el acoso.
   - **Decisión**: La corte ordenó al colegio que investigara el ciberacoso y que ofreciera disculpas públicas. También se le pidió que asegurara que en el futuro se investigaran todos los casos de acoso escolar de manera adecuada.


3. **Caso de TBQ (T-252/23)**:
   - **Contexto**: La madre de TBQ demandó porque su hijo sufrió acoso escolar y la escuela no actuó para protegerlo.
   - **Problema**: Esto llevó a que TBQ se retirara del colegio, y la madre buscaba una compensación económica por los gastos que tuvo que hacer.
   - **Decisión**: La corte encontró que la escuela había violado los derechos de TBQ y ordenó que se implementaran medidas para prevenir el acoso escolar en el futuro, además de ofrecer disculpas y un plan de reparación para el niño.

En resumen, estos casos muestran cómo las escuelas tienen la responsabilidad de proteger a los estudiantes del acoso escolar y de actuar de manera efectiva cuando ocurren estos incidentes. Las decisiones de la corte buscan garantizar que se respeten los derechos de los niños y se tomen medidas para evitar que situaciones similares se repitan.

**PREGUNTA 5: ¿Existen casos que hablan sobre el Plan Individual de Ajustes Razonables (PIAR)? Indique de qué trataron los casos y cuáles fueron sus sentencias**

Lo siento, pero no tengo información específica sobre casos que hablen sobre el Plan Individual de Ajustes Razonables (PIAR). Los casos que tengo son sobre conflictos de jurisdicción en temas de recobros de prestaciones de salud no incluidas en el plan de beneficios de salud (PBS), pero no mencionan el PIAR. Si necesitas información sobre otro tema o caso específico, estaré encantado de ayudarte.

### Análisis de desempeño

**Fortaleza observada: Comprensión de casos de acoso escolar**

El sistema demostró desempeño sobresaliente en las consultas relacionadas con acoso escolar. El modelo logró:

- Identificar múltiples demandas relacionadas con la temática.
- Recuperar información precisa y relevante de los casos pertinentes.
- Generar respuestas en lenguaje claro y accesible, manteniendo la precisión técnica necesaria.
  
**Limitación identificada: Ausencia de memoria conversacional**

Las dos primeras preguntas propuestas en el ejercicio se consolidaron en una única consulta debido a que la implementación actual carece de capacidad de memoria entre interacciones. El sistema no mantiene un historial conversacional que le permita referenciar demandas mencionadas en consultas previas. Esta limitación constituye una oportunidad de mejora clara para iteraciones futuras mediante la implementación de un buffer de memoria conversacional.

**Debilidad identificada: Fallo en recuperación de términos específicos (PIRA)**

El sistema no logró recuperar exitosamente demandas relacionadas con PIRA, a pesar de que un análisis manual de la base de datos confirma la existencia de al menos dos casos vinculados a esta temática. Este fallo se atribuye a las siguientes causas potenciales:

- El embebimiento semántico prioriza similitud conceptual sobre coincidencia léxica exacta.
- El término "PIRA" puede no tener representación semántica suficiente en el espacio vectorial del modelo de embebimiento.
- La descripción contextual agregada en la pregunta no fue suficiente para establecer la conexión semántica necesaria.

Esta limitación sugiere la implementación de estrategias de retrieval híbridas que combinen búsqueda semántica con búsqueda basadas en palabras claves para capturar tanto similitud conceptual como coincidencias terminológicas exactas.

### Conclusiones

A pesar de las limitaciones identificadas en esta implementación inicial, el sistema demuestra capacidades valiosas para:

- Comprensión y análisis de consultas en lenguaje natural.
- Generación de resúmenes precisos de casos relevantes.
- Aceleración significativa en la exploración de bases de datos jurídicas extensas.
- Presentación de información legal en lenguaje accesible sin sacrificar precisión.

Se concluye que la Prueba de Concepto cumple exitosamente su objetivo de validar la viabilidad del enfoque RAG para el problema planteado. Más aún, las limitaciones identificadas no son inherentes a la arquitectura propuesta sino deficiencias implementativas con caminos de mejora claramente definidos, lo que fortalece la propuesta de valor de continuar el desarrollo en esta dirección.


## Futuros ajustes o mejoras


Existen numerosas variaciones y extensiones sobre la arquitectura RAG base que han demostrado utilidad según las características específicas de la Knowledge Base y los requisitos del caso de uso. En el marco de esta Prueba de Concepto, y considerando las restricciones temporales del ejercicio, se optó por implementar el sistema más directo: embebimiento semántico para retrieval y adición simple de chunks al contexto del agente. Como se documentó en la sección de resultados, características como memoria conversacional y estrategias de retrieval avanzadas fueron deliberadamente excluidas de esta fase inicial, pero se identifican como prioritarias para el desarrollo futuro.

La implementación de retrieval híbrido constituye una mejora fundamental para abordar las limitaciones observadas. Una aproximación recomendada consiste en:

- Expandir el número de chunks recuperados (por ejemplo, k=10)
- Distribuir la recuperación entre dos estrategias complementarias:
  - 5 chunks mediante similitud semántica (embeddings)
  - 5 chunks mediante similitud por palabras clave.

Esta estrategia aumenta la complejidad computacional moderadamente, pero robustece significativamente el sistema frente a consultas que requieren coincidencia exacta de términos técnicos o acrónimos, como se evidenció en el caso de PIRA.

Otro eje de posible mejora consiste en la **exploración de modelos de embebimiento de mayor dimensionalidad** (como `text-embedding-3-large` o modelos especializados del dominio legal), ya que esto permitiría capturar representaciones semánticas más ricas. Si bien esto incrementa los costos operacionales, puede traducirse en mejoras significativas en la precisión del retrieval.

Además, considerar el **uso de modelos de lenguaje con ventanas de contexto más amplias** permitiría recuperar un mayor número de chunks relevantes (k=5-10), incluir contexto adicional sin sacrificar información crítica y mejorar la capacidad del modelo para sintetizar información de múltiples fuentes.

Otro eje de exploración interesante es **mejorar la estrategia de indexación y almacenamiento de chunks**, explorando por ejemplo la fragmentación de demandas extensas en múltiples chunks semánticos, pero agregando en la metadata cuáles chunks pertenecen a la misma demanda, para poder recuperarlos todos en caso de que uno de ellos marque alta similitud. Esta estrategia de chunking jerárquico equilibra la granularidad del retrieval con la integridad contextual de cada caso. 

Para finalizar estas ideas alrededor de la optimización del RAG, resulta indispensable la **creación de un dataset curado de evaluación** que incluya preguntas representativas, respuestas de referencia validadas por expertos legales, y las demandas relevantes esperadas para cada consulta. Este dataset permitiría evaluar numéricamente el desempeño de las diferentes alternativas mediante métricas estándar como precisión y recall del retrieval y métricas de calidad de respuesta (fidelidad, relevancia, completitud)

Otros trabajos futuros apuntan a llevar el sistema a una etapa de MVP o producción, tales como:

- Elaborar una interfaz de usuario minimalista que permita a los usuarios legales interactuar con la herramienta y visualizar su funcionamiento (se planteó inicialmente implementar una aplicación de Streamlit para esta prueba, pero se descartó por las restricciones temporales) 
- Migrar la base de datos vectorial a servicios en nube gestionados para mejorar escalabilidad y disponibilidad, junto con la automatización de la actualización de dicha base cuando se modifiquen o agreguen archivos con nuevas demandas mediante pipelines de reindexación incremental. 
- Implementar el manejo de logs y sesiones para rastrear interacciones y facilitar debugging, así como métricas de monitoreo sobre latencia, costos por consulta y tasa de éxito. 
- Aplicar Guardrails para garantizar que tanto las preguntas de los usuarios como las respuestas del modelo se ajusten a comportamientos adecuados y acordes con la finalidad del producto, validando entradas para filtrar consultas fuera del dominio y salidas para detectar alucinaciones o información inconsistente. 
- Explorar el fine-tuning de modelos especializados para el dominio legal, con el fin de proporcionarles conocimiento adicional de la terminología jurídica y potenciar la calidad de las respuestas dirigidas a profesionales del derecho, aunque esta mejora debe evaluarse cuidadosamente considerando el balance entre costo de desarrollo, mantenimiento continuo, y el beneficio incremental sobre la arquitectura RAG optimizada.