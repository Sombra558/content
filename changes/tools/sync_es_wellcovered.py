"""Sync well-covered additions from sc-content.en.json into sc-content.es.json."""
import json
import os


PATH = os.path.join("dist", "sc-content", "sc-content.es.json")


def load():
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def section(data, unit_number):
    return data["courses"][0]["sections"][unit_number - 1]["slides"]


def make_text(paragraphs, instruction="Lea lo siguiente y luego haga clic en Siguiente."):
    return {
        "order_index": 0,
        "min_time": 3,
        "content_type": "Text",
        "content_type_unique_id": "text",
        "contents": [{"order_index": 0, "text": {"paragraphs": paragraphs, "instruction": instruction}}],
    }


def make_multiple(question, options, correct_index, correct_fb,
                  incorrect_fb="Incorrecto.",
                  instruction="Lea el escenario y luego seleccione la mejor respuesta."):
    ids = ["opt_a", "opt_b", "opt_c", "opt_d", "opt_e"]
    opts = [{"id": ids[i], "label": lbl, "is_correct": i == correct_index}
            for i, lbl in enumerate(options)]
    return {
        "order_index": 0,
        "min_time": 3,
        "content_type": "Multiple",
        "content_type_unique_id": "multiple",
        "contents": [{"order_index": 0, "interactive": {
            "question": question,
            "instruction": instruction,
            "options": opts,
            "feedback": {"correct": correct_fb, "incorrect": incorrect_fb},
        }}],
    }


def make_completion(structure, items, instruction="Haga clic en cada elemento para obtener más información."):
    return {
        "order_index": 0,
        "min_time": 3,
        "content_type": "Completion",
        "content_type_unique_id": "completion",
        "contents": [{
            "order_index": 0,
            "text": {"instruction": instruction},
            "interactive": {"content_structure": [structure], "reveal_items": items},
        }],
    }


def add_image_to_slide(slide, asset_id, alt):
    slide["contents"].append({
        "order_index": len(slide["contents"]),
        "image": {
            "placeholder": True,
            "asset_id": asset_id,
            "alt": alt,
            "status": "pending",
        },
    })


def insert_after(slides, target_index, new_slides):
    for offset, slide in enumerate(new_slides, start=1):
        slides.insert(target_index + offset, slide)


def replace_paragraphs(slide, paragraphs):
    for block in slide["contents"]:
        if "text" in block and "paragraphs" in block["text"]:
            block["text"]["paragraphs"] = paragraphs
            return True
    return False


def reflow(slides):
    for i, slide in enumerate(slides):
        slide["order_index"] = i
        for j, content in enumerate(slide.get("contents", [])):
            content["order_index"] = j if "image" in content else i if j == 0 else j


def find_first(slides, substring):
    sub = substring.lower()
    for i, slide in enumerate(slides):
        if sub in json.dumps(slide, ensure_ascii=False).lower():
            return i
    return -1


def attach_unit2_image(slides):
    idx = find_first(slides, "bebida estándar")
    if idx >= 0 and not any("image" in content for content in slides[idx]["contents"]):
        add_image_to_slide(
            slides[idx],
            "sc-img-standard-drink",
            "Gráfico de equivalentes de bebida estándar: cerveza de 12 oz, vino de 5 oz y destilado de 1.5 oz.",
        )


