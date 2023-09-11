#!/usr/bin/python3
from flask import Flask, abort, redirect, request
import flask_limiter
from skyfield.api import EarthSatellite
from skyfield.api import load, wgs84
import numpy as np
import requests
from sqlalchemy import desc
from flask_limiter.util import get_remote_address
from core import app, models, limiter


#Error handling
@app.errorhandler(404)
def page_not_found(e):
    return 'Error 404: Page not found<br />Check your spelling to ensure you are accessing the correct endpoint.', 404
@app.errorhandler(400)
def missing_parameter(e):
    return 'Error 400: Missing parameter<br />Check your request and try again.', 400
@app.errorhandler(429)
def ratelimit_handler(e):
  return "Error 429: You have exceeded your rate limit:<br />" + e.description, 429
@app.errorhandler(500)
def internal_server_error(e):
    return "Error 500: Internal server error:<br />" + e.description, 500

#Redirects user to the Center for the Protection of Dark and Quiet Sky homepage
@app.route('/')
@app.route('/index')
@limiter.limit("1 per second", key_func=lambda:get_forwarded_address(request))
def root():
    return redirect('https://cps.iau.org/')

@app.route('/health')
@limiter.exempt
def health():
    return {'message': 'Healthy'}


@app.route('/ephemeris/name/')
@limiter.limit("1 per second", key_func=lambda:get_forwarded_address(request))
def get_ephemeris_by_name():
    '''
    Returns the Right Ascension and Declination relative to the observer's coordinates
    for the given satellite's Two Line Element Data Set at inputted Julian Date.

    **Please note, for the most accurate results, an inputted Julian Date close to the TLE epoch is necessary.

    Parameters
    ---------
    name: 'str'
        CelesTrak name of object
    latitude: 'float'
        The observers latitude coordinate (positive value represents north, negative value represents south)
    longitude: 'float'
        The observers longitude coordinate (positive value represents east, negatie value represents west)
    elevation: 'float'
        Elevation in meters
    julian_date: 'float'
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.

    Returns
    -------
    Name: 'str'
        The name of the query object
    JulianDate: 'float' or list of 'float'
        UT1 Universal Time Julian Date. 
    Right Ascension: 'float'
        The right ascension of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,360)
    Declination: 'float'
        The declination of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [-90,90]
    Altitude: 'float'
        The altitude of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,90]
    Azimuth: 'float'
        The azimuth of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,360)
    Range: 'float'
        Range to object in km
    '''

    
    name = request.args.get('name')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    elevation = request.args.get('elevation')
    julian_date = request.args.get('julian_date')

    #check for mandatory parameters
    if [x for x in (name, latitude, longitude, elevation, julian_date) if x is None]:
        abort(400) 
    
    tleLine1, tleLine2, date_collected = getTLE(name)

    #Cast the latitude, longitude, and jd to floats (request parses as a string)
    lat = float(latitude)
    lon = float(longitude)
    ele = float(elevation)
    
    # Converting string to list
    jul = str(julian_date).replace("%20", ' ').strip('][').split(', ')
   
    # Converting list elements to float
    jd = [float(i) for i in jul]
   
    # return {'jd':jd , "TLELine1":tleLine1, "TLELine2":tleLine2 } 
    # propagation and create output
    resultList = []
    for d in jd:
        [ra,dec,alt,az,r] = propagateSatellite(tleLine1,tleLine2,lat,lon,ele,d)
        resultList.append(jsonOutput(name,d,ra,dec,alt,az,r,date_collected)) 
    return resultList


