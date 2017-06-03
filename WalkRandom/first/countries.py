import pygal
# vm = pygal.maps.world.World()
from pygal.maps.world import COUNTRIES

for country_code in sorted(COUNTRIES.keys()):
	print(country_code,COUNTRIES[country_code])