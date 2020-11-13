.PHONY: visual

install:
	pip3 install ply
	pip3 install PyQt5
	pip3 install pydot

clean:
	rm -rf cmp/__pycache__
	rm -rf uis/__pycache__
	rm -rf utils/__pycache__
	rm -rf visitors/__pycache__

visual:
	# Corriendo Inferencia de Tipos ;)
	python3 type_inferer_visual.py

console:
	# Ejecutando en consola :)
	python3 type_inferer_console.py ../examples/test7.cl
