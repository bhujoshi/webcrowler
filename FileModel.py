import os
class FileModel:
    path=''
    def create_dir_or_file(self,mypath):
    #save the path for further use
        self.path=mypath
        if not os.path.isdir(mypath[ : mypath.rfind('/') ]):
            os.makedirs(mypath[ : mypath.rfind('/') ])
        if not os.path.exists(mypath):
            f = file(mypath, "w+")
    #write the current path        
    def write_file(self,data):
        if self.path == '' and data == '' :
            print("Should be required file path and unable to write file with empty string")
        else:
            f = open(self.path, 'w+')
            f.write(data)
        
    

    
    
