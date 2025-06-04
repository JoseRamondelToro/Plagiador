from openai import OpenAI
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-..."))  # Pon tu API aquí si no usas entorno

def analizar_texto(texto):
    prompt = f"""
Analiza el siguiente texto y responde de forma clara en el formato especificado.

1. ¿Cuál es la probabilidad de que el texto esté plagiado? (solo porcentaje, sin explicar).
2. ¿Cuál es la probabilidad de que el texto haya sido generado por una IA? (solo porcentaje).
3. Si se detecta plagio (mayor al 50%), indica brevemente la fuente probable o el tipo de obra original.
   Si no se detecta plagio, responde con "Fuente probable: No detectada".

Responde exactamente con este formato (no añadas explicaciones):

Plagio: XX%  
Generado por IA: XX%  
Fuente probable: [nombre de obra, autor, o tipo de fuente]

Texto:
\"\"\"{texto}\"\"\"
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # o "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content
        print("RESPUESTA OPENAI >>>")
        print(content)

        plagio = re.search(r"Plagio:\s*(\d+)%", content)
        ia = re.search(r"(?:IA|Generado por IA):\s*(\d+)%", content)
        fuente = re.search(r"Fuente probable:\s*(.*)", content)

        resultado = ""
        if plagio:
            resultado += f"Plagio: {plagio.group(1)}%\n"
        if ia:
            resultado += f"Generado por IA: {ia.group(1)}%\n"
        if fuente:
            resultado += f"Fuente probable: {fuente.group(1).strip()}"

        return resultado.strip()

    except Exception as e:
        return f"Error al conectar con OpenAI:\n{str(e)}"
