import os
import time
import subprocess

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


def config_yum():
    sys = int(input("""Where do you want to configure yum:
    Press 1 for local system
    Press 2 for remote system

    Enter your choice here: """))

    if sys == 1 or sys == 2:
        print('--------------Updating python3 library (gdown)--------------')
        os.system('pip3 install gdown')
        print('''\n--------------Downloading repo data. Please wait--------------
It may take a bit longer, please don't quit
''')
        os.system('gdown --id 1GAKatKIF00qdBIfkpr6N4tT5H3AYsu8y')

    if sys == 1:
        print('--------------Updating yum repository--------------')
        cmd = "rpm -ivh epel-release-latest-8.noarch.rpm"
        os.system(cmd)
        
    elif sys == 2:
        total_remote_sys = int(input("Enter the number of remote systems: "))
        for i in range(total_remote_sys):
            remote_sys_IP = input("Enter Remote System's IP: ")
            cmd = "scp epel-release-latest-8.noarch.rpm root@" + remote_sys_IP + ":/root"
            os.system(cmd)
            print('\n--------------Updating yum repository--------------\n')
            cmd = "ssh root@" + remote_sys_IP + " rpm -ivh /root/epel-release-latest-8.noarch.rpm"
            os.system(cmd)
    else:
        print("Invalid Input")


def hadoop_pyscript(ip, hdfs_name_tag, hdfs_value_tag, node_type, dn_no, curr_ip):
    ip = '"' + ip + '"'
    line_8 = 'nn_ip = ' + ip + '\n'
    line_9 = 'file_handling("' + hdfs_name_tag + '", "'+ hdfs_value_tag + '", "hdfs-site.xml")\n'
    pyscript = ['import os\n', 
    'os.system("pip3 install gdown")\n', 
    'os.system("gdown --id 1S7rpt9ituQQF8R0kYxWYMhfsmWPL3BOe")\n', 
    'os.system("gdown --id 15M3sTqRfiP8WKsHFNOcfK9IggRsd5ZEu")\n', 
    'os.system("rpm -ivh /root/jdk-8u171-linux-x64.rpm")\n', 
    'os.system("rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm --force")\n', 
    '\n', 
    'def file_handling(name_tag, value_tag, file_name):\n', 
    '\tname_tag = "<name>" + name_tag + "</name>\\n"\n', 
    '\tvalue_tag = "<value>" + value_tag + "</value>\\n"\n', 
    '\tdir = "/etc/hadoop/" + file_name\n', 
    '\n', 
    '\thdfs_file_lines = [\'<?xml version="1.0"?>\\n\', \'<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\\n\',\n', 
    '\t\'\\n\', \'<!-- Put site-specific property overrides in this file. -->\\n\', \'\\n\', \'<configuration>\\n\', \'<property>\\n\',\n', 
    '\tname_tag, value_tag, \'</property>\\n\', \'</configuration>\\n\']\n', 
    '\n', 
    '\thdfs_file = open(dir, "w")\n', 
    '\thdfs_file.writelines(hdfs_file_lines)\n', 
    '\thdfs_file.close()\n'
    '\n',
    line_8, 
    line_9, 
    'value_tag = "hdfs://" + nn_ip + ":9001"\n', 
    'file_handling("fs.default.name", value_tag , "core-site.xml")\n', 
    '\n']

    if node_type == 'N':
        pyscript.append('\nos.system("rm -rf /nn")')
        pyscript.append('\nos.system("mkdir /nn")')
        pyscript.append('\nos.system("hadoop namenode -format")')
        pyscript.append('\nos.system("systemctl stop firewalld")')
        pyscript.append('\nos.system("hadoop-daemon.sh start namenode")')
    elif node_type == 'D':
        cmd = 'os.system("rm -rf /dn' + str(dn_no) + '")'
        pyscript.append(cmd)
        cmd = '\nos.system("mkdir /dn'+ str(dn_no) +'")'
        pyscript.append(cmd)
        pyscript.append('\nos.system("systemctl stop firewalld")')
        pyscript.append('\nos.system("hadoop-daemon.sh start datanode")')
    elif node_type == 'C':
        pyscript.pop(20)
        pyscript.append('\nos.system("systemctl stop firewalld")')

    hdfs_file = open('imp.py', 'w')
    hdfs_file.writelines(pyscript)
    hdfs_file.close()

    cmd = "scp imp.py root@" + curr_ip + ":/root"
    os.system(cmd)
    cmd = "ssh root@" + curr_ip + " python3 /root/imp.py"
    os.system(cmd)


