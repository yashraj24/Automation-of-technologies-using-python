import os
import time
import subprocess

os.system("tput setaf 3")
os.system("tput setaf 7")

while True:

	print("""
		Press 1: To see available disks.
		Press 2: To Create Physical Volume.		  
		Press 3: To Display Physical Volume.	
		Press 4: To Creating Volume Group.		
		Press 5: To Display List Of Volume Group.	
		Press 6: To Create partition Of volume Group.
		Press 7: To Format Created partition.
		Press 8: To Mount The partiton On Folder.
		Press 9: To Extend The volume group.
		Press 10: To Extend The Logical volume.
		press 0: To Exit. 	

[NOTE : Make sure to attach extra volume to your system  to work on logical volume management]	
		""")
		

	ch = int(input("Enter Your Choice : "))

	if ch == 1:
		op = subprocess.getstatusoutput("fdisk -l | less")
		print("\n")			
		print(op[1])

	elif ch == 2:
		loc = input("Enter Disk Location : ")
		op = subprocess.getstatusoutput("pvcreate {}".format(loc))
		if op[0] == 0:
			print("\n{}\n".format(op[1]))
		else:
			print("\n{}\n".format(op[1]))			
	
	elif ch == 3:
		os.system("pvdisplay")
		time.sleep(5)
		os.system("clear")

	elif ch == 4:
		vgName = input("Enter Volume Group Name (it must be unique in local system) : ")
		loc = input("Location of Physical volume : ")
		op = subprocess.getstatusoutput("vgcreate {} {}".format(vgName,loc))
			

	elif ch == 5:
		os.system("vgdisplay | less")

	elif ch == 6:
		size =  input("Enter the Size of Logical Partition like (+T,+G,+M,+k) : ")
		lvname = input("Enter the Logical Volume Name : ")
		vgn =  input("Enter Volume Group name : ")
		os.system("lvcreate --size {} --name {} {}".format(size,lvname,vgn))

	elif ch == 7:
		vg = input("Enter The Volume Group Name : ")
		lv = input("Enter The Logical Volume Name : ")
		os.system("mkfs /dev/{}/{}".format(vg,lv))

	elif ch == 8:
		folder = input("Enter Folder Name : ")
		os.system("mkdir /{}".format(folder))
		vg = input("Enter The Name of Volume Group : ")
		lv = input("Enter The Name of Logical Volume : ")
		os.system("mount /dev/{}/{}  /{} ".format(vg,lv,folder))

	elif ch == 9:
		vg = input("Enter The Name of Volume Group : ")
		evg = input("Enter The New Disk Path like (/dev/xyz) : ")
		os.system("vgextend {} {}".format(vg,evg))
		time.sleep(5)

	elif ch == 10:
		elv = input("Enter The Size like(+1G,+1M...) : ")
		vg = input("Enter The Volume Group Name : ")
		lv = input("Enter The Logical Volume Name : ")
		os.system("Extend --size {} /dev/{}/{} ".format(elv,vg,lv))

	elif ch == 0 :
		 exit
			
	else:
		print("Invalid input")
	
	input("press enter to continue to menu")

	