@app.route('/ephemeris/namejdstep/')
@limiter.limit("1 per second", key_func=lambda:get_forwarded_address(request))
def get_ephemeris_by_name_jdstep():
    '''
    Returns the Right Ascension and Declination relative to the observer's coordinates
    for the given satellite's Two Line Element Data Set at inputted Julian Date.

    **Please note, for the most accurate results, an inputted Julian Date close to the TLE epoch is necessary.

    Parameters
    ---------
    name: 'str'
        CelesTrak name of object
    latitude: 'float'
        The observers latitude coordinate (positive value represents north, negative value represents south)
    longitude: 'float'
        The observers longitude coordinate (positive value represents east, negatie value represents west)
    elevation: 'float'
        Elevation in meters
    startjd: 'float'
        UT1 Universal Time Julian Date to start ephmeris calculation.
    stopjd: 'float'
        UT1 Universal Time Julian Date to stop ephmeris calculation.
    stepjd: 'float'
        UT1 Universal Time Julian Date timestep.

    Returns
    -------
    Name: 'str'
        The name of the query object
    JulianDate: 'float' or list of 'float'
        UT1 Universal Time Julian Date. 
    Right Ascension: 'float'
        The right ascension of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,360)
    Declination: 'float'
        The declination of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [-90,90]
    Altitude: 'float'
        The altitude of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,90]
    Azimuth: 'float'
        The azimuth of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,360)
    Range: 'float'
        Range to object in km
    '''
    name = request.args.get('name')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    elevation = request.args.get('elevation')
    startjd = request.args.get('startjd')
    stopjd = request.args.get('stopjd')
    stepjd = request.args.get('stepjd')

    #check for mandatory parameters
    if [x for x in (name, latitude, longitude, elevation, startjd, stopjd, stepjd) if x is None]:
        abort(400) 

    tleLine1, tleLine2, date_collected = getTLE(name)

    #Cast the latitude, longitude, and jd to floats (request parses as a string)
    lat = float(latitude)
    lon = float(longitude)
    ele = float(elevation)
    
    jd0 = float(startjd)
    jd1 = float(stopjd) 
    jds = float(stepjd)

    #return {'jd0':jd0,'jd1':jd1,'jds':jds}   
  
    jd = my_arange(jd0,jd1,jds)
    #jd = np.arange(jd0,jd1,jds)
    #jd = [2460000.5]
    #return {'jd':jd[3]}

    resultList = []
    for d in jd:
        [ra,dec,alt,az,r] = propagateSatellite(tleLine1,tleLine2,lat,lon,ele,d)
        resultList.append(jsonOutput(name,d,ra,dec,alt,az,r,date_collected))
    return resultList


@app.route('/ephemeris/tle/')
@limiter.limit("1 per second", key_func=lambda:get_forwarded_address(request))
def read_tle_string():
    '''
    Returns the Right Ascension and Declination relative to the observer's coordinates
    for the given satellite's Two Line Element Data Set at inputted Julian Date.

    **Please note, for the most accurate results, an inputted Julian Date close to the TLE epoch is necessary.

    Parameters
    ---------
    tle: 'str'
        The Two Line Element set
    latitude: 'float'
        The observers latitude coordinate (positive value represents north, negative value represents south)
    longitude: 'float'
        The observers longitude coordinate (positive value represents east, negatie value represents west)
    julian_date: 'float'
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    flags: 'str'
        Optional flags to be passed in. All flags begin with &, followed by the command, and then the value. Currently, the only flags supported are:
        &jpl: 'str'
            If 'true', will return JPL ephemeris response. If 'false', will return Skyfield ephemeris. Default is 'false'
            This assumes that the TLE uses the ASCII representation for newline, which is '%0A'
        &elevation: 'float'
            The elevation of the observer in meters. Default is 0

    Returns
    -------
    Right Ascension: 'float'
        The right ascension of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,360)
    Declination: 'float'
        The declination of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [-90,90]
    Altitude: 'float'
        The altitude of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,90]
    Azimuth: 'float'
        The azimuth of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,360)
    '''

    tle = request.args.get('tle')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    julian_date = request.args.get('julian_date')
    flags = request.args.get('flags')

    #check for mandatory parameters
    if [x for x in (tle, latitude, longitude, julian_date) if x is None]:
        abort(400) 

    #Get rid of ASCII representation for space
    tle = tle.replace("%20", ' ')
    #Retrieve the two lines
    u,w = tle[:69], tle[70:]

    #Cast the latitude, longitude, and jd to floats (request parses as a string)
    lat = float(latitude)
    lon = float(longitude)
    jd = float(julian_date)

    #Parse flags
    jpl = False
    elevation = 0
    if flags is not None:
        flags = flags.replace("%20", '')
        flag_list = flags.split('&')
        for flag in flag_list:
            if flag[:3] == 'jpl':
                if flag[4:] == 'true': jpl = True
            elif flag[:9] == 'elevation':
                elevation = float(flag[10:])

    #If JPL flag is true, use JPL ephemeris
    if jpl:
        elevation_km = elevation/1000
        return requests.get(f'https://ssd.jpl.nasa.gov/api/horizons.api/?format=json&COMMAND=\'TLE\'&TLE={tle}\
            &MAKE_EPHEM=\'YES\'&TLIST=\'{jd}\'&EPHEM_TYPE=\'OBSERVER\'&CENTER=\'coord\'\
            &SITE_COORD=\'{lon},{lat},{elevation_km}\'&COORD_TYPE=\'GEODETIC\'&ANG_FORMAT=\'DEG\'').json()

    #This is the skyfield implementation
    ts = load.timescale()
    satellite = EarthSatellite(u,w,ts = ts)

    #Get current position and find topocentric ra and dec
    currPos = wgs84.latlon(lat, lon, elevation)
    # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
    if jd == 0: t = ts.ut1_jd(satellite.model.jdsatepoch)
    else: t = ts.ut1_jd(jd)

    difference = satellite - currPos
    topocentric = difference.at(t)

    ra, dec, distance = topocentric.radec()
    alt, az, distance = topocentric.altaz()


    return {
        "RIGHT_ASCENSION-DEG": np.round(ra._degrees,11),
        "DECLINATION-DEG": np.round(dec.degrees,11),
        "ALTITUDE-DEG": np.round(alt.degrees,11),
        "AZIMUTH-DEG": np.round(az.degrees,11),
    }


