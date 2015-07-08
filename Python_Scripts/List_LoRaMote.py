# Python 2 code
import os

#mote = '00-30-35-83'
mote = raw_input('Donnez l-addrese MAC du LoRaMote ciblee, dans le format suivant XX-XX-XX-XX: \n\t')


gateway_target_1 = 'AA-55-5A-00-08-05-00-BC'
gateway_target_2 = 'AA-55-5A-00-08-05-02-67'
gateway_target_3 = 'AA-55-5A-00-08-05-03-0E'
gateway_target_4 = 'AA-55-5A-00-08-04-00-1B'
gateway_target_5 = 'FF-AA-00-11-FF-EE-12-34'
gateway_target_6 = 'AA-55-5A-00-08-05-00-C8'
gateway_target_7 = 'AA-55-5A-00-08-05-02-6D'
gateway_target_8 = 'AA-55-5A-00-08-05-03-5D'
#gateway_target_9 = 'AA-55-5A-00-08-05-01-50'
#gateway_target_10 = 'AA-55-5A-00-08-05-01-50'


#print '\n\n\t VERIFIER QUE LE NOMBRE DE PAQUETS A TELECHARGER SOI\n\t AU MAXIMUM LE NOMBRE DE PAQUETS DISPONIBLES \n\t DANS LE SERVEUR !!! \n\n'

number_packets   = raw_input('Donnez le nombre de paquets a recuperer pour chaque Gateway\n\t')
#number_packets_1 = raw_input('Donnez le nombre de paquets a recuperer pour\n\t Gateway: ' + gateway_target_1 + '\n\t')
#number_packets_2 = raw_input('Donnez le nombre de paquets a recuperer pour\n\t Gateway: ' + gateway_target_2 + '\n\t')
#number_packets_3 = raw_input('Donnez le nombre de paquets a recuperer pour\n\t Gateway: ' + gateway_target_3 + '\n\t')
#number_packets_4 = raw_input('Donnez le nombre de paquets a recuperer pour\n\t Gateway: ' + gateway_target_4 + '\n\t')

# python TEST\LoRaMote_results.py loramote gateway number_packets
# python TEST\LoRaMote_results.py 00-30-35-83 AA-55-5A-00-08-05-00-BC 200


#os.system('python TEST\LoRaMote_results.py '+ mote + ' ' + gateway_target_1 + ' ' + str(number_packets_1) + ' ' + str(1))

#os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_1 + ' ' + number_packets_1 + ' ' + str(1))
#os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_2 + ' ' + number_packets_2 + ' ' + str(2))
#os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_3 + ' ' + number_packets_3 + ' ' + str(3))
#os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_4 + ' ' + number_packets_4 + ' ' + str(4))

os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_1 + ' ' + number_packets + ' ' + str(1))
os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_2 + ' ' + number_packets + ' ' + str(2))
os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_3 + ' ' + number_packets + ' ' + str(3))
os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_4 + ' ' + number_packets + ' ' + str(4))
os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_5 + ' ' + number_packets + ' ' + str(5))
os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_6 + ' ' + number_packets + ' ' + str(6))
os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_7 + ' ' + number_packets + ' ' + str(7))
os.system('python Results_LoRaMote.py '+ mote + ' ' + gateway_target_8 + ' ' + number_packets + ' ' + str(8))