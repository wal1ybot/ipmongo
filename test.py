#!/usr/bin/env python

# Imports necessary for using ipmongo
from pymongo.son_manipulator import SONManipulator
from ipaddr import IPAddress, IPNetwork
from ipaddr import IPv4Address, IPv4Network
from ipaddr import IPv6Address, IPv6Network
from pymongo import MongoClient
from ipmongo import TransformIP

# Import for demo purpose only
from pprint import pprint

if __name__ == '__main__':
	# Assume database is on localhost with default port, and no authentication required
	# Assume database name is 'test_db'

	c = MongoClient('localhost', 27017)
	db = c.test_db

	# In ipmongo.py, the class 'TransformIP' is implemented for conversion of ipaddr object
	# Add this class as 'handler' in db object, so that when ipaddr object is encountered,
	# methods within TransforIP are called to convert ipaddr object for inserting doc in MongoDB,
	# or converting back to ipaddr object after retrieved from MongoDB
	db.add_son_manipulator(TransformIP())

	# List of ipaddr objs for insert
	ipaddr_objs = set([
		IPAddress('8.8.8.8'),
		IPNetwork('8.8.8.0/24'),
		IPAddress('2001:4860:4860::8888'),
		IPNetwork('2001:4860::/32'),
	])

	# Create doc dicts for insert later
	docs = [{"desc": 'This is {}'.format(ipaddr_obj), "ip": ipaddr_obj} for ipaddr_obj in ipaddr_objs]

	# Insert data (assume collection name is 'test_collection')
	print 'Insert doc into MongoDB...'
	for doc in docs:
		db.test_collection.insert(doc)
		print 'Inserted {}...'.format(doc)

	# Select data
	print '\nSelect doc from MongoDB...'
	for doc in db.test_collection.find():
		desc = doc['desc']
		ip = doc['ip']
		print '{} -> '.format(desc),
		pprint(ip)