def config_hadoop():
    nn = input("Enter Name Node's IP: ")
    hadoop_pyscript(nn, 'dfs.name.dir', '/nn', 'N', 0, nn)

    dnn = int(input("Number of Data Nodes: "))
    for i in range(dnn):
        dn = input("Enter Data Node {}'s IP: ".format(i+1))
        dn_dir = '/dn' + str(i+1)
        hadoop_pyscript(nn, 'dfs.data.dir', dn_dir, 'D', i+1, dn)

    client = int(input("Number of Client Nodes: "))
    for i in range(client):
        client_ip = input("Enter Client {}'s IP: ".format(i+1))
        hadoop_pyscript(nn, '', '', 'C', 0, client_ip)


def hadoop_client_services(ip):

    script_lines = ['import os\n', 
    'while True:\n', 
    '\tchoice = int(input(\'\'\'Available hadoop client services:\n', 
    '\tPress 1: To see dfs report\n', 
    '\tPress 2: To list files in cluster\n', 
    '\tPress 3: To read a file\n', 
    '\tPress 4: To upload a file\n', 
    '\tPress 5: To exit\n', 
    '\n', 
    '\tEnter your choice here: \'\'\'))\n', 
    '\n', 
    '\tif choice == 1:\n', 
    '\t\tos.system("hadoop dfsadmin -report")\n', 
    '\telif choice == 2:\n', 
    '\t\tdir = input("Directory (default /): ")\n', 
    '\t\tif len(dir) == 0:\n', 
    '\t\t\tdir = "/"\n', 
    '\t\tcmd = "hadoop fs -ls " + dir\n', 
    '\t\tos.system(cmd)\n', 
    '\telif choice == 3:\n', 
    '\t\tfile_name = input("Enter file name with extension and full path in the cluster: ")\n', 
    '\t\tcmd = "hadoop fs -cat " + file_name\n', 
    '\t\tos.system(cmd)\n', 
    '\telif choice == 4:\n', 
    '\t\tfile_name = input("Enter local file name with extension and it\'s full path in the local system: ")\n', 
    '\t\tblock_size = int(input("Block size (default 64MB): "))\n', 
    '\t\tif len(block_size) == 0:\n', 
    '\t\t\tblock_size = 67108864\n', 
    '\t\telse:\n', 
    '\t\t\tblock_size = block_size * 1048576\n', 
    '\t\tdir = input("Directory path where you want to upload (default /): ")\n', 
    '\t\tif len(dir) == 0:\n', 
    '\t\t\tdir = "/"\n', 
    '\t\tcmd = "hadoop fs -Dfs.block.size=" + block_size + " -put " + file_name + " " + dir\n', 
    '\telif choice == 5:\n', 
    '\t\tbreak\n', 
    '\telse:\n', 
    '\t\tprint("Invalid Choice\\n")\n', 
    '\tinput("Press enter to continue: ")\n']

    client_script = open('hc_spript.py', 'w')
    client_script.writelines(script_lines)
    client_script.close()

    print('\n--------------Establishing Connection--------------\n')
    cmd = "scp hc_spript.py root@" + ip + ":/root"
    os.system(cmd)
    cmd = "ssh root@" + ip + " python3 /root/hc_spript.py"
    os.system(cmd)
    

def hapoop_services():
    choice = int(input('''Available hadoop services:
    Press 1: To setup a cluster
    Press 2: To use WebUI
    Press 3: To access hadoop client services
    
    Enter your choice here: '''))

    if choice == 1:
        config_hadoop()

    elif choice == 2:
        nn_IP = input('Enter the IP of your cluster\'s Name Node: ')
        cmd = 'firefox ' + nn_IP + ':50070'
        os.system(cmd) 

    elif choice == 3:
        cli_ip = input('\tEnter the IP of the Client: ')
        hadoop_client_services(cli_ip)

    else:
        print('Invalid Choice')


