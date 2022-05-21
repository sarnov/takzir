import os
from hoveret_processor import HoveretProcessor

directory = 'hovrot/72'
out_directory='processed/72'

for filename in os.listdir(directory):
    hoveret_file = os.path.join(directory, filename)
    if os.path.isfile(hoveret_file):
        with open(hoveret_file,"r",encoding="cp862") as f:            
            hoveret = f.read()
        hoveret = HoveretProcessor(hoveret).process_hoveret()
        html_filename = filename.replace("HG1","html")
        with open(os.path.join(out_directory, html_filename),"w", encoding="utf-8") as f:
            f.write(hoveret)
            f.close()