def unit1_additions():
    return [
        make_text([
            "Carolina del Sur emite distintos permisos según lo que vende un negocio y cuándo lo vende. Un permiso PBW (On-Premises Beer & Wine Permit) permite vender cerveza y vino para consumo en el local y para llevar, hasta seis días por semana, las veinticuatro horas del día. Las ventas en domingo solo se permiten si el condado aprobó una opción local. Un permiso PO7 (7-Day On-Premises Beer & Wine Permit) permite vender cerveza y vino siete días por semana, excepto los domingos de 2 a. m. a 10 a. m., y solo se emite en condados que aprobaron las ventas dominicales por referéndum. Conocer el permiso de su establecimiento le indica exactamente qué puede servir y cuándo. Estatutos aplicables: SC Code §§ 61-4-120, 61-4-510 y 61-4-630."
        ]),
        make_text([
            "El licor por bebida requiere su propio permiso. Una licencia PLB (Business Liquor by the Drink) cubre negocios enfocados en comidas u hospedaje y permite servir licor de lunes a sábado, de 10 a. m. a 2 a. m. Una licencia PLC (Nonprofit Private Club Liquor by the Drink) cubre organizaciones sin fines de lucro válidas los siete días de la semana, de 10 a. m. a 2 a. m. Un permiso LOP (Local Option Permit) agrega servicio de licor los domingos para negocios que ya tienen PLB, pero solo en condados que aprobaron la venta dominical de licor. Servir fuera del horario o tipo autorizado por su permiso constituye una venta ilegal. Estatutos aplicables: SC Code §§ 61-6-1600 y 61-6-1610."
        ]),
        make_text([
            "Todo titular de permiso debe exhibir sus licencias de alcohol en un lugar claramente visible dentro del establecimiento. Esto permite que reguladores, fuerzas del orden y el público confirmen que el negocio está autorizado para vender alcohol. Como servidor, debe saber dónde están exhibidos los permisos de su establecimiento. Referencia: SC Code of Regulations 7-200.3."
        ]),
        make_text([
            "Operar un negocio minorista o mayorista de alcohol sin permiso es un delito menor sancionado con una multa de $10 a $100 o prisión de 10 a 30 días. Cada día que el negocio opera sin permiso constituye una infracción separada, y toda la cerveza, el vino y el licor en el local se consideran contrabando que la State Law Enforcement Division (SLED) debe incautar. Por eso los permisos y sus renovaciones se toman tan en serio. Estatutos aplicables: SC Code §§ 61-4-150, 61-4-560, 61-6-2600 y 61-6-2610."
        ]),
        make_text([
            "La ley de Carolina del Sur establece que una persona no puede entrar en un negocio que vende alcohol para consumo en el local portando un arma de fuego y luego consumir alcohol. Violar esta norma es un delito menor sancionado con una multa de hasta $2,000 o hasta dos años de prisión, o ambas, y el permiso de armas ocultas se revoca por cinco años. Un negocio también puede colocar un letrero de 'NO CONCEALABLE WEAPONS ALLOWED'; quien se niegue a cumplir puede recibir una multa de hasta $200 o hasta 30 días de cárcel. Estatutos aplicables: SC Code §§ 16-23-465 y 23-31-220."
        ]),
        make_completion(
            "Los permisos de consumo en el local en Carolina del Sur incluyen {{item_1}} {{item_2}} {{item_3}} {{item_4}} {{item_5}}. Conocer su permiso le dice qué puede servir y cuándo.",
            [
                {"id": "item_1", "title": "PBW", "revealed_text": "Beer & Wine para consumo en el local: cerveza y vino en el local y para llevar, 6 días por semana, 24 horas al día; domingos solo con opción local."},
                {"id": "item_2", "title": "PO7", "revealed_text": "Beer & Wine de 7 días: 7 días por semana excepto los domingos de 2 a. m. a 10 a. m.; solo en condados con ventas dominicales aprobadas."},
                {"id": "item_3", "title": "PLB", "revealed_text": "Licor por bebida para negocios (restaurante y hotel): lunes a sábado de 10 a. m. a 2 a. m."},
                {"id": "item_4", "title": "PLC", "revealed_text": "Licor por bebida para organizaciones sin fines de lucro (club privado): 7 días por semana de 10 a. m. a 2 a. m."},
                {"id": "item_5", "title": "LOP", "revealed_text": "Permiso de opción local: licor los domingos para titulares de PLB en condados que aprobaron ventas dominicales de licor."},
            ],
        ),
        make_multiple(
            "Su restaurante tiene una licencia PLB, pero no un Local Option Permit. Un cliente pide un cóctel a la 1 p. m. de un domingo. ¿Qué es correcto?",
            [
                "A. Servírselo; el licor por bebida siempre está permitido",
                "B. No servir licor por bebida los domingos sin un Local Option Permit",
                "C. Servirlo solo si también pide comida",
                "D. Servir un doble en su lugar",
            ],
            1,
            "Una licencia PLB permite licor de lunes a sábado. El licor por bebida los domingos requiere un Local Option Permit (LOP), emitido solo donde el condado aprobó las ventas dominicales de licor.",
        ),
    ]


def unit2_additions():
    completion = make_completion(
        "Varios factores cambian la rapidez con la que el alcohol eleva la concentración de alcohol en sangre (BAC): {{item_1}} {{item_2}} {{item_3}} {{item_4}} {{item_5}} Como estos factores varían de una persona a otra, la misma cantidad de bebidas afecta de manera distinta a cada cliente.",
        [
            {"id": "item_1", "title": "Peso corporal", "revealed_text": "Una persona con menor peso corporal suele alcanzar un BAC más alto con la misma cantidad de alcohol."},
            {"id": "item_2", "title": "Sexo biológico", "revealed_text": "Las diferencias en composición corporal y enzimas hacen que el alcohol a menudo afecte a las mujeres más rápido que a los hombres."},
            {"id": "item_3", "title": "Velocidad de consumo", "revealed_text": "Beber rápido eleva el BAC más deprisa de lo que el cuerpo puede procesar el alcohol."},
            {"id": "item_4", "title": "Comida en el estómago", "revealed_text": "La comida ralentiza la absorción del alcohol; beber con el estómago vacío eleva el BAC más rápido."},
            {"id": "item_5", "title": "Fuerza de la bebida y carbonatación", "revealed_text": "Las bebidas más fuertes y los mezcladores carbonatados pueden elevar el BAC con mayor rapidez."},
        ],
    )
    drugs = make_text([
        "El alcohol interactúa de forma peligrosa con muchos medicamentos recetados, de venta libre y drogas ilegales. Los sedantes, opioides, antihistamínicos y otros depresores pueden multiplicar los efectos del alcohol, por lo que un cliente puede parecer mucho más incapacitado de lo que sugiere su número de bebidas. Usted no puede saber qué ha tomado un cliente, así que evalúe la incapacidad por la conducta observada, no solo por la cuenta de bebidas."
    ])
    tolerance = make_text([
        "La tolerancia significa que una persona que bebe mucho con regularidad puede no parecer tan incapacitada como realmente indica su BAC. La tolerancia no vuelve segura a una persona para conducir; solo enmascara las señales. Nunca use la aparente 'capacidad para aguantar' de un cliente como razón para seguir sirviendo; apóyese en el conteo de bebidas, el tiempo y la conducta."
    ])
    legal_bac = make_text([
        "En Carolina del Sur, una concentración de alcohol en sangre de 0.08% o más crea una inferencia de que el conductor estaba bajo la influencia, y un BAC entre 0.05% y 0.08% puede considerarse junto con otras pruebas. Las bebidas estándar elevan el BAC de maneras predecibles, por eso importan el ritmo del consumo y cortar el servicio a tiempo. Estatutos aplicables: SC Code §§ 56-5-2930 y 56-5-2933."
    ])
    add_image_to_slide(
        legal_bac,
        "sc-img-bac-chart",
        "Gráfico que relaciona la cantidad de bebidas estándar y el peso corporal con la concentración estimada de alcohol en sangre.",
    )
    quiz = make_multiple(
        "Dos clientes tomaron tres bebidas en una hora. Uno parece mucho más incapacitado que el otro. ¿Cuál es la mejor explicación que debe tener presente un servidor?",
        [
            "A. El cliente más tranquilo puede seguir bebiendo con seguridad",
            "B. Factores como peso corporal, comida, velocidad de consumo, tolerancia y medicamentos cambian cómo afecta el alcohol a cada persona, así que debe evaluarse la incapacidad por la conducta",
            "C. Debieron haber contado mal sus bebidas",
            "D. El BAC es igual para todos después de tres bebidas",
        ],
        1,
        "El BAC y la incapacidad visible varían según el peso corporal, el sexo biológico, la comida, la velocidad de consumo, la tolerancia y cualquier droga o medicamento ingerido. Siempre evalúe la incapacidad por la conducta observada, no solo por la cantidad de bebidas.",
    )
    return [completion, drugs, tolerance, legal_bac, quiz]