def aws_cli():
	while True:
		os.system("clear")
		print("""Welcome to AWS automation 
		press 1: To install AWS CLI
		press 2: To check the AWS CLI version
		press 3: To configure ASW CLI
		press 4: To describe all instances
		press 5: To describe a specific instance
		press 6: To create an EC2 instance
		press 7: To start an EC2 instance
		press 8: To stop an EC2 instance
		press 9: To create an EBS volume
		press 10: To attach an EBS volume
		press 11: Exit
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
		elif ch==11:
			exit()
		
		input("press enter to continue to AWS CLI menu")
        
##################################Ansible#########################################

def ansible_config():
    os.system('rm -rf /etc/ansible /root/ansible_inventory')
    os.system('mkdir /etc/ansible')
    os.system('mkdir /root/ansible_inventory')
    os.system('touch /root/ansible_inventory/ip.txt')
    fh = open('/etc/ansible/ansible.cfg','w')
    fh.write('[defaults]\ninventory = /root/ansible_inventory/ip.txt\nhost_key_checking = false \n')
    fh.close()

def write_inventory(group_name, mode):

    ip_address = input("Enter IP address of client device: ")    
    username = input("Enter the user name of client device: ")
    password = input("Enter the password of client device: ")

    file_lines = ['{}  ansible_ssh_user={}  ansible_ssh_pass={}\n'.format(ip_address , username , password)]

    if mode == 'N':
        fh = open('/root/ansible_inventory/ip.txt', 'a+')
        fh.write(group_name)
        fh.write(file_lines[0])
        fh.close()
    elif mode == 'E':
        fh = open('/root/ansible_inventory/ip.txt', 'r')
        all_lines = fh.readlines()
        fh.close()

        is_there = 0
        for i, line in enumerate(all_lines):
            if group_name == line:
                is_there = 1
                all_lines.insert(i+1, file_lines[0])
                break
        if is_there == 1:
            fh = open('/root/ansible_inventory/ip.txt', 'w+')
            fh.writelines(all_lines)
            fh.close()
        else:
            print('\nGroup not found')


def file_handling_ansible():
    group = int(input('''Press 1: To create a new group
Press 2: To add to an existing group

Enter your choice here: '''))
    group_name = input('Enter the group name without using "[]": ')
    group_name = '[' + group_name + ']\n'

    if group == 1:
        write_inventory(group_name, 'N')

    elif group == 2:
        write_inventory(group_name, 'E')

    else:
        print('Invalid Choice')

def ansible_services():
	while True:
		print("""
ANSIBLE OPERATIONS

Press 1: TO install ansible
Press 2: TO COnfigure ansible
Press 3: TO enter IP, username and password of the system on which you want run commands using ansible
Press 4: Enter your ansible commands
Press 5: To exit from ansible menu
""")
		ch = int(input("Enter your choice: "))
		if ch == 1:
			os.system ("pip3 install ansible")
		elif ch == 2:
			ansible_config()
		elif ch == 3:
			file_handling_ansible()
		elif ch == 4:
			cmd = input("Enter your ansible commands: ")
			os.system(cmd)
		elif ch == 5:
			break
		
		input("\nPress enter to continue: ")
	
###########################################################################

def lvm_services():
    while True:
        print('''Available LVM services
        
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
        Press 0: To Exit.
        
    [NOTE : Make sure to attach extra volume to your system  to work on logical volume management]	
		''')
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
            break
        
        else:
            print("Invalid input")
            
        input("\n\tPress enter to continue to menu")
	

while True:

    print("""Welcome
    Enter your choice:
    Press 1: To configure yum repository
    Press 2: To access hadoop services
    Press 3: To access AWS CLI
    Press 4: To acess docker services
    Press 5: To access ansible services
    Press 6: To access LVM services
    """)

    user_choice1 = int(input("Enter your choice here: "))
    
    if user_choice1 == 1:
        config_yum()   

    elif user_choice1 == 2:
        hapoop_services()
    
    elif user_choice1 == 3:
        aws_cli()

    elif user_choice1 == 4:
        docker()

    elif user_choice1 == 5:
        ansible_services()
	
    elif user_choice1 == 6:
        lvm_services()

    # add extra functionalities here inside elif

    else:
        print("Invalid Input")
    
    choice_to_loop = input("Press 'y' to continue or 'n' to quit: ")
    if choice_to_loop != 'y' and choice_to_loop != 'Y':
        break
