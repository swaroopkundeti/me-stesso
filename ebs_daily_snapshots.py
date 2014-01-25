#!/usr/bin/python
# Script for taking daily snapshots which are attached to instance


import datetime
import boto.ec2
import dateutil.relativedelta

conn = boto.ec2.connect_to_region(
        'us-east-1',
        aws_access_key_id = 'your_access_key',
        aws_secret_access_key = 'your_private_key',
 )    
    

res = conn.get_all_instances()
instances = [i for r in res for i in r.instances]
vol = conn.get_all_volumes()
snap = conn.get_all_snapshots()

def snapshots():
    date_time_today = datetime.datetime.today()
    for volumes in vol:
        if volumes.attachment_state() == 'attached':
            filter = {'block-device-mapping.volume-id':volumes.id}
            volumesinstance = conn.get_all_instances(filters=filter)
            ids = [z for k in volumesinstance for z in k.instances]
            
            for s in ids:
                description = str(volumes.id)+'_'+str(s.tags['Name'])+'_'+ str(date_time_today)
                print description
                if volumes.create_snapshot(description):
                    print 'Snapshot created with description: ' + description
    
snapshots()