def unit3_additions():
    s2 = make_text([
        "Toda identificación válida muestra una fecha de nacimiento. En una licencia de conducir de Carolina del Sur aparece cerca del nombre y la foto, etiquetada como 'DOB'. Lea siempre la fecha de nacimiento directamente de la tarjeta en lugar de confiar en la palabra del cliente o en una mirada rápida a la foto. Confirme la fecha de nacimiento, la fecha de vencimiento y que la foto coincida con la persona que tiene delante."
    ])
    add_image_to_slide(s2, "sc-img-id-anatomy", "Diagrama de una licencia de conducir de Carolina del Sur con el campo de fecha de nacimiento resaltado.")
    s3 = make_text([
        "Carolina del Sur emite licencias de conducir y tarjetas de identificación verticales a personas menores de 21 años, y licencias horizontales a personas de 21 años o más. La orientación vertical es una señal visual inmediata de que el titular era menor de 21 años cuando se emitió la tarjeta, por lo que debe revisar cuidadosamente la fecha de nacimiento. Nunca confíe solo en la orientación: siempre confirme la fecha real de nacimiento, porque una persona con licencia vertical puede haber cumplido 21 años después y las tarjetas pueden alterarse."
    ])
    add_image_to_slide(s3, "sc-img-vertical-vs-horizontal", "Comparación lado a lado entre una licencia vertical de menor de 21 años y una licencia horizontal para mayores de 21 años en Carolina del Sur.")
    s4 = make_text([
        "Para vender alcohol legalmente, el cliente debe tener al menos 21 años hoy. La verificación más rápida es tomar la fecha de hoy y restarle 21 años; eso da la 'fecha de nacimiento requerida'. Cualquier persona nacida en esa fecha o antes tiene 21 años o más; cualquiera nacida después de esa fecha es menor de 21 años y no puede recibir alcohol. Por ejemplo, si hoy es 6 de julio de 2026, la fecha de nacimiento requerida es 6 de julio de 2005: el cliente debe haber nacido en esa fecha o antes."
    ])
    add_image_to_slide(s4, "sc-img-dob-math", "Visual que muestra la fecha de hoy menos 21 años para encontrar la fecha de nacimiento requerida.")
    s9 = make_completion(
        "Una verificación exhaustiva de ID sigue siempre los mismos pasos: {{item_1}} {{item_2}} {{item_3}} {{item_4}} {{item_5}} La consistencia es lo que hace que la revisión sea legal y confiable.",
        [
            {"id": "item_1", "title": "Tocar la tarjeta", "revealed_text": "Sienta si la tarjeta tiene grosor desigual, bultos o desprendimiento alrededor de la foto y la fecha de nacimiento."},
            {"id": "item_2", "title": "Revisar medidas de seguridad", "revealed_text": "Busque hologramas, microtexto, tipografías claras y bordes que no hayan sido abiertos ni pegados de nuevo."},
            {"id": "item_3", "title": "Revisar la fecha de nacimiento", "revealed_text": "Lea la fecha de nacimiento y compárela con la fecha de nacimiento requerida de hoy (fecha actual menos 21 años)."},
            {"id": "item_4", "title": "Comparar foto y descripción", "revealed_text": "Haga coincidir la foto, la estatura y la descripción con la persona que tiene delante."},
            {"id": "item_5", "title": "Decidir", "revealed_text": "Si algo falla o usted no está seguro, rechace la venta y siga la política del establecimiento."},
        ],
    )
    add_image_to_slide(s9, "sc-img-idcheck-steps", "Secuencia de cinco pasos para revisar una ID: tocar la tarjeta, revisar medidas de seguridad, revisar fecha de nacimiento, comparar foto y descripción, decidir.")
    return [
        make_text([
            "En Carolina del Sur debe verificar la edad del cliente con una identificación válida con foto emitida por el gobierno antes de vender alcohol. Las tres formas que verá con más frecuencia son una licencia de conducir válida, una tarjeta de identificación estatal y un pasaporte válido (una identificación militar también es aceptable). El documento no debe estar vencido, debe tener foto y debe mostrar claramente la fecha de nacimiento. Si no está seguro de que la identificación sea válida y pertenezca al cliente, no complete la venta."
        ]),
        s2,
        s3,
        s4,
        make_text([
            "Una vez que conozca la fecha de nacimiento requerida, compárela con la fecha de nacimiento impresa en la identificación. Si la fecha de nacimiento de la ID es esa fecha o anterior, el cliente tiene la edad suficiente. Si es posterior, el cliente es menor de 21 años y usted debe rechazar la venta. Haga el cálculo siempre; no estime la edad por la apariencia y no redondee porque un cliente 'parece suficientemente mayor'."
        ]),
        make_text([
            "Carolina del Sur exige verificaciones de ID consistentes. Una regla de la casa común y defendible es revisar la ID de cualquier persona que parezca menor de 30 años (algunos establecimientos usan 35 o 40), pero la práctica más segura es revisar a todos los clientes, siempre, sin importar la edad aparente. Las verificaciones consistentes lo protegen personalmente: no exigir identificación para verificar la edad es prueba prima facie de una venta ilegal según la ley de Carolina del Sur."
        ]),
        make_text([
            "Una identificación falsa o alterada es una de las formas más comunes en que un menor intenta obtener servicio. Revise la tarjeta físicamente: sienta si hay grosor desigual, bultos o desprendimiento alrededor de la foto y la fecha de nacimiento. Busque texto borroso, tipografías que no coinciden, hologramas ausentes o apagados y bordes que hayan sido abiertos o pegados de nuevo. Compare la foto, la estatura y la descripción con la persona. Haga una pregunta de verificación que el verdadero titular respondería de inmediato, como su segundo nombre, código postal o signo zodiacal según la fecha de nacimiento mostrada."
        ]),
        make_text([
            "Si determina que una ID es falsa, alterada, prestada o pertenece a otra persona, no venda alcohol. Siga la política de su establecimiento: rechace la venta con cortesía y, según las reglas internas, retenga la ID y notifique a un gerente. Nunca discuta ni acuse a la persona en voz alta. Documente lo ocurrido si su establecimiento exige un informe de incidente. Rechazar la venta lo protege de responsabilidad penal."
        ]),
        s9,
        make_text([
            "Vender alcohol a una persona menor de 21 años es un delito menor en Carolina del Sur, y la sanción recae sobre la persona que hizo la venta: usted. Una primera infracción conlleva una multa de $200 a $300 o hasta 30 días de cárcel, o ambas. Una segunda o posterior infracción conlleva una multa de $400 a $500 o hasta 30 días de cárcel, o ambas. Debido a que no revisar la ID es prueba prima facie de la infracción, revisar todas las identificaciones es su mejor protección legal. Estatutos aplicables: SC Code §§ 61-4-50 y 61-6-4080."
        ]),
        make_text([
            "También es ilegal comprar, transferir o entregar cerveza, vino o licor a una persona menor de 21 años para su consumo. Esto incluye a un cliente mayor de edad que compra una bebida para pasársela a un amigo menor en la barra. Las sanciones siguen la misma escala que una venta ilegal. Esté atento a las 'compras por tercero' en las que un cliente pide para un acompañante menor de edad. Estatutos aplicables: SC Code §§ 61-4-90, 61-6-4070 y 61-6-4075."
        ]),
        make_text([
            "Todo vendedor minorista debe exhibir un aviso que indique: 'The possession of beer, wine, or alcoholic liquors, by a person under twenty-one years of age is a criminal offense under the laws of this State, and it is also unlawful for a person to knowingly give false information concerning his age for the purpose of purchasing beer, wine, or liquor.' No exhibir este aviso constituye por sí mismo un delito menor. Estatutos aplicables: SC Code §§ 61-4-70 y 61-6-1530."
        ]),
        make_text([
            "Vender a un menor no solo pone en riesgo su trabajo: puede cambiar la vida del menor. Una condena puede generar antecedentes penales, y una segunda o posterior infracción relacionada con alcohol hace que un estudiante pierda elegibilidad para becas importantes de Carolina del Sur: Palmetto Fellows Scholarship por un año, SC HOPE Scholarship para el siguiente año académico y SC LIFE Scholarship para los períodos siguientes. Entender estas consecuencias es parte de por qué rechazar una venta a un menor siempre está por encima de concretar la venta. Estatutos aplicables: SC Code §§ 59-104-20, 61-4-100 y 61-6-4085."
        ]),
        make_multiple(
            "Hoy es 6 de julio de 2026. La identificación de un cliente muestra fecha de nacimiento del 2 de septiembre de 2005. ¿Puede venderle alcohol?",
            [
                "A. Sí, porque 2005 significa que ya tiene 21 años",
                "B. No; cumple 21 años el 2 de septiembre de 2026, que es después de hoy, así que todavía es menor de 21 años",
                "C. Sí, si también muestra una segunda identificación",
                "D. Solo después de las 9 p. m.",
            ],
            1,
            "La fecha de nacimiento requerida hoy es el 6 de julio de 2005. Una fecha de nacimiento del 2 de septiembre de 2005 es posterior a esa fecha, por lo que el cliente sigue siendo menor de 21 años hasta el 2 de septiembre de 2026. Debe rechazar la venta.",
        ),
        make_multiple(
            "Un cliente le entrega una licencia. El cabello y el rostro de la foto se ven distintos, la tarjeta se siente abultada alrededor de la fecha de nacimiento y la persona no puede recordar su propio código postal. ¿Qué debe hacer?",
            [
                "A. Vender; probablemente la tarjeta está bien",
                "B. Rechazar la venta y retener la ID y avisar a un gerente según la política del establecimiento",
                "C. Vender, pero solo cerveza",
                "D. Pedirle que la firme",
            ],
            1,
            "Múltiples señales de alerta, como foto que no coincide, sensación de manipulación y no poder responder una pregunta básica de verificación, significan que no debe vender. Rechace la venta y siga la política del establecimiento sobre retener la ID y avisar a un gerente.",
        ),
        make_multiple(
            "Un cliente adulto pide una cerveza y de inmediato se la pasa a un acompañante visiblemente menor de edad en la mesa. ¿Cuál es la respuesta correcta?",
            [
                "A. Nada; el adulto la compró legalmente",
                "B. Retirar o rechazar la bebida; transferir alcohol a una persona menor de 21 años es ilegal y no puede seguir sirviendo a la pareja con ese fin",
                "C. Cobrarle la bebida al menor",
                "D. Pedirles que cambien de mesa",
            ],
            1,
            "Comprar o transferir alcohol a una persona menor de 21 años para su consumo es ilegal. Interrumpa la transferencia, rechace más servicio con ese fin e involucre a un gerente si es necesario.",
        ),
        make_text([
            "La ley de Carolina del Sur establece que, al ser condenado por vender alcohol a una persona menor de 21 años, quien realizó la venta es culpable de un delito menor y debe recibir una multa de entre $200 y $300 o hasta 30 días de cárcel, o ambas, por una primera infracción. En una segunda o posterior infracción, la multa debe ser de entre $400 y $500 o hasta 30 días de cárcel, o ambas. La misma estructura de consecuencias se aplica a la transferencia ilegal de cerveza, vino o licor a una persona menor de 21 años para su consumo."
        ]),
    ]


