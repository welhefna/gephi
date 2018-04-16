Support Graph Formats
========================

This Python Impelemtation of Supported graph formats by `Gephi <https://gephi.org/> and `networkX <https://networkx.github.io/>` _.  
what are supported data files and the general structure to follow:

* GEXF
* GDF
* GML
* GraphML
* Pajek NET
* GraphViz DOT
* CSV
* UCINET DL
* Tulip TPL
* Netdraw VNA
* Spreadsheet

The following table help to choose which format you want to encode your graph _.
..image:: https://gephi.org/images/graph-format-table-comparison.png

Usage
-----

	>>> import gephi
	>>> data = {'a' : (['a','b','c'],[12,11,10]) , 'b' : (['a','c','d'],[14,1,20]) , 'c' : (['a','d'],[.5,12]) , 'd' : (['b','c'],[3,4]) }
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.CVS('edge-list')
	a;a
	a;b
	a;c
	c;a
	c;d
	b;a
	b;c
	b;d
	d;b
	d;c


This simple project is an example repo for Python projects.

`Learn more <http://www.kennethreitz.org/essays/repository-structure-and-python>`_.

---------------

If you want to learn more about ``setup.py`` files, check out `this repository <https://github.com/kennethreitz/setup.py>`_.

✨🍰✨
