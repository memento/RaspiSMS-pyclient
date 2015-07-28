# RaspiSMS-pyclient: Python client for RaspiSMS API

Small client for [RaspiSMS](http://raspisms.raspbian-france.fr/) server. It simply propose a trivial interface to send SMS from a python script or from command line.

See: 
* http://raspisms.raspbian-france.fr/
* https://github.com/RaspbianFrance/RaspiSMS

Fork :
* https://github.com/enavarro222/RaspiSMS-pyclient  (enavarro222)

Licence : GNU LGPL (see LICENCE.txt)

## Install

    $ pip install git+https://github.com/memento/RaspiSMS-pyclient.git


## Python module usage

```python
from raspisms import RaspiSMS
rsms = RaspiSMS("http://URL_TO/RaspiSMS", email="ADMIN@EMAIL.DD", password="PASSWORD")
rsms.send("PHONENUMBER", "SMS text !"[, "YYYY-MM-DD hh:mm"])
```

## Command-line tool

A command line tool `raspisms-send` is provided, you can use it this way:

    $ raspisms-send -u http://URL_TO/RaspiSMS -e ADMIN@EMAIL.DD -p ADMIN_PASSWORD  PHONENUMBER "SMS text" ["YYYY-MM-DD_hh:mm"]
    
The date is optional. If you don't put anything, the curent date and time will be chosen. For example, if you want to send an sms on July the 27th 2015 at 9:50 P.M. (21:46), you'll add 2015-07-27_21:46 at the end of the command.

See also `-h` for some help.

## TODO

See #TODO in [raspisms.py](raspisms.py), don't hesitate to send a push request !
