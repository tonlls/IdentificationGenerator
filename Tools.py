import hashlib
import json

import qrcode
from PIL import ImageDraw, Image

import Constants


def draw_text(image, text, pos, font=Constants.FONT):
	ImageDraw.Draw(image).text((pos[0], pos[1]), text, (95, 36, 147), font=font)


def scale(image, max_size, add_mask=True, method=Image.ANTIALIAS):
	"""
	resize 'image' to 'max_size' keeping the aspect ratio
	and place it in center of white 'max_size' image
	"""
	im_aspect = float(image.size[0]) / float(image.size[1])
	out_aspect = float(max_size[0]) / float(max_size[1])
	if im_aspect >= out_aspect:
		scaled = image.resize((max_size[0], int((float(max_size[0]) / im_aspect) + 0.5)), method)
	else:
		scaled = image.resize((int((float(max_size[1]) * im_aspect) + 0.5), max_size[1]), method)

	offset = (((max_size[0] - scaled.size[0]) / 2), ((max_size[1] - scaled.size[1]) / 2))
	back = Image.new("RGB", max_size, "white")
	if add_mask:
		back.paste(scaled, (int(offset[0]),int(offset[1])),scaled)
	else:
		back.paste(scaled, (int(offset[0]),int(offset[1])))
	return back


def generate_qr(input, size, border_size):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=int(size / 25),
		border=border_size)
	qr.add_data(input)
	qr.make(fit=True)
	return qr.make_image()


def crypt(input, method='md5'):
	m = hashlib.new(method)
	m.update(bytes(input, 'utf'))
	return str(m.digest())


class DataFile:
	__contents = {}

	@staticmethod
	def get_content(filepath, type, reload_if_cached=False):
		if not reload_if_cached and filepath in DataFile.__contents:
			return DataFile.__contents[filepath]
		else:
			with open(filepath, 'r',encoding='utf-8') as json_file:
				if type == 'JSON':
					data = json.load(json_file)
					DataFile.__contents[filepath] = data
					return data
				else:
					raise Exception(NotImplemented)

	@staticmethod
	def clear_cached_content(filepath):
		if filepath in DataFile.__contents:
			del DataFile.__contents[filepath]
			return True
		else:
			return False

	@staticmethod
	def clear_cache():
		DataFile.__contents = {}