def unit4_additions():
    c1 = make_completion(
        "Las señales de intoxicación suelen aparecer en cuatro áreas: {{item_1}} {{item_2}} {{item_3}} {{item_4}} Observe los cambios con el tiempo, no solo un momento aislado.",
        [
            {"id": "item_1", "title": "Habla", "revealed_text": "Habla arrastrada, fuerte, incoherente o repetitiva."},
            {"id": "item_2", "title": "Coordinación", "revealed_text": "Balanceo, tropiezos, dejar caer objetos o dificultad con tareas simples como manejar dinero."},
            {"id": "item_3", "title": "Juicio y conducta", "revealed_text": "Agresividad, exceso de confianza, toma de riesgos o cambios bruscos de ánimo."},
            {"id": "item_4", "title": "Apariencia", "revealed_text": "Ojos vidriosos o enrojecidos, rostro ruborizado o aspecto desarreglado."},
        ],
    )
    add_image_to_slide(c1, "sc-img-intoxication-signs", "Cuadrícula de señales comunes de intoxicación agrupadas por habla, coordinación, juicio y apariencia.")
    return [
        c1,
        make_text([
            "Reconocer temprano el consumo problemático permite actuar antes de que un cliente se convierta en un peligro para sí mismo o para otros. Observe a los clientes que beben rápido, piden rondas una tras otra, se vuelven más ruidosos o más retraídos, o piden bebidas a pesar de señales claras de incapacidad. Detectar estos patrones a tiempo le da margen para ralentizar el servicio, ofrecer comida o agua y prepararse para rechazar más alcohol."
        ]),
        make_text([
            "Debe saber cuándo y dónde pedir ayuda. Si el consumo de un cliente se vuelve un problema de seguridad, involucre de inmediato a su gerente o al personal de seguridad y organice transporte seguro cuando haga falta. Los servidores suelen ser la primera línea de defensa contra daños relacionados con el alcohol, así que advertir temprano es una señal de profesionalismo, no de debilidad. Nunca permita que un cliente visiblemente intoxicado conduzca."
        ]),
        make_multiple(
            "Un cliente arrastra las palabras, se balancea en el taburete y acaba de tirar un vaso al intentar alcanzar su bebida. ¿Qué debe hacer?",
            [
                "A. Servir una más porque todavía está sentado",
                "B. Detener el servicio de alcohol, ofrecer agua o comida e involucrar a un gerente mientras organiza transporte seguro",
                "C. Esperar a que se caiga antes de actuar",
                "D. Pasarlo a un booth y seguir sirviendo",
            ],
            1,
            "El habla arrastrada, el balanceo y la pérdida de coordinación son señales claras de intoxicación. Detenga el servicio de alcohol, ofrezca agua o comida, involucre a un gerente y ayude a organizar transporte seguro.",
        ),
    ]


