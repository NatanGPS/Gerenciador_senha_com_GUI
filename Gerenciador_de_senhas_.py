from re import S

import PySimpleGUI as sg
sg.change_look_and_feel('Purple')

import sqlite3

class teste:
    def __init__(self):
        self.senha_mestra = '3452'
        self.respostas = ['Nova', 'Serviços', 'Ver', 'Sair']
        self.valor_senha = False
        self.conn = sqlite3.connect('passwords.db')   
        self.cursor = self.conn.cursor()
        self.Liberou = False
            # Cria uma tabela com algumas opções, caso essa tabela ja não exista usuarios
        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users(
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );  
        ''')





    def Iniciar(self):
        layout1 = [
            [sg.Text('É PRECISO A SENHA MESTRA PARA ENTRAR:',size=(60,0)), sg.Input(key='senha_mestra', password_char='*'), sg.Button('Enviar')]
         ]
        
        layout2 = [
            [sg.Text('Nova: Para inserir nova senha',size=(50,0))],
            [sg.Text('Serviços: Para ver os serviços salvos',size=(50,0))],
            [sg.Text('Ver : Para recuperar uma senha',size=(50,0))],
            [sg.Text('Sair: Para sair',size=(20,0))],
            [sg.Text('O QUE DESEJA FAZER?'),sg.Input(key= 'Decisao')],
            [sg.Button('Enviar')]
        ]
        
        layout3 = [
            [sg.Text('Nome do serviço: '), sg.Input(key='servico')],
            [sg.Text('Nome do usuario: '), sg.Input(key='username')],
            [sg.Text('Sua senha: '), sg.Input(key='senha')],
            [sg.Button('Enviar')]
        ]
        
        layout4 = [
            [sg.Text('Qual serviço voce gostaria de saber sua senha? '), sg.Input(key='qual_servico'), sg.Button('Enviar')],
            [sg.Text(' ==Suas senhas== ')],
                   [sg.Output()],
                [sg.Text('FECHAR'), sg.Button('Sair')]
        ]

        layout5 = [
            [sg.Text(' ==Seus Serviços cadastrados são == ')],
                               [sg.Output()],
                   [sg.Text('FECHAR'), sg.Button('Sair')]
        ]


       
        self.janela1 = sg.Window('validador de senha mestre', layout1)

        
        self.LerValorDaTela1()
        self.janela1.close()
           
            
        if self.evento == 'Enviar':
            if self.valores['senha_mestra']  != self.senha_mestra:
                print(" Essa opção não é válida!")
                exit()

            else:
                self.valor_senha = True
                if self.valor_senha == True:
                    self.janela2 = sg.Window('Gerenciador de senha', layout2)
                    self.evento, self.valores = self.janela2.Read()
                    self.janela2.close()
                    if self.evento == 'Enviar':
                        if self.valores['Decisao'] == 'Sair':
                            print('ok, encerrando...')
                            exit()  
                        
                        elif self.valores['Decisao'] == 'Nova':
                            self.janela3 = sg.Window('Novo Cadastro', layout3)       
                            self.evento3, self.valores3 = self.janela3.Read()            
                            self.service = self.valores3['servico'] 
                            self.username = self.valores3['username'] 
                            self.password = self.valores3['senha'] 
                            self.janela3.close()
                            
                            self.cursor.execute(f''' 
                                INSERT INTO users (service, username, password)
                                VALUES ('{self.service}', '{self.username}', '{self.password}')
                                ''')
                            self.conn.commit()
                            
                        elif self.valores['Decisao'] == 'Ver':
                            self.janela4 = sg.Window('Ver Senhas', layout4)
                            while True:
                                self.evento4, self.valores4 = self.janela4.Read()
                                self.service = self.valores4['qual_servico']
                                self.cursor.execute(f'''
                                    SELECT username, password FROM users
                                    WHERE service = '{self.service}'
                                    ''' )   
                                if self.cursor.rowcount == 0:
                                    print('Esse serviço não está no nosso sistema, por favor use a opção " serviços" para verificar seus serviços')
                                else:
                                    for user in self.cursor.fetchall():
                                        print(user)
                                    if self.evento4 == 'Sair':
                                        break
                        
                        elif self.valores['Decisao'] == 'Serviços':
                            self.janela5 = sg.Window('Ver Serviços', layout5)
                            while True:
                                self.evento5, self.valores5 = self.janela5.Read()
                                self.cursor.execute(''' 
                                    SELECT service FROM users;
                                    ''')
                                for service in self.cursor.fetchall():
                                    print(service)
                                
                                if self.evento5 == 'Sair':
                                            break

    
    
    
    def mostrar_servicos(self):
        self.cursor.execute(''' 
            SELECT service FROM users;
        ''')
        for service in self.cursor.fetchall():
            print(service)
    
    
    def get_password(self, service):
        self.cursor.execute(f'''
            SELECT username, password FROM users
            WHERE service = '{service}'
    ''' )   
        if self.cursor.rowcount == 0:
            print('Esse serviço não está no nosso sistema, por favor use a opção " serviços" para verificar seus serviços')
        else:
            for user in self.cursor.fetchall():
                print(user)

    
    def LerValorDaTela1(self):
        self.evento, self.valores = self.janela1.Read()

    




comecar = teste()
comecar.Iniciar()