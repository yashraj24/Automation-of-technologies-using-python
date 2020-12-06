import os

def docker():
	print("Welcome to Docker services")
	
	while(1):
		print("1.Start Docker Services \n2.Stop Docker Services \n3.Launch OS container \n4.Pull OS Image from Docker \n5.Check Images Available \n6.Exit Services /n")
		n = int(input())
		if(n==1):
			cmd = "systemctl start docker"
			os.system(cmd)
			print("Your docker service succefully started")
		elif(n==2):
			cmd = "systemctl stop docker"
			os.system(cmd)
			print("Your docker service succefully stopped")
		elif(n==3):
			print("OS Available")
			cmd="docker images"
			os.system(cmd)
			print("Enter the OS you want to launch")
			OS= input()
			print("Enter the OS name")
			OS_name=input()
			cmd="docker run -it --name {} {}".format(OS_name,OS)
			os.system(cmd)
			print("OS Launched Successfully") 
		elif(n==4):
			print("Enter the OS name you want to install")
			OS = input()
			cmd="docker pull {}".format(OS)
			os.system(cmd)
		elif(n==5):
			print("OS Available")
			cmd="docker images"
			os.system(cmd)
		elif(n==6):
			print("Thankyou for using docker services")
			break
docker()
