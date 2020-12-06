# Note:
# epel-release-latest-8.noarch.rpm needs to be present at /root/Downloads in the controler system
# jdk-8u171-linux-x64.rpm and hadoop-1.2.1-1.x86_64.rpm needs to be present at /root/Downloads/hadoop in the controler system

import os

def config_yum():
    sys = int(input("""Where do you want to configure yum:
    Press 1 for local system
    Press 2 for remote system
    Enter your choice here: """))

    if sys == 1:
        cmd = "rpm -ivh /root/Downloads/epel-release-latest-8.noarch.rpm"
        os.system(cmd)
    elif sys == 2:
        total_remote_sys = int(input("Enter the number of remote systems: "))
        for i in range(total_remote_sys):
            remote_sys_IP = input("Enter Remote System's IP: ")
            cmd = "scp /root/Downloads/epel-release-latest-8.noarch.rpm root@" + remote_sys_IP + ":/root/Downloads/"
            os.system(cmd)
            cmd = "ssh root@" + remote_sys_IP + " rpm -ivh /root/Downloads/epel-release-latest-8.noarch.rpm"
            os.system(cmd)
    else:
        print("Invalid Input")


def config_hadoop():
    nn = input("Enter Name Node's IP: ")
    cmd = "scp -r /root/Downloads/hadoop root@" + nn + ":/root/Downloads/"
    os.system(cmd)
    cmd = "ssh root@" + nn + " rpm -ivh /root/Downloads/hadoop/jdk-8u171-linux-x64.rpm"
    os.system(cmd)
    cmd = "ssh root@" + nn + " rpm -ivh /root/Downloads/hadoop/hadoop-1.2.1-1.x86_64.rpm  --force"
    os.system(cmd)

    dnn = int(input("Number of Data Nodes: "))
    for i in range(dnn):
        dn = input("Enter Data Node {}'s IP: ", i)
        cmd = "scp -r /root/Downloads/hadoop root@" + dn + ":/root/Downloads/"
        os.system(cmd)
        cmd = "ssh root@" + dn + "rpm -ivh /root/Downloads/hadoop/jdk-8u171-linux-x64.rpm"
        os.system(cmd)
        cmd = "ssh root@" + dn + "rpm -ivh /root/Downloads/hadoop/hadoop-1.2.1-1.x86_64.rpm  --force"
        os.system(cmd)

while True:

    print("""Welcome
    Enter your choice:
    Press 1: To configure yum repository
    Press 2: To setup a hadoop cluster

    """)

    user_choice1 = int(input("Enter your choice here: "))
    
    if user_choice1 == 1:
        config_yum()   

    elif user_choice1 == 2:
        config_hadoop()
    
    # add extra functionalities here inside elif

    else:
        print("Invalid Input")
    
    choice_to_loop = input("Press 'y' to continue or 'n' to quit: ")
    if choice_to_loop != 'y' and choice_to_loop != 'Y':
        break