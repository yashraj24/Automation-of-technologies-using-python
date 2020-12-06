import os

os.system("tput setaf 3")
os.system("tput setaf 7")


def ansible_config():
    os.system('rm -rf /etc/ansible /root/ansible_inventory')
    os.system('mkdir /etc/ansible')
    os.system('mkdir /root/ansible_inventory')
    os.system('touch /root/ansible_inventory/ip.txt')
    fh = open('/etc/ansible/ansible.cfg','w')
    fh.write('[defaults]\ninventory = /root/ansible_inventory/ip.txt\nhost_key_checking = false \n')
    fh.close()

def file_handling_ansible():
    group = int(input('''Press 1 to create a new group: 
    \t\t\t\tOr
    \tPress 2 to add to an existing group:'''))
    group_name = input('Enter the group name without using "[]": ')
    group_name = '[' + group_name + ']\n'

    if group == 1:
        write_inventory(group_name, 'N')

    elif group == 2:
        write_inventory(group_name, 'E')
        

def write_inventory(group_name, mode):

    ip_address = input("Enter IP address of client device: ")    
    username = input("Enter the user name of client device: ")
    password = input("Enter the password of client device: ")

    file_lines = ['{}  ansible_ssh_user={}  ansible_ssh_pass={}\n'.format(ip_address , username , password)]

    if mode == 'N':
        fh = open('/root/ansible_inventory/ip.txt', 'a+')
        fh.write(group_name)
        fh.writelines(file_lines)
        fh.close()
    elif mode == 'E':
        fh = open('/root/ansible_inventory/ip.txt', 'r')
        all_lines = fh.readlines()
        fh.close()
        for i, line in enumerate(all_lines):
            if group_name == line:
                all_lines.insert(i+1, file_lines[0])
                break
        fh = open('/root/ansible_inventory/ip.txt', 'w')
        fh.writelines(all_lines)
        fh.close()

while True:
    print("""
        ANSIBLE OPERATIONS

        press 1: TO install ansible
        press 2: TO COnfigure ansible
        press 3: TO enter IP, username and password of the system on which you want run commands using ansible
        press 4: Enter your ansible commands
        press 5: To exit from ansible menu
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
	    exit
	
    input("press enter to continue: ")
