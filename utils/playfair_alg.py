import numpy as np

def grade(chave:str):
    """
    Responsavel por criar a tabela 5*5 usada na encriptação e decriptação.
    Ultiliza numpy para iterar e manusear a tabela e os dados com mais fluidez posteriormente
    """

    #Essa sessão garante texto em caixa alta, tamanho máximo e exclusão de espaços na chave
    key = chave.upper().replace(" ","")
    if (len(key)>25):
        key = key[:24]

    #Inicialização da matriz vazia do tipo textual e de um alfabeto
    temp = np.empty((5,5), dtype='U16')
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXY"

    #Remove repetições na chave e seus caractéres do alfabeto
    for char in key:
        if (key.count(char)) > 1:
            index = key.rfind(char)                                 #Encontra a última aparicão do caractere repetido, se houver
            key = key[:index] + key[index + 1:]                     #Cria duas fatias da String de forma a isolar o caractere repetido e depois as une devolta, efetivamente deletando o caractere.
        alfabeto = alfabeto.replace(char, "")

    #Itera pela matriz adicionando a sequencia do alfabeto gerada usando um iterador de matrizes do numpy
    with np.nditer(temp, op_flags=['readwrite']) as it:
        for x in it:                                                #ultiliza um método de sempre adicionar o primeiro caractére da sequencia na próxima célula da matriz e depois deletar o caractére na célula
            if (key != ""):                                         #começa pela chave e depois usa o alfabeto
                char = key[0]
                x[...] = char
                key = key.lstrip(char)
            else:
                x[...] = alfabeto[0]
                alfabeto = alfabeto.lstrip(alfabeto[0])

    return temp


def encrypt (mensagem:str, key: str):
    """
    Função para encriptar uma string usando uma chave
    """

    #cria o grid 5*5 e formata a mensagem para encriptação
    grid = grade(key)
    msg = mensagem.upper().replace(" ","")

    def bogusCheck (msj):
        '''
        Função que define duas letras 'bogus' e checa pelo uso adequado de cada uma, retornando a correta.
        Letras bogus são letras usadas para preencher pares com letras dublicadas ou fazer par com letras sozinhas
        '''
        bogus = "K"
        if (msj == "K"):
            bogus = "W"
        return bogus

    #Remover a letra Z das mensagens por estar banida
    if (msg.count('Z') > 0):
        indx = msg.rfind('Z')                                
        msg = msg[:indx] + bogusCheck(msg[indx]) + msg[indx + 1:]

    #Descobre se a mensagem possui um número ímpar de caracteres para aplicar o caractere bogus
    if (len(msg)% 2 == 1):
        b = bogusCheck(msg[-1])
        msg += b

    #cria o resultado que será resultado e inicia o loop que fará a criptografia.
    result = ""
    for j in range(1, len(msg), 2):                                 #O loop inicia do segundo caractere, avança e dois em dois para processar em pares.
        #adiciona um bogus entre caracteres duplicados.
        if msg[j] == msg[j-1]:
            bogus = bogusCheck(msg[j])
            msg = msg[:j-1] + bogus + msg[j-1:]

        #Ultiliza numpy.where para procurar os elementos da mensagem na tabela e registrar suas coordenadas
        #Coord[0][0] = linha; Coord[1][0] = coluna (0 = y, 1 = x)
        coordA = np.where(grid == msg[j-1])
        coordB = np.where(grid == msg[j])

        #Caso as células estejam verticalmente alinhadas
        if (coordA[0][0] == coordB[0][0]):

            if (coordA[1][0] < 4):                                  #Checa se a célula não está no finalda coluna, se sim, a célula encriptada apontará para o início da coluna, senão ela apontará para a próxima célula na
                result  += grid[coordA[0][0]][coordA[1][0]+1]
            else:
                result  += grid[coordA[0][0]][0]

            if (coordB[1][0] < 4):
                result  += grid[coordB[0][0]][coordB[1][0]+1]
            else:
                result  += grid[coordB[0][0]][0]

        #Caso as células estejam horizontalmente alinhadas
        elif (coordA[1][0] == coordB[1][0]):
            if (coordA[0][0] < 4):                                   #Checa se a célula não está no finalda coluna, se sim, a célula encriptada apontará para o início da coluna, senão ela apontará para a próxima célula na
                result  += grid[coordA[0][0]+1][coordA[1][0]]
            else:
                result  += grid[0][coordA[0][0]]

            if (coordB[0][0] < 4):
                result  += grid[coordB[0][0]+1][coordB[1][0]]
            else:
                result  += grid[0][coordB[1][0]]

        else:                                                       #Se a célula passar por todos os checks, o processo será localizar a célula na linha do primeiro caracter e na coluna do segundo e virse-versa.
            result += grid[coordA[0][0]][coordB[1][0]]
            result += grid[coordB[0][0]][coordA[1][0]]
                

    return result

def decrypt (mensagem:str, key:srt):
    """
    Decodifica as mensagens geradas por encrypt() usando a mesma chave usada para encryptar.
    """
    grid = grade(key)
    msg = mensagem.upper().replace(" ","")

    result = ""
    for j in range(1, len(msg), 2):                                 #Recria o mesmo processo de encriptação mas invertido para células alinhadas e removendo código desnecessário como bogus

        coordA = np.where(grid == msg[j-1])
        coordB = np.where(grid == msg[j])

        if (coordA[0][0] == coordB[0][0]):

            if (coordA[1][0] >0):
                result  += grid[coordA[0][0]][coordA[1][0]-1]
            else:
                result  += grid[coordA[0][0]][4]

            if (coordB[1][0] >0):
                result  += grid[coordB[0][0]][coordB[1][0]-1]
            else:
                result  += grid[coordB[0][0]][4]

        elif (coordA[1][0] == coordB[1][0]):
            if (coordA[0][0] >0):
                result  += grid[coordA[0][0]-1][coordA[1][0]]
            else:
                result  += grid[4][coordA[0][0]]

            if (coordB[0][0] >0):
                result  += grid[coordB[0][0]-1][coordB[1][0]]
            else:
                result  += grid[4][coordB[1][0]]

        else:
            result += grid[coordA[0][0]][coordB[1][0]]
            result += grid[coordB[0][0]][coordA[1][0]]
                

    return result

'''
DEBUG
'''
'''
k = 'GordomRamsey'
x = encrypt('HalfLife', k)
a = decrypt(x, k)

print(grade(k))
print(x)
print(a)
'''