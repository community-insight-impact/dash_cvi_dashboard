import dash_html_components as html
import base64



def make_legend(index):
	image_filename = "colorscales/" + str(index) + ".png" # replace with your own image
	encoded_image = base64.b64encode(open(image_filename, 'rb').read())
	return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

color_scale = html.Div(id= 'color-scales', className= 'legend',children=[])

