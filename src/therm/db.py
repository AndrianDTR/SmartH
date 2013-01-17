
from error import *

import os
import sys
import MySQLdb as mdb

class Singleton(object):
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Singleton, cls).__new__(cls)
		return cls._instance

class DB(Singleton):
	conn = None
	
	def __init__(self):
		pass
	
	def connect(self, host, db, user, passwd):
		
		try:
			conn = mdb.connect(host, user, passwd, db)
		except mdb.Error, e:
			raise Error("Error {0}: {1}".format(e.args[0], e.args[1]))
		self.conn = conn
	
	def close(self):
		if self.conn:
			self.conn.close()
		self.conn = None
		
	def execute(self, statement):
		try:
			if not self.conn:
				raise Error("Error! No connection to DB.")
			
			cur = self.conn.cursor()
			cur.execute(statement)
		except mdb.Error, e:
			raise Error("Error {0}: {1}".format(e.args[0], e.args[1]))
		
		return cur
	
	def sync(self):
		self.conn.commit()
		
