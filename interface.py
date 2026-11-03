import utils.playfair_alg as pf

debugMode = False

print('Bem vindo, o que gostaria de fazer?\n\n')

while(True):
    resp = input('1 - Encryptar\n2 - Decryptar \n\t\t:')

    if (resp == '1'):
        print('ENCRYPT MODE\n')
        msg = input('Insira sua mensagem\t')
        key = input('\nInsira uma chave\t')

        crypt = pf.encrypt(msg, key)

        print ('\n\nApós encryptar, ' + msg + ', se tronou:\n\t\t' + crypt +"\nGuarde sua chave.")
        if (debugMode ==True):
            print('\nTabela gerada:\n')
            print(pf.grade(key))
        
        input("Use qualquer botão para sair")
        break

    elif (resp == '2'):
        print('DECRYPT MODE')

        crypt = input('Insira sua mensagem criptografada\t')
        key = input('\nInsira uma chave\t')

        msg = pf.decrypt(crypt, key)

        print ('\n\nApós decodificar, ' + crypt + ', se tronou:\n\t\t' + msg)
        if (debugMode ==True):
            print('\nTabela gerada:\n')
            print(pf.grade(key))

        input("Use qualquer botão para sair")
        break
        
    elif (resp == 'DEBUG'):
        if (debugMode == False):
            debugMode = True
            print('Debug On')
        else:
            debugMode = False
            print('Debug Off')
        
    else:
        print('Resposta Inválida')