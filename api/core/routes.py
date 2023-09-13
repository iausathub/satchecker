#!/usr/bin/python3
from flask import Flask, abort, redirect, request
import flask_limiter
from skyfield.api import EarthSatellite
from skyfield.api import load, wgs84
import numpy as np
import requests
from sqlalchemy import desc
from flask_limiter.util import get_remote_address
from core import app, limiter
from core.database import models
from core.extensions import db


#Error handling
@app.errorhandler(404)
def page_not_found(e):
    return 'Error 404: Page not found<br />Check your spelling to ensure you are accessing the correct endpoint.', 404
@app.errorhandler(400)
def missing_parameter(e):
    return 'Error 400: Missing parameter or too many results to return<br />Check your request and try again.', 400
@app.errorhandler(429)
def ratelimit_handler(e):
  return "Error 429: You have exceeded your rate limit:<br />" + e.description, 429
@app.errorhandler(500)
def internal_server_error(e):
    return "Error 500: Internal server error:<br />" + e.description, 500

#Redirects user to the Center for the Protection of Dark and Quiet Sky homepage
@app.route('/')
@app.route('/index')
@limiter.limit("100 per second, 2000 per minute", key_func=lambda:get_forwarded_address(request))
def root():
    return redirect('https://cps.iau.org/')

@app.route('/health')
@limiter.exempt
def health():
    return {'message': 'Healthy'}


@app.route('/ephemeris/name/')
@limiter.limit("100 per second, 2000 per minute", key_func=lambda:get_forwarded_address(request))
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
    
    tleLine1, tleLine2, date_collected, name = get_TLE_by_name(name)

    #Cast the latitude, longitude, and jd to floats (request parses as a string)
    lat = float(latitude)
    lon = float(longitude)
    ele = float(elevation)
    
    # Converting string to list
    jul = str(julian_date).replace("%20", ' ').strip('][').split(', ')
   
    # Converting list elements to float
    jd = [float(i) for i in jul]

    if(len(jd)>1000):
        abort(400)
   
    # propagation and create output
    resultList = []
    for d in jd:
        #Right ascension RA (deg), Declination Dec (deg), dRA/dt*cos(Dec) (deg/day), dDec/dt (deg/day),
        # Altitude (deg), Azimuth (deg), dAlt/dt (deg/day), dAz/dt (deg/day), distance (km), range rate (km/s), phaseangle(deg), illuminated (T/F)   
        [ra, dec, dracosdec, ddec, alt, az,  
         r, dr, phaseangle, illuminated] = propagateSatellite(tleLine1,tleLine2,lat,lon,ele,d)
        
        resultList.append(jsonOutput(name, d, ra, dec, date_collected, 
                                    dracosdec, ddec,
                                    alt, az, 
                                    r, dr, phaseangle, illuminated)) 
    return resultList


@app.route('/ephemeris/namejdstep/')
@limiter.limit("100 per second, 2000 per minute", key_func=lambda:get_forwarded_address(request))
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

    tleLine1, tleLine2, date_collected, name = get_TLE_by_name(name)

    #Cast the latitude, longitude, and jd to floats (request parses as a string)
    lat = float(latitude)
    lon = float(longitude)
    ele = float(elevation)
    
    jd0 = float(startjd)
    jd1 = float(stopjd) 
    jds = float(stepjd)
  
    jd = my_arange(jd0,jd1,jds)

    if(len(jd)>1000):
        abort(400)

    resultList = []
    for d in jd:
        [ra, dec, dracosdec, ddec, alt, az, 
         r, dr, phaseangle, illuminated] = propagateSatellite(tleLine1,tleLine2,lat,lon,ele,d)
        resultList.append(jsonOutput(name, d, ra, dec, date_collected,
                                    dracosdec, ddec,
                                    alt, az, 
                                    r, dr, phaseangle, illuminated))
    return resultList

