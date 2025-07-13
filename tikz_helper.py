import os
import glob
import subprocess
from typing import Optional
import sys
class Graph:
    def __init__(self, n:int, vn: list[str], pos:list[tuple[float,float]] , erel:list[tuple[str,str,float,float]], ns:Optional[list[str]] = None,es:Optional[list[str]] = None) -> None:
        if len(pos) == n:
            self.num_vertices = n
            self.vertex_names = vn
            self.vertex_position = list.copy(pos)
            self.edge_relations = list.copy(erel)
        else:
            print('Number of coordinates are not mathcing the number of vertcies')
            exit(0)

        if ns is None :
            self.vertex_style = ['yellow_vertex','[fill=yellow, draw=black, shape=circle, text=red]']
        else:
            self.vertex_style = ns

        if es is None :
            self.edge_style = ["red_edge" , "[fill=none, ->, draw=red, thick]"]
        else :
            self.edge_style = es
        
        self.tikz_vertex = ''
        self.tikz_edges = ''
        self.tex_output = ''
        self.tikzpicture =''

        self.create_tikzpicture()

    
    def create_vertices(self)-> None:
        vertex_style = self.vertex_style[0]
        self.tikz_vertex = '\n'.join(["\t"+rf"\node[style={vertex_style}] ({self.vertex_names[x]}) at ({self.vertex_position[x][0]},{self.vertex_position[x][1]}) {{{x+1}}};" for x in range(self.num_vertices)])
    
    def create_edges(self) -> None:
        edge_style = self.edge_style[0]
        self.tikz_edges = '\n'.join([f"\t\draw[style={edge_style}, bend left={l}] ({x}) to ({y});" if r==0  else f"\t\draw[style={edge_style}, bend right={r}] ({x}) to ({y});" for (x,y,l,r) in self.edge_relations])
    
    def create_tikzpicture(self) -> str:
        self.create_vertices()
        self.create_edges()
        self.tikzpicture = rf'''
\tikzstyle{{{self.vertex_style[0]}}}={self.vertex_style[1]}
\tikzstyle{{{self.edge_style[0]}}}={self.edge_style[1]}

\begin{{tikzpicture}}

{self.tikz_vertex}


{self.tikz_edges}

\end{{tikzpicture}}
        '''
        return self.tikzpicture
    
    def save_tikzpicture_to_file(self, file_name='default.tikzpicture') ->None:
        # Open a file in write mode
        print(f"Using {file_name} for writing into tikzpicture?[y/n]")
        x = input()
        if x=="Y" or x=='y' or x =='':
            with open(file_name, "w") as file:
                file.write(self.tikzpicture)
        else:
            print('File writing is aborted!')
            


    def run_pdflatex(self)-> None:
        source_latex = self.__str__()
        with open("temp.tex", "w") as file :
            file.write(source_latex)
        print("running pdflatex...")
        result = subprocess.run(["pdflatex", "-interaction=nonstopmode", "temp.tex"])
        if result.returncode == 0:
            print("PDF generated successfully.")
            res = subprocess.run(["open", "temp.pdf"])
        else:
            print("Compilation failed.")
            print(result.stdout.decode())                
            print(result.stderr.decode())
        
        files = glob.glob("temp.*")
        print(f"Delete the following files:{files}?[y/n]")
        x = input()
        if x=='Y' or x =='y' or x=='':
            for x in glob.glob("temp.*"): 
                os.remove(x)
        else:
            print(f"{files} are not deleted.")



    def __str__(self) -> str:
        
        self.tex_output= rf'''
\documentclass[tikz]{{standalone}}
\usepackage{{tikz}}

\begin{{document}}

{self.tikzpicture}

\end{{document}}
            '''

        return self.tex_output

