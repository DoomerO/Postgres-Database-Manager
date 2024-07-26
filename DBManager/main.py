import os
import psycopg2
import json

localcolor = [
                '\033[31m', #red 0
                '\033[32m', #green 1
                '\033[0m',  #reset 2
                '\033[33m', #yellow 3
                '\033[34m', #blue 4
                '\033[91m', #red bright 5
                '\033[92m', #green bright 6
                '\033[93m', #yellow bright 7
                '\033[94m', #blue bright 8
                '\033[97m', #white bright 9
                '\033[44m' #blue bright bg 10
            ]
conn = 0
cur = 0

def getConfig():
    with open('./config/config.json', 'r') as file:
        return json.load(file)

config = getConfig()

def mainPrint():
    print(f'{localcolor[10]}{localcolor[9]}=============================PG MANAGER===============================\n{localcolor[2]}')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear()
    mainPrint()
    setup()

def yorN(msg):
    while True:
        opt = input(f'{msg}? [y/n]:');
        if (opt not in "YySsNn"):
            opt = input('Type a value corresponding to [y/n]:')
        else:
            break;

    return True if opt in "YySs" else False

def customConfig():
    print(f'{localcolor[7]}INFO -> Type "def" to use default{localcolor[2]}\n')
    host = input('Host:')
    port = input('Port:')
    user = input('User:')
    password = input('Password:')
    
    if (host == "def"): host = config['connection']['host']
    if (port == "def"): port = config['connection']['port']
    if (user == "def"): user = config['connection']['user']
    if (password == "def"): password = config['connection']['password']
    
    connectDB(host, port, password, user)

def setup():
    if (yorN("Do you wish to use the default configurations")):
        print(config['connection']['host'])
        connectDB(config['connection']['host'], config['connection']['port'], config['connection']['password'], config['connection']['user'])
    else:
        clear();
        mainPrint();
        customConfig();

def connectDB(host, port, password, user):
    clear()
    mainPrint()
    try :
        connect = psycopg2.connect(f'host={host} port={port} password={password} user={user}');
        conn = connect
        print(f'{localcolor[6]}Connection Established!!{localcolor[2]}')
    except Exception as e:
        print(f'{localcolor[5]}Connection Failed...{localcolor[2]}\n')
        print(f'{localcolor[5]}ERROR ->{localcolor[7]} {e}{localcolor[2]}')


main()