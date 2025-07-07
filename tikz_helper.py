
class Graph:
    def __init__(self, n:int, vn: list[str], pos:list[(float, float)] , erel:list[(str, str)], ns=None,es=None):
        if len(pos) == n:
            self.num_vertices = n
            self.vertex_names = vn
            self.vertex_position = list.copy(pos)
            self.edge_relations = list.copy(erel)
        else:
            print('Number of coordinates are not mathcing the number of vertcies')
            exit(0)

        if ns is None or len(ns)>1:
            self.vertex_style = ['yellow_vertex','[fill=yellow, draw=black, shape=circle, text=red]']
        else:
            self.vertex_style = ns

        if es is None or len(es)>1:
            self.edge_style = ["red_edge" , "[fill=none, ->, draw=red, thick]"]
        else :
            self.edge_style = es
        
        self.tikz_vertex = ''
        self.tikz_edges = ''
        self.tex_output = ''
        self.tikzpicture =''

    
    def create_vertices(self):
        vertex_style = self.vertex_style[0]
        self.tikz_vertex = '\n'.join([rf"\node[style={vertex_style}] ({self.vertex_names[x]}) at ({self.vertex_position[x][0]},{self.vertex_position[x][1]}) {{{x+1}}};" for x in range(self.num_vertices)])
    
    def create_edges(self):
        edge_style = self.edge_style[0]
        self.tikz_edges = '\n'.join([f"\draw[style={edge_style}] ({x}) to ({y});" for (x,y) in self.edge_relations])
    
    def create_tikzpicture(self):
        self.create_vertices()
        self.create_edges()
        self.tikzpicture = rf""
    
    def run_pdflatex(self):
        source_latex = self.__str__()
        #or first save source_latex to a file then run pdflatex on it

    def __str__(self):
        self.create_vertices()
        self.create_edges()



        self.tex_output= rf'''
\documentclass[tikz]{{standalone}}
\usepackage{{tikz}}

\begin{{document}}

\tikzstyle{{{self.vertex_style[0]}}}={self.vertex_style[1]}
\tikzstyle{{{self.edge_style[0]}}}={self.edge_style[1]}

\begin{{tikzpicture}}

{self.tikz_vertex}


{self.tikz_edges}

\end{{tikzpicture}}

\end{{document}}
            '''

        return self.tex_output
       

def main():
    g = Graph(8, [f"q{x}" for x in range(1,9)], [(0,0),(0,2),(2,4),(4,2),(4,0),(2,-2),(2,-4),(6,4)], [('q1','q2'), ('q2','q3'),('q3','q4'),('q4','q5'),('q5','q6'),('q6','q7'),('q4','q8'),('q8','q7')])
    print(g)
    
if __name__ == '__main__':
    main()