def unit5_additions():
    return [
        make_text([
            "Rechazar el servicio funciona mejor cuando se hace con calma, firmeza y respeto. Use lenguaje claro como: 'No puedo servirle otra bebida alcohólica esta noche' y evite debatir o culpar al cliente. Ofrezca agua, comida, una bebida sin alcohol o ayuda para organizar transporte. Su objetivo es terminar el servicio de alcohol de forma segura mientras preserva la dignidad y reduce el conflicto."
        ]),
        make_completion(
            "Use siempre los mismos pasos de escalamiento: {{item_1}} {{item_2}} {{item_3}} {{item_4}} {{item_5}} Un proceso consistente protege a clientes, personal y negocio.",
            [
                {"id": "item_1", "title": "Pausar el servicio", "revealed_text": "Deje de servir alcohol mientras evalúa la situación."},
                {"id": "item_2", "title": "Ofrecer alternativas", "revealed_text": "Ofrezca agua, comida, bebidas sin alcohol o tiempo para descansar."},
                {"id": "item_3", "title": "Involucrar a un gerente", "revealed_text": "Llame a un gerente o supervisor cuando el cliente se resista, se altere o requiera una negativa formal."},
                {"id": "item_4", "title": "Organizar transporte seguro", "revealed_text": "Ayude al cliente a conseguir transporte, pedir un rideshare o taxi, o contactar a un amigo sobrio."},
                {"id": "item_5", "title": "Documentar el incidente", "revealed_text": "Complete un informe de incidente según la política del establecimiento."},
            ],
        ),
        make_text([
            "Las políticas internas convierten el servicio responsable en un proceso repetible. Una política sólida explica cuándo revisar la ID, cuándo rechazar el servicio, cuándo involucrar a un gerente, cómo evitar que un cliente conduzca y cuándo completar un informe de incidente. Seguir la política lo protege porque demuestra que sus decisiones fueron consistentes, documentadas y basadas en la seguridad, no solo en su juicio personal."
        ]),
        make_text([
            "En Carolina del Sur, rechazar una venta ilegal o insegura siempre está por encima de concretar la venta o complacer al cliente. Una sola venta nunca vale un cargo penal, la pérdida de su certificado o un accidente que cambie vidas. Las negativas seguras y consistentes son una marca de profesionalismo, no de mala educación, y la cultura de responsabilidad de su establecimiento depende de que cada servidor mantenga esa línea."
        ]),
        make_multiple(
            "Un cliente se irrita después de que usted le niega otra bebida y dice: 'Conozco al dueño. Sírveme de todos modos'. ¿Qué debe hacer?",
            [
                "A. Servir la bebida para evitar conflicto",
                "B. Mantener la calma, repetir la negativa, ofrecer agua u otra opción sin alcohol e involucrar a un gerente si el cliente sigue presionando",
                "C. Discutir hasta que admita que está intoxicado",
                "D. Ignorarlo e irse sin avisar a nadie",
            ],
            1,
            "La negativa debe ser calmada, firme y respetuosa. Repita el límite, ofrezca alternativas e involucre a un gerente cuando el cliente se resista o escale la situación.",
        ),
        make_multiple(
            "Un servidor corta el servicio a un cliente visiblemente intoxicado. El cliente se va molesto y empieza a caminar hacia el estacionamiento con las llaves del auto en la mano. ¿Cuál es el mejor siguiente paso?",
            [
                "A. No hacer nada porque ya se detuvo el servicio",
                "B. Seguir los procedimientos de escalamiento: alertar a un gerente o a seguridad, intentar organizar transporte seguro y documentar el incidente",
                "C. Servir café y asumir que se le pasará de inmediato",
                "D. Dejarlo conducir si promete ir despacio",
            ],
            1,
            "Detener el servicio es solo una parte del servicio responsable. Escale la situación, involucre a gerencia o seguridad, organice transporte seguro cuando sea posible y documente el incidente según la política del establecimiento.",
        ),
    ]


