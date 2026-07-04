Changelog — sc-content.es.json / sc-content.en.json

Resumen de cambios aplicados en la auditoria de contenido, sincronizacion bilingue y refuerzo legal.

- Archivos afectados: [dist/sc-content/sc-content.es.json](dist/sc-content/sc-content.es.json)
- Archivos afectados: [dist/sc-content/sc-content.en.json](dist/sc-content/sc-content.en.json)
- Archivo de soporte ajustado previamente para QA visual: [dist/index.html](dist/index.html)

Cambios principales:
- Se dejo de usar el enfoque sobre el archivo quiz y se concentro el trabajo en los JSON principales de contenido en espanol e ingles.
- Se sincronizaron bloques equivalentes entre ambos idiomas para que mantengan la misma secuencia, sentido legal y nivel de detalle.
- Se corrigio la traduccion incorrecta de "sobered up" en espanol por una formulacion natural y legalmente coherente.
- Se restauro en ingles el bloque correcto sobre identificaciones falsas cuando habia quedado reemplazado por texto de intoxicacion.
- Se alineo la logica de verificacion de edad e identificacion en ambos idiomas para evitar contradicciones entre pasos, ejemplos y mensajes de retroalimentacion.
- Se ajustaron los titulos de las unidades 4 a 7 para que reflejen el contenido real del curso.
- Se limpiaron y compactaron multiples textos largos para volverlos mas claros sin perder contenido normativo esencial.
- Se reforzaron referencias operativas a entidades y procesos como SLED, ABL y MYDORWAY donde el contenido lo requeria.

Refuerzo legal agregado desde el South Carolina Legal Supplement:
- Menores de edad y verificacion de ID: se agregaron o reforzaron citas a disposiciones sobre edad minima, documentos, venta a menores y compras para terceros.
- Responsabilidad por servicio: se incorporaron referencias sobre venta ilegal, horarios, responsabilidad individual del servidor y consecuencias administrativas o civiles.
- DUI, consentimiento implicito y open container: se anadieron menciones mas explicitas a articulos aplicables para conectar la operacion del servidor con el marco legal estatal.
- Armas, licencias y cumplimiento en el local: se agregaron referencias sobre exhibicion de permisos, control regulatorio y restricciones relevantes para el establecimiento.
- Becas, promociones y seguro de responsabilidad por licor: se integraron citas concretas para que esos temas no quedaran solo descritos de forma general.
- Tipos de permiso para consumo en el local: se anadieron menciones a PBW, PO7, PLB, PLC y LOP en los bloques de licenciamiento.
- Avisos visibles y menores: se agregaron referencias a la obligacion de ciertos negocios de mostrar senalizacion relacionada con menores de edad.
- Edades minimas del personal: se incorporaron referencias sobre limites de edad aplicables a ciertos empleados y bartenders.
- Promociones con retiro o entrega al vehiculo: se sumo la referencia a Reg. 7-202.5 en el bloque final de promociones para cubrir drive-thru y curbside.

Impacto funcional:
- El contenido en espanol e ingles quedo mas consistente entre si.
- El curso ahora cita con mas frecuencia articulos y regulaciones especificas, en lugar de hablar de obligaciones solo en abstracto.
- La estructura actual del JSON sigue siendo compatible con el visor QA ya ajustado en index.html.

Validacion:
- Se validaron [dist/sc-content/sc-content.es.json](dist/sc-content/sc-content.es.json) y [dist/sc-content/sc-content.en.json](dist/sc-content/sc-content.en.json) despues de la ultima ronda de cambios.
- No se reportaron errores en ninguno de los dos archivos.

Nota:
- Este changelog reemplaza la referencia anterior al archivo quiz porque ese ya no es el foco activo del proyecto.
