from netaddr import *
mac = EUI('EC:FA:BC:2E:EE:F2')
print (mac)
print(str(mac))
print(int(mac))
mac2 = EUI(260561643171570)
print (mac2)
if mac == mac2:
	print ("Match")
