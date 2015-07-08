# Python 2 code
import sys
import urllib
import csv

####################################################################################################
##################################### Functions ####################################################

# function to convert the hexadecimal latitude value of the payload to an apropiate decimal value
def latitude_hex2dec_correction(hex_latitude):
	hex_latitude = '0x' + hex_latitude		# Formatting hexadecimal
	dec_latitude = int(hex_latitude,16)		# Conversion to decimal
	dec_latitude_corrected = float(dec_latitude)*90/8388607	# Correction factor
	return  dec_latitude_corrected

# function to convert the hexadecimal longitud value of the payload to an apropiate decimal value
def longitude_hex2dec_correction(hex_longitude):
	hex_longitude = '0x' + hex_longitude		# Formatting hexadecimal
	dec_longitude = int(hex_longitude,16)		# Conversion to decimal
	dec_longitude_corrected = float(dec_longitude)*180/8388607	# Correction factor
	return  dec_longitude_corrected

# function to convert the hexadecimal battery status of the payload to an apropiate decimal value
def battery_hex2dec(hex_battery):
	hex_battery = '0x' + hex_battery		# Formatting hexadecimal
	if hex_battery == '0x00' :
		return 'Ext. power source'
	elif hex_battery == '0xFF' :
		return 'Not available'
	else :
		dec_battery = round(float(int(hex_battery,16))/2.54,2)		# Conversion to decimal
		return  str(dec_battery) + ' %'

# function to get the number of packets in a downloaded file
def get_numberPackets(csv_payload):
	
	file_loaded = open(csv_payload)
	file_read 	= csv.reader(file_loaded)	

	number_packets = sum(1 for row in file_read) - 1
	
	return number_packets