@app.route('/ephemeris/tle_file/')
@limiter.limit("1 per second", key_func=lambda:get_forwarded_address(request))
def read_tle_from_file():
    '''
    Returns dictionary of relative Right Ascension and Declination for all
    epoch times in Two Line Element data set text file

    ***This function is not complete. Will need a file upload of some sort to properly
    parse the data. This is a future project.***

    Parameters
    ---------
    file_path: 'file_path'
        The Two Line Element text file. This is the relative path

    Returns
    -------
    Dictionary of values
    '''
    file_path = request.args.get('file_path')

    #check for mandatory parameters
    if file_path is None:
        abort(400) 

    to_return = []
    f = open(file_path)
    words = f.read()
    single_lines = words.split('\n')
    lat_lon = single_lines[0]
    for i in range(1, len(single_lines)-1, 2):
        u = single_lines[i]
        w = single_lines[i+1]
        TLE = f'{u} {w}, {lat_lon}'
        to_return.append(read_tle_string(TLE))

    return to_return


@app.route('/ephemeris/pos/')
@limiter.limit("1 per second", key_func=lambda:get_forwarded_address(request))
def get_ephemeris():
    '''
    Returns the geocentric Right Ascension and Declination of the orbiting 
    mass given the geocentric position vector

    Parameters
    ---------
    x: 'float'
        The x position of the orbiting mass in km
    y: 'float'
        The y position of the orbiting mass in km
    z: 'float'
        The z position of the orbiting mass in km
        

    Returns
    -------
    Right Ascension: 'float'
        The geocentric right ascension of the satellite in degrees
    Declination: 'float'
        The geocentric declination of the satellite in degrees
    '''

    pos_str = request.args.get('pos_str')

    #check for mandatory parameters
    if pos_str is None:
        abort(400) 

    standardized_pos = pos_str.replace("%20", '')
    x, y, z = standardized_pos.split(',')
    position = np.array([float(x), float(y), float(z)])
    ra, dec = icrf2radec(position)

    return {
        'Right Ascension': ra,
        'Declination': dec
    }


### HELPER FUNCTIONS NOT EXPOSED TO API


def getTLE(targetName):
    """
    Query Two Line Element (orbital element) API and return TLE lines for propagation
    
    Paremeters:
    ------------
    targetName: 'str'
        Name of satellite as displayed in TLE file
    tleapi: 'str'
        URL of TLE API
        
        
    Returns:
    --------
    tleLine1: 'str'
        TLE line 1
    tleLine2: 'str'
        TLE line 2
    """

    # uncomment if json output is required
    #tleapiResult=requests.get(f'{tleapi}{targetName}&FORMAT=JSON').json()	    

    #use the supplemental TLE if it is the most recently collected one, otherwise use the general one
    tle_sup = models.TLE.query.filter_by(is_supplemental='true').join(models.Satellite, models.TLE.sat_id == models.Satellite.id)\
                        .filter_by(sat_name=targetName).order_by(desc('date_collected')).first()
    

    
    tle_gp = models.TLE.query.filter_by(is_supplemental='false').join(models.Satellite, models.TLE.sat_id == models.Satellite.id)\
                        .filter_by(sat_name=targetName).order_by(desc('date_collected')).first()
    
    tle = None
    if(tle_sup is None and tle_gp is None):
        abort(500)
    elif(tle_sup is None and tle_gp is not None):
        tle = tle_gp
    else:
        tle = tle_sup if tle_sup.date_collected > tle_gp.date_collected else tle_gp
        

    #Retrieve the two lines
    tleLine1 = tle.tle_line1
    tleLine2 = tle.tle_line2

    return tleLine1, tleLine2, tle.date_collected


