#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="swaroop"
__date__ ="$24 Jan, 2014 3:30:33 PM$"



import boto.ec2
from dateutil import parser
from datetime import timedelta, datetime

# Make connection to aws ec2.

conn = boto.ec2.connect_to_region(
	'us-east-1',
	aws_access_key_id = 'your_access_key',
	aws_secret_access_key = 'your_private_key',
 )
 
# Pull all the snapshots which you have in aws 
# Note: you should give a parameter "owner='self'" else 
# without that it will pull all public snapshots

snaps = conn.get_all_snapshots(owner='self')

# Here is the logic for purging snapshots which are 2 weeks older
for snap in snaps:
    # "limit" is a variable which will have a 2 weeks old date.
    limit = datetime.now() - timedelta(days=14)
    
    # "snap.start_time will display a date in string format and 
    # it is not possible to compare unicode with date.
    if parser.parse(snap.start_time).date() <= limit.date():
        # Snapshot cannot be deleted when you create a volume out of it
        # and mount it on running system, If this encounter such snapshots
        # this program will stop excuting. So to avoid them and continue 
        # future i used exception.
        try:
            print "Deleting two weeks old snapshots %s,%s",snap.id, snap.description, conn.delete_snapshot(snap.id)
        except Exception, e:
            print e
    
