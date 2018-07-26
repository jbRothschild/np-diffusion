import numpy as np

def count(data_array, concentration=1, dx=2, dy=2, dz=2):
    #gives number of nanoparticles in
    return sum(data_array)*concentration*dx*dy*dz

def total_volume_nm(num_particles, size=50.):
    #calculates the total volume of gold in nm^3
    return num_particles*(4./3.)*np.pi*size**3

def total_weight_nm2mg(total_volume):
    #converts the volume in nm*3 to weight in mg
    return total_volume*19.282*10**(-18)

def analyze_timepoint(folder, data_file):
    num_np = count(folder+data_file)
    tot_vol = total_volume_nm(num_np)
    tot_weight = total_weight_nm2mg(tot_vol)
    print num_np
    print tot_vol
    print tot_weight
    return num_np, tot_vol, tot_weight

def create_results():
    return 0

if __name__ == "__main__":
    analyze_timepoint("../data/sim_holes_diffusion_20.0","/diff_1800sec.npy")
