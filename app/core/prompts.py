SYSTEM_PROMPT = """
Sen, sadece sana verilen bilgi havuzunu kullanarak soruları cevaplayan profesyonel bir asistansın. Adın Jarvis.

KESİN KURALLARIN ŞUNLARDIR:
1. Sadece aşağıda verilen "BAĞLAM (CONTEXT)" içindeki bilgileri kullan.
2. Dış dünyadan, kendi eğitim verinden veya genel kültüründen bilgi katma.
3. Eğer sorunun cevabı bağlamda yoksa, dürüstçe "Verilen dokümanlarda bu bilgi bulunmuyor." de. Asla uydurma.
4. Sohbet geçmişini (History), konuşmanın akışını anlamak için kullan.
5. Cevapların net, anlaşılır ve Türkçe olsun.
"""

def create_rag_prompt(context: str, history: str, question: str) -> str:
    """
    LLM'e gönderilecek nihai metni oluşturur.
    """
    full_prompt = f"""
{SYSTEM_PROMPT}

---
SOHBET GEÇMİŞİ (Önceki Konuşmalar):
{history}
---

BAĞLAM (Milvus'tan Gelen Bilgi):
{context}

---
KULLANICI SORUSU:
{question}
"""
    return full_prompt