import os

processed_dir='processed'

volumes = sorted(os.listdir(processed_dir),reverse=True)

html_prefix = '<!DOCTYPE html><html dir="rtl" lang="he"><head><title>תקציר סביר</title></head><body>'
html_suffix = '</body></html>'

dir_name_map = {
    1:"א'",
    2:"ב'",
    3:"ג'",
    4:"ד'",
    5:"ה'",
    6:"ו'",
    7:"ז'",
    8:"ח'",
    9:"ט'",
    10:"י'",
    11:'י"א',
    12:'י"ב',
    13:'י"ג',
    14:'י"ד',
    15:'ט"ו',
    16:'ט"ז',
    17:'י"ז',
    18:'י"ח',
    19:'י"ט',
    20:"כ'",
    21:'כ"א',
    22:'כ"ב',
    23:'כ"ג',
    24:'כ"ד',
    25:'כ"ה',
    26:'כ"ו',
    27:'כ"ז',
    28:'כ"ח',
    29:'כ"ט',
    30:"ל'",
    31:'ל"א',
    32:'ל"ב',
    33:'ל"ג',
    34:'ל"ד',
    35:'ל"ה',
    36:'ל"ו',
    37:'ל"ז',
    38:'ל"ח',
    39:'ל"ט',
    40:"מ'",
    41:'מ"א',
    42:'מ"ב',
    43:'מ"ג',
    44:'מ"ד',
    45:'מ"ה',
    46:'מ"ו',
    47:'מ"ז',
    48:'מ"ח',
    49:'מ"ט',
    50:"נ'",
    51:'נ"א',
    52:'נ"ב',
    53:'נ"ג',
    54:'נ"ד',
    55:'נ"ה',
    56:'נ"ו',
    57:'נ"ז',
    58:'נ"ח',
    59:'נ"ט',
    60:"ס'",
    61:'ס"א',
    62:'ס"ב',
    63:'ס"ג',
    64:'ס"ד',
    65:'ס"ה',
    66:'ס"ו',
    67:'ס"ז',
    68:'ס"ח',
    69:'ס"ט',
    70:"ע'",
    71:'ע"א',
    72:'ע"ב',
}

index_file = html_prefix
for vol_dir in volumes:
    vol_num = int(vol_dir[4:6])
    if vol_num in dir_name_map:
        index_file = index_file + f'<h3>כרך {dir_name_map[vol_num]}</h3><ul>'
        vol_dir_path = os.path.join(processed_dir, vol_dir)
        hovrot = os.listdir(vol_dir_path)
        hovrot_dict = {int(hov[:-5][3:]):hov for hov in hovrot}
        for hoveret in sorted(hovrot_dict):
            index_file = index_file + f'<li style="display:inline;padding: 10px 10px;"><a href="{os.path.join(vol_dir_path, hovrot_dict[hoveret])}">{hoveret}</a></li>'
        index_file  =index_file+'</ul>'
index_file + index_file + html_suffix

with open("process.html","w", encoding="utf-8") as f:
    f.write(index_file)
    f.close()
