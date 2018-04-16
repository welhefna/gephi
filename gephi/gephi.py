"""Graph Format

Gephi convert graph [Adj. Matrix, or Edge. list] to gephi and networkX supported graphs data files formats and general structure. 
Gephi support the following gephi and networkX standard graph file formats :  

. GEXF
. GDF
. GML
. GraphML
. Pajek NET
. GraphViz DOT
. CSV
. UCINET DL
. Tulip TPL
. Netdraw VNA
. Spreadsheet

Gephi is `Supported Graph Formats` contains documentation, samples and implementation details. 


Gephi module usage:
	from .gephi import Gephi

For more information about different graphs file formats:
   https://gephi.org/users/supported-graph-formats/

Todo :
	support more graph formats based on research plan and requirements.
	
"""

class Gephi(object):
	"""Gephi 
	
	Gephi module is graph format library support varoius graphs data files formats and the general structure for gephi and networkx applications.
    	
    	Attributes:
        data (dict): dictionary map of graph information <key,value>, key is node name value is tuple of two items first item is list of edges and second item is list of edges weights.
        keys (list): nodes names of the graph
        graph_type (str): graph type
	
	"""
	
	__slots__ = ['data','keys','graph_type']
	
	def __init__(self, data , graph_type = 'undirect'):
	
		"""Gephi Constructor
		
		Args :
			data (str):     python dictionary <key (str): node name, values (tuple) : (edges (list): nodes names , weight (list): edges weights)>
			
		Kwargs:
			graph_type (str, default 'undirect') : type of graph 'directed' or 'undirected'

		Returns :
			none
			
		Raises :
			ValueError : raise exception when value of graph_type is not direct nor undirect.
			TypeError : raise exception when the input data type is not a dictionary 'map'.
		
		"""
	
		if type(data) == dict :
		
			self.graph_type = graph_type 
			self.keys = data.keys()
			
			if graph_type == 'undirect' :
				
				check_hash_set = set()
				self.data = dict()
				
				for key in self.keys :
					
					nodes = data[key][0] 
					weights = data[key][1]
					t_nodes = []
					t_weights = []
					
					for node_index in xrange(len(nodes)) :
						if (key,nodes[node_index]) not in check_hash_set and (nodes[node_index],key) not in check_hash_set :
							t_nodes.append(nodes[node_index])
							t_weights.append(weights[node_index])
							check_hash_set.add((key,nodes[node_index]))
							check_hash_set.add((nodes[node_index],key))
					
					self.data[key] = (t_nodes,t_weights)
					
					
			elif graph_type == 'direct':
			
				self.data = data
			
			else:
			
				raise ValueError('Unspported Graph type : ' + graph_type + ' : Gephi only support direct and undirect graphs types')
				
			
				
		else :
		
			raise TypeError('Unsupported data type : ' + str(type(data)) + ' : Gephi support dictionary data container ')
			
			
	def CVS(self, graph_format = 'adjacency-list'):
	
		"""CSV Format
		
		Gephi supports CSV files that simply represents relationships. The CSV format can be obtained from any row data, databases or Excel export. 
		Each line must contains at least two elements, separated by a separator (coma, semicolon, pipe or whitespace). Values can be encapsulated by 
		single or double quotes. By default graphs imported from CSV are directed graphs, but the user can select undirected in the import report dialog.
		
		Args:
			None
		kwargs:
			  graph_format (str),  specifiy te format of graph to generate the default format is adjacency-list.
			. edge-list, the CSV example below represents a graph with two edges: "a" -> "b" and "b" -> "c".
				
				a;b
				b;c
				
			. adjacency-list, All edges can be written as node pairs. It's also possible to write all node's connection on the same line. 
			  		  The example below represents a graph with 3 edges: "a" -> "b", "b" -> "c" and "b" -> "d".
				a;b
				b;c;d
				
			. mixed, the following example shows various cases that CSV supports as well. Self-loops and mutual edges are supported. It's also 
				 possible to repeat an edge, "D" -> "E" is repeated twice in this example. As a consequence the edge weight is incremented. 
				 "D" -> "E" has a edge weight at two, whereas default value is one.
				 
				A,B
				B,A
				C,C
				D,E
				A,D
				D,B,E
				F,G,A,B
				
			. matrix, the sample below shows a graph with 5 nodes. An edge is created when the the cell is '1'.
			
				;A;B;C;D;E
				A;0;1;0;1;0
				B;1;0;0;0;0
				C;0;0;1;0;0
				D;0;1;0;1;0
				E;0;0;0;0;0
				
			. edge-weight, Simply replace '1' values by the edge weight value, formatted as a 'double'.
			
				;A;B;C;D;E
				A;0.0;0.1;0.0;1.2;0.0
				B;1.0;0.0;0.0;0.0;0.0
				C;0.0;0.0;0.4;0.0;0.0
				D;0.0;0.1;0;0.1.2;0.0
				E;0.0;0.0;0.0;0.0;0.0
			
			
		
		Returns :
			A string CSV selected format based on gtype.
			
		Raises:
			ValueError : raise exception when graph_format is not supportted by the methon.
		
		"""
		
		csv_str=''
		
		
		
		if graph_format == 'edge-list' :
		
			for key in self.keys :
				nodes = self.data[key][0]
				for node in nodes:
					csv_str += key + ';' + node + '\n'
		
		elif graph_format == 'adjacency-list' :

			for key in self.keys :
				buffer=''
				nodes = self.data[key][0]
				for node in nodes:
					buffer += ';' + node
					
				csv_str += key + buffer + '\n'
				
		elif graph_format == 'mixed' :
	
			for key in self.keys :
				buffer=''
				nodes = self.data[key][0]
				for node in nodes:
					buffer += ',' + node
				csv_str += key + buffer + '\n'
				
		elif graph_format == 'matrix' :
			
			matrix=[list() for _ in self.keys]
			for i in xrange(len(self.keys)):
				matrix[i]=[0 for _ in self.keys]
				
			csv_str = ';'+";".join([str(key) for key in self.keys])+'\n'
			
			if self.graph_type == 'undirect' :
			
				for key in self.keys :

					nodes = self.data[key][0]
					for node in nodes:
						matrix[self.keys.index(key)][self.keys.index(node)] = 1
						matrix[self.keys.index(node)][self.keys.index(key)] = 1

						buffer=''	
						for cell in matrix[self.keys.index(key)]:
							buffer += ";{}".format(cell)

					csv_str += key + buffer + '\n'
					
			else :
			
				for key in self.keys :

					nodes = self.data[key][0]
					for node in nodes:
						matrix[self.keys.index(key)][self.keys.index(node)] = 1

					buffer=''	
					for cell in matrix[self.keys.index(key)]:
						buffer += ";{}".format(cell)

					csv_str += key + buffer + '\n'
				
		elif graph_format == 'edge-weight' :
			
			matrix=[list() for _ in self.keys]
			for i in xrange(len(self.keys)):
				matrix[i]=[0 for _ in self.keys]
			
			csv_str = ';'+";".join([str(key) for key in self.keys])+'\n'
			
			if self.graph_type == 'undirect' :
			
				for key in self.keys :

					nodes = self.data[key][0]
					weights = self.data[key][1]
					
					for node in nodes:
						matrix[self.keys.index(key)][self.keys.index(node)] = weights[nodes.index(node)]
						matrix[self.keys.index(node)][self.keys.index(key)] = weights[nodes.index(node)]

						buffer=''	
						for cell in matrix[self.keys.index(key)]:
							buffer += ";{0:.1f}".format(cell)

					csv_str += key + buffer + '\n'
					
			else :
			
				for key in self.keys :

					nodes = self.data[key][0]
					weights = self.data[key][1]
					
					for node in nodes:
						matrix[self.keys.index(key)][self.keys.index(node)] = weights[nodes.index(node)]

					buffer=''	
					for cell in matrix[self.keys.index(key)]:
						buffer += ";{0:.1f}".format(cell)

					csv_str += key + buffer + '\n'
					
		else :
			raise ValueError('Unsupported CSV graph type : ' + graph_format)
			
		return csv_str[:-1]
		
	def adjacency_list(self):
		"""Adjacency list 
		
		Adjacency list format is useful for graphs without data associated with nodes or edges 
		and for nodes that can be meaningfully represented as strings. The adjacency list format 
		consists of lines with node labels. The first label in a line is the source node. Further 
		labels in the line are considered target nodes and are added to the graph along with an edge 
		between the source node and target node. The graph with edges a-b, a-c, d-e can be represented
		as the following adjacency list (anything following the # in a line is a comment):

		a b c # source target target
		d e
		
		Args:
			none
		
		kwargs:
			none
			
		Returns:
			r_str (str): adjacency list in string format
			
		Raises:
			none
		
		"""
		
		r_str = ''
		
		for key in self.keys :
			buffer=''
			nodes = self.data[key][0]
			for node in nodes:
				buffer += ' ' + node
			r_str += key + buffer + '\n'
			
		return r_str[:-1]
		
	def multiline_adjacency_list(self):		
		"""Multiline Adjacency List
		
		The multi-line adjacency list format is useful for graphs with nodes that can be meaningfully represented as strings. 
		With this format simple edge data can be stored but node or graph data is not. The first label in a line is the source 
		node label followed by the node degree d. The next d lines are target node labels and optional edge data. That pattern 
		repeats for all nodes in the graph. The graph with edges a-b, a-c, d-e can be represented as the following adjacency list (anything following the # in a line is a comment):

		# example.multiline-adjlist
		a 2
		b
		c
		d 1
		e
		
		Args:
			none
		
		kwargs:
			none
			
		Returns:
			r_str (str): multiline adjacency list in string format
			
		Raises:
			none
		
		"""
		
		r_str = ''
		
		for key in self.keys :
		
			nodes = self.data[key][0]
			buffer = "{} {}\n".format( key , len(nodes) )
			
			for node in nodes:
				buffer += node + '\n'
			r_str += buffer
			
		return r_str[:-1]
		
	def pajek_net(self, scheme , labels = True):
		"""Pajek NET Format
		
		This format use NET extension and is easy to use. Attributes support is however missing, 
		only the network topology can be represented with a Pajek File. The structure is easy, 
		Pajek files are text files, where each line is an element, and the list of edges follows 
		the list of nodes. It is supported by nearly most of graph softwares, including Pajek, NodeXL and NetworkX.

		Nodes
		Nodes have basically one unique identifier and a label. The definition of nodes starts with the chain *vertices N 
		where N is the number of nodes following. For instance this is the beginning of a Pajek file of 82670 nodes. Labels 
		are quoted directly after the nodes identifier.
		
		*Vertices 82670
		1 "entity"
		2 "thing"
		3 "anything"
		4 "something"
		5 "nothing"
		6 "whole"

		When nodes do not have labels, the list of identifier is hence useless (only ordered numbers). Thus only the vertices 
		count is set. The importer will create the exact number of edges.

		*Vertices 2536
		
		Edges
		Edges are either defined as list of nodes identifier or pair of two nodes.
		For the first case; edges are defined as pair of nodes identifier. The *arcs marker goes before the pairs list.
		
		*arcs
		4244 107
		4244 238
		4244 4292
		4247 107
		4248 1
		4248 54

		Weight is added by a third column, here the weight of the first edge is 5:
		
		*arcs
		4244 107 5

		For the second scheme, the first identifier is the source node and all following are the neighbors. The dedicated marker is edgeslist.

		*edgeslist
		4941 386 395 451
		1 3553 3586 3587 3637
		2 3583
		3 4930
		4 88
		5 13 120
		
		
		Args:
			scheme (str) : specifiy the format of output edges, weight, edges-list
		
		kwargs:
			labels (bool) : enable nodes labels
			
		Returns:
			r_str (str): Pajek NET in string format
			
		Raises:
			Exception unsupported scheme format
 
		"""
		
		r_str = '*Vertices ' + str(len(self.keys)) + '\n'
		
		if labels :
			for key in enumerate(self.keys):
				r_str += '{} "{}"\n'.format( key[0] + 1 , key[1])
			
		if scheme == 'edges' :
		
			r_str += '*arcs' + '\n'
			
			for key in self.keys :
				buffer=''
				nodes = self.data[key][0]
				for node in nodes:
					buffer += "{} {}\n".format( self.keys.index(key) + 1 , self.keys.index(node) + 1 )
				r_str += buffer
		
		elif scheme == 'weight' :
		
			r_str += '*arcs' + '\n'
			
			for key in self.keys :
				buffer=''
				nodes = self.data[key][0]
				weights = self.data[key][1]
				for node in nodes:
					buffer += "{} {} {}\n".format( self.keys.index(key) + 1 , self.keys.index(node) + 1 , weights[nodes.index(node)])
				r_str += buffer
				
		elif  scheme == 'edges-list' :
		
			r_str += '*edgeslist' + '\n'
			
			for key in self.keys :
				buffer=''
				nodes = self.data[key][0]
				for node in nodes:
					buffer += " {}".format(self.keys.index(node)+1)
				r_str += "{}{}\n".format( self.keys.index(key) + 1 , buffer )
				
		else:
			raise Exception('Unspprted Scheme ' + scheme)
			
		return r_str[:-1]
		
	def GDF_format(self,colors = []):
		"""GDF Format
		
		GDF is the file format used by GUESS. It is built like a database table or a coma separated file (CSV). 
		It supports attributes to both nodes and edges. A standard file is divided in two sections, one for nodes 
		and one for edges. Each section has a header line, which basically is the column title. Each element 
		(i.e. node or edge) is on a line and values are separated by coma. The GDF format is therefore very easy 
		to read and can be easily converted from CSV.

		The following link shows the official manual, where information is available about attributes types and logic.
		Examples
		Basic example

		The GDF below is the minimum you need to be supported by Gephi's current file Importer. The label column is optional.

		nodedef>name VARCHAR,label VARCHAR
		s1,Site number 1
		s2,Site number 2
		s3,Site number 3
		edgedef>node1 VARCHAR,node2 VARCHAR
		s1,s2
		s2,s3
		s3,s2
		s3,s1

		With edge weight

		Edge weight is basically edge thickness and is defined as follow.

		nodedef>name VARCHAR,label VARCHAR
		s1,Site number 1
		s2,Site number 2
		s3,Site number 3
		edgedef>node1 VARCHAR,node2 VARCHAR, weight DOUBLE
		s1,s2,1.2341
		s2,s3,0.453
		s3,s2, 2.34
		s3,s1, 0.871

		Various attributes

		Add as many attributes as you need. Add attributes title in the header line and respect order, as you would do for CSV.
		On the below example, all attributes are design attributes expect "class" that I added. Attributes are central in Gephi, 
		because they can be used by Filter Module.

		nodedef>name VARCHAR,label VARCHAR,class VARCHAR, visible BOOLEAN,labelvisible BOOLEAN,width DOUBLE,height DOUBLE,x DOUBLE,y DOUBLE,color VARCHAR
		s1,SiteA,blog,true,true,10.0,10.0,-52.11296,-25.921143,'114,116,177'
		s2,SiteB,forum,true,true,10.986123,10.986123,-20.114172,25.740356,'219,116,251'
		s3,SiteC,webpage,true,true,10.986123,10.986123,8.598924,-26.867584,'192,208,223'
		edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN,color VARCHAR
		s1,s2,true,'114,116,177'
		s2,s3,true,'219,116,251'
		s3,s2,true,'192,208,223'
		s3,s1,true,'192,208,223'

		Working with texts

		Problems often comes when coma, apostrophe (i.e. single-quote) or double-quote are used in texts. The example below shows how to manage these 
		strings, wrap single-quotes around it.

		nodedef>name VARCHAR,label VARCHAR,class VARCHAR, visible BOOLEAN,labelvisible BOOLEAN,width DOUBLE,height DOUBLE,x DOUBLE,y DOUBLE,color VARCHAR
		s1,'Hello "world" !',type1,true,true,10.0,10.0,-52.11296,-25.921143,'114,116,177'
		s2,'Well, this is',type1,true,true,10.986123,10.986123,-20.114172,25.740356,'219,116,251'
		s3,'A correct 'GDF' file',type1,true,true,10.986123,10.986123,8.598924,-26.867584,'192,208,223'
		edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN,color VARCHAR
		s1,s2,true,'114,116,177'
		s2,s3,true,'219,116,251'
		s3,s2,true,'192,208,223'
		s3,s1,true,'192,208,223'

		Implementation details
		Missing values

		When values are missing, don't omit to put the coma.

		nodedef>name VARCHAR, label VARCHAR, att1 VARCHAR, att2 VARCHAR, att3 VARCHAR,att4 BOOLEAN
		s1,SiteA,blabla,blabla,blabla,true
		s2,SiteB, , , ,false
		s3,SiteC,blabla, , ,true

		Colors

		Color is a VARCHAR attribute with 3 values for red, blue and green. Values should be from 0 to 255.
		Example: '114,116,177'

		Position & size

		Position is set with X and Y values, plus an optional Z value. They must be DOUBLE columns. Size of nodes is set with the width DOUBLE attribute.

		Common problems
		* I don't see my special characters. Square are drawn instead.
		For characters different from ASCII, encode your file in UTF-8 (with BOM). One can use Notepad++ for doing this.

		* ArrayIndexOutOfBoundsException: 1
		Be sure you mentioned a label in each node line.
		
		Args:
			scheme (str) : specifiy the format of output edges, weight, edges-list
		
		kwargs:
			colors (list) : colors list in RGB format ['127,123,20', .... , '0,0,0']
			
		Returns:
			r_str (str): GDF Format in string format
			
		Raises:
			none
		
		"""
		
		if colors == []:
			colors = [ '0,0,0' for _ in self.keys ]
			
		r_str = 'nodedef>name VARCHAR,label VARCHAR,class VARCHAR, visible BOOLEAN,labelvisible BOOLEAN,width DOUBLE,color VARCHAR' + '\n'
		
		for key in enumerate(self.keys):
			r_str += "{0},{0},{0},true,true,{1},'{2}'\n".format( key[1] , len(self.data[key[1]]) , colors[key[0]] )
			
		r_str += 'edgedef>node1 VARCHAR,node2 VARCHAR,weight DOUBLE' + '\n'		
		
		for key in self.keys :
			buffer=''
			nodes = self.data[key][0]
			weights = self.data[key][1]
			for node in nodes:
				buffer += "{},{},{}\n".format( key , node , weights[nodes.index(node)] )
				
			r_str += buffer		
		
		return r_str[:-1]
		
	def GEXF(self):
		"""Graph Exchange XML Format
		
		GEXF (Graph Exchange XML Format) is a language for describing complex networks structures, their associated 
		data and dynamics. Started in 2007 at Gephi project by different actors, deeply involved in graph exchange issues, 
		the gexf specifications are mature enough to claim being both extensible and open, and suitable for real specific 
		applications.
		
		Manifest
		It has been a long time a new graph format was created, so we decided to do one ourselves. No, this is not the reason. 
		Here are some of the reasons we decided to create the GEXF format:
		Strong pedestal but addition liberty: The key word is exchange, respect the base constraints to exchange at least 
		the graph topology and data but let people add their own namespace to do their own businesses.
		Network only: Our community domain of interest is networks, nothing else. 
		The goal is to represent a network's elements: nodes, edges and data associated to them. We tried to keep it simple 
		and focus on what we have in common.
		Hierarchy structure: Some other formats do have this as well. Nodes can simply host other nodes and so on. The format 
		allows creating hierarchical structure. This is essential for represent clustering.
		Dynamic ready: The support of dynamic functionalities is experimental and need more feedback but networks dynamics is 
		a growing topic of research and it is appropriate to think dynamic from the beginning.
		Implementation aware: Because hierarchy and dynamic support are not easy tasks, the format can include specific implementation 
		attribute to help parsers to do their job. Again, this is not mandatory but we think it will help.
		Utility of XML: You probably already know the utility of markup languages in general, but why XML? Because it is a well known language, 
		because we intend to use namespaces, because XML parsers exists in all programming languages and because XML databases are coming.
		
		Dummy example
		
		This is a minimal file for a static graph containing 2 nodes and 1 edge between them:
		http://gexf.net/data/hello-world.gexf
		
		<?xml version="1.0" encoding="UTF-8"?>
		<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
		    <meta lastmodifieddate="2009-03-20">
			<creator>Gexf.net</creator>
			<description>A hello world! file</description>
		    </meta>
		    <graph mode="static" defaultedgetype="directed">
			<nodes>
			    <node id="0" label="Hello" />
			    <node id="1" label="Word" />
			</nodes>
			<edges>
			    <edge id="0" source="0" target="1" />
			</edges>
		    </graph>
		</gexf>
		
		Notes:
			This implementation does not support mixed graphs (directed and undirected edges together).
		
		Args:
			None
		
		kwargs:
			None
			
		Returns:
			r_str (str): GEXF Format in string format
			
		Raises:
			none
		
		"""	
		
		r_str = '<?xml version="1.0" encoding="UTF-8"?>' + '\n'
		r_str += '<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">' + '\n'
		r_str += '<meta lastmodifieddate="2009-03-20">' + '\n'
		r_str += '<creator>Gexf.net</creator>' + '\n'
		r_str += '<description>A hello world! file</description>' + '\n'
		r_str += '</meta>' + '\n'
		r_str += '<graph mode="static" defaultedgetype="' + self.graph_type + '">' + '\n'
		r_str += '<nodes>' + '\n'
		
		for key in self.keys:	 
			 r_str += '<node id="'+ key +'" label="'+ key +'" />' + '\n'
			    
		r_str += '</nodes>' + '\n'
		r_str += '<edges>' + '\n'
		
		edge_id = 0
		for key in self.keys :
			nodes = self.data[key][0]
			weights = self.data[key][1]
			for node in nodes:
			    r_str += '<edge id="'+ str(edge_id) +'" source="'+ key +'" target="'+ node +'" />' + '\n'
			    edge_id += 1
			    
		r_str += '</edges>' + '\n'
		r_str += '</graph>' + '\n'
		r_str += '</gexf>' + '\n'
		
		return r_str[:-1]
		
	def GML(self):
		"""GML Format
		
		GML (Graph Modeling Language) is a text file format supporting network data with a very easy syntax. It is 
		used by Graphlet, Pajek, yEd, LEDA and NetworkX.
		
		Gephi currently doesn't provide a complete support of the GML format. Data structures are not supported.

		Datasets
		Mark Newman's page provides a large range of networks in GML here.

		Examples
		Basic examples

		The sample below shows a graph of three nodes and two edges.
		graph
		[
		  node
		  [
		   id A
		  ]
		  node
		  [
		   id B
		  ]
		  node
		  [
		   id C
		  ]
		   edge
		  [
		   source B
		   target A
		  ]
		  edge
		  [
		   source C
		   target A
		  ]
		]

		Labels

		The sample below shows the same example but with both node and edge labels.
		graph
		[
		  node
		  [
		   id A
		   label "Node A"
		  ]
		  node
		  [
		   id B
		   label "Node B"
		  ]
		  node
		  [
		   id C
		   label "Node C"
		  ]
		   edge
		  [
		   source B
		   target A
		   label "Edge B to A"
		  ]
		  edge
		  [
		   source C
		   target A
		   label "Edge C to A"
		  ]
		]
		
		Notes:
			This implementation does not support mixed graphs (directed and undirected edges together).
		
		Args:
			None
		
		kwargs:
			None
			
		Returns:
			r_str (str): GML Format in string format
			
		Raises:
			none
		
		"""
		
		r_str = 'graph' + '\n'
		r_str += '[' + '\n'
		
		for key in self.keys:
			r_str += 'node' + '\n'
			r_str += '[' + '\n'
			r_str += 'id '+ key + '\n'
			r_str += 'label "Node ' + key + '"' + '\n'
			r_str += ']' + '\n'
			
		for key in self.keys:
			nodes = self.data[key][0]
			weights = self.data[key][1]
			for node in nodes:
				r_str += 'edge' + '\n'
				r_str += '[' + '\n'
				r_str += 'source ' + key + '\n'
				r_str += 'target ' + node + '\n'
				r_str += 'label "Edge ' + node + ' to ' + key + ' : ' + str(weights[nodes.index(node)]) + '"' + '\n'
				r_str += ']' + '\n'		
		
		r_str += ']' + '\n'
		
			
		return r_str[:-1]
		
	def graph_ML(self , weights = None , colors = []):
	
		r_str = '<?xml version="1.0" encoding="UTF-8"?>' + '\n'
		r_str += '<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
		r_str += 'xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">' + '\n'
		
		r_str += '<key id="d0" for="node" attr.name="color" attr.type="string">' + '\n'
		r_str += '<default>yellow</default>' + '\n'
		r_str += '</key>' + '\n'
		
		r_str += '<key id="d1" for="edge" attr.name="weight" attr.type="double"/>' + '\n'
		
		r_str += '<graph id="G" edgedefault="' + self.graph_type + '">' + '\n'
		
		if colors:
			for key in self.keys:
				r_str += '<node id="' + key + '">' + '\n'
				r_str += '<data key="d0">' + colors[self.keys.index(key)] + '</data>' + '\n'
				r_str += '</node>' + '\n'
		else:
			for key in self.keys:
				r_str += '<node id="' + key + '"/>' + '\n'
		
		
		edge_id = 0
		
		if weights:
			for key in self.keys:
				nodes = self.data[key][0]
				weights = self.data[key][1]
				for node in nodes:		
					r_str += '<edge id="e' + str(edge_id) + '" source="' + key + '" target="' + node + '">' + '\n'
					r_str += '<data key="d1">'+ str(weights[nodes.index(node)])+'</data>' + '\n'
					r_str += '</edge>' + '\n'
					edge_id += 1
		else:
			for key in self.keys:
				nodes = self.data[key][0]
				for node in nodes:		
					r_str += '<edge id="e' + str(edge_id) + '" source="' + key + '" target="' + node + '"/>' + '\n'
					edge_id += 1	
				
		
		r_str += '</graph>' + '\n'
		r_str += '</graphml>' + '\n'
		
		return r_str[:-1]
		
	def spread_sheet(self):
		"""Spreadsheet (Excel)
		
		Nodes tables and edge tables are the file formats used in the Data Laboratory to import data from Excel. 
		It is a convenient way to transform any Excel data for Gephi without programming. The file extension is CSV 
		thought it should not be confused with the CSV file format itself. Each row is a node or edge entry. 
		It supports nodes and edges attributes, edge weight and dynamics with time intervals. See how to import spreadsheet data on the wiki.

		Examples
		Basic example

		The sample below shows a node table of of three nodes. The column of node identifiers must be named "Id".
		Id
		A
		B
		C

		The sample below shows an edge table of of two edge. The columns must be named "Source" and "Target".
		Source;Target
		A;B
		C;A

		Labels

		There tables are the same as above with labels. The columns of labels must be named "Label".

		Node Table:
		Id;Label
		A;"Node A"
		B;"Node B"
		C;"Node C"

		Edge Table:
		Source;Target;Label
		A;B;"Edge from A to B"
		C;A;"Edge from C to A"

		Edge identifiers

		Add a column named "Id" in the edge table.

		Edge types

		Add a column named "Type" in the edge table. Values must be either "Directed", "Undirected" or "Mixed".

		Edge weights

		Add a column named "Weight" in the edge table.

		Node and edge attributes

		Add a column with the name of your attribute in the corresponding table.
		
		Args :
			None
		Kwargs :
			None
		Returns :
			r_str (str) : string of graph format
		Raises:
			None
		
		"""
		
		r_str = 'Id;Label' + '\n'
		
		for key in self.keys:
			r_str += key + ';' + key + '\n'
			
		r_str += 'Source;Target;Label' + '\n'
		for key in self.keys:
			nodes = self.data[key][0]
			weights = self.data[key][1]
			for node in nodes:
				r_str += '{0};{1};"{0} to {1} : {2}"'.format(key,node,weights[nodes.index(node)]) + '\n'
		
		return r_str[:-1]
		
	def GraphViz_dot_format(self, graph_format = 'basic'):
		"""GraphViz DOT Format
		
		DOT is the text file format of the suite GraphViz. It has a human-readable syntax that describes network data, 
		including subgraphs and elements appearances (i.e. color, width, label). NetworkX, Tulip or ZGRViewer can import DOT 
		files as well. Additional informations can be found on Wikipedia.

		The following link shows the official website, where information is available about the DOT format.
		Examples
		Basic example

		The sample below shows a directed graph with two edges.

		digraph sample {
		A -> B;
		B -> C;
		}

		Labels

		The sample below shows the same example but with both node and edge labels.

		digraph sample2 {
		A -> B [ label = "Edge A to B" ];
		B -> C [ label = "Edge B to C" ];
		A [label="Node A"];
		}

		Adjacency lists

		The sample below shows edges can be put as adjacency lists.

		digraph sample3 {
		A -> {B ; C ; D}
		C -> {B ; A}
		}
		
		Args : 
			None
		Kwargs : 
			graph_format (str) : specifiy the graph format. 
		Returns :
			r_str (str) : string of GraphViz dot format.
		Raises:
			ValueError :  raise exception when graph format is unsupported by GraphViz_dot_format
		
		"""
	
		r_str = 'digraph G {' + '\n'
		
		if graph_format == 'Labels':
		
			for key in self.keys:
				nodes = self.data[key][0]
				weights = self.data[key][1]
				for node in nodes:
					r_str += '{0} -> {1} [ label = " {0} to {1} : {2} " ]; '.format(key,node,weights[nodes.index(node)]) + '\n'

			for key in self.keys:
				r_str += key + '[label="' + key + '"];' + '\n'
		
		elif graph_format == 'adjacency-list' :
			for key in self.keys:
				buffer = ''
				nodes = self.data[key][0]
				for node in nodes:
					buffer += node + ';'
					
				r_str += key + ' -> {' + buffer[:-1] +'}' + '\n'
				
				
		elif graph_format == 'basic' :
			for key in self.keys:
				buffer = ''
				nodes = self.data[key][0]
				for node in nodes:
					r_str += key + ' -> ' + node + ';' + '\n'
					
		else :
			raise ValueError('Unsupported graph format : ' + graph_format)
					
			
		r_str += '}' + '\n'
		
		return r_str[:-1]
		
	def ucinet_DL(self, graph_format = 'basic'):
		"""UCINET DL Format
		
		UCINET DL format is the most common file format used by UCINET package. Gephi currently supports the fullmatrix 
		and edgelist1 sub-formats. Full matrix format is the default for DL file extension. Unfortunately, a reference page 
		or manual seems not to be available about UCINET file formats.

		Full Matrix
		Basic example

		The DL sample below shows a graph with 5 nodes. An edge is created when the the cell is '1'.

		DL N = 5
		Data:
		0 1 1 1 1
		1 0 1 0 0
		1 1 0 0 1
		1 0 0 0 0
		1 0 1 0 0

		With node labels

		This example includes labels for each node. Labels must be put in a line after the "labels:" line.

		dl n=5
		format = fullmatrix
		labels:
		barry,david,lin,pat,russ
		data:
		0 1 1 1 0
		1 0 0 0 1
		1 0 0 1 0
		1 0 1 0 1
		0 1 0 1 0

		Edge weight

		Simply replace '1' values by the edge weight value, formatted as a 'double'.

		Edge list
		When the data are sparse, it is often more convenient to to enter just the pairs of nodes that are connected. 
		In the edgelist1 format, each line of data is an ordered pair of nodes, optionally followed by a value indicating 
		the strength of the relationship.

		Basic example

		A five nodes graph, with labels.

		DL n=5
		format = edgelist1
		labels:
		george, sally, jim, billy, jane
		data:
		1 2
		1 3
		2 3
		3 1
		4 3

		Labels embedded

		This example includes labels in the data.

		DL n=5
		format = edgelist1
		labels embedded:
		data:
		george sally
		george jim
		sally jim
		billy george
		jane jim

		Edge weight

		Edge weight comes as the third parameter on the row.

		dl
		format=edgelist1
		n=3
		data:
		1 2 1.56263736263736
		1 3 1.48687978687979
		2 3 1.39597069597070
		3 1 0.676190476190476
		
		Args :
			None
		Kwargs :
			None
		Returns :
			r_str (str) : string of graph format
		Raises:
			ValueError
		
		"""
		
		if graph_format == 'basic':
			
			r_str = 'dl N = ' + str(len(self.keys)) + '\n'
			r_str += 'format = fullmatrix' + '\n'
			r_str += 'labels:' + '\n'
			
			for key in self.keys:
				r_str += key + ','
			r_str=r_str[:-1] + '\n'
			
			r_str += 'data:' + '\n'
			
			
			matrix=[list() for _ in self.keys]
			for i in xrange(len(self.keys)):
				matrix[i]=[0 for _ in self.keys]
				
			if self.graph_type == 'undriect' :
			
				for key in self.keys :
					nodes = self.data[key][0]
					for node in nodes:
						matrix[self.keys.index(key)][self.keys.index(node)] = 1
						matrix[self.keys.index(node)][self.keys.index(key)] = 1

					buffer=''	
					for cell in matrix[self.keys.index(key)]:
						buffer += "{0:.1f} ".format(float(cell))
					buffer = buffer[:-1]
					r_str +=  buffer + '\n'
			else:
			
				for key in self.keys :
					nodes = self.data[key][0]
					for node in nodes:
						matrix[self.keys.index(key)][self.keys.index(node)] = 1

					buffer=''	
					for cell in matrix[self.keys.index(key)]:
						buffer += "{0:.1f} ".format( float(cell) )
					buffer = buffer[:-1]
					r_str +=  buffer + '\n'
				
		elif graph_format == 'weight':
			
			r_str = 'dl N = ' + str(len(self.keys)) + '\n'
			r_str += 'format = fullmatrix' + '\n'
			r_str += 'labels:' + '\n'
			
			for key in self.keys:
				r_str += key + ','
			r_str=r_str[:-1] + '\n'
			
			r_str += 'data:' + '\n'
			
			
			matrix=[list() for _ in self.keys]
			for i in xrange(len(self.keys)):
				matrix[i]=[0 for _ in self.keys]
			
			
			if self.graph_type == 'undriect' :
			
				for key in self.keys :

					nodes = self.data[key][0]
					weights = self.data[key][1]
					for node in nodes:
						matrix[self.keys.index(key)][self.keys.index(node)] = weights[nodes.index(node)]
						matrix[self.keys.index(node)][self.keys.index(key)] = weights[nodes.index(node)]

					buffer=''	
					for cell in matrix[self.keys.index(key)]:
						buffer += "{0:.1f} ".format(float(cell))
					buffer = buffer[:-1]
					r_str +=  buffer + '\n'
			else:
			
				for key in self.keys :

					nodes = self.data[key][0]
					weights = self.data[key][1]
					for node in nodes:
						matrix[self.keys.index(key)][self.keys.index(node)] = weights[nodes.index(node)]

					buffer=''	
					for cell in matrix[self.keys.index(key)]:
						buffer += "{0:.1f} ".format( float(cell) )
					buffer = buffer[:-1]
					r_str +=  buffer + '\n'
					
				
		elif graph_format == 'edge-list':
			
			r_str = 'dl N = ' + str(len(self.keys)) + '\n'
			r_str += 'format = edgelist1' + '\n'
			r_str += 'labels:' + '\n'
			
			for key in self.keys:
				r_str += key + ','
			r_str=r_str[:-1] + '\n'
			
			r_str += 'data:' + '\n'
	
			for key in self.keys :
				nodes = self.data[key][0]
				for node in nodes:
					r_str += "{} {}\n".format( self.keys.index(key) , self.keys.index(node) )
					
		elif graph_format == 'labels-embedded':
			
			r_str = 'dl N = ' + str(len(self.keys)) + '\n'
			r_str += 'format = edgelist1' + '\n'
			r_str += 'labels:' + '\n'
			
			for key in self.keys:
				r_str += key + ','
			r_str=r_str[:-1] + '\n'
			
			r_str += 'data:' + '\n'
	
			for key in self.keys :
				nodes = self.data[key][0]
				for node in nodes:
					r_str += "{} {}\n".format( key , node )
				
		elif graph_format == 'edge-weight':
			
			r_str = 'dl N = ' + str(len(self.keys)) + '\n'
			r_str += 'format = edgelist1' + '\n'
			r_str += 'labels:' + '\n'
			
			for key in self.keys:
				r_str += key + ','
			r_str=r_str[:-1] + '\n'
			
			r_str += 'data:' + '\n'
	
			for key in self.keys :
				nodes = self.data[key][0]
				weights = self.data[key][1]
				for node in nodes:
					r_str += "{} {} {:.2f}\n".format( self.keys.index(key) , self.keys.index(node) , weights[nodes.index(node)] )
					
		else:
			raise ValueError('Unsupported graph format : '+ graph_format)
					
		return r_str[:-1]
		
	def TLP(self):
		"""TLP Format
		
		TLP is the file format used by Tulip. Only network topology (nodes and edges) is currently supported.

		TLP Specification	Official TLP Specification (Tulip)
		Example
		The sample below shows a graph of three nodes and two edges.
		(tlp "2.0"
		(nodes 0 1 2)
		(edge 0 1 0)
		(edge 1 0 2)
		)

		Nodes syntax:
		(nodes node_id node_id ...)

		Edges syntax:
		(edge edge_id source_id target_id)
		
		Args :
			None
		Kwargs :
			None
		Returns :
			r_str (str) : string of graph format
		Raises:
			None
		
		"""
		
		r_str = '(tlp "2.0" ' + '\n'
		r_str += '(date "09-11-2006")' + '\n'
		r_str += '(author "Wessam Elhefnawy")' + '\n'
		r_str += '(comments "This file was generated by Tulip Gephi.")' + '\n'
		r_str += '(nodes' 
		
		for key in self.keys:
			r_str += " {}".format(self.keys.index(key))
		r_str += ')' + '\n'
		
		edge_id = 0
		for key in self.keys :
			nodes = self.data[key][0]
			for node in nodes:
				r_str += "(edge {} {} {})\n".format(edge_id , self.keys.index(key) , self.keys.index(node) )
				edge_id += 1
		
		r_str += ')' + '\n'	
		
		return r_str[:-1]
		
	def netdraw_VNA(self):
		"""Netdraw VNA format
		The VNA format is commonly used by Netdraw, and is very similar to Pajek format. It defines nodes and edges (ties), 
		and supports attributes. Each section of the file is separated by an asterisk.

		More details about the format can be found in Netdraw's manual.

		Basic example
		The VNA sample below shows a graph with 3 nodes and 4 edges. Each section has a column header line. The "ties" are 
		edges, and 'from' and 'to' defines the direction. The 'strength' attribute encodes the weight of the edge.


		*node data
		ID name gender age
		j101 joe male 56
		w067 wendy female 23
		b303 bill male 48
		*tie data
		from to strength
		j101 w067 1
		w067 j101 2
		j101 b303 1
		w067 b303 5
		
		Args :
			None
		Kwargs :
			None
		Returns :
			r_str (str) : string of graph format
		Raises:
			None
		
		
		"""
		
		r_str = '*node data' + '\n'
		r_str += 'ID name' + '\n'
		for key in self.keys:
			r_str += "{} {}\n".format( self.keys.index(key) , key )
			
		r_str += '*Node properties' + '\n'
		r_str += 'ID color shape size shortlabel' + '\n'
		for key in self.keys:
			r_str += "{} {} {} {} {}\n".format( self.keys.index(key) , 100 , 1 , len(self.data[key][1]) , key)
			
		r_str += '*tie data' + '\n'
		r_str += 'from to strength' + '\n'
	
		for key in self.keys :
			nodes = self.data[key][0]
			weights = self.data[key][1]
			for node in nodes:
				r_str += "{} {} {:.2f}\n".format( self.keys.index(key) , self.keys.index(node) , weights[nodes.index(node)])
					
		return r_str[:-1]
		
	
if __name__ == "__main__" :
	pass
	
			
		
	