def unit6_additions():
    return [
        make_text([
            "El servicio responsable no es una lección de una sola vez. El marco normativo y las mejores prácticas de Carolina del Sur esperan que los servidores mantengan actualizado su conocimiento mediante capacitaciones de repaso, autoevaluaciones periódicas y módulos digitales. Las leyes, las reglas de permisos y las sanciones cambian; incluso el Legal Supplement tiene una fecha de vigencia, así que lo que aprendió el año pasado puede no ser correcto hoy."
        ]),
        make_text([
            "Convierta la capacitación continua en un hábito: complete repasos cuando su empleador los ofrezca, vuelva a revisar periódicamente sus habilidades para verificar ID y rechazar servicio, y manténgase atento a actualizaciones en la ley de alcohol de Carolina del Sur. Los empleadores que mantienen certificados a todos sus servidores también reducen su requisito de seguro de responsabilidad por licor, por lo que su capacitación continua beneficia directamente al negocio."
        ]),
        make_multiple(
            "Usted escucha que Carolina del Sur podría haber cambiado una regla sobre horarios de servicio, pero no está seguro. ¿Cuál es la mejor respuesta profesional?",
            [
                "A. Seguir sirviendo como siempre hasta que alguien se queje",
                "B. Revisar recursos actuales de Carolina del Sur o consultar a su gerente, y completar capacitación de repaso para mantenerse al día",
                "C. Adivinar según lo que hacen otros bares",
                "D. Ignorarlo; la capacitación solo importa cuando lo contratan",
            ],
            1,
            "Las leyes y reglas cambian con el tiempo. Mantenerse al día mediante capacitación de repaso y consultar fuentes autorizadas de Carolina del Sur o a su gerente forma parte de una conducta profesional responsable y continua.",
        ),
        make_text([
            "Los negocios abiertos después de las 5 p. m. que venden alcohol para consumo en el local deben contar con al menos $1 millón en cobertura de responsabilidad por licor. Carolina del Sur permite reducir ese requisito mediante mitigación de riesgo; por ejemplo, una reducción de $100,000 cuando cada servidor completa el SC Alcohol Server Certificate dentro de los 60 días de contratación, o cuando el negocio deja de servir a medianoche, lo que reduce $250,000. Esta es una razón financiera directa por la que su capacitación y servicio responsable importan a su empleador. Estatuto aplicable: SC Code § 61-2-145."
        ]),
        make_text([
            "Si un cliente intoxicado causa daños después, el establecimiento puede compartir responsabilidad civil. Según la ley de Carolina del Sur, un negocio ya no es responsable de más del 50% de los daños de un incidente de DUI, y la responsabilidad puede repartirse entre múltiples partes si así lo decide un jurado. El servicio responsable, como cortar el servicio a clientes intoxicados y rechazar ventas ilegales, es la forma en que usted y su empleador limitan esa exposición. Estatutos aplicables: SC Code §§ 15-38-15 a 15-38-40 y 61-2-147."
        ]),
        make_text([
            "Carolina del Sur restringe las promociones de alcohol que fomentan el consumo excesivo. Para consumo en el local, un negocio no puede anunciar, vender ni dispensar cerveza, vino o licor gratis, a menos de la mitad del precio regular o en formato dos por uno. También es ilegal realizar 'drinking contests' o 'drinking games'. Estatutos aplicables: SC Code §§ 61-4-160 y 61-6-4550."
        ]),
        make_text([
            "Las ventas de alcohol tipo curbside y drive-thru están prohibidas. Un titular de permiso o empleado no puede vender ni entregar cerveza o vino a una persona que permanece dentro de un vehículo durante la transacción; esta regla prohíbe específicamente ventas drive-in, drive-thru y curb service. Referencia: SC Code of Regulations 7-202.5."
        ]),
        make_text([
            "Cuando complete este curso y apruebe el examen, su Alcohol Server Certificate se emite a través del South Carolina Department of Revenue (SCDOR). Puede acceder a su certificado aprobado y a su número de certificado a través del portal MYDORWAY. Conserve ese número; empleadores y reguladores pueden pedirle que confirme su certificación."
        ]),
    ]


