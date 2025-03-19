from fenics import *
import gmsh
import meshio

def calculate_fos(step_file, E, nu, yield_strength, left_wall_tag, right_wall_tag, traction_force):
    
    """
    Calculate the Factor of Safety (FOS) for a given STEP file and material properties.

    Parameters:
        step_file (str): Path to the STEP file.
        E (float): Young's modulus (Pa).
        nu (float): Poisson's ratio.
        yield_stress (float): Yield stress of the material (Pa).
        left_wall_tag (int): Physical tag for the left wall boundary.
        right_wall_tag (int): Physical tag for the right wall boundary.
        traction_force (tuple): Traction force vector (e.g., (1e6, 0.0, 0.0) for 1 MPa in x-direction).

    Returns:
        float: Factor of Safety (FOS).
    """

    # Step 1: GMSH Mesh Generation
    msh_file = "mesh.msh"
    xdmf_file_mesh = "mesh.xdmf"
    xdmf_file_surface_tags = "surface_tags.xdmf"

    # Initialize GMSH
    gmsh.initialize()
    gmsh.merge(step_file)

    # Physical Tag for Volume (assuming only 1 volume)
    gmsh.model.addPhysicalGroup(3, [1], tag=1)

    # Physical Tags for Surfaces
    surfaces = gmsh.model.occ.getEntities(dim=2)
    for surface in surfaces:
        gmsh.model.addPhysicalGroup(surface[0], [surface[1]])

    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)  # 3D mesh generation
    gmsh.write(msh_file)
    gmsh.finalize()

    
    # Utility function to extract specific cell types 
    def create_mesh(mesh, cell_type, prune_z=False):
        cells = mesh.get_cells_type(cell_type)
        cell_data = mesh.get_cell_data("gmsh:physical", cell_type)
        points = mesh.points[:, :2] if prune_z else mesh.points
        out_mesh = meshio.Mesh(points=points, cells={cell_type: cells}, cell_data={"name_to_read": [cell_data]})
        return out_mesh
    
    # Read the .msh file using meshio
    msh = meshio.read(msh_file)

    # Write the volumetric mesh (tetrahedrons) to mesh.xdmf
    tetra_mesh = create_mesh(msh, "tetra")
    meshio.write(xdmf_file_mesh, tetra_mesh)

    # Write the surface tags (triangles) to surface_tags.xdmf
    triangle_mesh = create_mesh(msh, "triangle")
    meshio.write(xdmf_file_surface_tags, triangle_mesh)

    # Step 2: FEniCS Simulation
    
    # Load the mesh
    mesh = Mesh()
    with XDMFFile(xdmf_file_mesh) as infile:
        infile.read(mesh)

    # Load the surface tags
    mvc = MeshValueCollection("size_t", mesh, 2)
    with XDMFFile(xdmf_file_surface_tags) as infile:
        infile.read(mvc, "name_to_read")
    mf = cpp.mesh.MeshFunctionSizet(mesh, mvc)

    # Define function space for displacement
    V = VectorFunctionSpace(mesh, "CG", 2)
    W = FunctionSpace(mesh, "CG", 2)

    # Define boundary conditions
    bc_left = DirichletBC(V, Constant((0.0, 0.0, 0.0)), mf, left_wall_tag)

    # Define material properties
    mu = E / (2.0 * (1.0 + nu))  # Shear modulus
    lmbda = E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))  # First Lamé parameter

    # Define strain and stress
    def epsilon(u):
        return 0.5 * (grad(u) + grad(u).T)

    def sigma(u):
        return 2.0 * mu * epsilon(u) + lmbda * tr(epsilon(u)) * Identity(3)

    # Define variational problem
    u = TrialFunction(V)
    v = TestFunction(V)
    f = Constant((0.0, 0.0, 0.0))  # Body force (assumed zero)

    # Weak form
    a = inner(sigma(u), epsilon(v)) * dx
    ds = Measure("ds", domain=mesh, subdomain_data=mf)
    L = dot(f, v) * dx + dot(Constant(traction_force), v) * ds(right_wall_tag)

    # Solve the problem
    u = Function(V)
    solve(a == L, u, bc_left)

    # Compute von Mises stress
    s = sigma(u) - (1.0 / 3) * tr(sigma(u)) * Identity(3)
    von_Mises = project(sqrt(3.0 / 2.0 * inner(s, s)), W, solver_type="cg")

    # Compute maximum von Mises stress
    max_stress = von_Mises.vector().max()

    # Compute Factor of Safety (FOS)
    FOS =  yield_strength/max_stress

    return FOS

# Input parameters
step_file = "**ADD FILE PATH HERE**"
E = 210e9  # Young's modulus (Pa) for steel
nu = 0.3   # Poisson's ratio
yield_strength = 200e6  # Yield stress for steel (Pa)
left_wall_tag = **ADD SURFACE TAG NUMBER HERE**  # Physical tag for the left wall
right_wall_tag = ** ADD SURFACE TAG NUMBER HERE**  # Physical tag for the right wall
traction_force = (10e6, 0.0, 0.0)  # Traction force in x-direction (1 MPa)

# Calculate FOS
FOS = calculate_fos(step_file, E, nu, yield_strength, left_wall_tag, right_wall_tag, traction_force)
print(f"Factor of Safety (FOS): {FOS}")
