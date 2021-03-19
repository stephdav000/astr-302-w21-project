#!/usr/bin/env python3

import sys
from astropy.io import ascii

test = '{}'.format(sys.argv[1])

if test == 'sdss':
    from astroquery.sdss import SDSS
        
    query = """
    {}
    """.format(sys.argv[2])

    res = SDSS.query_sql(query)

    ascii.write(res, "{}".format(sys.argv[3]), delimiter=",")
        
if test == 'gaia':
    from astroquery.gaia import Gaia
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    Gaia.ROW_LIMIT = -1
    shape = '{}'.format(sys.argv[2])
    if shape == 'cone':
        print('This may take some time')
        coord = SkyCoord(ra = sys.argv[3], dec = sys.argv[4], unit=(u.degree, u.degree), frame='icrs')
        radius = u.Quantity(sys.argv[5], u.deg)
        j = Gaia.cone_search_async(coord, radius)
        r = j.get_results()
        ascii.write(r, "{}".format(sys.argv[6]), delimiter=",")
    else:
        coord = SkyCoord(ra= sys.argv[3], dec= sys.argv[4], unit=(u.degree, u.degree), frame='icrs')
        width = u.Quantity(sys.argv[5], u.deg)
        height = u.Quantity(sys.argv[6], u.deg)
        r = Gaia.query_object_async(coordinate=coord, width=width, height=height)
        ascii.write(r, "{}".format(sys.argv[7]), delimiter=",")
if test == 'help':
    print("\nThis program will query either the SDSS or Gaia databases and download the result as a csv file.\nTo query SDSS use the format: <sdss> <'Query'> <filename>\nTo query Gaia, use the format: <gaia> <cone> <RA> <DEC> <Radius> <filename>\nor <gaia> <rectangle> <RA> <DEC> <Width> <height> <filename>\ndepending on if you want to query a circular region or rectangular.\n")
else:
    print("Enter <help> for instuctions")

#SDSS: <SDSS> <Query> <filename>
#Gaia: <Gaia> <cone>  <RA> <DEC> <Radius> <filename>
#Gaia: <Gaia> <rectangle> <RA> <DEC> <Width> <height> <filename>