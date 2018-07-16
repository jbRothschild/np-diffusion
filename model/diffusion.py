def diffusion(u, un, ijk, diffusion_location, vis, dt, dx, dy, dz, mod):
     """
     Function that calculates the diffusion from solution un to solution u in the diffusion_location. Time in between is dt, with diffusion coeffecient vis. This iteration of this diffusion function assumes that anywhere that is not a diffusion location has a reflective boundary (hence the *diffusion_locationf[:,ijk+-1,:]=0 for non diffusion spots.)

     Args:
         u(array,3): solution
         un(array,3): Previous time step solution
         ijk(array,1): array of length the size of the total solution array
         diffusion_location(array,3): The domain over which diffusion happens
         vis(float): diffusion coefficient
         dt(int), dx(int), dy(int), dz(int): spacetime intervals
     Returns:
         None
     """
     u[ijk,:,:] += diffusion_location[ijk,:,:]*( vis*dt*diffusion_location[ijk+1,:,:]*( un[ijk+1,:,:]-un[ijk,:,:] ) + vis*dt*diffusion_location[ijk-1,:,:]*( un[ijk-1,:,:]-un[ijk,:,:] ))/(dx**2)

     u[:,ijk,:] += diffusion_location[:,ijk,:]*( vis*dt*diffusion_location[:,ijk+1,:]*( un[:,ijk+1,:]-un[:,ijk,:] ) + vis*dt*diffusion_location[:,ijk-1,:]*( un[:,ijk-1,:]-un[:,ijk,:] ))/(dy**2)

     u[:,:,ijk] += diffusion_location[:,:,ijk]*( vis*dt*diffusion_location[:,:,ijk+1]*( un[:,:,ijk+1]-un[:,:,ijk] ) + vis*dt*diffusion_location[:,:,ijk-1]*( un[:,:,ijk-1]-un[:,:,ijk] ))/(dz**2)

def dirichlet_source_term(u, source_location, i, dt, mod):
    """
    Function that fixes the source terms(after diffusion has happened)

    Args:
        u(array,3): solution
        source(array,3): value of source term (dirichlet)
        source_location(array,3): The location of the source terms
        i(int): time step #
        dt(int): spacetime intervals
    Returns:
        None
    if load == True:
        import data_model as mod
    else:
        import dustom_model as mod
    """
    #u += -u*source_location + mod.set_dirichlet(source_location, i, dt)

def neumann_source_term(u, un, flow_location, i, dt, nu, dx, mod):
    """
    Function that fixes the source terms(after diffusion has happened)

    Args:
        u(array,3): solution
        un(array,3): previous solution
        flow_location(array,3): The location of the flow terms
        i(int): time step #
        dt(int), dx(int): spacetime intervals
        nu(float): du/dx
    Returns:
        None
    """
    u += mod.neumann_flow(un, flow_location, i, dt, nu, dx)*dt
