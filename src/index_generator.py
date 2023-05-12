import os
from constants import dir_name_map
processed_dir='processed'

volumes = sorted(os.listdir(processed_dir),reverse=True)

sitemap="http://nsavir.co.il/process.html\n"

html_prefix = '<!DOCTYPE html>\n<html dir="rtl" lang="he">\n<head>\n<title>תקציר סביר</title>\n' + \
  '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet" ' + \
  'integrity="sha384-+4j30LffJ4tgIMrq9CwHvn0NjEvmuDCOfk6Rpg2xg7zgOxWWtLtozDEEVvBPgHqE" crossorigin="anonymous">\n ' +\
    '<meta name="viewport" content="width=device-width, initial-scale=1">' + \
    '</head>\n<body>\n' + \
  '<div class="container">\n <div class="row text-center"> \n <div class="col-md-4"> \n <h1 style="text-align:center">תקציר פסקי דין</h1> \n' + \
    '<h2 style="text-align:center">עו"ד נח סביר</h2>\n </div> \n <div class="col-md-4"> \n <img class="" src="savir_logo.png" width="100px">' + \
    '</div>\n  </div> \n <script async src="https://cse.google.com/cse.js?cx=a1085d1dce08c4f3e"></script> \n <div class="gcse-search"></div></div> \n'
html_suffix = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" ' + \
    'integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>\n'  + \
    '</body></html>'



index_file = html_prefix
for vol_dir in volumes:
    vol_num = int(vol_dir[4:6])
    if vol_num in dir_name_map:
        index_file = index_file + f'<h3>כרך {dir_name_map[vol_num]}</h3><ul class="list-inline">\n'
        vol_dir_path = os.path.join(processed_dir, vol_dir)
        hovrot = os.listdir(vol_dir_path)
        hovrot_dict = {int(hov[:-5][3:]):hov for hov in hovrot}
        for hoveret in sorted(hovrot_dict):
            if hoveret == 0:
                continue
            index_file = index_file + f'<li class="list-inline-item" style="font-size: 3vw;  padding: 1vw;"><a href="{os.path.join(vol_dir_path, hovrot_dict[hoveret])}">{hoveret}</a></li>\n'
            sitemap = sitemap + f'http://nsavir.co.il/{os.path.join(vol_dir_path, hovrot_dict[hoveret])}\n'
        index_file  =index_file+'</ul>\n'
index_file = index_file + html_suffix

with open("process.html","w", encoding="utf-8") as f:
    f.write(index_file)
    f.close()
with open("sitemap.txt","w", encoding="utf-8") as f:
    f.write(sitemap)
    f.close()
