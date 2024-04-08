from mayavi import mlab
from stl import mesh


def display_3d_model(file_path):                # funkcja do wyświetlenia geometrii z pliku .obj
    fig = mlab.figure(size=(800, 600))
    mesh = mlab.pipeline.open(file_path)
    mlab.pipeline.surface(mesh)
    mlab.show()



def stl_to_obj(stl_filename, obj_filename):     #funkcja do konwersji .stl na .obj
    
    stl_mesh = mesh.Mesh.from_file(stl_filename) # wczytanie pliku STL

    # Zapisanie danych jako pliku OBJ
    with open(obj_filename, 'w') as f:
        f.write("# OBJ file generated from STL\n")
        for i, vertex in enumerate(stl_mesh.vectors):
            f.write("v {:f} {:f} {:f}\n".format(*vertex[0]))
            f.write("v {:f} {:f} {:f}\n".format(*vertex[1]))
            f.write("v {:f} {:f} {:f}\n".format(*vertex[2]))
            f.write("f {:d} {:d} {:d}\n".format(i*3+1, i*3+2, i*3+3))


stl_to_obj('pretstl.stl', 'output_file.obj') # konwersja .stl na .obj     
file_path = 'output_file.obj' # wczytanie pliku .obj
display_3d_model(file_path) # wyświetlenie pliku .obj