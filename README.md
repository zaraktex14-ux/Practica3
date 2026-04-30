# Simulador de Autómatas Finitos y Conversión a Expresiones Regulares

## Descripción

Este proyecto consiste en el desarrollo de una **aplicación gráfica para diseñar, simular y analizar Autómatas Finitos**.
La herramienta permite trabajar con **Autómatas Finitos Deterministas (AFD)**, **Autómatas Finitos No Deterministas (AFND)** y **Autómatas No Deterministas con transiciones lambda (AFN-λ)**.

La aplicación incluye funcionalidades para:

* Definir autómatas manualmente
* Simular el procesamiento de cadenas
* Convertir autómatas entre diferentes tipos
* Generar expresiones regulares equivalentes
* Minimizar autómatas deterministas
* Analizar cadenas mediante validadores basados en expresiones regulares

Además, se utiliza la herramienta **JFLAP** para realizar la conversión de autómatas a expresiones regulares y analizar diferentes métodos de conversión.

Este proyecto fue desarrollado como parte de la materia **Teoría de la Computación**.

---

# Características del Sistema

## Interfaz Gráfica

La aplicación cuenta con una interfaz gráfica organizada mediante pestañas para facilitar la interacción del usuario.

Funciones principales de la interfaz:

* Creación de estados
* Definición de transiciones
* Selección de estado inicial
* Selección de estados de aceptación
* Visualización gráfica del autómata

La visualización del autómata se realiza utilizando **Graphviz**.

---

# Simulación de Autómatas

## Simulación de AFD

El sistema permite validar cadenas en un **Autómata Finito Determinista**.

Durante la simulación se muestra:

* Estado actual
* Símbolo procesado
* Transición utilizada
* Resultado final (aceptado o rechazado)

---

## Simulación de AFND

El simulador permite manejar **múltiples estados activos simultáneamente** durante el procesamiento de la cadena.

Características:

* Exploración de múltiples caminos
* Gestión de ramificaciones
* Aceptación si al menos un camino llega a un estado final

---

## Simulación de AFN con Transiciones Lambda (AFN-λ)

El sistema también soporta autómatas con **transiciones lambda (λ)**.

Funciones implementadas:

* Definición de transiciones lambda
* Visualización de transiciones λ
* Cálculo de **λ-clausura**

### Algoritmo de λ-clausura

La λ-clausura permite determinar todos los estados alcanzables desde un estado dado utilizando únicamente transiciones lambda.

Durante la simulación se realizan los siguientes pasos:

1. Calcular λ-clausura del estado actual
2. Consumir símbolo de entrada
3. Aplicar transiciones correspondientes
4. Calcular nuevamente λ-clausura

---

# Conversión entre Autómatas

## Conversión AFND → AFD

Se implementa el **algoritmo de subconjuntos**, que permite convertir un autómata no determinista en su equivalente determinista.

El proceso incluye:

* Construcción de la tabla de transiciones
* Identificación de nuevos estados
* Determinación de estados de aceptación

---

# Minimización de Autómatas Finitos Deterministas

El sistema implementa el algoritmo de **minimización de AFD** basado en clases de equivalencia.

El proceso incluye:

1. Eliminación de estados inaccesibles
2. Identificación de estados equivalentes
3. Construcción del autómata mínimo

La aplicación muestra:

* Autómata original
* Autómata minimizado
* Número de estados eliminados

---

# Conversión de Autómatas a Expresiones Regulares

## Uso de JFLAP

Se utilizó la herramienta **JFLAP** para convertir Autómatas Finitos Deterministas a **Expresiones Regulares**.

### Procedimiento

1. Seleccionar un autómata determinista
2. Aplicar el **método de eliminación de estados**
3. Obtener la expresión regular equivalente

Durante el proceso se documenta:

* Eliminación progresiva de estados
* Transformación de las transiciones
* Expresión regular final

---

# Comparación de Métodos de Conversión

los tres métodos principales que se implementeron para convertir autómatas en expresiones regulares:

### Método de eliminación de estados

Consiste en eliminar estados del autómata mientras se actualizan las transiciones hasta obtener una expresión regular equivalente.

### Método de ecuaciones

Se basa en representar el comportamiento del autómata mediante ecuaciones regulares que luego se resuelven algebraicamente.

### Método de Arden

Utiliza el **Lema de Arden** para resolver ecuaciones regulares y obtener la expresión regular equivalente.

---

# Funciones Adicionales

## Subcadenas, Prefijos y Sufijos

La aplicación puede generar de una cadena :

* subcadenas
* prefijos
* sufijos


---

# Tecnologías Utilizadas

* **Python 3.8+**
* **Tkinter** (interfaz gráfica)
* **Graphviz** (visualización de autómatas)
* **JSON / JFLAP (.jff)** para almacenamiento de autómatas

---

# Instalación

## Requisitos

* Python 3.8 o superior
* Graphviz instalado

Instalar dependencias:

```bash
pip install graphviz
```

---

# Uso

Ejecutar el programa:

```bash
py main.py
```
---

# Ejemplos de Uso

### Cargar autómata desde JFLAP

El sistema permite importar autómatas definidos en archivos `.jff`.

### Convertir AFND a AFD

El sistema realiza automáticamente la conversión utilizando el algoritmo de subconjuntos.

### Generar expresión regular

A partir de un AFD se puede obtener una expresión regular equivalente.

---

