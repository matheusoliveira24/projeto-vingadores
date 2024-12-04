from string import capwords
from model.vingador import Vingador
from os import system
from model.database import Database

class Interface:

    def __init__(self):
        Vingador.carregar_herois()
        self.menu_principal()

    def menu_principal(self):
        self.exibe_titulo_app()
        while True:
            self.exibe_titulo("Menu Principal")
            print("1 - Cadastrar Vingador")
            print("2 - Listar Vingadores")
            print("3 - Convocar Vingador")
            print("4 - Aplicar Tornozeleira")
            print("5 - Aplicar Chip GPS")
            print("6 - Listar Detalhes do Vingador")
            print("7 - Emitir Mandato de Prisão")
            print("8 - Listar Convocados")
            print("9 - Listar quem está com Tornozeleira")
            print("10 - Listar Prisioneiros")
            print("0 - Sair", end="\n\n")
            opcao = input("Digite a opção desejada: ")

            if opcao == '1':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Cadastro de Vingador")
                self.cadastrar_vingador()
                self.aguardar_enter()
            elif opcao == '2':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Lista de Vingadores")
                Vingador.listar_vingadores()
                self.aguardar_enter()
            elif opcao == '3':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Convocação de Vingador")
                self.convocar_vingador()
                self.aguardar_enter()
            elif opcao == '4':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Aplicação de Tornozeleira")
                self.aplicar_tornozeleira()
                self.aguardar_enter()
            elif opcao == '5':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Aplicação de Chip GPS")
                self.aplicar_chip_gps()
                self.aguardar_enter()
            elif opcao == '6':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Listar Detalhes do Vingador")
                self.listar_detalhes_vingador()
                self.aguardar_enter()
            elif opcao == '7':
                self.exibe_titulo("Prender Herói")
                nome_heroi = capwords(input("Nome do herói: "))
                for vingador in Vingador.lista_vingadores:
                    if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                        print(vingador.prender()) 
                        self.aguardar_enter()
                    return
                print(f"Herói '{nome_heroi}' não encontrado.")
                self.aguardar_enter()
            elif opcao == '8':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Lista de Convocados")
                Vingador.listar_convocados()  # Agora chamado corretamente
                self.aguardar_enter()
            elif opcao == '9':
                self.exibe_titulo_app()
                self.exibe_titulo("<< Lista de Tornozeleirados")
                Vingador.listar_tornozeleirados()  # Agora chamado corretamente
                self.aguardar_enter()
            elif opcao == '10':
                self.exibe_titulo("Heróis Presos")
                self.listar_herois_presos()  # Chama a função para listar os heróis na prisão
                self.aguardar_enter()

            elif opcao == '0':
                exit()
            else:
                print("Opção inválida.")
                self.aguardar_enter()
                self.menu_principal()

    def listar_herois_presos(self):
        print(f"{'Nome do Herói'.ljust(20)} |  {'Nome Real'.ljust(20)} |  {'Categoria'.ljust(15)} |  {'Prisao Ativa'.ljust(15)}")
        print('-' * 95)
        for vingador in Vingador.lista_vingadores:
            if vingador.prisao_ativa == 'YES':  # Verifica se o herói está preso
                print(vingador)


    def cadastrar_vingador(self):
        '''Exibe o formulário de cadastro de vingador e cria um novo vingador.'''
        nome_heroi = input("Nome do herói: ")
        nome_real = input("Nome real: ")
        categoria = input("Categoria: ").capitalize()
        poderes = input("Poderes (separados por vírgula): ").split(',') # armazena em uma lista
        poder_principal = input("Poder Principal: ")
        fraquezas = input("Fraquezas: (separadas por vírgula): ").split(',') # armazena em uma lista
        nivel_forca = int(input("Nível de Força: "))


        try:
            db = Database()
            db.connect()

            query = "INSERT INTO heroi (nome_heroi, nome_real, categoria, poderes, poder_principal, fraquezas, nivel_forca) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            
            values = (nome_heroi, nome_real, categoria, ', '.join(poderes), poder_principal, ', '.join(fraquezas), nivel_forca)

            cursor = db.execute_query(query, values) 
            
            Vingador(cursor.lastrowid, nome_heroi, nome_real, categoria, poderes, poder_principal, fraquezas, nivel_forca)
            
        except Exception as e:
            print(f"Erro ao salvar vingador no banco de dados: {e}")
        finally:
            db.disconnect()

        print(f"Vingador(a) '{nome_heroi}' cadastrado com sucesso.")
        self.aguardar_enter()

    def aguardar_enter(self):
        input("\nPressione Enter para continuar...")
        self.menu_principal()

    def convocar_vingador(self):
        nome_heroi = capwords(input("Nome do herói: "))
        for vingador in Vingador.lista_vingadores:
            if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                print(vingador.convocar())
                self.aguardar_enter()
                return
        print(f"Vingador(a) '{nome_heroi}' não encontrado.")
        self.aguardar_enter()

    
    def aplicar_tornozeleira(heroi_id):
        db = Database()
        db.connect() 
        
        query_check = "SELECT id FROM convocados WHERE id = %s"
        result = db.select(query_check, (heroi_id,))
        
        if result:
            data_torno = int(datetime.now().timestamp())
            query_insert = """
                INSERT INTO tornozeleira (heroi_id, data_torno)
                VALUES (%s, %s)
            """
            db.execute_query(query_insert, (heroi_id, data_torno))
            print(f"Tornozeleira aplicada ao herói com ID {heroi_id} em timestamp {data_torno}")
        else:
            print(f"Herói com ID {heroi_id} não encontrado na tabela convocados.")
        
        db.disconnect()  

    def aplicar_chip_gps(heroi_id, localizacao):
        db = Database()
        db.connect()  
        
        query_check = "SELECT id, nome_heroi FROM tornozeleira WHERE heroi_id = %s"
        result = db.select(query_check, (heroi_id,))
        
        if result:
            nome_heroi = result[0][1]
            data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query_insert = """
                INSERT INTO gps (heroi_id, nome_heroi, localizacao, data_hora)
                VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query_insert, (heroi_id, nome_heroi, localizacao, data_hora))
            print(f"Chip GPS foi aplicado ao herói {nome_heroi} com a localização '{localizacao}' em {data_hora}")
        else:
            print(f"Herói com ID {heroi_id} não encontrado na tabela tornozeleira.")
        
        db.disconnect()  
    
    @staticmethod
    def listar_herois_com_gps():
        db = Database()
        db.connect()  
        
        query = "SELECT nome_heroi, localizacao, data_hora FROM gps"
        result = db.select(query)
        
        if result:
            print("\nHeróis com GPS:")
            for row in result:
                nome_heroi = row[0]
                localizacao = row[1]
                data_hora = row[2]
                print(f"Herói: {nome_heroi}, Localização: {localizacao}, Data e Hora: {data_hora}")
        else:
            print("Nenhum herói com chip GPS encontrado.")
        
        db.disconnect()

    def listar_detalhes_vingador(self):
        nome_heroi = capwords(input("Nome do herói: "))
        for vingador in Vingador.lista_vingadores:
            if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                vingador.listar_detalhes_vingador()
                self.aguardar_enter()
                return
        print(f"Vingador(a) '{nome_heroi}' não encontrado.")
        self.aguardar_enter()

    def prender(self):
        nome_heroi = capwords(input("Nome do herói: "))
        for vingador in Vingador.lista_vingadores:
            if nome_heroi in vingador.nome_heroi or nome_heroi in vingador.nome_real:
                print(vingador.prender())
                self.aguardar_enter()
                return
        print(f"Vingador(a) '{nome_heroi}' não encontrado.")
        self.aguardar_enter()

    @staticmethod
    def exibe_titulo(titulo):
        print(f"\n{titulo}")
        print('-' * len(titulo))

    @staticmethod
    def exibe_titulo_app():
        system('cls')
        print('''

 ███████████████▀█████████████████████████████████████
  █▄─█─▄█▄─▄█─▄▄▄▄█▄─▄█▄─▄████▀▄─██▄─▀█▄─▄█─▄─▄─█▄─▄▄─█
   ██▄▀▄███─██─██▄─██─███─██▀██─▀─███─█▄▀─████─████─▄█▀█
    ▀▀▀▄▀▀▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▀▀▄▄▄▄▄▀        
        ''')