def unit7_dui_additions():
    return [
        make_completion(
            "Las sanciones por DUI en Carolina del Sur aumentan con cada infracción: {{item_1}} {{item_2}} {{item_3}} {{item_4}} Incluso una primera infracción puede implicar cárcel, multas y suspensión de la licencia.",
            [
                {"id": "item_1", "title": "Primera infracción", "revealed_text": "Hasta $400 de multa ($992 con recargos y cargos), de 48 horas a 30 días de cárcel y suspensión de la licencia de conducir por 6 meses."},
                {"id": "item_2", "title": "Segunda infracción", "revealed_text": "Multa de $2,100 a $5,100 ($10,744.50 con recargos y cargos), de 5 días a 1 año de cárcel y suspensión de la licencia por 1 año."},
                {"id": "item_3", "title": "Tercera infracción", "revealed_text": "Multa de $3,800 a $6,300 ($13,234.50 con recargos y cargos), de 60 días a 3 años de cárcel y suspensión de la licencia por 2 años; si ocurre dentro de 5 años de la primera, la suspensión es de 4 años."},
                {"id": "item_4", "title": "Cuarta infracción", "revealed_text": "Prisión de 1 a 5 años y revocación permanente de la licencia de conducir."},
            ],
        ),
        make_text([
            "La ley de DUI de Carolina del Sur cubre conducir bajo la influencia del alcohol en la medida en que las facultades para conducir de la persona estén material y apreciablemente afectadas. Un BAC de 0.08% o más crea una inferencia de que la persona estaba bajo la influencia, y un BAC entre 0.05% y 0.08% puede considerarse junto con otras pruebas. Estatutos aplicables: SC Code §§ 56-5-2930, 56-5-2933 y 56-5-2940."
        ]),
        make_text([
            "El DUI grave aplica cuando conducir incapacitado causa lesiones corporales graves o la muerte. Si hay lesiones corporales graves, la sanción obligatoria es una multa de $5,100 a $10,100 ($21,119.50 con recargos y cargos) y prisión de 30 días a 15 años. Si hay una muerte, la sanción obligatoria es una multa de $10,100 a $25,100 ($52,244.50 con recargos y cargos) y prisión de 1 a 25 años. Estatuto aplicable: SC Code § 56-5-2945."
        ]),
        make_text([
            "El consentimiento implícito significa que toda persona que conduce en Carolina del Sur se considera que ha dado consentimiento para pruebas de aliento, sangre u orina cuando las autoridades alegan una infracción relacionada con alcohol o drogas. Negarse a la prueba activa una suspensión automática de 90 días de la licencia de conducir para personas de 21 años o más, o 180 días si la persona tuvo una condena o suspensión previa relacionada con alcohol dentro de los 10 años anteriores. Estatutos aplicables: SC Code §§ 56-5-2950 y 56-5-2951."
        ]),
        make_text([
            "La ley de contenedor abierto de Carolina del Sur prohíbe tener un contenedor abierto de cerveza, vino o licor en un vehículo en movimiento de cualquier tipo, excepto en el compartimiento de equipaje. Una condena puede resultar en una multa de hasta $100 o hasta 30 días de cárcel. Estas reglas importan a los servidores porque permitir que un cliente salga con bebidas abiertas aumenta el riesgo legal para el cliente y para el establecimiento. Estatutos aplicables: SC Code §§ 61-4-110 y 61-6-4020."
        ]),
        make_multiple(
            "Un cliente dice que puede negarse a una prueba de aliento porque nunca aceptó someterse a pruebas. ¿Qué debe entender un servidor sobre la ley de Carolina del Sur?",
            [
                "A. La negativa no tiene consecuencias si la persona es educada",
                "B. Conducir en Carolina del Sur se considera consentimiento implícito a las pruebas, y la negativa puede activar una suspensión automática de la licencia",
                "C. El consentimiento implícito aplica solo a conductores comerciales",
                "D. La negativa está permitida después de medianoche",
            ],
            1,
            "Según la ley de consentimiento implícito de Carolina del Sur, conducir en el estado se considera consentimiento a las pruebas cuando se alega una infracción relacionada con alcohol o drogas. La negativa puede activar una suspensión automática de la licencia.",
        ),
        make_multiple(
            "Un cliente quiere llevarse una cerveza abierta sin terminar en el auto para el viaje de regreso a casa. ¿Cuál es la respuesta correcta?",
            [
                "A. Permitirlo si la lleva el pasajero",
                "B. No permitirlo; Carolina del Sur prohíbe contenedores abiertos de cerveza, vino o licor en un vehículo en movimiento, excepto en el compartimiento de equipaje",
                "C. Permitirlo si el conductor no está intoxicado",
                "D. Verterla en un vaso de café",
            ],
            1,
            "Carolina del Sur prohíbe contenedores abiertos de cerveza, vino o licor en un vehículo en movimiento, excepto en el compartimiento de equipaje. No deje que los clientes se lleven alcohol abierto al auto.",
        ),
    ]


