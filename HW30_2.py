from HW30_1 import HashTable

ht = HashTable(10)
ht['a'] = '1'
ht['Maks'] = 'happy'
ht['Anna'] = 'true'
ht['Alex'] = '100'
ht['xxx'] = 'yyy'
ht['dog'] = 'Bou'
ht['cat'] = 'Mau'

# Registration

login = str(input('\nRegistration\n Enter login:'))
if login in ht.keys:
    print('This login already exists. Try to authorize')
else:
    while True:
        parole = str(input(' Enter parole:'))
        if parole in ht.values:
            print('Generate other parole, this is too simple')
        else:
            ht[login] = parole
            break

# Authorization

you_login = str(input('\nAuthorization\n Enter login:'))
you_parole = str(input(' Enter parole:'))
if (you_login, you_parole) in ht.pairs:
    print('You are successfully authorized.')
else:
    print('Sorry, such login-parole pair is not registered. Try again or register.')
