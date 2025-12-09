import asyncio
import json
import sys

async def spam_bot(login: str, password: str, message_count: int = 100, delay: float = 0.01):
    """Bot qui envoie un grand nombre de messages rapidement."""
    try:
        # Connexion
        reader, writer = await asyncio.open_connection('vassor.org', 12345)
        
        # Authentification
        auth_message = json.dumps({"login": login, "password": password}, separators=(', ', ':')) + "\n"
        writer.write(auth_message.encode())
        await writer.drain()
        
        # Réception de la réponse d'authentification
        response = json.loads((await reader.readline()).decode())
        if response == "Failure":
            print("Erreur d'authentification")
            writer.close()
            await writer.wait_closed()
            return
        
        print(f"Authentification réussie. Envoi de {message_count} messages...")
        
        # Envoi massif de messages
        for i in range(message_count):
            message_json = json.dumps({"msg": f"SPAM {i}"}, separators=(', ', ':')) + "\n"
            writer.write(message_json.encode())
            if i % 100 == 0:
                print(f"Envoi du message {i}...")
            await asyncio.sleep(delay)
        
        await writer.drain()
        print(f"Tous les messages ont été envoyés ({message_count} messages)")
        
        # Fermeture de la connexion
        writer.close()
        await writer.wait_closed()
        
    except Exception as e:
        print(f"Erreur: {e}")

async def flood_bot(login: str, password: str):
    """Bot qui envoie des messages sans délai pour saturer le serveur."""
    try:
        reader, writer = await asyncio.open_connection('vassor.org', 12345)
        
        auth_message = json.dumps({"login": login, "password": password}, separators=(', ', ':')) + "\n"
        writer.write(auth_message.encode())
        await writer.drain()
        
        response = json.loads((await reader.readline()).decode())
        if response == "Failure":
            print("Erreur d'authentification")
            writer.close()
            await writer.wait_closed()
            return
        
        print("Authentification réussie. Flood en cours...")
        
        # Envoi sans délai
        i = 0
        while True:
            try:
                message_json = json.dumps({"msg": f"FLOOD {i}"}, separators=(', ', ':')) + "\n"
                writer.write(message_json.encode())
                i += 1
                if i % 1000 == 0:
                    print(f"Messages envoyés: {i}")
                # Pas de drain() pour saturer le buffer
            except Exception as e:
                print(f"Erreur après {i} messages: {e}")
                break
        
        writer.close()
        await writer.wait_closed()
        
    except Exception as e:
        print(f"Erreur: {e}")


if __name__ == "__main__":
    login = sys.argv[1]
    password = sys.argv[2]
    mode = sys.argv[3]
    
    if mode == "spam":
        count = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
        delay = float(sys.argv[5]) if len(sys.argv) > 5 else 0.01
        asyncio.run(spam_bot(login, password, count, delay))
    elif mode == "flood":
        asyncio.run(flood_bot(login, password))
    else:
        print(f"Mode inconnu: {mode}")
