import os
import glob
import subprocess

class Graph:
    def __init__(self, n:int, vn: list[str], pos:list[tuple[float,float]] , erel:list[tuple[str,str,float,float]], ns=None,es=None):
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
        self.tikz_vertex = '\n'.join(["\t"+rf"\node[style={vertex_style}] ({self.vertex_names[x]}) at ({self.vertex_position[x][0]},{self.vertex_position[x][1]}) {{{x+1}}};" for x in range(self.num_vertices)])
    
    def create_edges(self):
        edge_style = self.edge_style[0]
        self.tikz_edges = '\n'.join([f"\t\draw[style={edge_style}, bend left={l}] ({x}) to ({y});" if r==0  else f"\t\draw[style={edge_style}, bend right={r}] ({x}) to ({y});" for (x,y,l,r) in self.edge_relations])
    
    def create_tikzpicture(self):
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
    
    def save_tikzpicture_to_file(self, file_name='default.tikzpicture'):
        # Open a file in write mode
        print(f"Using {file_name} for writing into tikzpicture?[y/n]")
        x = input()
        if x=="Y" or x=='y':
            with open(file_name, "w") as file:
                file.write(self.create_tikzpicture())
        else:
            print('File writing is aborted!')
            


    def run_pdflatex(self):
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
        if x=='Y' or x =='y':
            for x in glob.glob("temp.*"): 
                os.remove(x)
        else:
            print(f"{files} are not deleted.")



    def __str__(self):
        
        self.tex_output= rf'''
\documentclass[tikz]{{standalone}}
\usepackage{{tikz}}

\begin{{document}}

{self.create_tikzpicture()}

\end{{document}}
            '''

        return self.tex_output
       

def main():
    #edge relation : ('starting vertex', 'ending vertec', left bend, right bend)
    g = Graph(8, [f"q{x}" for x in range(1,9)], [(0,0),(0,2),(2,4),(4,2),(4,0),(2,-2),(2,-4),(6,4)], [('q1','q2',0,0), ('q2','q3',0,0),('q3','q4',0,0),('q4','q5',0,0),('q5','q6',0,0),('q6','q7',0,0),('q4','q8',0,0),('q8','q7',15,0)])
    g.save_tikzpicture_to_file()
    g.run_pdflatex()
    
if __name__ == '__main__':
    main()