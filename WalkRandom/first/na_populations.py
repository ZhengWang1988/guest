import pygal
# import json
# from country_codes import get_country_code

wm = pygal.maps.world.World()
wm.title = 'Populations of Countries in North America'
wm.add('North America',{'ca':34126000,'us':309349000,'mx':113423000})

wm.render_to_file('na_populations.svg')