import psycopg2
import subprocess,os


class DB:
	def __init__(self, db_name):
		self.db_name = db_name

	def connect(self):
		self.db = psycopg2.connect(	"dbname='{}' ".format(self.db_name) +\
									"user='verifyrecordsaccess' " +\
									"host='164.68.97.194' " +\
									"password='mRL92PLqgb7Y4MsL'")
		self.db.autocommit = True

	def query(self, sql):
		try:
			cursor = self.db.cursor()
			cursor.execute(sql)
		except (AttributeError, psycopg2.OperationalError):
			self.connect()
			cursor = self.db.cursor()
			cursor.execute(sql)
		return cursor

	def close(self):
		self.db.close()


class Record:
	def __init__(self, _id, _date, hour, channel, pc_name, ip, filename, alive=1):
		self._id = int(_id)
		self._date = _date
		self.hour = int(hour)
		self.channel = channel
		self.pc_name = pc_name
		self.ip = ip
		self._input = filename
		self._output = self.getFilename(filename)
		self.alive = alive

	def getFilename(self, f):
		return f[:-3] + "_small" + f[-3:]

	def __repr__(self):
		return f"ID: {self._id}\nDATE: {self._date}\nHOUR: {self.hour}\nCHANNEL: {self.channel}\nINPUT: {self._input}\nOUTPUT: {self._output}\nALIVE: {self.alive}\n============================\n"


def getRecords():
	records = []
	query = "SELECT a.id, a.date, a.hour, a.channel, a.pc_name, a.ip, a.filename FROM records_location a LEFT JOIN records_location_small b ON a.id = b.id WHERE b.id IS NULL;"
	db = DB("catalog_registerads")
	results = db.query(query)
	for result in results:
		records.append(Record(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
	db.close()
	reduceSize(records)

def reduceSize(records):
	for record in records:
		#cmd = f"ffmpeg -y -i {record._input} -vcodec libx264 -crf 30 -preset veryfast -c:a copy -s 960x540 {record._output}"
		othervar = '%{pts\:gmtime\:1580833680}'
		cmd = """ffmpeg -y -i %s -vf drawtext="text='Ch\: %s | Broadcasted at\: %s | ADsrecognition.com - Recordings archive': fontcolor=white: fontsize=38: box=1: boxcolor=black: boxborderw=5: x=30: y=20" -vcodec libx264 -crf 30 -preset veryfast -c:a copy -s 960x540 -codec:a copy -map 0:v -map 0:a -scodec copy -map 0:s -y %s""" % (record._input, record.channel, othervar, record._output)
		os.system(cmd)
		# subprocess.call(cmd.split())
		sendDataToDb(record)

def sendDataToDb(record):
	db = DB("catalog_registerads")
	query = f"INSERT INTO records_location_small(id, date, hour, channel, pc_name, ip, filename, alive) VALUES ({record._id}, '{record._date}', {record.hour}, {record.channel}, '{record.pc_name}', '{record.ip}', '{record._output}', {record.alive});"
	db.query(query)
	db.close()

getRecords()