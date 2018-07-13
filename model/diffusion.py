def concentration_time(time):
    """
    Function that calculates the change in concentration in the blood vessel as a function of time (according to Syed et co. observations)

    Args:
        time(float): time in hours
    Returns:
        The concentration
    """
    #return 1.0
    return 0.7521*np.exp(-1.877*time) + 0.2479*np.exp(-0.1353*time)

def neumann_flow(un, flow_location, i, dt, nu):
    #contribution due to neumann flow_location.
    return flow_location*nu

def set_dirichlet(source, source_location, i, dt):
    #contribution
    return bd.concentration_time(i*dt/3600.)*source*source_location

def diffusion(u, un, ijk, diffusion_location, vis, dt, dx, dy, dz):
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
     u[ijk,:,:] += diffusion_location[ijk,:,:]*( vis*dt*diffusion_locationf[ijk+1,:,:]*( un[ijk+1,:,:]-un[ijk,:,:] ) + vis*dt*diffusion_locationf[ijk-1,:,:]*( un[ijk-1,:,:]-un[ijk,:,:] ))/(dx**2)

     u[:,ijk,:] += diffusion_locationf[:,ijk,:]*( vis*dt*diffusion_locationf[:,ijk+1,:]*( un[:,ijk+1,:]-un[:,ijk,:] ) + vis*dt*diffusion_locationf[:,ijk-1,:]*( un[:,ijk-1,:]-un[:,ijk,:] ))/(dy**2)

     u[:,:,ijk] += diffusion_locationf[:,:,ijk]*( vis*dt*diffusion_locationf[:,:,ijk+1]*( un[:,:,ijk+1]-un[:,:,ijk] ) + vis*dt*diffusion_locationf[:,:,ijk-1]*( un[:,:,ijk-1]-un[:,:,ijk] ))/(dz**2)

def dirichlet_source_term(u, source, source_location, i, dt, load):
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
    u += -u*source_location + mod.set_dirichlet(source, source_location, i, dt)

def neumann_source_term(u, un, flow_location, i, dt, nu, dx):
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
    #u += dm.neumann_flow(un, flow_location, i, dt, nu)
