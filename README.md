# tikXgenerator
A simple tool to automate tikz graphs. The program takes input from a file with extension .graph. The skeleton of the file is given below:


    n   // number of vertices
    1 2 3 4 5 6 7 8 .... // vertices name
    x,y //vertex postions
    x,y
    x,y
    x,y
    x,y
    x,y
    x,y
    x,y
    ...
    #
    v1,v2,l,r //edge relations with left and right bend
    v1,v2,l,r
    v1,v2,l,r
    ...
    #
    node_style [tikz node style] // node styling
    edge_style [tikz edge style] // edge styling

TODO: Need to add a string stripper.