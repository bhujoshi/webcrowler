import urllib2
import urllib
from FileModel import FileModel

class Model(FileModel):
    tags=['script','link','img']
    str_files_path=[]
    str_img_path=[]
    tags_positions=[]
    file_paths_inside_css=[]
    all_html_str=None
    #constructer funtion for class 
    def __init__(self,url):
        self.default(url)
            
    #default function
    def default(self,url):
        response = urllib2.urlopen(url)
        self.all_html_str = response.read()
        self.create_dir_or_file('myproject/index.html')
        self.write_file(self.all_html_str)
        for tag in self.tags :
            self.tags_positions.append(self.find_tag(tag))
        print ("Downloading.................");    
        #print self.tags_positions
        self.file_full_src()
        #print(self.str_files_path)
        #print(self.str_img_path)
        
        for file_path in self.str_files_path:
                
            full_path=url+'/'+file_path
            #print(full_path)
            url_obj = urllib2.urlopen(full_path)
            all_html_str = url_obj.read()
            #check inside  css file for url off other css file and images those are inside styles
            if self.check_tag_match(file_path[-3:],'css'):
                self.get_file_path_from_css_file(all_html_str)
                
            self.create_dir_or_file('myproject/'+file_path)
            self.write_file(all_html_str)

        print(self.file_paths_inside_css)             
        #download images and import files inside css files 
        for file_path in self.file_paths_inside_css:
            
            if(self.check_tag_match(file_path[0:3],'../')):
                full_path=url+'/'+file_path[3:]
                file_path=file_path[3:]
                
            else:
                full_path=url+'/css/'+file_path
                
            if(self.check_tag_match(file_path[0:4],'http')==False):                    
                try:
                    url_obj = urllib2.urlopen(full_path)
                    all_html_str = url_obj.read()
                    if(all_html_str == ''):
                        self.create_dir_or_file('myproject/'+file_path)
                        urllib.urlretrieve(full_path, 'myproject/'+file_path)
                    else:
                        self.create_dir_or_file('myproject/'+file_path)
                        self.write_file(all_html_str)
            
                except Exception  as inst:
                    print("url not found "+full_path);     

                
        for file_path in self.str_img_path:
            full_path=url+'/'+file_path
            #print (full_path)
            self.create_dir_or_file('myproject/'+file_path)
            urllib.urlretrieve(full_path, 'myproject/'+file_path)
            
            
        print("your site is download sucessfully!");
        
    #get image or file path from css file
    def get_file_path_from_css_file(self,file_str):
        i =0
        
        while (  i < len( file_str )  ):
            
            if (file_str[i:i+4]=='url(' or file_str[i:i+5]=='url (' ) :
                i=i+3
                path_and_index=self.get_full_url_using_index(i,file_str)
                if(path_and_index['path'] != '' ):
                    path_and_index=self.get_full_url_using_index_of_import_file(i,file_str)
                
                self.file_paths_inside_css.append(path_and_index['path'])
                i=path_and_index['index'];
            if (file_str[i:i+7]=='@import' ) :
                i=i+7
                path_and_index=self.get_full_url_using_index(i,file_str)
                if(path_and_index['path'] != '' ):
                    path_and_index=self.get_full_url_using_index_main(i,file_str)
                    print(path_and_index)
                self.file_paths_inside_css.append(path_and_index['path'])
                i=path_and_index['index'];
            i = i + 1
        #print(self.file_paths_inside_css)    
                
    #return url path string recuresive function
    def get_full_url_using_index(self,index,file_str):
        start_index=0
        i = index
        myList={}
        while (   i < len( file_str ) ):
            if (file_str[i:i+1]=='"' or file_str[i:i+1]=="'") :
                if( start_index != 0):
                    end_index=i
                    break;
                start_index=i+1
                
            i = i + 1
            
        path=file_str[start_index+1:end_index-1]
        #print(path)
        myList['index']=index
        myList['path']=path
        return myList

    #return url path string recuresive function
    def get_full_url_using_index_main(self,index,file_str):
        start_index=0
        i = index
        myList={}
        while (   i < len( file_str ) ):
            if (file_str[i:i+1]=='"' or file_str[i:i+1]=="'") :
                if( start_index != 0):
                    end_index=i
                    break;
                start_index=i+1
                
            i = i + 1
            
        path=file_str[start_index:end_index]
        #print(path)
        myList['index']=index
        myList['path']=path
        return myList

    #return url of import file inside css file
    def get_full_url_using_index_of_import_file(self,index,file_str):
        start_index=index+1
        i = index+1
        myList={}
        while (   i < len( file_str ) ):
            if (file_str[i:i+1]==')') :
                end_index=i
                break;
            i = i + 1
            
        path=file_str[start_index+1:end_index-1]
        #print(path)
        myList['index']=index
        myList['path']=path
        return myList
    
                
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
        #print(self.tags_positions);
        count=0
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
                            my_file= self.all_html_str[url_string_start_index:tag_index['start']]
                            if(count != 2):
                                if self.check_http_file(my_file):
                                    self.str_files_path.append(my_file)       
                                
                            else:
                                if self.check_http_file(my_file):
                                    self.str_img_path.append(my_file)       

                            tag_index['start'] = tag_index['end'] 
                    tag_index['start']=tag_index['start']+1
            count=count+1        
    
    def check_http_file(self,str):
        if str[:4]=='http':
            return False
        else:
            return True
            
        
    
obj = Model('http://myshuttlecar.com')
