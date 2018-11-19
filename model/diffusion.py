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

     #Periodic Boundary Conditions
     u[0,:,:] += diffusion_location[0,:,:]*( vis*dt*diffusion_location[1,:,:]*( un[1,:,:]-un[0,:,:] ) + vis*dt*diffusion_location[-1,::-1,::-1]*( un[-1,::-1,::-1]-un[0,:,:] ))/(dx**2)

     u[:,0,:] += diffusion_location[:,0,:]*( vis*dt*diffusion_location[:,1,:]*( un[:,1,:]-un[:,0,:] ) + vis*dt*diffusion_location[::-1,-1,::-1]*( un[::-1,-1,::-1]-un[:,0,:] ))/(dy**2)

     u[:,:,0] += diffusion_location[:,:,0]*( vis*dt*diffusion_location[:,:,1]*( un[:,:,1]-un[:,:,0] ) + vis*dt*diffusion_location[::-1,::-1,-1]*( un[::-1,::-1,-1]-un[:,:,0] ))/(dz**2)

     u[-1,:,:] += diffusion_location[-1,:,:]*( vis*dt*diffusion_location[-2,:,:]*( un[-2,:,:]-un[-1,:,:] ) + vis*dt*diffusion_location[0,::-1,::-1]*( un[0,::-1,::-1]-un[-1,:,:] ))/(dx**2)

     u[:,-1,:] += diffusion_location[:,-1,:]*( vis*dt*diffusion_location[:,-2,:]*( un[:,-2,:]-un[:,-1,:] ) + vis*dt*diffusion_location[::-1,0,::-1]*( un[::-1,0,::-1]-un[:,-1,:] ))/(dy**2)

     u[:,:,-1] += diffusion_location[:,:,-1]*( vis*dt*diffusion_location[:,:,-2]*( un[:,:,-2]-un[:,:,-1] ) + vis*dt*diffusion_location[::-1,::-1,0]*( un[::-1,::-1,0]-un[:,:,-1] ))/(dz**2)

def dirichlet_source_term(u, source_location, i, dt, mod):
    """
    Function that fixes the source terms(after diffusion has happened)

    Args:
        u(array,3): solution
        source_location(array,3): The location of the source terms
        i(int): time step #
        dt(int): spacetime intervals
        mod: the model we're using
    Returns:
        None
    """
    u += -u*source_location + mod.set_dirichlet(source_location, i, dt)

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
    
def neumann_source_term_mo(u, un, flow_location_mo, i, dt, nu, dx, mod):
    """
    Function that fixes the source terms(after diffusion has happened)

    Args:
        u(array,3): solution
        un(array,3): previous solution
        flow_location_mo(array,3): The location of the macrophage flow terms
        i(int): time step #
        dt(int), dx(int): spacetime intervals
        nu(float): du/dx
    Returns:
        None
    """
    u += mod.neumann_flow(un, flow_location_mo, i, dt, nu, dx)*dt    
