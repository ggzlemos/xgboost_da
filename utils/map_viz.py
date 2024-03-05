import os
import uuid
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import pyplot as plt

def plot(longi: np.ndarray, lat: np.ndarray, data: np.ndarray, title: np.ndarray,
          x:tuple =None, y:tuple=None,
         figsize:tuple=(10,8.5), save_dir:str=None) -> None:
    
    """Generates a .png file with the variable values, adding the political division to the map
    
    Keywords arguments:
    longi -- longitue values
    lat -- latitude values
    data -- variable values
    title -- map title
    x -- custom longitude tuple
    y -- custom latitude tuple
    save_dir -- path to save the image
    """

    fig = plt.figure(figsize=figsize)

    ax=plt.axes(projection=ccrs.PlateCarree())

    cs=ax.contourf(longi.T, lat.T, data.T,
                transform = ccrs.PlateCarree(),cmap='jet',extend='both')

    ax.coastlines()
    states = cfeature.NaturalEarthFeature(
                category='cultural',
                name='admin_0_boundary_lines_land', #admin_1_states_provinces - admin_0_boundary_lines_land
                scale='10m',
                facecolor='none',
                edgecolor='black')

    cbar = plt.colorbar(cs,shrink=0.5,orientation='vertical',
                        label='Temperatura 2M')
    ax.add_feature(states, linewidth=2, edgecolor="black")
    ax.add_feature(cfeature.LAND)

    if x and y:
        ax.set_xlim(x)
        ax.set_ylim(y)
    else:
        ax.set_xlim((longi.min(), longi.max()))
        ax.set_ylim((lat.min(), lat.max()))
    ax.set_ylim((lat.min(), lat.max()))
    ax.coastlines()
    ax.set_title(title)

    if save_dir:
        plt.savefig(f'{save_dir}/{str(uuid.uuid4())}')
    else:
        plt.savefig(f'{os.getcwd()}/{str(uuid.uuid4())}')