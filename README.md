# Inferencia de Tipos

La *inferencia de tipos* es la capacidad de deducir, ya sea parcial o totalmente, el tipo de una expresión en tiempo de compilación. El objetivo de este proyecto es la implementación de un intérprete de _COOL (Classroom Object-Oriented Language)_ que posea inferencia de tipos mediante la adición del tipo **AUTO_TYPE**. Para más información consulte las especificaciones del proyecto en el documento [`Segundo proyecto de Compilacion`](/docs/Orientacion.pdf).

## Sobre el lenguaje COOL

Usted podrá encontrar la especificación formal del lenguaje **COOL** en el documento [`COOL Language Reference Manual.pdf`](/docs/Manual.pdf).

## Ejecutando la aplicación

Para lanzar la aplicación de escritorio, ejecute las siguientes instrucciones:

```bash
$ cd src/
$ make visual
```

Sim embargo puede correr el proyecto en consola mediante las líneas donde aperece ya un archivo predeterminado:

```bash
$ cd src/
$ make console
```

## Sobre la implementación

#### Arquitectura

La arquitectura de la aplicación consiste primeramente en un lexer, el cual nos transforma una entrada de código _COOL_ en una serie de tokens que lo representan y detecta errores respecto a la escritura incorrecta de sı́mbolos. La segunda fase del compilador es el parser, el cual nos transforma la serie de tokens devueltos por el lexer en un _Árbol de Sintaxis Abstracta (AST)_ que nos representa el código del programa. La siguiente y última fase es el análisis semántico en donde se verifica el cumplimiento de las reglas semánticas del lenguaje y la inferencia de tipos.

#### Análisis Lexicográfico

Las implementaciones del lexer fueron realizadas utilizando la biblioteca de python *ply*. La gramática base con la cual se reconoce el lenguaje es la especificada en las clases prácticas.

#### Análisis Sintáctico

El parser escogido fue el _LR(1)_, siendo este uno de los más usados.

#### Análisis Semántico

En el análisis semántico se realizan tres pasadas (mediante el patrón visitor) por el _AST_, las dos primeras para construir los contextos de objetos y de métodos respectivamente y una tercera para realizar el chequeo de tipos. Durante la construcción de los contextos se detectan tempranamente algunos errores, y todos aquellos errores semánticos que no aparecen como parte de expresiones. Finalmente se realiza un último recorrido por el _AST_, nuevamente mediante el patrón visitor, haciendo la inferencia de tipos.

## Sobre la aplicación

Esta aplicación puede ser ejecutada en los sistemas operativos *window* y *linux*, siempre y cuando estén instalados las librerías *ply*, *PyQt5* y *pydot*.

## Sobre los autores

Est. Liset Silva Oropesa l.silva@estudiantes.matcom.uh.cu

Est. Ariel Plasencia Díaz a.plasencia@estudiantes.matcom.uh.cu
