import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TARGET_GIST_ID = os.getenv("GITHUB_GIST_ID")

def post_comment_to_gist(comment_text: str) -> bool:
    if not GITHUB_TOKEN or not TARGET_GIST_ID:
        print("Token ou Gist ID não configurados.")
        return False
        
    try:
        g = Github(GITHUB_TOKEN)
        gist = g.get_gist(TARGET_GIST_ID)
        gist.create_comment(comment_text) 
        
        print(f"Sucesso: Comentário enviado para o Gist {TARGET_GIST_ID}.")
        return True

    except Exception as e:
        print(f"Erro GitHub Service: Falha ao enviar comentário ao Gist: {e}")
        return False

if __name__ == "__main__":
    test_message = f"teste comentario"
    post_comment_to_gist(test_message)
    print("----------------------------------------")
