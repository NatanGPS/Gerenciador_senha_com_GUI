
import PySimpleGUI as sg

import sqlite3

class teste:
    def __init__(self):
        self.senha_mestra = '3452'
        self.respostas = ['Nova', 'Serviços', 'Ver', 'Sair']
        self.valor_senha = False
        self.conn = sqlite3.connect('passwords.db')   
        self.cursor = self.conn.cursor()

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
            [sg.Text('O QUE DESEJA FAZER?'),sg.Input(key= 'Decisao_Usuario')],
            [sg.Button('Enviar')]
        ]
        
        layout3 = [
            [sg.Text('Nome do serviço: '), sg.Input(key='novo_servico')],
            [sg.Text('Nome do usuario: '), sg.Input(key='novo_username')],
            [sg.Text('Sua senha: '), sg.Input(key='nova_senha')],
            [sg.Button('Enviar')]
        ]
        
        self.janela1 = sg.Window('validador de senha mestre', layout1)

        
        self.LerValorDaTela1()
            #self.respondeu = self.valores['Decisao_Usuario']
            
        if self.evento1 == 'Enviar':
            if self.valores1['senha_mestra']  != self.senha_mestra:
                print(" Essa opção não é válida!")
                exit()

            else:
                 self.valor_senha = True
              
            if self.valor_senha == True:
                self.janela1.close()
                
                self.janela2 = sg.Window('Gerenciador de senha', layout2)
                self.LerValorDaTela2()
                self.janela2.close()
               
                if self.evento2 == 'Enviar':
                    
                    
                    if self.valores2 == self.respostas[-1]:
                        exit()    
                    
                    elif self.valores2 == self.respostas[0]:
                        self.janela3 = sg.Window('Novo Cadastro', layout3)
                        self.LerValorDaTela3()
                            
                        if self.valores2 == 'Enviar':
                            self.inserir_senha(self.evento3['novo_servico'], self.evento3['novo_username'], self.evento3['nova_senha'])
                    
                    
                    elif self.valores2 == self.respostas[-2]:
                        pass
                                    
                    
                    elif self.valores2 == self.respostas[1]:
                        pass
                        
    
    
    
    
    def inserir_senha(self, service, username, password):
        self.cursor.execute(f''' 
            INSERT INTO users (service, username, password)
            VALUES ('{service}', '{username}', '{password}')
        ''')
        self.conn.commit()
    
    
    
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
        self.evento1, self.valores1 = self.janela1.Read()

    def LerValorDaTela2(self):
      self.evento2, self.valores2 = self.janela2.Read()

    def LerValorDaTela3(self):
      self.evento3, self.valores3 = self.janela3.Read()






comecar = teste()
comecar.Iniciar()