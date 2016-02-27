import urllib2

class Model:
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
            #print html[i:i+len(tag)]
            if self.check_tag_match( self.all_html_str[i:i+len(tag)], tag):
                tag_position.append(i)
                i=i+len(tag)
            else:
                i=i+1
                
        return tag_position     
    
        
obj = Model('http://www.ezeeport.com')
