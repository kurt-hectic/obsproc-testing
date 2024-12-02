docker run -v %cd%/in:/input -v %cd%/out:/out -it csv2bufr /bin/bash

csv2bufr mappings create 301150 301011 301012 301021 010004 012104 > /input/mapping.json

