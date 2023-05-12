import os
from hoveret_processor import HoveretProcessor

hovrot_dir = 'hovrot'
processed_dir='processed'

volumes = sorted(os.listdir(hovrot_dir))

for vol_dir in volumes:
    if not "taks" in vol_dir.lower():
        continue
    vol_dir_path = os.path.join(hovrot_dir, vol_dir)
    hovrot = os.listdir(vol_dir_path)
    hovrot_dict = {int(hov[:-4][3:]):hov for hov in hovrot if "hg1" in hov.lower()}
    for hov in sorted(hovrot_dict):
        print(f"processing file {hovrot_dict[hov]}")
        filename = hovrot_dict[hov]
        hoveret_file = os.path.join(vol_dir_path, filename)
        if os.path.isfile(hoveret_file):
            with open(hoveret_file,"r",encoding="cp862") as f:            
                hoveret = f.read()
            try:
                volume = int(os.path.basename(hoveret_file).split(".")[0].split("-")[0])
                hoveret_num = int(os.path.basename(hoveret_file).split(".")[0].split("-")[1])
            except:
                volume = None
                hoveret_num = None
            hoveret = HoveretProcessor(hoveret).process_hoveret(volume, hoveret_num)
            html_filename = filename.upper().replace("HG1","html")
            out_dir_path = os.path.join(processed_dir, vol_dir).lower()
            try:
                os.mkdir(out_dir_path)
            except FileExistsError:
                pass
            with open(os.path.join(out_dir_path, html_filename),"w", encoding="utf-8") as f:
                f.write(hoveret)
                f.close()