def unit7_stats_additions():
    return [
        make_text([
            "Conducir incapacitado sigue siendo uno de los problemas más graves de seguridad vial en Carolina del Sur. Según el Fatality Analysis Reporting System de NHTSA, 413 personas murieron en choques con conducción incapacitada por alcohol en Carolina del Sur en 2023, y conductores con una concentración de alcohol en sangre de 0.08% o más estuvieron involucrados en el 39% de todos los conductores en choques fatales de ese año. Carolina del Sur figura de forma constante entre los estados con mayor proporción de choques fatales relacionados con alcohol. Como servidor, la decisión de detener el servicio a un cliente incapacitado forma parte de prevenir estas muertes."
        ]),
        make_text([
            "El South Carolina Department of Public Safety reportó 5,319 colisiones relacionadas con alcohol o drogas en 2023, en las que 367 personas murieron y 3,372 resultaron heridas (SCDPS 2023 Traffic Collision Fact Book). Dicho de otro modo, aproximadamente cada 21.2 horas una persona murió en una colisión por conducción bajo la influencia en Carolina del Sur. Detrás de cada cifra hay una decisión prevenible sobre cuándo dejar de servir."
        ]),
        make_text([
            "La aplicación de la ley está aumentando. La South Carolina Law Enforcement Division reportó que los arrestos por DUI subieron 24.6% en todo el estado de 2022 a 2023, y algunos condados más que duplicaron sus cifras. La tasa de mortalidad por millaje en 2024 de Carolina del Sur fue de 1.68 muertes por cada 100 millones de millas recorridas, aproximadamente 40% más alta que la tasa nacional de 1.20 (SCDPS). Más aplicación significa que el exceso de servicio tiene más probabilidades de rastrearse hasta el establecimiento y el servidor que sirvió la última bebida."
        ]),
        make_completion(
            "Las estadísticas vuelven a su función: {{item_1}} {{item_2}} {{item_3}} {{item_4}} Cada negativa responsable cambia las cifras.",
            [
                {"id": "item_1", "title": "Prevención", "revealed_text": "Detener el servicio a un cliente incapacitado puede evitar un choque antes de que ocurra."},
                {"id": "item_2", "title": "Exposición legal", "revealed_text": "El exceso de servicio puede rastrearse hasta el servidor y el establecimiento mediante la aplicación de la ley y la investigación."},
                {"id": "item_3", "title": "Impacto comunitario", "revealed_text": "Cada muerte o lesión relacionada con alcohol afecta a familias, compañeros de trabajo y a la comunidad en general."},
                {"id": "item_4", "title": "Responsabilidad profesional", "revealed_text": "El servicio responsable es una parte medible de la reducción del costo de la conducción incapacitada en Carolina del Sur."},
            ],
        ),
        make_multiple(
            "Según datos de NHTSA FARS, aproximadamente ¿qué proporción de los conductores en choques fatales de Carolina del Sur en 2023 tenía una concentración de alcohol en sangre de 0.08% o más?",
            [
                "A. Aproximadamente 10%",
                "B. Aproximadamente 25%",
                "C. Aproximadamente 39%",
                "D. Aproximadamente 75%",
            ],
            2,
            "En 2023, aproximadamente el 39% de los conductores en choques fatales de Carolina del Sur tenían un BAC de 0.08% o más, y 413 personas murieron en choques con conducción incapacitada por alcohol (NHTSA FARS, 2023).",
        ),
    ]


def main():
    data = load()

    s1 = section(data, 1)
    anchor = find_first(s1, "licencia adecuada")
    if anchor == -1:
        anchor = 1
    insert_after(s1, anchor, unit1_additions())
    reflow(s1)

    s2 = section(data, 2)
    attach_unit2_image(s2)
    anchor = find_first(s2, "alcohol en sangre")
    if anchor == -1:
        anchor = 3
    insert_after(s2, anchor, unit2_additions())
    reflow(s2)

    s3 = section(data, 3)
    anchor = find_first(s3, "identificación")
    if anchor == -1:
        anchor = 4
    insert_after(s3, anchor, unit3_additions())
    reflow(s3)

    s4 = section(data, 4)
    anchor = find_first(s4, "intoxic")
    if anchor == -1:
        anchor = 3
    insert_after(s4, anchor, unit4_additions())
    reflow(s4)

    s5 = section(data, 5)
    anchor = find_first(s5, "rechaz")
    if anchor == -1:
        anchor = 3
    insert_after(s5, anchor, unit5_additions())
    reflow(s5)

    s6 = section(data, 6)
    anchor = find_first(s6, "gerente")
    if anchor == -1:
        anchor = 3
    insert_after(s6, anchor, unit6_additions())
    reflow(s6)

    s7 = section(data, 7)
    insert_after(s7, 0, unit7_dui_additions())
    fatality_idx = find_first(s7, "gran proporción")
    if fatality_idx == -1:
        fatality_idx = find_first(s7, "porción notable")
    if fatality_idx == -1:
        fatality_idx = find_first(s7, "colisiones relacionadas con el alcohol")
    if fatality_idx == -1:
        fatality_idx = 8
    replace_paragraphs(s7[fatality_idx], unit7_stats_additions()[0]["contents"][0]["text"]["paragraphs"])
    insert_after(s7, fatality_idx, unit7_stats_additions()[1:])
    reflow(s7)

    save(data)


if __name__ == "__main__":
    main()