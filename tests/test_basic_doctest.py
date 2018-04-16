"""Run basic doctest for gephi

To run the basic test using doctest module use the following command : 

"""

import doctest
from context import gephi

def test_gephi():
	"""Basic doctest for gephi methods

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
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.CVS('adjacency-list')
	a;a;b;c
	c;a;d
	b;a;c;d
	d;b;c
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.CVS('mixed')
	a,a,b,c
	c,a,d
	b,a,c,d
	d,b,c
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.CVS('matrix')
	;a;c;b;d
	a;1;1;1;0
	c;1;0;0;1
	b;1;1;0;1
	d;0;1;1;0
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.CVS('edge-weight')
	;a;c;b;d
	a;12.0;10.0;11.0;0.0
	c;0.5;0.0;0.0;12.0
	b;14.0;1.0;0.0;20.0
	d;0.0;4.0;3.0;0.0
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.adjacency_list()
	a a b c
	c a d
	b a c d
	d b c
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.multiline_adjacency_list()
	a 3
	a
	b
	c
	c 2
	a
	d
	b 3
	a
	c
	d
	d 2
	b
	c
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.pajek_net('edges-list')
	*Vertices 4
	1 "a"
	2 "c"
	3 "b"
	4 "d"
	*edgeslist
	1 1 3 2
	2 1 4
	3 1 2 4
	4 3 2
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.pajek_net('weight',labels=None)
	*Vertices 4
	*arcs
	1 1 12
	1 3 11
	1 2 10
	2 1 0.5
	2 4 12
	3 1 14
	3 2 1
	3 4 20
	4 3 3
	4 2 4
	>>> G = gephi.Gephi(data , graph_type = 'direct')
	>>> print G.GDF_format()
	nodedef>name VARCHAR,label VARCHAR,class VARCHAR, visible BOOLEAN,labelvisible BOOLEAN,width DOUBLE,color VARCHAR
	a,a,a,true,true,2,'0,0,0'
	c,c,c,true,true,2,'0,0,0'
	b,b,b,true,true,2,'0,0,0'
	d,d,d,true,true,2,'0,0,0'
	edgedef>node1 VARCHAR,node2 VARCHAR,weight DOUBLE
	a,a,12
	a,b,11
	a,c,10
	c,a,0.5
	c,d,12
	b,a,14
	b,c,1
	b,d,20
	d,b,3
	d,c,4
	
	"""


if __name__ == '__main__':
	print __doc__ , '\nrun $python -m ' , __file__ , ' -v' , '\n'
	doctest.testmod()