from pyswip import Prolog
from consultas import obter_recomendacao
from classes import Menu
from classes import Conversor
from classes import Historico
from classes import Dicas
from classes import DicasCultura
from classes import Hidroponia


def main():
    try:
        prolog = Prolog()
        prolog.consult("conhecimento.pl")
    except Exception as e:
        print("Erro ao carregar o sistema.")
        print(f"Detalhe: {e}")
        print("Verifique se o SWI-Prolog está instalado e se o ficheiro conhecimento.pl existe.")
        return

    #Registo do Agricultor
    nome_usuario = input("Digite seu nome: ")
    print(f"\nBem-vindo ao AgriCV, {nome_usuario}!")

    #loop para que o usuário possa fazer várias consultas sem precisar reiniciar o programa
    while True :
        
        print("\nO que deseja fazer?")
        print("1 - Obter recomendação")
        print("2 - Ver todas as culturas de uma ilha")
        print("3 - Hidroponia")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            print("\nObrigado por usar o AgriCV!")
            break
        
        elif opcao == "1":
            Menu.mostrar_menu_ilhas()
            opcao_ilha = input("\nEscolha a ilha: ")
            ilha = Conversor.converter_ilha(opcao_ilha)

            if ilha is None:
                print("\nIlha inválida.")
                continue

            Menu.mostrar_menu_agricultura()
            opcao_tipo = input("\nEscolha o tipo de agricultura: ")
            tipo = Conversor.converter_tipo(opcao_tipo)

            if tipo is None:
                print("\nTipo de agricultura inválido.")
                continue

            Menu.mostrar_menu_meses()
            opcao_mes = input("\nEscolha o mês: ")
            mes = Conversor.converter_mes(opcao_mes)

            if mes is None:
                print("\nMês inválido.")
                continue

            
            epoca, clima, resultados = obter_recomendacao(prolog, ilha, tipo, mes)
            

            if epoca is None:
                print("\nMês inválido.")
                continue
            
            ilhas_risco = ["sal", "boa_vista", "maio"]

            if ilha in ilhas_risco:
                print("Aviso: Esta ilha está em risco de seca.")
                print("Considere culturas resistentes à falta de água.")

            if epoca == "seca" and tipo == "sequeiro":
                print("Aviso: Epoca seca.")
                print("Sequeiro pode ter resultados limitados. Considere escolher outro tipo de agricultura ou mês.")
                continue

            print("\n==========================================")
            print("Resultado da Recomendação")
            print("==========================================")
            print(f"Ilha: {ilha.replace('_', ' ').title()}")
            print(f"Tipo de agricultura: {tipo.title()}")
            print(f"Mês: {mes.title()}")
            print(f"Época identificada: {str(epoca).title()}")
            print(f"Clima predominante: {str(clima).replace('_', ' ').title()}")

            if resultados:
                print("\nCulturas recomendadas:")
                for resultado in resultados:
                    cultura = str(resultado["Cultura"]).replace("_", " ").title()
                    print(f"- {cultura}")
            else:
                print("\nNão foram encontradas culturas recomendadas para estes dados.")
                print("Pode ser necessário escolher outro mês, ilha ou tipo de agricultura.")

            # Dicas de rega por cultura
            DicasCultura.mostrar_dicas(resultados)
            
            # Dicas de rega por ilha
            Dicas.mostrar_dica_rega(ilha)

            print("\n==========================================")
            print("Consulta concluída.")
            print("==========================================")

            # guardar no ficheiro
            Historico.guardar(nome_usuario, ilha, tipo, mes, epoca, clima)


            resposta = input("\nDeseja fazer nova consulta? (s/n): ")
            if resposta.lower() not in ("s", "sim"):
                print("\nObrigado por usar o AgriCV!")
                break

        elif opcao == "2":
                Menu.mostrar_menu_ilhas()
                opcao_ilha = input("\nEscolha a ilha: ")
                ilha = Conversor.converter_ilha(opcao_ilha)
                if ilha is None:
                    print("\nIlha inválida.")
                    continue
        
                resultados_todos = list(prolog.query(f"cultura({ilha}, Cultura, _, _)"))
                culturas_vistas = []
                print(f"\nTodas as culturas de {ilha.replace('_', ' ').title()}:")
                for r in resultados_todos:
                    cultura = str(r["Cultura"]).replace("_", " ").title()
                    if cultura not in culturas_vistas:
                        culturas_vistas.append(cultura)
                        print(f"- {cultura}")
                continue
        
        elif opcao == "3":
            while True:
                Hidroponia.mostrar_menu_hidroponia()
                opcao_hidroponia = input("\nEscolha a sua opcao: ")
                if opcao_hidroponia == "0":
                    break
                elif opcao_hidroponia == "1":
                    Hidroponia.o_que_e()
                    
                elif opcao_hidroponia == "2":
                    Hidroponia.culturas()
                    
                elif opcao_hidroponia == "3":
                    Hidroponia.como_comecar()
                    
                elif opcao_hidroponia == "4":
                    Hidroponia.dicas_por_ilha()
                       
                else:
                    print("\nOpção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
