from main import app


# --- ÁREA DE TESTE RÁPIDO (Só roda se executar este arquivo direto) ---
if __name__ == "__main__":
    # Criamos uma ficha de teste
    ficha_teste = {
        "telefone_cliente": "5511950864582",
        "msg_cliente": "Gostaria de uma pizza de calabresa",
        "contexto_conversa": [],
        "novo_cliente": True
    }
    
    # Rodamos a fábrica com essa ficha
    resultado = app.invoke(ficha_teste)
    
    print("\n--- FIM DO PROCESSO ---")
    print("Resultado Final do Estado:")
    print(resultado)