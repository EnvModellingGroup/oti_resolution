from thetis import *
import os.path
import argparse

def main():

    parser = argparse.ArgumentParser(
         prog="project_to_DG",
         description="""Project a h5 file to CG"""
    )
    parser.add_argument(
            'input_file',
            metavar='input_file',
            help='The h5 file'
            )
    parser.add_argument(
            'output_file',
            metavar='output_file',
            help='The output h5 file'
            )
    parser.add_argument(
            'model_dir',
            metavar='model_dir',
            help='Model_dir inc output/hdf5 - we get the mesh from the first Elevation file'
            )

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    model_dir = args.model_dir
    e_file = os.path.join(model_dir,"Elevation2d_00000.h5")
    with CheckpointFile(e_file, "r") as f:
        mesh2d = f.load_mesh()

    
    with CheckpointFile(input_file, "r") as f:
        bmesh2d = f.load_mesh()
        function = f.load_function(bmesh2d,"bathymetry")
        # create a p1-cg space for vorticity
        p1dg = FunctionSpace(mesh2d, 'DG', 1)
        funcdg = project(function, p1dg)
        chk = CheckpointFile(output_file, 'w')
        chk.save_mesh(mesh2d)
        chk.save_function(funcdg, name='bathymetry')
        File('bathydg.pvd').write(funcdg)  


if __name__ == "__main__":
    main()
