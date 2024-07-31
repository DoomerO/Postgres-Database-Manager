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
                '\033[96m', #cyan bright 10
                '\033[44m', #blue bright bg 11
                '\033[43m' #yellow bright bg 12
            ]
conn = None
cur = None
closeApp = False

def getConfig():
    with open('./config/config.json', 'r') as file:
        return json.load(file)

def getLang(arg):
    with open(f'./langs/{arg}.json', 'r') as file:
        return json.load(file)

config = getConfig()

lang = getLang(config['lang'])

def mainPrint():
    print(f'{localcolor[11]}{localcolor[9]}=============================PG MANAGER===============================\n{localcolor[2]}')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear()
    mainPrint()
    mainMenu()
    
def mainMenu():
    while True:
        clear()
        mainPrint()
        print(f'{localcolor[8]}-->{lang['mainMenuTitle']}{localcolor[2]}\n')
        print(f'{lang['mainMenuOpts']['connect']}\n')
        print(f'{lang['mainMenuOpts']['lang']}\n')
        print(f'{lang['mainMenuOpts']['end']}\n')
        while True: 
            opt = input(f'{lang['mainMenuSelect']}')
            if(opt == '1'):
                setup()
                break
            if(opt == '2'):
                setLangMenu()
                break
            if(opt == '3'):
                global closeApp 
                closeApp = True
                print(f'\n{localcolor[7]}###{lang['closeMsg']}###{localcolor[2]}\n')
                if conn:
                    conn.close()
                if cur:
                    conn.close()
                break
            else:
                print(f'{localcolor[7]}{lang['mainMenuAllert']}{localcolor[2]}')
        if closeApp:
            break
        
def yorN(msg):
    while True:
        opt = input(f'{msg}? [y/n]:')
        if (opt not in "YySsNn"):
            opt = input(lang['yesOrNo'])
        else:
            break

    return True if opt in "YySs" else False

def customConfig():
    print(f'{localcolor[7]}INFO -> {lang['connectConfigMsg']}{localcolor[2]}\n')
    host = input(lang['connectionInfo']['host'])
    port = input(lang['connectionInfo']['port'])
    user = input(lang['connectionInfo']['user'])
    password = input(lang['connectionInfo']['password'])
    dbname = input(lang['connectionInfo']['dbname'])
    
    if (host == "def"): host = config['connection']['host']
    if (port == "def"): port = config['connection']['port']
    if (user == "def"): user = config['connection']['user']
    if (password == "def"): password = config['connection']['password']
    if (dbname == "def"): dbname = config['connection']['dbname']
    
    connectDB(host, port, password, user, dbname)

def setup():
    clear()
    mainPrint()
    print(f'{localcolor[8]}-->{lang['connectTitle']}{localcolor[2]}\n')
    if (yorN(lang['configConfirm'])):
        print(config['connection']['host'])
        connectDB(config['connection']['host'], config['connection']['port'], config['connection']['password'], config['connection']['user'], config['connection']['dbname'])
    else:
        clear()
        mainPrint()
        customConfig()

def connectDB(host, port, password, user, dbname):
    clear()
    mainPrint()
    global conn, cur
    try :
        connect = psycopg2.connect(f'host={host} port={port} password={password} user={user} dbname={dbname}')
        conn = connect
        cur = conn.cursor()
        print(f'{localcolor[6]}{lang['connectSuccess']}{localcolor[2]}')
        input(lang['easyWayOut'])
        oprtMenu()
    except Exception as e:
        print(f'{localcolor[5]}{lang['connectFail']}{localcolor[2]}\n')
        print(f'{localcolor[5]}ERROR ->{localcolor[7]} {e}{localcolor[2]}')
        input(lang['easyWayOut'])

def setLangMenu():
    clear()
    mainPrint()
    global lang
    print(f'{localcolor[8]}-->{lang['langConfigTitle']}{localcolor[2]}\n')
    print(f'{localcolor[7]}{lang['langsCode']['english']}{localcolor[2]}\n')
    print(f'{localcolor[7]}{lang['langsCode']['portuguese']}{localcolor[2]}\n')
    while True: 
        opt = input(f'{lang['langConfig']}{localcolor[2]}\n')
        if(opt == '1'):
            lang = getLang('english')
            break
        elif (opt == '2'):
            lang = getLang('portuguese')
            break
        else:
            print(f'{localcolor[5]}{lang['langsCode']['error']}{localcolor[2]}\n')
            
def oprtMenu():
    while True:
        clear()
        mainPrint()
        global cur, conn
        error = False
        print(f'{localcolor[8]}-->{lang['oprtTitle']}{localcolor[2]}\n')
        print(f'{localcolor[7]}INFO -> {lang['oprtMsgBack']}{localcolor[2]}\n')
        oprt = input(f'\n{lang['oprtMsg']}\n{localcolor[10]}')
        if (oprt in "escext"):
            conn.close()
            cur.close()
            break
        print(localcolor[2])
        try:
            cur.execute(oprt)
            if ("select" in oprt or "SELECT" in oprt):
                rows = cur.fetchall()
                for row in rows:
                    print(f'{row}\n')
        except Exception as e:
            error = True
            print(f'{localcolor[5]}{lang['oprtFail']}{localcolor[2]}\n')
            print(f'{localcolor[5]}ERROR ->{localcolor[7]} {e}{localcolor[2]}')
            if ("current transaction is aborted, commands ignored until end of transaction block" in str(e)):
                if(yorN(f'{localcolor[7]}\nINFO ->{lang['oprtErrorNeedCommit']}{localcolor[2]}')):
                    conn.commit()
                else:
                    conn.close()
                    cur.close()
                    break
        if (not error) :
            print(f'{localcolor[6]}{lang['oprtSuccess']}{localcolor[2]}\n')
        
        if (not yorN(lang['oprtNewOprt'])):
            if(yorN(f'\n{lang['oprtMsgConfirmAlt']}')):
                conn.commit()
            break
main()