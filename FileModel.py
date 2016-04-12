import os
class FileModel:
    def create_dir_or_file(self,mypath):
        if not os.path.isdir(mypath[ : mypath.rfind('/') ]):
            os.makedirs(mypath[ : mypath.rfind('/') ])
        if not os.path.exists(mypath):
            f = file(mypath, "w+")
    

    
    
