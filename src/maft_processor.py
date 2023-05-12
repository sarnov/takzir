import os
import re

class MaftProcessor:

    numbers_re = re.compile ('[0-9A-Z]+[/.,+%]*[0-9A-Z]+[/.,+%]*[0-9A-Z]*')
    start_numbers_re = re.compile ('\n(\d)+ ')
    main_header_re = re.compile ('((\s|\n)*)=(.*)\n')
    secondary_header_re = re.compile ('((\s|\n)*)\\\\(.*)\n')
    third_header_re = re.compile ('((\s|\n)*)\|(.*)\n')
    page_ref_re = re.compile('')
    html_prefix = '<!DOCTYPE html>\n<html dir="rtl" lang="he">\n<head>\n' + \
         '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>'
    title_suffix = '</title>\n</head>\n<body>\n'

    def __init__(self, maft_section):
        self.maft_section = maft_section

    def process_section(self):
        self.maft_section="<br>"+self.maft_section
        self.maft_section=self.maft_section.replace('╚',"<br>")
        self.maft_section=self.maft_section.replace(')',"^^^")
        self.maft_section=self.maft_section.replace('(',")")
        self.maft_section=self.maft_section.replace("^^^","(")
        self.maft_section=self.maft_section.replace(']',"^^^")
        self.maft_section=self.maft_section.replace('[',"]")
        self.maft_section=self.maft_section.replace("^^^","[")
        self.inverse_numbers()
        self.cleanup_start_numbers()
        self.process_secondary_headers()
        main_header = self.process_main_header()
        self.maft_section=self.maft_section.replace('\n',"<br>\n")
        self.maft_section=self.maft_section.replace('</h2><br>\n',"</h2>\n")
        self.maft_section=self.maft_section.replace('</h3><br>\n',"</h3>\n")
        self.maft_section = self.html_prefix + main_header + self.title_suffix + self.maft_section
        return self.maft_section

    def inverse_numbers(self):
        numbers = self.numbers_re.finditer(self.maft_section)
        for match in numbers:
            s=match.span()
            orig_str = self.maft_section[s[0]:s[1]]
            if orig_str[-1] in ['/','.',',',"+","%"]:
                reverse_str=orig_str[:-1][::-1] + orig_str[-1]
            else:
                reverse_str=orig_str[::-1]
                
            self.maft_section = self.maft_section[:s[0]] + reverse_str + self.maft_section[s[1]:]

    def cleanup_start_numbers(self):
        match = self.start_numbers_re.search(self.maft_section)
        start_pos=0
        while match is not None:
            s=match.span()     
            self.maft_section = self.maft_section[:s[0]+1+start_pos] + self.maft_section[s[1]+start_pos:]
            start_pos = s[1]+start_pos
            match = self.start_numbers_re.search(self.maft_section[start_pos:])

    def process_main_header(self):
        match = self.main_header_re.search(self.maft_section)
        main_header = match.groups()[-1]
        main_header_pos = match.span(3)
        self.maft_section = '<h2>' + self.maft_section[main_header_pos[0]:main_header_pos[1]] + '</h2>' + self.headers_toc + self.maft_section[main_header_pos[1]:]
        return main_header

    def process_secondary_headers(self):
        match = self.secondary_header_re.search(self.maft_section)
        secondary_headers = []
        start_pos=0
        while match is not None:
            secondary_header = match.groups()[-1]
            secondary_header_pos = match.span(3)
            secondary_header_id = secondary_header.replace(" ","_")
            h3_header = f'<h3 id={secondary_header_id}>'
            self.maft_section = self.maft_section[:start_pos + secondary_header_pos[0] - 1] + h3_header + self.maft_section[
                secondary_header_pos[0]+start_pos:secondary_header_pos[1]+start_pos] + '</h3>' + self.maft_section[secondary_header_pos[1]+start_pos:]
            start_pos = start_pos + secondary_header_pos[1] + len(h3_header) + 5
            secondary_headers.append({"header":secondary_header, "id": secondary_header_id})
            match = self.secondary_header_re.search(self.maft_section[start_pos:])
            end_section_pos = match.span(3)[0] if match is not None else len(self.maft_section)
            third_headers_toc = self.process_third_headers(start_pos, end_section_pos+start_pos)
            self.maft_section = self.maft_section[:start_pos] + third_headers_toc + self.maft_section[start_pos:]
            start_pos = start_pos + len(third_headers_toc)
            match = self.secondary_header_re.search(self.maft_section[start_pos:])
        headers_toc = ""
        for header in secondary_headers:
            headers_toc += '<a href ="#'+header["id"]+'">' + header["header"] + '</a>\n'
        self.headers_toc = headers_toc

    def process_third_headers(self, start_section_pos, end_section_pos):
        match = self.third_header_re.search(self.maft_section[start_section_pos:end_section_pos])
        third_headers = []
        start_pos=start_section_pos
        while match is not None:
            third_header = match.groups()[-1]
            third_header_pos = match.span(3)
            third_header_id = third_header.replace(" ","_")
            h4_header = f'<h4 id={third_header_id}>'
            self.maft_section = self.maft_section[:start_pos + third_header_pos[0] - 1] + h4_header + self.maft_section[
                third_header_pos[0]+start_pos:third_header_pos[1]+start_pos] + '</h4>' + self.maft_section[third_header_pos[1]+start_pos:]
            start_pos = start_pos + third_header_pos[1] + len(h4_header) + 5
            third_headers.append({"header":third_header, "id": third_header_id})
            match = self.third_header_re.search(self.maft_section[start_pos:end_section_pos])
        headers_toc = ""
        for header in third_headers:
            headers_toc += '<a href ="#'+header["id"]+'">' + header["header"] + '</a>\n'
        return headers_toc

if __name__ == "__main__":
    filename = "BAGAZ.MM1"
    print(f"processing file {filename}")
    maft_file = os.path.join("maft", filename)
    with open(maft_file,"r",encoding="cp862") as f:            
        maft_section = f.read()
    maft_section = MaftProcessor(maft_section).process_section()
    html_filename = filename.upper().replace("MM1","html")
    out_dir_path = "maft_processed"
    with open(os.path.join(out_dir_path, html_filename),"w", encoding="utf-8") as f:
        f.write(maft_section)
        f.close()