class InputHandler:
    def __init__(self, file_path:str) -> None:
        if os.path.exists(file_path):
            self.file = open(file_path, 'r')
            self.num_vertices:int  = 0
            self.vertex_names:list[str] = []
            self.vertex_position: list[tuple[float,float]] = []
            self.edge_relations : list[tuple[str,str,float,float]] = []
            self.vertex_style:Optional[list[str]] = []
            self.edge_style:Optional[list[str]] = []
            self.input_graph()
        else:
            print(f"No Such file is found: {file_path}")
               
    def input_graph(self):
        lines = self.file.readlines()
        self.num_vertices = int(lines[0])
        lines = lines[1:]
        
        self.vertex_names = lines[0].split(' ')

        if len(self.vertex_names) != self.num_vertices:
            print("Number of vertices does not match the number of vertex names")
            sys.exit(1)
        self.vertex_names[self.num_vertices -1] = self.vertex_names[self.num_vertices -1][:-1] 
        lines = lines[1:]
        try:
            self.vertex_position = [tuple(map(float, lines[c].split(',')))  for c in range(self.num_vertices)]
        except Exception as e:
            print(f'{"="*20}\n{e}\n{"="*20}')
            print("There is some problem in number of positions and number of vertices specified earlier.\nRefer to README to properly get the .graph file ")
            sys.exit(1)
        
        lines = lines[self.num_vertices:]
        if "#" in lines[0] :
            try:
                s, e = tuple ([i for i, x in enumerate(lines) if "#" in x ])
            except ValueError as e:
                print(e)
                print("Edge relations must end with '#'\nSee the README file.")
                sys.exit(1)
            edges = lines[s+1:e]
            self.edge_relations = [ tuple(map(lambda x : float (x[1]) if x[0]>1 else x[1], enumerate(edge.split(',')))) for edge in edges]
            lines = lines[e+1:]
        else:
            print(f"Edge relations must start with '#'. First few lines of \n{'='*10}\n{''.join(lines[:2])}\n{'='*10}\nSee the README file.")
            sys.exit(1)
        if len(lines)!=0:
            sp1 = lines[0].index(' ')
            sp2 = lines[1].index(' ')
            self.vertex_style = [lines[0][:sp1],lines[0][sp1+1:-1]]
            self.edge_style =  [lines[1][:sp2],lines[1][sp2+1:-1]]
        else:
            self.vertex_style = None
            self.edge_style = None
        
    
    def create_Graph(self):
        g = Graph(self.num_vertices, self.vertex_names, self.vertex_position,self.edge_relations,self.vertex_style,self.edge_style)
        return g
    
    def __str__(self) -> str:
        return f"{self.num_vertices}\n{self.vertex_names}\n{self.vertex_position}\n{self.edge_relations}\n{self.edge_style}\n{self.vertex_style}"
        
        

def main(file_name='g2.graph'):
    #edge relation : ('starting vertex', 'ending vertec', left bend, right bend)
    #g = Graph(8, [f"q{x}" for x in range(1,9)], [(0,0),(0,2),(2,4),(4,2),(4,0),(2,-2),(2,-4),(6,4)], [('q1','q2',0,0), ('q2','q3',0,0),('q3','q4',0,0),('q4','q5',0,0),('q5','q6',0,0),('q6','q7',0,0),('q4','q8',0,0),('q8','q7',15,0)])
    #g = Graph(8, [f"q{x}" for x in range(1,9)], [(0,0),(1,1),(0,2),(-1,1),(-2,-1),(2,-1),(-1,-2),(1,-2)], [('q1','q2',0,0), ('q2','q3',0,0),('q3','q4',0,0),('q4','q1',0,0),('q1','q5',0,0),('q1','q6',0,0),('q5','q7',0,0),('q6','q8',0,0)])
    #g.save_tikzpicture_to_file()
    #g.run_pdflatex()
    
    h = InputHandler(file_name)
    g1 = h.create_Graph()
    g1.save_tikzpicture_to_file()
    g1.run_pdflatex()
    
    
if __name__ == '__main__':
    arg_list = sys.argv
    if len(arg_list) == 2:
        main(arg_list[1])
    else: 
        print('usage: pyhton3 tikz_helper.py pat/to/the/file.graph')