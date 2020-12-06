import os

os.system("tput setaf 3")
os.system("tput setaf 7")

while True:
	os.system("clear")
	print("""Welcome to AWS automation 
	press1: To install AWS CLI
	press2:	To check the AWS CLI version
	press3: To configure ASW CLI
	press4: To describe all instances
	press5: To describe a specific instance
	press6: To create an EC2 instance
	press7: To start an EC2 instance
	press8: To stop an EC2 instance
	press9: To create an EBS volume
	press10: To attach an EBS volume
	""")

	ch = int(input("enter your choice here:"))
	
	if ch==1:
		os.system("pip3 install awscli --upgrade --user")

	elif ch==2:
		os.system("aws --version")

	elif ch==3:
		os.system("aws configure")

	elif ch==4:
		os.system("aws ec2 describe-instances")

	elif ch==5:
		ins_id = input("enter the instance id: ")
		os.system("aws ec2 describe-instance-status --instance-id {}".format(ins_id))

	elif ch==6:
		img_id = input("Enter image ID: ")
		ins_type = input("Enter instance type: ")
		cnt = input("Enter the number of instances you want to launch: ")
		key_nm = input("Enter AWS key name: ")
		sec_id = input("Enter security group ids: ")
		sub_id = input("Enter subnet id: ")
		
		os.system("asw ec2 run-instances  --image-id {} --instance-type {} --count {} --key-name {} --security-group-ids {} --subnet-id {}".format(img_id , ins_type , cnt , key_nm , sec_id , sub_id))

	elif ch==7:
		ins_id = input("Enter instance Id: ")
		os.system(" aws ec2 start-instances --instance-ids {} ".format(ins_id))

	elif ch==8:
		ins_id = input("Enter instance Id: ")
		os.system(" aws ec2 stop-instances --instance-ids {} ".format(ins_id))

	elif ch==9:
		size = input("Enter the size of stotage in GB: ")
		vol_type = input("Enter volume type: ")
		av_zone = input("Enter the availability zone: ")
		os.system("aws ec2 create-volume --size {} --volume-type {} --availability-zone {}".format(size , vol_type , av_zone))

	elif ch==10:
		vol_id = input("Enter your EBS volume Id: ")
		ins_id = input("Enter your EC2 instance Id: ")
		dev_name = input("Enter your EBS storage name: ")
		os.system("aws ec2 attach-volume  --volume-id {}  --instance-id {} --device {}".format(vol_id , ins_id , dev_name)
		)
	
	input("press enter to continue to menu...")
