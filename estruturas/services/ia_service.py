from groq import Groq

# Importa o cérebro do J.A.R.V.I.S
from core.prompt_mestre import PromptMestre


class IAService:

    # Modelo da IA
    MODELO = "llama-3.3-70b-versatile"

    # Quantidade máxima de tokens
    MAX_TOKENS = 1024

    def __init__(self):

        # Cria conexão com a Groq
        self.cliente = Groq(
            api_key="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"
        )

        # Cria o Prompt Mestre
        self.prompt_mestre = PromptMestre()

        # Gera o system prompt automaticamente
        self.system_prompt = self.prompt_mestre.get_prompt()

    def enviar_mensagem(self, mensagem, historico: list) -> str:

        try:

            # Junta:
            # system prompt + histórico
            mensagens = [
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            ] + historico

            # Envia para a IA
            resposta = self.cliente.chat.completions.create(
                model=self.MODELO,
                max_tokens=self.MAX_TOKENS,
                messages=mensagens,
            )

            # Retorna apenas o texto da resposta
            return resposta.choices[0].message.content

        except Exception as e:

            mensagem = str(e)

            if "401" in mensagem or "invalid_api_key" in mensagem.lower():

                raise Exception(
                    "Erro de autenticação: verifique sua GROQ_API_KEY."
                )

            elif "429" in mensagem or "rate_limit" in mensagem.lower():

                raise Exception(
                    "Limite de requisições atingido. Aguarde um momento."
                )

            else:

                raise Exception(
                    f"Erro na API da Groq: {mensagem}"
                )


# Teste do sistema
if __name__ == "__main__":

    # Cria o J.A.R.V.I.S
    jarvis = IAService()

    # Histórico da conversa
    historico_teste = [
        {
            "role": "user",
            "content": "Me dê 3 ideias de reels para uma loja de roupas femininas."
        }
    ]

    print("=" * 60)
    print("J.A.R.V.I.S INICIADO")
    print("=" * 60)

    # Envia mensagem
    resposta = jarvis.enviar_mensagem(historico_teste)

    print("\nRESPOSTA:\n")
    print(resposta)