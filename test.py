import re

filename='Shreya Ghoshal *HD* Jaadu Hai Nasha Hai - Jism (16:9)'
print(re.sub('[^A-Z a-z]','',filename).strip(' ').replace(' ','_'))