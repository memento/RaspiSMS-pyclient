#!/usr/bin/env python
#-*- coding:utf-8 -*-
""" Small client for RaspiSMS

see: http://raspisms.raspbian-france.fr/
"""
from __future__ import print_function
import os
import sys
import string

__version__ = "0.1.0"

class RaspiSMSError(RuntimeError):
    pass


class RaspiSMS(object):
    """ Minimal client for RaspiSMS API (http://raspisms.raspbian-france.fr)
    """
    def __init__(self, raspisms_url, email, password, date=None):
        #TODO check host ok
        #TODO add options for a HTTP auth system
        self._raspisms_url = raspisms_url
        self._email = email
        self._password = password
        if date is not None:
            # Time to replace the "_" char by a " " char
            self._date = string.replace(date, '_', ' ')
        else:
            self._date = None

    def send(self, num, text):
        #Note: import here to be able to import the module from setup.py whitout any dep
        import requests 
        url = "%s/smsAPI/send/" % (self._raspisms_url)
        data = {}
        data['email'] = self._email
        data['password'] = self._password
        data['numbers'] = num
        data['text'] = text
        if self._date is not None:
            data['date'] = self._date
        res = requests.post(url, data=data)
        #TODO: check on a bien 200
        returns = res.json()
        if returns["error"] == 0:
            # everything is ok
            pass
        elif returns["error"] == 1:
            raise RaspiSMSError("Invalid auth (email/password)")
        elif returns["error"] == 2:
            raise RaspiSMSError("Imposible to create this SMS")
        elif returns["error"] == 3:
            raise RaspiSMSError("Some arguments are missing")
        else:
            raise RaspiSMSError("Unknow error")


def raspisms_send():
    """ raspisms-send: Command line tool to send SMS
    """
    import argparse
    parser = argparse.ArgumentParser(description='Send a SMS with throw a RaspiSMS server.')
    parser.add_argument("NUM", help="Recipient phone number")
    parser.add_argument("TEXT", help="SMS itself !")
    
    parser_raspisms = parser.add_argument_group('RaspiSMS arguments')
    parser_raspisms.add_argument("-u", "--url", dest="url", help="RaspiSMS base url", required=True)
    parser_raspisms.add_argument("-e", "--email", dest="email", help="RaspiSMS admin email", required=True)
    parser_raspisms.add_argument("-p", "--password", dest="password", help="RaspiSMS admin password", required=True)
    parser_raspisms.add_argument("-d", "--date", dest="date", help="Add a sending date and time (optional). Format : YYYY-MM-DD_hh:mm", required=False)

    #TODO add .raspisms config file
    #TODO add interactive read of data

    args = parser.parse_args()
    if args.date is None:
        rsms = RaspiSMS(args.url, email=args.email, password=args.password)
    else:
        rsms = RaspiSMS(args.url, email=args.email, password=args.password, date=args.date)
    try:
        rsms.send(args.NUM, args.TEXT)
    except RaspiSMSError as err:
        print("Error: %s" % err, file=sys.stderr)
        return 1
    else:
        if args.date is None:
            print("SMS of %d char will be sent to %s" % (len(args.TEXT), args.NUM))
        else:
            print("SMS of %d char will be sent to %s on %s" % (len(args.TEXT), args.NUM, string.replace(args.date, '_', ' ')))
        return 0

if __name__ == '__main__':
    sys.exit(raspisms_send())


