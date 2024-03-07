import os, json
from subprocess import Popen, PIPE, STDOUT
import cairosvg
import time
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

import multiprocessing



def convertRunner(iconPath, fpath):
	print("Working on", iconPath)
	for res in [8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
		cairosvg.svg2png(url=fpath, write_to=os.path.join(iconPath, str(res)+".png"), output_width=res, output_height=res)
		cairosvg.svg2ps(url=fpath, write_to=os.path.join(iconPath, str(res)+".ps"), output_width=res, output_height=res)
		cairosvg.svg2pdf(url=fpath, write_to=os.path.join(iconPath, str(res)+".pdf"), output_width=res, output_height=res)

		im = Image.open(os.path.join(iconPath, str(res)+".ps"))
		rgb_im = im.convert('RGB')
		rgb_im.save(os.path.join(iconPath, str(res)+".jpg"), "jpeg")

		im = Image.open(os.path.join(iconPath, str(res)+".png"))
		rgb_im = im.convert('RGBA')
		rgb_im.save(os.path.join(iconPath, str(res)+".webp"), 'webp')
def main():
	if len(os.listdir("icons")) == 0:
		print("ERROR: You must recursivly clone this repo to run main.py!!!")
		exit(1)
	# os.system("rm -r docs/*")

	iconsData = []
	with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as exe:
		for icon in set(os.listdir(os.path.join("icons", "icons"))):
			iconPath = os.path.join("docs", os.path.splitext(icon)[0])
			try: os.mkdir(iconPath)
			except: pass
			fpath = os.path.join("icons", "icons", icon)

			with open(fpath, "r") as f:
				svgData = f.read()
				if os.path.exists(os.path.join(iconPath, "icon.svg")):
					with open(os.path.join(iconPath, "icon.svg"), "r") as f2:
						if f2.read() == svgData:
							continue
				iconsData.append([
						svgData,
						os.path.join(iconPath, "android.xml"),
						os.path.join(iconPath, "icon.svg")
					])
			exe.submit(convertRunner, iconPath, fpath)


		# break
	print("Starting svg conversion stage")
	# print(json.dumps(iconsData))
	p = Popen(['node', 'mass_convert.js'], stdout=PIPE, stdin=PIPE, text=True)
	stdout_data = p.communicate(input=json.dumps(iconsData))[0]

	f = open("readme.md", "w")
	f2 = open("readme.md.template", "r")
	f.write(f2.read())
	f2.close()

	for icon in os.listdir(os.path.join("icons", "icons")):
		name = os.path.splitext(icon)[0]
		f.write("<h3>"+name + ":</h3>\n")
		f.write(f"<img width=\"128\" src=\"https://raw.githubusercontent.com/HeronErin/Bootstrap-Icons-Auto-convert/main/docs/{name}/128.png\">\n<br>\n")
	f.write("<br><sup>Last generated at "+time.ctime()+"</sup>")
	f.close()

	os.system("cp readme.md docs/")
if __name__ == "__main__":
	main()
