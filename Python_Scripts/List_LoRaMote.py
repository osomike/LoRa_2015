# Python 2 code
import os

#mote = '00-30-35-83'
mote = raw_input('Donnez l-addrese MAC du LoRaMote ciblee, dans le format suivant XX-XX-XX-XX: \n\t')

gateway_target_1 = 'AA-55-5A-00-08-05-00-BC'
gateway_target_2 = 'FF-AA-00-11-FF-EE-12-34'
gateway_target_3 = 'AA-55-5A-00-08-05-02-67'
gateway_target_4 = 'AA-55-5A-00-08-04-00-1B'

#print '\n\n\t VERIFIER QUE LE NOMBRE DE PAQUETS A TELECHARGER SOI\n\t AU MAXIMUM LE NOMBRE DE PAQUETS DISPONIBLES \n\t DANS LE SERVEUR !!! \n\n'

#number_packets_1 = 500
number_packets_1 = raw_input('Donnez le nombre de paquets a recuperer pour\n\t Gateway: ' + gateway_target_1 + '\n\t')
number_packets_2 = raw_input('Donnez le nombre de paquets a recuperer pour\n\t Gateway: ' + gateway_target_2 + '\n\t')
number_packets_3 = raw_input('Donnez le nombre de paquets a recuperer pour\n\t Gateway: ' + gateway_target_3 + '\n\t')
number_packets_4 = raw_input('Donnez le nombre de paquets a recuperer pour\n\t Gateway: ' + gateway_target_4 + '\n\t')

# python TEST\LoRaMote_results.py loramote gateway number_packets
# python TEST\LoRaMote_results.py 00-30-35-83 AA-55-5A-00-08-05-00-BC 200


#os.system('python TEST\LoRaMote_results.py '+ mote + ' ' + gateway_target_1 + ' ' + str(number_packets_1) + ' ' + str(1))

os.system('python TEST\LoRaMote_results.py '+ mote + ' ' + gateway_target_1 + ' ' + number_packets_1 + ' ' + str(1))
os.system('python TEST\LoRaMote_results.py '+ mote + ' ' + gateway_target_2 + ' ' + number_packets_2 + ' ' + str(2))
os.system('python TEST\LoRaMote_results.py '+ mote + ' ' + gateway_target_3 + ' ' + number_packets_3 + ' ' + str(3))
os.system('python TEST\LoRaMote_results.py '+ mote + ' ' + gateway_target_4 + ' ' + number_packets_4 + ' ' + str(4))

