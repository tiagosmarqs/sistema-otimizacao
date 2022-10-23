import tkinter as tk
import tkinter.font as tkFont
import back

janela = tk.Tk()

janela.title("Sistema de Otimização Contoso")
janela.geometry('700x500')

fonte1 = tkFont.Font(family="Lucida Grande", size=20)
fonte2 = tkFont.Font(family="Lucida Grande", size=15)

ano_selecionado = 1

frame1 = tk.Frame(janela)
frame2 = tk.Frame(janela)
frame3 = tk.Frame(janela)

def home():
    frame3.pack_forget()
    frame2.pack_forget()
    frame1.pack()


def segunda():
    frame3.pack_forget()
    frame1.pack_forget()
    frame2.pack()

def terceira():
    frame2.pack_forget()
    frame1.pack_forget()
    frame3.pack()

def otimizar():
    
    lista_produtos = back.implementacao(ano_selecionado)
    for item in lista_produtos:
        
        lb_produtos.insert(tk.END, item.replace("_", " "))
    terceira()

def ano_base():
    
    lista_produtos = back.anoselecionado(ano_selecionado)
    for item in lista_produtos:
        
        lb2_produtos.insert(tk.END, item.replace("_", " "))
    segunda()


def enviar_ano():
    
    global ano_selecionado
    ano_selecionado = var_ano.get()
    print(ano_selecionado)



var_ano = tk.IntVar(value=1)
var_categoria = tk.IntVar(value=1)

#Primeiro Frame
mensagem1 = tk.Label(frame1, text="Selecione o ano base desejado:", fg='white', bg='black', font=fonte1)
mensagem1.grid(row=0, column=0, columnspan=3, sticky="NSEW")
botao_2007 = tk.Radiobutton(frame1, text="2007", variable=var_ano, value=1, command=enviar_ano, font=fonte2)
botao_2007.grid(row=1, column=0)
botao_2008 = tk.Radiobutton(frame1, text="2008", variable=var_ano, value=2, command=enviar_ano, font=fonte2)
botao_2008.grid(row=1, column=1)
botao_2009 = tk.Radiobutton(frame1, text="2009", variable=var_ano, value=3, command=enviar_ano, font=fonte2)
botao_2009.grid(row=1, column=2)


btn_pag2 = tk.Button(frame1, text="CONTINUAR", command=ano_base, fg='white', bg='green')
btn_pag2.grid(row=2, column=2)


#Segundo Frame

mensagem2 = tk.Label(frame2, text="Lista de Desconto por Produto - Ano Base", fg='white', bg='black', font=fonte1)
mensagem2.grid(row=0, column=0, columnspan=3, sticky="NSEW")
lb2_produtos = tk.Listbox(frame2, width=100, height=20)
lb2_produtos.grid(row=1, column=0, columnspan=3)

btn_ot = tk.Button(frame2, text="OTIMIZAR", command=otimizar, fg='white', bg='green')
btn_ot.grid(row=2, column=2)



#Terceiro Frame
mensagem3 = tk.Label(frame3, text="Lista de Desconto por Produto - Otimizado", fg='white', bg='black', font=fonte1)
mensagem3.grid(row=0, column=0, columnspan=3, sticky="NSEW")
lb_produtos = tk.Listbox(frame3, width=100, height=20)
lb_produtos.grid(row=1, column=0, columnspan=3)

btn_home2 = tk.Button(frame3, text="FECHAR", command=janela.destroy, fg='white', bg='grey')
btn_home2.grid(row=2, column=2, columnspan=3)

frame1.pack()



janela.mainloop()