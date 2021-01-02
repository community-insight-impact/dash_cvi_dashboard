import dash_html_components as html
import base64

#Code for the legends to show colorscales of the map


def make_legend(index):
	image_filename = "/assets/colorscales/" + str(index) + ".png" #image of the color scale
	# encoded_image = base64.b64encode(open(image_filename, 'rb').read())
	return html.Img(src='{}'.format(image_filename))

color_scale = html.Div(className= 'legend',children=[html.P(id = "legs", children = "Legends:"),
	html.Div([html.Div(id ='color-scales', children = []), 
	html.I(id='point-down', className="fa fa-angle-down", **{'aria-hidden': 'true'})])])

