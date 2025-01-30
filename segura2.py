import socket
import uuid
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime

# Configuração do e-mail
EMAIL_REMETENTE = "pedrolima1618@gmail.com"  
EMAIL_SENHA = "xgde rilo mgjt pseq"  #senha do Gmail
EMAIL_DESTINO = "pedrolima1618@gmail.com"  
def obter_informacoes():
    """
    Obtém informações do sistema, incluindo nome da máquina, IP, MAC, localização e data/hora atual.
    """
    nome_maquina = socket.gethostname()
    ip_maquina = socket.gethostbyname(nome_maquina)
    mac_maquina = ':'.join(format(x, '02x') for x in uuid.getnode().to_bytes(6, 'big'))
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        resposta = requests.get("http://ip-api.com/json/")
        dados_geo = resposta.json()
        localizacao = f"{dados_geo['city']}, {dados_geo['regionName']}, {dados_geo['country']}"
    except Exception:
        localizacao = "Não foi possível obter a localização"

    return {
        "Nome da Máquina": nome_maquina,
        "Endereço IP": ip_maquina,
        "Endereço MAC": mac_maquina,
        "Localização": localizacao,
        "Data e Hora": data_hora
    }

def enviar_email(dados):
    """
    Envia um e-mail com as informações coletadas.
    """
    try:
        # Formatar os dados em texto
        corpo_email = "\n".join([f"{chave}: {valor}" for chave, valor in dados.items()])

        # Criar o e-mail
        msg = MIMEText(corpo_email)
        msg["Subject"] = "Novo Acesso Detectado"
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = EMAIL_DESTINO

        # Conectar ao servidor SMTP com o gmail
        servidor_smtp = smtplib.SMTP("smtp.gmail.com", 587)
        servidor_smtp.starttls()  # Iniciar conexão segura
        servidor_smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor_smtp.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())
        servidor_smtp.quit()

        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Executando a coleta e envio
info = obter_informacoes()
for chave, valor in info.items():
    print(f"{chave}: {valor}")
enviar_email(info)
