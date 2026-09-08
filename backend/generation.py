import json
from dotenv import load_dotenv
load_dotenv()
import anthropic
from models import Quiz,QuizQuestion,FlashCard

client = anthropic.Anthropic()

CONTENT_CONFIG = {
    "quiz": {
        "model": Quiz,
        "tool_name": "generate_quiz",
        "system": "Tu es un professeur qui rédige des quiz suivant des cours",
        "prompt": 'Avec le cours suivant, délimité par des triples guillemets, crée un quiz. Cours : """{course}"""',
        "tool": {
            "name": "generate_quiz",
            "description": "Génère un quiz structuré à partir d'un cours",
            "input_schema": {
                "type": "object",
                "properties": {
                    "quiz": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "question": {"type": "string", "description": "Enoncé de la question qui est posée"},
                                "options": {"type": "array", "items": {"type": "string"}, "description": "Les quatre choix proposés"},
                                "correct_answer": {"type": "integer", "description": "Index de la bonne réponse, commençant à 0"},
                                "explanation": {"type": "string", "description": "Explication de la réponse"}
                            },
                            "required": ["question", "options", "correct_answer", "explanation"]
                        }
                    }
                },
                "required": ["quiz"]
            }
        }
    },
    "flashcard": {
        "model": FlashCard,
        "tool_name": "generate_flashCard",
        "system": "Tu es un professeur qui rédige des fiches de synthèse à partir de cours",
        "prompt": 'Avec le cours suivant, délimité par des triples guillemets, crée une fiche de synthèse organisée en sections thématiques. Cours : """{course}"""',
        "tool": {
            "name": "generate_flashCard",
            "description": "Génère une fiche de synthese à partir d'un cours",
            "input_schema": {
                "type": "object",
                "properties": {
                    "sections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string", "description": "Titre de la section abordée"},
                                "content": {"type": "string", "description": "Contenu de la section"}
                            },
                            "required": ["title", "content"]
                        }
                    }
                },
                "required": ["sections"]
            }
        }
    }
}

def generate_content(course,content_type,max_retries=2):

    if content_type not in CONTENT_CONFIG:
        raise ValueError(f"Type de contenu inconnu : {content_type}")
    
    config = CONTENT_CONFIG[content_type]
    prompt = config["prompt"].format(course=course)
    messages = [{"role": "user", "content": prompt}]
    tool_choice = {"type": "tool", "name": config["tool_name"]}

    last_error = None

    for attempt in range(max_retries + 1):
        try:
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=4096,
                temperature=0,
                system=config["system"],
                messages=messages,
                tools=[config["tool"]], 
                tool_choice = tool_choice
            )   

            for block in message.content:
                if block.type == "tool_use":
                    return config["model"](**block.input)
                
        except Exception as e:
            last_error = e
            print(f"Tentative {attempt + 1} échouée : {e}")
        
    raise ValueError(f"Échec de génération après {max_retries + 1} tentatives : {last_error}")


if __name__ == "__main__":
    f = open("cours_test.txt", encoding="utf-8")
    course = f.read()
    f.close()

    print("=== QUIZ ===")
    print(generate_content(course, "quiz"))

    print("\n=== FICHE ===")
    print(generate_content(course, "flashcard"))