@app.route('/ephemeris/catalog_number/')
@limiter.limit("100 per second, 2000 per minute", key_func=lambda:get_forwarded_address(request))
def get_ephemeris_by_catalog_number():
    '''
    Returns the Right Ascension and Declination relative to the observer's coordinates
    for the given satellite's catalog number using the Two Line Element Data Set at inputted Julian Date.

    **Please note, for the most accurate results, an inputted Julian Date close to the TLE epoch is necessary.

    Parameters
    ---------
    catalog_number: 'str'
        Satellite Catalog Number of object
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

    
    catalog_number = request.args.get('catalog_number')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    elevation = request.args.get('elevation')
    julian_date = request.args.get('julian_date')

    #check for mandatory parameters
    if [x for x in (catalog_number, latitude, longitude, elevation, julian_date) if x is None]:
        abort(400) 
    
    tleLine1, tleLine2, date_collected, name = get_TLE_by_catalog_number(catalog_number)

    #Cast the latitude, longitude, and jd to floats (request parses as a string)
    lat = float(latitude)
    lon = float(longitude)
    ele = float(elevation)
    
    # Converting string to list
    jul = str(julian_date).replace("%20", ' ').strip('][').split(', ')
   
    # Converting list elements to float
    jd = [float(i) for i in jul]

    if(len(jd)>1000):
        abort(400)
   
    # propagation and create output
    resultList = []
    for d in jd:
        #Right ascension RA (deg), Declination Dec (deg), dRA/dt*cos(Dec) (deg/day), dDec/dt (deg/day),
        # Altitude (deg), Azimuth (deg), dAlt/dt (deg/day), dAz/dt (deg/day), distance (km), range rate (km/s), phaseangle(deg), illuminated (T/F)   
        [ra, dec, dracosdec, ddec, alt, az,  
         r, dr, phaseangle, illuminated] = propagateSatellite(tleLine1,tleLine2,lat,lon,ele,d)
        
        resultList.append(jsonOutput(name, d, ra, dec, date_collected, 
                                    dracosdec, ddec,
                                    alt, az, 
                                    r, dr, phaseangle, illuminated)) 
    return resultList

### HELPER FUNCTIONS NOT EXPOSED TO API ###
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

def get_TLE_by_name(targetName):
    """
    Query Two Line Element (orbital element) API and return TLE lines for propagation
    
    Paremeters:
    ------------
    targetName: 'str'
        Name of satellite as displayed in TLE file
     
    Returns:
    --------
    tleLine1: 'str'
        TLE line 1
    tleLine2: 'str'
        TLE line 2
    """

    #use the supplemental TLE if it is the most recently collected one, otherwise use the general one
    tle_sup = db.session.query(models.TLE, models.Satellite).filter_by(is_supplemental='true').join(models.Satellite, models.TLE.sat_id == models.Satellite.id)\
                        .filter_by(sat_name=targetName).order_by(desc('date_collected')).first()
    
    tle_gp = db.session.query(models.TLE, models.Satellite).filter_by(is_supplemental='false').join(models.Satellite, models.TLE.sat_id == models.Satellite.id)\
                        .filter_by(sat_name=targetName).order_by(desc('date_collected')).first()
    
    return return_TLE(tle_sup, tle_gp)

def get_TLE_by_catalog_number(targetNumber):
    """
    Query Two Line Element (orbital element) API and return TLE lines for propagation
    
    Paremeters:
    ------------
    targetNumber: 'str'
        Catalog number of satellite as displayed in TLE file   
        
    Returns:
    --------
    tleLine1: 'str'
        TLE line 1
    tleLine2: 'str'
        TLE line 2
    """

    #use the supplemental TLE if it is the most recently collected one, otherwise use the general one
    tle_sup = db.session.query(models.TLE, models.Satellite).filter_by(is_supplemental='true').join(models.Satellite, models.TLE.sat_id == models.Satellite.id)\
                        .filter_by(sat_number=targetNumber).order_by(desc('date_collected')).first()
    
    tle_gp = db.session.query(models.TLE, models.Satellite).filter_by(is_supplemental='false').join(models.Satellite, models.TLE.sat_id == models.Satellite.id)\
                        .filter_by(sat_number=targetNumber).order_by(desc('date_collected')).first()
    
    return return_TLE(tle_sup, tle_gp)


def return_TLE(tle_sup, tle_gp):
    tle = None
    satellite = None
    if(tle_sup is None and tle_gp is None):
        abort(500)
    elif(tle_sup is None and tle_gp is not None):
        tle = tle_gp[0]
        satellite = tle_gp[1]
    else:
        tle, satellite = (tle_sup[0], tle_sup[1]) if tle_sup.date_collected > tle_gp.date_collected else (tle_gp[0], tle_gp[1])        

    #Retrieve the two lines
    tleLine1 = tle.tle_line1
    tleLine2 = tle.tle_line2

    return tleLine1, tleLine2, tle.date_collected, satellite.sat_name

def propagateSatellite(tleLine1, tleLine2, lat, lon, elevation, jd, dtsec=1):
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
    topocentricn = topocentric.position.km/np.linalg.norm(topocentric.position.km)
    
    ra, dec, distance = topocentric.radec()
    alt, az, distance = topocentric.altaz()
    
    secperday = 86400
    dtday=dtsec/secperday
    tplusdt = ts.ut1_jd(jd+dtday)
    tminusdt = ts.ut1_jd(jd-dtday)

    dtx2 = 2*dtsec 

    sat = satellite.at(t).position.km

    satn = sat/np.linalg.norm(sat)
    satpdt = satellite.at(tplusdt).position.km
    satmdt = satellite.at(tminusdt).position.km
    vsat = (satpdt - satmdt)/dtx2
    
    sattop = difference.at(t).position.km
    sattopr = np.linalg.norm(sattop)
    sattopn = sattop/sattopr
    sattoppdt = difference.at(tplusdt).position.km
    sattopmdt = difference.at(tminusdt).position.km
    
    ratoppdt,dectoppdt = icrf2radec(sattoppdt)
    ratopmdt,dectopmdt = icrf2radec(sattopmdt)
    
    vsattop = (sattoppdt - sattopmdt)/dtx2
    
    ddistance = np.dot(vsattop,sattopn)
    rxy = np.dot(sattop[0:2],sattop[0:2])
    dra = (sattop[1]*vsattop[0]-sattop[0]*vsattop[1])/rxy
    ddec = vsattop[2]/np.sqrt(1-sattopn[2]*sattopn[2])
    dracosdec = dra*np.cos(dec.radians)

    dra = (ratoppdt - ratopmdt)/dtx2
    ddec = (dectoppdt - dectopmdt)/dtx2
    dracosdec = dra*np.cos(dec.radians)

    drav, ddecv = icrf2radec(vsattop/sattopr, unitVector=True)
    dracosdecv = drav*np.cos(dec.radians)
    
 
    eph = load('de430t.bsp')
    earth = eph['Earth']
    sun = eph['Sun']
 
    earthp = earth.at(ts.ut1_jd(jd)).position.km
    sunp = sun.at(ts.ut1_jd(jd)).position.km
    earthsun = sunp - earthp
    earthsunn = earthsun/np.linalg.norm(earthsun)
    satsun =  sat - earthsun
    satsunn = satsun/np.linalg.norm(satsun)
    phase_angle = np.rad2deg(np.arccos(np.dot(satsunn,topocentricn)))
    
    #Is the satellite in Earth's Shadow?
    r_parallel = np.dot(sat,earthsunn)*earthsunn
    r_tangential = sat-r_parallel

    illuminated = True

    if(np.linalg.norm(r_parallel)<0):
        #rearthkm
        if(np.linalg.norm(r_tangential)<6370):
            #print(np.linalg.norm(r_tangential),np.linalg.norm(r))
            #yes the satellite is in Earth's shadow, no need to continue (except for the moon of course)
            illuminated = False
    
    return (ra, dec, dracosdec, ddec, alt, az, 
            distance, ddistance, phase_angle, illuminated)


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

def tle2ICRFstate(tleLine1,tleLine2,jd):

    #This is the skyfield implementation
    ts = load.timescale()
    satellite = EarthSatellite(tleLine1,tleLine2,ts = ts)

    # Set time to satellite epoch if input jd is 0, otherwise time is inputted jd
    if jd == 0: t = ts.ut1_jd(satellite.model.jdsatepoch)
    else: t = ts.ut1_jd(jd)

    r =  satellite.at(t).position.km
    # print(satellite.at(t))
    v = satellite.at(t).velocity.km_per_s
    return np.concatenate(np.array([r,v]))

def jsonOutput(name,time,ra,dec,dateCollected,dracosdec,ddec, 
               alt, az, 
               #dalt, daz, 
               r, dr, phaseangle, illuminated, 
               precisionAngles=11,precisionDate=12,precisionRange=12):
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
            "DRA_COSDEC-DEG_PER_SEC":  myRound(dracosdec,precisionAngles),
            "DDEC-DEG_PER_SEC": myRound(ddec,precisionAngles),
            "ALTITUDE-DEG": myRound(alt.degrees,precisionAngles),
            "AZIMUTH-DEG": myRound(az.degrees,precisionAngles),
            "RANGE-KM": myRound(r.km,precisionRange),
            "RANGE_RATE-KM_PER_SEC": myRound(dr,precisionRange),
            "PHASE_ANGLE-DEG": myRound(phaseangle, precisionAngles),
            "ILLUMINATED": illuminated,
            "TLE-DATE": dateCollected.strftime("%Y-%m-%d %H:%M:%S")} 
    
    return output  


def icrf2radec(pos, unitVector=False, deg=True):
    """
    Convert ICRF xyz or xyz unit vector to Right Ascension and Declination.
    Geometric states on unit sphere, no light travel time/aberration correction.
    
    Parameters:
    -----------
    pos ... real, dim=[n, 3], 3D vector of unit length (ICRF)
    unitVector ... False: pos is unit vector, False: pos is not unit vector
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
    
    r = 1
    if(pos.ndim>1):
        if not unitVector: r=norm(pos,axis=1)
        xu=pos[:,0]/r
        yu=pos[:,1]/r
        zu=pos[:,2]/r
    else:
        if not unitVector: r=norm(pos)
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