from tvtk.api import tvtk, write_data
import numpy as np

def save_to_vtk_2d(topview_array,saveDir, filename, 
                   dx = 1, dy = 1,
                   stride_x = 1, stride_y = 1,
                   factor_z = 1, 
                   dataname = "Data"):
    """
    Save a given array to vtk
    """
    
    print("Saving VTK file")
    topview_array=topview_array.transpose((1,2,0))[::stride_x,::stride_y,:][:,:,::1]

    grid = tvtk.ImageData(spacing=(dx,dy,dz*factor_z),origin=(0, 0, 0), dimensions=topview_array.shape)
    grid.point_data.scalars = (np.abs(topview_array)*np.abs(topview_array)).ravel(order='F')
    grid.point_data.scalars.name = dataname
    
    # Writes legacy ".vtk" format if filename ends with "vtk", otherwise
    # this will write data using the newer xml-based format.
    write_data(grid, saveDir + '/'+str(filename)+".vtk")
    print("VTK file saved")
 