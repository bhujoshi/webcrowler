import urllib2
from FileModel import FileModel 
class Model(FileModel):
    tags=['script','link','img']
    tags_positions=[]
    all_html_str=None
    #constructer funtion for class 
    def __init__(self,url):
        response = urllib2.urlopen(url)
        self.all_html_str = response.read()
        for tag in self.tags :
            self.tags_positions.append(self.find_tag(tag))
            
        print self.tags_positions

        self.file_full_src()
        
        
    #check if tag is match 
    def check_tag_match( self, html_str, tag):
        if html_str == tag:
            return True
        else:
            return False
        
    #return position of matched tag in array         
    def find_tag( self, tag):
        tag='<'+tag
        tag_position=[]
        i=0
        while i < len(self.all_html_str):
            if self.check_tag_match( self.all_html_str[i:i+len(tag)], tag):
                start_and_end={}
                start_and_end['start']=i
                start_and_end['end']=self.find_tag_end_postion(i)
                tag_position.append(start_and_end)
                i=i+len(tag)
            else:
                i=i+1
                
        return tag_position
    
    #return tag end ( > ) position
    #this function return  the next > position index 
    def find_tag_end_postion( self, index):
        while index < len(self.all_html_str):
            if self.check_tag_match( self.all_html_str[index:index+1], '>'):
                return index
            index=index+1
                
    
    #find full address of file using index
    def file_full_src(self):
        attr_in_tag_to_match=['src','href']
        url_string_start_index=None
        for tag_positions in self.tags_positions:
            for tag_index in tag_positions:
                #print self.all_html_str[tag_index['start']:tag_index['end']+1]
                url_string_start_index=None
                while tag_index['start'] < tag_index['end']:
                    
                    if self.check_tag_match(attr_in_tag_to_match[0],self.all_html_str[tag_index['start']:tag_index['start']+3]):
                        url_string_start_index= tag_index['start']+5
                        tag_index['start']=tag_index['start']+2
                        
                    if self.check_tag_match(attr_in_tag_to_match[1],self.all_html_str[tag_index['start']:tag_index['start']+4]):
                        url_string_start_index= tag_index['start']+6
                        tag_index['start']=tag_index['start']+2

                   
                    if url_string_start_index != None and self.check_tag_match('"',self.all_html_str[tag_index['start']:tag_index['start']+1]):
                        if self.all_html_str[url_string_start_index:tag_index['start']] != '':
                            print self.all_html_str[url_string_start_index:tag_index['start']]
                            tag_index['start'] = tag_index['end']
                     
                        
                    tag_index['start']=tag_index['start']+1
    
                
    
obj = Model('http://www.ezeeport.com')
