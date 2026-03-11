from ParticleAdvector import Advection
from FTLE import FTLE
import os
from datetime import datetime, timedelta, date

def CreateLCSField(file, lons, lats, ts, sep, dur, output, start):
    """
        Advects particles using ParticleAdvector.py, which creates an output file.
        Uses this output file to compute LCSs. 
    Args:
        lons    [list]      :   A list [lon1, lon2], where lon1 is bottom left corner of domain and lon2 is top right corner of domain. 
        lats    [list]      :   A list [lat1, lat2], where lat1 is bottom left corner of domain and lat2 is top right corner of domain.
        ts      [float]     :   Time step for integration, given in seconds
        sep     [int]       :   Initial separation between particles, given in meters.
        dur     [int]       :   Duration of integration, given in hours
        date    [str]       :   A string of the date, in format 'ymd', no spacings.
        member  [int]       :   Number of ensemble member, between 0-23.
        output  [str]       :   Name of output file. Particle positions are saved to output.nc, LCS are saved to output_LCS.nc
        at_time [int]       :   Which hour of the day LCSs are computed for
    """
    advector = Advection(file, lons, lats, ts, sep, dur, start)
    parts = advector.run()
    LCS = FTLE(parts, outfile=output, model_file=file, RLCS=True)

def Run(output, start, file, dur):
    """
        Runs the particle and LCS simulation
    Args:
        i       [int]   :   The ensemble member for which LCSs should be computed
        date    [str]   :   A string of the date, in format 'ymd', no spacings.
        at_time [int]   :   Which hour of the day LCSs are computed for
    """
    CreateLCSField(file, lons=[25, 40], lats=[67,84], ts=3600, sep=2500, dur=dur, output=output, start=start)

def CreateFTLEField(file, lons, lats, ts, sep, dur, ftle_output, start, particle_outfile=None, ensemble_member = None, RLCS=False, z=0, proj4=None):
    advector = Advection(file, lons, lats, ts, sep, dur, start, proj4=proj4)
    parts = advector.run(outfile=particle_outfile, ensemble_member=ensemble_member, z=z)
    ftle = FTLE(parts, outfile=ftle_output, model_file=file, RLCS=RLCS, proj4=proj4)


if __name__ == '__main__':
    file = 'https://thredds.met.no/thredds/dodsC/fou-hi/norkystv3_800m_m00_be'
    proj4 = '+proj=stere +lat_0=90 +lat_ts=60 +lon_0=70 +x_0=3369600 +y_0=1844800 +a=6378137 +b=6356752.3142 +units=m +no_defs +type=crs'
    output = 'FTLE_test_4h_400m_vmix'
    start = datetime(2025,12,1,0,0)
    lons = [4, 13]
    lats = [57, 59.4]
    ts = -1800
    sep = 400
    dur = 4
    #file = 'https://thredds.met.no/thredds/dodsC/barents25km_agg'
    #proj4 = '+proj=lcc +lat_0=77.5 +lon_0=-25 +lat_1=77.5 +lat_2=77.5 +no_defs +R=6.371e+06'
    #start = datetime(2020,12,1,0,0)
    #lons = [4.5,23]
    #lats = [67,69.9]
    CreateFTLEField(file, lons, lats, ts, sep, dur, output, start, proj4=proj4)
    