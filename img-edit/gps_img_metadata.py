import PIL.Image
import PIL.ExifTags

''' GPS Location From Image Metadata in Python '''
# >>> pip install pillow
# >>> pip install geopy
# >>> pip install gmplot
img = PIL.Image.open("sample.jpg")

exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
}

north = exif['GPSInfo'][2]
east = exif['GPSInfo'][4]

lat = ((((north[0] * 60) + north[1]) * 60) + north[2]) / 60 / 60
long = ((((east[0] * 60) + east[1]) * 60) + east[2]) / 60 / 60

lat, long = float(lat), float(long)

from gmplot import gmplot

gmap = gmplot.GoogleMapPlotter(lat, long, 12)
gmap.marker(lat, long, "cornflowerblue")
gmap.draw("location.html")

from geopy.geocoders import Nominatim

geoLoc = Nominatim(user_agent="GetLoc")
locname = geoLoc.reverse(f"{lat}, {long}")
print(locname.address)

import webbrowser

webbrowser.open("location.html", new=2)



import piexif
# changing metadata
exif_dict = piexif.load('sample.jpg')
new_exif = piexif.load('sample_2.jpg')
exif_bytes = piexif.dump(new_exif)
piexif.insert(exif_bytes, "sample.jpg")