def propagateSatellite(tleLine1,tleLine2,lat,lon,elevation,jd):
    """Use Skyfield (https://rhodesmill.org/skyfield/earth-satellites.html) 
     to propagate satellite and observer states.
     
     Parameters
    ---------
    tleLine1: 'str'
        TLE line 1
    tleLine2: 'str'
         TLE line 2
    lat: 'float'
        The observer WGS84 latitude in degrees
    lon: 'float'
        The observers WGS84 longitude in degrees (positive value represents east, negatie value represents west)
    elevation: 'float'
        The observer elevation above WGS84 ellipsoid in meters
    julian_date: 'float'
        UT1 Universal Time Julian Date. An input of 0 will use the TLE epoch.
    tleapi: 'str'
        base API for query

    Returns
    -------
    Right Ascension: 'float'
        The right ascension of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,360)
    Declination: 'float'
        The declination of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [-90,90]
    Altitude: 'float'
        The altitude of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,90]
    Azimuth: 'float'
        The azimuth of the satellite relative to observer coordinates in ICRS reference frame in degrees. Range of response is [0,360)
    distance: 'float'
        Range from observer to object in km
    """
    
    #This is the skyfield implementation
    ts = load.timescale()
    satellite = EarthSatellite(tleLine1,tleLine2,ts = ts)

    #Get current position and find topocentric ra and dec
    currPos = wgs84.latlon(lat, lon, elevation)
    # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
    if jd == 0: t = ts.ut1_jd(satellite.model.jdsatepoch)
    else: t = ts.ut1_jd(jd)

    difference = satellite - currPos
    topocentric = difference.at(t)
    ra, dec, distance = topocentric.radec()
    alt, az, distance = topocentric.altaz()
    return (ra,dec,alt,az,distance)


def my_arange(a, b, dr, decimals=11):
    """
    Better arange function that compensates for round-off errors.
    
    Parameters:
    -----------
    a: 'float'
        first element in range 
    b: 'float'
        last element in range
    dr: 'float'
        range increment
    decimals: 'integer'
        post comma digits to be rounded to
        
    Returns:
    --------
    res: 'numpy array of floats'
        array of numbers between a and b with dr increments
    """
    
    res = [a]
    k = 1
    while res[-1] < b:
        tmp = np.round(a + k*dr,decimals)
        if tmp > b:
            break   
        res.append(tmp)
        k+=1

    return np.asarray(res) 


def jsonOutput(name,time,ra,dec,alt,az,r,date,precisionAngles=11,precisionDate=12,precisionRange=12):
    """
    Convert API output to JSON format
    
    Parameters:
    -----------
    name: 'str'
        Name of the target satellite
    time: 'float'
        Julian Date
    ra: Skyfield object / 'float'
        Right Ascension 
    dec: Skyfield object / 'float'
        Declination
    alt: Skyfield object / 'float'
        Altitude
    az: Skyfield object / 'float'
        Azimuth
    r: Skyfield object / 'float'
        Range to target
    precisionAngles: 'integer'
        number of digits for angles to be rounded to (default: micro arcsec)
    precisionDate: 'integer'
        number of digits for Julian Date to be rounded to (default: micro sec)
    precisionRange: 'integer'
        number of digits for angles to be rounded to (default: nano meters)   
        
    Returns:
    --------
    output: 'dictionary'
        JSON dictionary of the above quantities
    
    """
    
    
    #looking up the numpy round function once instead of multiple times makes things a little faster
    myRound = np.round
    
    
    output= {"NAME": name,
            "JULIAN_DATE": myRound(time,precisionDate),
            "RIGHT_ASCENSION-DEG": myRound(ra._degrees,precisionAngles),
            "DECLINATION-DEG": myRound(dec.degrees,precisionAngles),
            "ALTITUDE-DEG": myRound(alt.degrees,precisionAngles),
            "AZIMUTH-DEG": myRound(az.degrees,precisionAngles),
            "RANGE-KM": myRound(r.km,precisionRange),
            "TLE-DATE": date.strftime("%Y-%m-%d %H:%M:%S")} 
    
    return output  


def icrf2radec(pos, deg=True):
    """
    Convert ICRF xyz to Right Ascension and Declination.
    Geometric states on unit sphere, no light travel time/aberration correction.
    
    Parameters:
    -----------
    pos ... real, dim=[n, 3], 3D vector of unit length (ICRF)
    deg ... True: angles in degrees, False: angles in radians
    Returns:
    --------
    ra ... Right Ascension [deg]
    dec ... Declination [deg]
    """
    norm=np.linalg.norm
    array=np.array
    arctan2=np.arctan2
    arcsin=np.arcsin
    rad2deg=np.rad2deg
    modulo=np.mod
    pix2=2.*np.pi
    
    if(pos.ndim>1):
        r=norm(pos,axis=1)
        xu=pos[:,0]/r
        yu=pos[:,1]/r
        zu=pos[:,2]/r
    else:
        r=norm(pos)
        xu=pos[0]/r
        yu=pos[1]/r
        zu=pos[2]/r
    
    phi=arctan2(yu,xu)
    delta=arcsin(zu)
    
    if(deg):
        ra = modulo(rad2deg(phi)+360,360)
        dec = rad2deg(delta)
    else:
        ra = modulo(phi+pix2,pix2)
        dec = delta
    
    return ra, dec

def get_forwarded_address(request):
    forwarded_header = request.headers.get("X-Forwarded-For")
    if forwarded_header:                                  
        return request.headers.getlist("X-Forwarded-For")[0]
    return get_remote_address