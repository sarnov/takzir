
import re
from constants import dir_name_map

class HoveretProcessor:

    html_prefix = '<!DOCTYPE html>\n<html dir="rtl" lang="he">\n<head>\n' + \
         '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>'
    title_suffix = '</title>\n</head>\n<body>\n'
    html_suffix = '</body>\n</html>'
    numbers_re = re.compile ('[0-9A-Z]+[/.,+%]*[0-9A-Z]+[/.,+%]*[0-9A-Z]*')
    header_re = re.compile ('(<br>\s*=.*?<br>)\s*(?:\[.*?\])?([\*\(].*?\)(?:\.| <br>|<br>))')
    page_re = re.compile ('<br>[0-9 ]*תקציר פסקי דין.*?<br>')
    footer_re = re.compile ('<br>....בפני.*?<br>|<br>...בפני.*?<br>|<br>..בפני.*?<br>|<br>בפני.*?<br>|<br>.בפני.*?<br>')
    initial_header_re = re.compile('(?:בתוכן|ב ת ו כ ן).*?=')

    def __init__(self, hoveret):
        self.hoveret = hoveret

    def process_hoveret(self, volume, hoveret_num):
        self.hoveret="<br>"+self.hoveret
        self.hoveret=self.hoveret.replace('╚',"<br>")
        self.hoveret=self.hoveret.replace(')',"^^^")
        self.hoveret=self.hoveret.replace('(',")")
        self.hoveret=self.hoveret.replace("^^^","(")
        self.hoveret=self.hoveret.replace(']',"^^^")
        self.hoveret=self.hoveret.replace('[',"]")
        self.hoveret=self.hoveret.replace("^^^","[")
        self.hoveret=self.hoveret.replace("\n","")
        self.inverse_numbers()
        self.clear_initial_header()
        self.process_header()
        self.clean_page_footer()
        self.process_footer()
        self.hoveret=self.hoveret.replace("<br><br>","<br>")
        end_pos = self.hoveret.find("ב ת ו כ ן")
        self.hoveret = self.hoveret[:end_pos]
        while self.hoveret.find("<br><br>")>0:
            self.hoveret=self.hoveret.replace("<br><br>", "<br>")
        if volume is not None:
            title = "תקציר סביר כרך " + dir_name_map[volume] + " חוברת " + str(hoveret_num)
        else:
            title = "תקציר סביר"
        self.hoveret=self.html_prefix + title + self.title_suffix + self.hoveret + self.html_suffix 
        return self.hoveret 

    def inverse_numbers(self):
        numbers = self.numbers_re.finditer(self.hoveret)
        for match in numbers:
            s=match.span()
            orig_str = self.hoveret[s[0]:s[1]]
            if orig_str[-1] in ['/','.',',',"+","%"]:
                reverse_str=orig_str[:-1][::-1] + orig_str[-1]
            else:
                reverse_str=orig_str[::-1]
                
            self.hoveret = self.hoveret[:s[0]] + reverse_str + self.hoveret[s[1]:]

    def clear_initial_header(self):
        match = self.initial_header_re.search(self.hoveret)
        if match is not None:
            start_pos=match.span()[0]
            end_pos = match.span()[1]
            if start_pos <=100:
                self.hoveret="<br>" + self.hoveret[end_pos-1:]
    
    def process_header(self):
        match = self.header_re.search(self.hoveret)
        start_pos=0
        while match is not None:
            s0=match.span(1)
            orig_header_str = self.hoveret[s0[0]+start_pos:s0[1]+start_pos]
            header_str = "<h2>"+orig_header_str[5:]+"</h2>"        
            s1=match.span(2)
            orig_secondary_header_str = self.hoveret[s1[0]+start_pos:s1[1]+start_pos]
            if len(orig_secondary_header_str) < 200:
                secondary_header_str = "<h3>"+orig_secondary_header_str+"</h3>"  
            else:
                secondary_header_str = orig_secondary_header_str      
            self.hoveret = self.hoveret[:s0[0]+start_pos] + header_str + secondary_header_str+ self.hoveret[s1[1]+start_pos:]
            start_pos = s0[0]+start_pos+len(header_str + secondary_header_str)
            match = self.header_re.search(self.hoveret[start_pos:])

    def clean_page_footer(self):
        match = self.page_re.search(self.hoveret)
        start_pos=0
        while match is not None:
            s=match.span()     
            self.hoveret = self.hoveret[:s[0]+start_pos] + self.hoveret[s[1]+start_pos:]
            start_pos = s[1]+start_pos
            match = self.page_re.search(self.hoveret[start_pos:])
        self.hoveret = self.hoveret + "<br>"

    def process_footer(self):
        match = self.footer_re.search(self.hoveret)
        start_pos=0
        while match is not None:
            s=match.span()     
            orig_footer_str = self.hoveret[s[0]+start_pos:s[1]+start_pos]
            footer_str = "<h4>"+orig_footer_str+"</h4><br>"        
            self.hoveret = self.hoveret[:s[0]+start_pos] + footer_str+ self.hoveret[s[1]+start_pos:]
            start_pos = s[1]+start_pos
            match = self.footer_re.search(self.hoveret[start_pos:])
        print(match)
