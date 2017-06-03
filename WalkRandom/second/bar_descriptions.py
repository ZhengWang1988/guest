import pygal
from pygal.style import LightColorizedStyle,LightenStyle

my_style = LightenStyle('#333366',
	base_style=LightColorizedStyle)
chart = pygal.Bar(style=my_style,
	x_label_rotation=45,
	show_legend=False)
chart.title = 'Python Projects'
chart.x_labels = ['awesome-python','httpie','thefuck']

plot_dicts = [
    {'value':34584,'label':'Description of awesome-python.'},
    {'value':29892,'label':'Description of httpie.'},
    {'value':28243,'label':'Description of thefuck.'}
]

chart.add('',plot_dicts)
chart.render_to_file('bar_description.svg')