def select_desired_sequence(csv_payload, loramote_target, gateway_target) :

	number_packets = get_numberPackets(csv_payload)

	data 		= [[0 for x in range(4)] for x in range(int(number_packets)+1)]
	detected_seq = [[0 for x in range(5)] for x in range(int(number_packets)+1)] # Store here the detected sequences into the file

	detected_seq[0] = ['Sequence', 'Start Time','End Time', 'Start row','End row']

	seq_counter = 1
	row_counter = 0

	file_loaded = open(csv_payload)
	file_read 	= csv.reader(file_loaded)	
	
	for row in file_read :
		data[row_counter] = row 

		if (row_counter > 1) and (int(data[row_counter][2]) > (int(data[row_counter-1][2]))) :
	
			if seq_counter == 1 : # Start Time
				end_row = 2
				start_row = row_counter
			else :
				end_row = int(detected_seq[seq_counter-1][3]) + 1
				start_row = row_counter

			detected_seq[seq_counter][0] = str(seq_counter);	# Sequence
			detected_seq[seq_counter][1] = data[start_row-1][1] # Start time
			detected_seq[seq_counter][2] = data[end_row-1][1] 	# End time
			detected_seq[seq_counter][3] = str(start_row)		# Start row
			detected_seq[seq_counter][4] = str(end_row)			# End row

			seq_counter += 1

		row_counter += 1
		
		if seq_counter == 1 :
			end_row = 2
			start_row = number_packets

		else :
			end_row = int(detected_seq[seq_counter-1][3]) + 1
			start_row = number_packets+1
		
		detected_seq[seq_counter][0] = str(seq_counter) 	# Sequence
		detected_seq[seq_counter][1] = data[start_row-1][1] 	# Start time
		detected_seq[seq_counter][2] = data[end_row-1][1]	# End Time
		detected_seq[seq_counter][3] = str(start_row)	 	# Start row
		detected_seq[seq_counter][4] = str(end_row) 		# End row
	
	print '\n\tLoRaMote cible : ' + loramote_target
	print '\tGateway : ' + gateway_target
	print '\n\tIci les sequences trouvees :\n'
	for i in range (1, seq_counter + 1) :
		print '\t[' + str(i) +']  -->'
		print '\t\tStartTime: \t' + str(detected_seq[i][1])
		print '\t\tEndTime: \t' + str(detected_seq[i][2])
		print '\t\tPackets: \t' + str(int(detected_seq[i][3])-int(detected_seq[i][4]) + 1 )
		print '\t\tStartLine: \t' + str(detected_seq[i][3])
		print '\t\tEndLine: \t' + str(detected_seq[i][4])

	selection = raw_input('\n\tSelectionez la sequence a traiter : ')

	# Write the data into a .csv file
	with open('loramote_' + loramote_target + '_gateway_' + gateway_target + '_sequenceDetection.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerows(detected_seq)

	return  detected_seq[int(selection)]


def results_csv_generator(first_line, last_line, number_packets, csv_payload, csv_performance, loramote_target, gateway_target) :

	results_size = last_line - first_line + 1
	data 		= [[0 for x in range(4)] for x in range(int(number_packets)+1)]
	performance = [[0 for x in range(11)] for x in range(int(number_packets)+1)]
	results 	= [[0 for x in range(21)] for x in range(int(results_size)+1)]

	file_loaded = open(csv_payload)
	file_read 	= csv.reader(file_loaded)

	row_counter = 0
	for row in file_read :
		data[row_counter] = row 
		row_counter+=1

	file_loaded = open(csv_performance)
	file_read 	= csv.reader(file_loaded)

	row_counter = 0
	for row in file_read :
		performance[row_counter] = row 
		row_counter+=1

	results[0] = ['Sequence', 'Date - Time','Frequency [MHz]', 'Channel', 'Modulation', 'Bandwidth [KHz]', 'SF', 'Coding rate', 'ADR', 'RSSI [dBm]', 'SNR [dB]', 'Port', 'Payload ', 'Led 3 status', 'Athmospheric pressure', 'Temperature', 'Altitude (Pressure based)', 'Battery status', 'Latitude', 'Longitude', 'Altitude']

	for i in range (first_line-1, last_line) :
		results[i-first_line+2][0]	= performance[i][0]		# Sequence
		results[i-first_line+2][1]	= performance[i][7]		# Date - Time
		results[i-first_line+2][2]	= performance[i][1]		# Frequency
		results[i-first_line+2][3]	= performance[i][8]		# Channel
		results[i-first_line+2][4]	= performance[i][2]		# Modulation
		results[i-first_line+2][5]	= performance[i][3]		# Bandwidth
		results[i-first_line+2][6]	= performance[i][4]		# SF
		results[i-first_line+2][7]	= performance[i][5]		# Coding rate
		results[i-first_line+2][8]	= performance[i][6]		# ADR
		results[i-first_line+2][9]	= performance[i][9]		# RSSI
		results[i-first_line+2][10]	= performance[i][10]	# SNR
		results[i-first_line+2][11]	= data[i][0]			# Port
		results[i-first_line+2][12]	= data[i][3]			# Payload
		results[i-first_line+2][13]	= (data[i][3])[:2]							# LED 3 STATUS
		results[i-first_line+2][14]	= (data[i][3])[2:6]							# Athmosphere Pressure
		results[i-first_line+2][15]	= (data[i][3])[6:10]						# Temperature
		results[i-first_line+2][16]	= (data[i][3])[10:14]						# Altitude (Pressure sensor)
		results[i-first_line+2][17]	= battery_hex2dec((data[i][3])[14:16])					# Battery Status
		results[i-first_line+2][18]	= latitude_hex2dec_correction((data[i][3])[16:22])		# Latitude GPS
		results[i-first_line+2][19]	= longitude_hex2dec_correction((data[i][3])[22:28]) 	# Longitude GPS
		results[i-first_line+2][20]	= (data[i][3])[28:32]						# Altitud GPS
		

	# Write the data into a .csv file
	with open('loramote_' + loramote_target + '_gateway_' + gateway_target + '_results.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerows(results)


	print 'Le fichier Results a ete cree. \n\tLoramote: ' + loramote_target + '\n\tGateway: ' + gateway_target + '\n'

	return results

def kml_generator(results_input, number_rows_input, kml_icon, loramote_target, gateway_target):

	name_input = 'Testdrive_LoRaMote_' + loramote_target + '_gateway_' + gateway_target
	file_name_input = 'loramote_' + loramote_target + '_gateway_'+ gateway_target +'_testdrive.kml'

	tmp = '<kml>\n'
	tmp += ' <Document>\n'
	tmp += '  <name>%s</name>\n' % name_input
	# Style du point
	tmp += '<Style id="pin_style">'
	tmp += '	<IconStyle>'

	if kml_icon == 1 :
		tmp += '    <color>641400ff</color>' # Red
	elif kml_icon == 2 :
		tmp += '    <color>6414f0ff</color>' # yellow
	elif kml_icon == 3 :
		tmp += '    <color>64ff78f0</color>' # pink
	elif kml_icon == 4 :
		tmp += '    <color>6400dc14</color>' # green
	elif kml_icon == 5 :
		tmp += '    <color>64f0ff14</color>' # ligth blue
	elif kml_icon == 6 :
		tmp += '    <color>641478ff</color>' # orange
	elif kml_icon == 7 :
		tmp += '    <color>64f00014</color>' # blue

	tmp += '		<scale>1.0</scale>'
	tmp += '		<Icon>'


	if kml_icon == 1 :
		tmp += '			<href>http://maps.google.com/mapfiles/kml/shapes/donut.png</href>' # Donut
	elif kml_icon == 2 :
		tmp += '			<href>http://maps.google.com/mapfiles/kml/shapes/forbidden.png</href>' # Forbidden
	elif kml_icon == 3 :
		tmp += '			<href>http://maps.google.com/mapfiles/kml/shapes/open-diamond.png</href>' # Diamond
	elif kml_icon == 4 :
		tmp += '			<href>http://maps.google.com/mapfiles/kml/shapes/polygon.png</href>' # Polygon
	elif kml_icon == 5 :
		tmp += '			<href>http://maps.google.com/mapfiles/kml/shapes/square.png</href>' # Square
	elif kml_icon == 6 :
		tmp += '			<href>http://maps.google.com/mapfiles/kml/shapes/star.png</href>' # Start
	elif kml_icon == 7 :
		tmp += '			<href>http://maps.google.com/mapfiles/kml/shapes/triangle.png</href>' # Triangle

	tmp += '		</Icon>'
	tmp += '		<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>'
	tmp += '	</IconStyle>'
	tmp += '	<ListStyle>'
	tmp += '	</ListStyle>'
	tmp += '</Style>'
	# Style du ligne
	tmp += '<StyleMap id="Sheet1Map2">'
	tmp += '	<Pair>'
	tmp += '		<key>normal</key>'
	tmp += '		<styleUrl>#NormalSheet1Map2</styleUrl>'
	tmp += '	</Pair>'
	tmp += '	<Pair>'
	tmp += '		<key>highlight</key>'
	tmp += '		<styleUrl>#HighlightSheet1Map2</styleUrl>'
	tmp += '	</Pair>'
	tmp += '</StyleMap>'
	tmp += '<Style id="NormalSheet1Map2">'
	tmp += '	<IconStyle>'
	tmp += '		<Icon>'
	tmp += '		</Icon>'
	tmp += '	</IconStyle>'
	tmp += '	<BalloonStyle>'
	tmp += '		<text>$[description]</text>'
	tmp += '	</BalloonStyle>'
	tmp += '	<LineStyle>'
	tmp += '		<color>ffffff00</color>'
	tmp += '		<width>2</width>'
	tmp += '	</LineStyle>'
	tmp += '	<PolyStyle>'
	tmp += '		<color>00ffff00</color>'
	tmp += '		<fill>0</fill>'
	tmp += '	</PolyStyle>'
	tmp += '</Style>'
	tmp += '<Style id="HighlightSheet1Map2">'
	tmp += '	<IconStyle>'
	tmp += '		<Icon>'
	tmp += '		</Icon>'
	tmp += '	</IconStyle>'
	tmp += '	<BalloonStyle>'
	tmp += '		<text>$[description]</text>'
	tmp += '	</BalloonStyle>'
	tmp += '	<LineStyle>'
	tmp += '		<color>ffffff00</color>'
	tmp += '		<width>3</width>'
	tmp += '	</LineStyle>'
	tmp += '	<PolyStyle>'
	tmp += '		<color>70ffff00</color>'
	tmp += '		<fill>0</fill>'
	tmp += '	</PolyStyle>'
	tmp += '</Style>'

	for i in range(1,number_rows_input) :
		# POINT
		if (results_input[i][19] > 4) and (results_input[i][19] < 9) and (results_input[i][18] > 43) and (results_input[i][18] < 49) :
			tmp += '   <Placemark>\n' 
			tmp += '    <name>%s</name>\n' % ('P_' + results_input[i][0])
			tmp += '     <description>\n'
			tmp += '      <![CDATA[\n      <table border="1" >\n\n'
			tmp += '      <tr><td>Seq</td><td>%s</td>\n' % results_input[i][0]
			tmp += '      <tr><td>Date-Time</td><td>%s</td>\n' % results_input[i][1]
			tmp += '      <tr><td>Freq</td><td>%s [MHz]</td>\n' % results_input[i][2]
			tmp += '      <tr><td>Channel</td><td>%s</td>\n' % results_input[i][3]
			tmp += '      <tr><td>Modulation</td><td>%s</td>\n' % results_input[i][4]
			tmp += '      <tr><td>Bandwidth</td><td>%s [KHz]</td>\n' % results_input[i][5]
			tmp += '      <tr><td>SF</td><td>%s</td>\n' % results_input[i][6]
			tmp += '      <tr><td>Coding rate</td><td>%s</td>\n' % results_input[i][7]
			tmp += '      <tr><td>ADR</td><td>%s</td>\n' % results_input[i][8]
			tmp += '      <tr><td>RSSI</td><td>%s [dBm]</td>\n' % results_input[i][9]
			tmp += '      <tr><td>SNR</td><td>%s [dB]</td>\n' % results_input[i][10]
			tmp += '      <tr><td>Battery</td><td>%s</td>\n' % results_input[i][17]
			tmp += '      </table>\n'
			tmp += '      ]]>\n'
			tmp += '     </description>\n'
			tmp += '    <styleUrl>#pin_style</styleUrl>'
			tmp += '    <Point>\n'
			tmp += '     <coordinates>{LONGITUDE},{LATITUDE}</coordinates>\n'.format(LONGITUDE=results_input[i][19],LATITUDE=results_input[i][18])
			tmp += '    </Point>\n'
			tmp += '   </Placemark>\n'

		#LINE
		if (results_input[i][19] > 4) and (results_input[i][19] < 9) and (results_input[i][18] > 43) and (results_input[i][18] < 49) and (results_input[i+1][19] > 4) and (results_input[i+1][19] < 9) and (results_input[i+1][18] > 43) and (results_input[i+1][18] < 49) :

			if i < number_rows_input : 
				tmp += '<Placemark>'
				tmp += '	<name>%s</name>' % ('M_' + results_input[i][0])
				tmp += '	<styleUrl>#Sheet1Map2</styleUrl>'
				tmp += '	<LineString>'
				tmp += '		<tessellate>1</tessellate>'
				tmp += '		<coordinates>'
				tmp += '			{LONGITUDE_A},{LATITUDE_A} {LONGITUDE_B},{LATITUDE_B}'.format(LONGITUDE_A=results_input[i][19],LATITUDE_A=results_input[i][18],LONGITUDE_B=results_input[i+1][19],LATITUDE_B=results_input[i+1][18]) 
				tmp += '		</coordinates>'
				tmp += '	</LineString>'
				tmp += '</Placemark>'

	tmp += ' </Document>\n'
	tmp += '</kml>'

	with open(file_name_input,'w') as f:
		f.write(tmp)
	
	print 'Le fichier kml a ete cree. \n\tLoramote: ' + loramote_target + '\n\tGateway: ' + gateway_target + '\n'

	return 

def loramote_do_all(mote, gateway_target, number_packets, kml_icon):

	loramote_target = '00-00-00-00-' + mote

	# URL link for the data packets
	url_payload = 'http://iot.semtech.com/raw/motes/' + loramote_target + '/data/?count=' + str(number_packets) + '&gateway=' + gateway_target + '&submit=Download'
	csv_payload = 'loramote_' + loramote_target + '_gateway_'  +  gateway_target + '_data.csv'

	# URL link for the performance packets
	url_performance = 'http://iot.semtech.com/raw/motes/' + loramote_target + '/performance/?count=' + str(number_packets) + '&gateway=' + gateway_target + '&submit=Download'
	csv_performance = 'loramote_' + loramote_target + '_gateway_'  +  gateway_target + ' _performance.csv'
	 

	
	print '-----------------------------------------------------------'
	print '--------- LoRaMote cible: '+ loramote_target + ' ---------'
	print '--------- Gateway  cible: '+ gateway_target + ' ---------'
	print '-----------------------------------------------------------'


	print '\nOn comence le telechargement du fichier payload' + '\n\t LoRaMote cible: ' + loramote_target + '\n\t Gateway: ' + gateway_target + '\n\t Nb packets: ' + str(number_packets)  
	urllib.urlretrieve(url_payload, csv_payload )
	print '\n\tLe fichier Payload a ete telecharge. \n'

	print '\nOn comence le telechargement du fichier performance' + '\n\t LoRaMote cible: ' + loramote_target + '\n\t Gateway: ' + gateway_target + '\n\t Nb packets: ' + str(number_packets)
	urllib.urlretrieve(url_performance, csv_performance)
	print '\n\tLe fichier Performance a ete telecharge. \n'

	number_packets = get_numberPackets(csv_payload) # Correct the number of packets gathered from SEMTECH SERVER


	selection = select_desired_sequence(csv_payload, loramote_target, gateway_target)
	last_line = int(selection[3])
	first_line =  int(selection[4])
	total_packets = last_line - first_line + 1


	results = results_csv_generator(first_line, last_line, number_packets, csv_payload, csv_performance, loramote_target, gateway_target)
	
	kml_generator(results, total_packets, kml_icon , loramote_target, gateway_target)

	print '-----------------------------------------------------------\n\n'
	return

####################################################################################################
####################################################################################################
if __name__ == "__main__":
    mote = str(sys.argv[1])
    gateway_target = str(sys.argv[2])
    number_packets = int(sys.argv[3])
    kml_icon = int(sys.argv[4])

    loramote_do_all(mote, gateway_target, number_packets, kml_icon)