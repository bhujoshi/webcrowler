import urllib2
response = urllib2.urlopen('http://www.ezeeport.com/')
html = response.read()
#print html
def check_tag_match( html_str, tag):
    if html_str == tag:
        return True
    else:
        return False
    
def find_tag( html , tag ):
    tag_position=[]
    i=0
    while i < len(html):
        #print html[i:i+len(tag)]
        if check_tag_match( html[i:i+len(tag)] , tag ):
            tag_position.append(i)
            i=i+len(tag)
        else:
            i=i+1
            
    return tag_position    
            
tag_position=find_tag(html,'<link');
print tag_position

print html[tag_position[0]:tag_position[0]+54]
print html[tag_position[1]:tag_position[1]+54]
print html[tag_position[2]:tag_position[2]+54]


