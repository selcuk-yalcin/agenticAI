"""
FastAPI Server - Email Automation Agent Bağlantısı
Tek bir agent'ı admin paneline bağlama örneği
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import sys
from pathlib import Path

# Proje yolunu ekle
sys.path.insert(0, str(Path(__file__).parent))

# Email Agent'ı import et
try:
    from projects.email_automation.agents.email_agent import create_email_agent
except ImportError:
    print("⚠️  Email agent bulunamadı. Test modu ile başlatılıyor...")
    create_email_agent = None

# FastAPI uygulaması oluştur
app = FastAPI(
    title="Agentic AI API",
    description="Email Automation Agent API",
    version="1.0.0"
)

# CORS ayarı - React admin panelinden erişim için gerekli
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server URL'leri
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Email Request Modeli
class EmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str
    template_name: str = "default"

# 📌 Email Response Modeli
class EmailResponse(BaseModel):
    status: str
    message: str
    email_id: str
    timestamp: str

# 📌 Root Cause Analysis Request Modeli
class RootCauseRequest(BaseModel):
    incident_description: str
    location: str
    date_time: str
    witnesses: str = ""

# 📌 Root Cause Analysis Response Modeli
class RootCauseResponse(BaseModel):
    status: str
    message: str
    report_id: str
    analysis: dict = None
    timestamp: str
    timestamp: str

# 🏠 Ana sayfa - API durumu
@app.get("/")
async def root():
    return {
        "message": "Email Automation API Çalışıyor! �",
        "endpoints": {
            "health": "/api/health",
            "send_email": "/api/email/send"
        }
    }

# ✅ Health check endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Agentic AI API"
    }

# 📧 EMAIL AGENT ENDPOINT
@app.post("/api/email/send", response_model=EmailResponse)
async def send_email(request: EmailRequest):
    """
    Email gönderme endpoint'i
    
    Admin panelden email gönderme:
    - recipient: Alıcı email adresi
    - subject: Email konusu
    - body: Email içeriği
    - template_name: Kullanılacak template (opsiyonel)
    """
    try:
        # TODO: Email agent gerçek entegrasyonu
        # Şimdilik mock response döndürüyoruz
        
        print(f"📧 Email Request:")
        print(f"   To: {request.recipient}")
        print(f"   Subject: {request.subject}")
        print(f"   Body: {request.body[:50]}...")
        
        # Simüle edilmiş başarılı yanıt
        return EmailResponse(
            status="success",
            message=f"Email successfully sent to {request.recipient}",
            email_id=f"EMAIL_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        return EmailResponse(
            status="error",
            message=f"Email sending failed: {str(e)}",
            email_id="N/A",
            timestamp=datetime.now().isoformat()
        )

# 🔍 ROOT CAUSE ANALYSIS ENDPOINT
@app.post("/api/rootcause/analyze", response_model=RootCauseResponse)
async def analyze_root_cause(request: RootCauseRequest):
    """
    Root Cause Analysis endpoint'i
    
    Admin panelden kaza/olay kök neden analizi:
    - incident_description: Olay açıklaması
    - location: Olay yeri
    - date_time: Olay tarihi/saati
    - witnesses: Tanıklar (opsiyonel)
    """
    try:
        # TODO: Root Cause agent gerçek entegrasyonu
        # Şimdilik mock response döndürüyoruz
        
        print(f"🔍 Root Cause Analysis Request:")
        print(f"   Incident: {request.incident_description[:50]}...")
        print(f"   Location: {request.location}")
        print(f"   Date/Time: {request.date_time}")
        print(f"   Witnesses: {request.witnesses[:30] if request.witnesses else 'None'}...")
        
        # Simüle edilmiş analiz sonucu
        mock_analysis = {
            "root_causes": """1. İş Güvenliği Ekipmanı Eksikliği
   - Koruyucu ekipman kullanılmamış
   - Güvenlik prosedürlerine uyulmamış
   
2. Yetersiz Eğitim
   - Çalışanlar risk konusunda bilgilendirilmemiş
   - Güvenlik eğitimleri eksik
   
3. Çevresel Faktörler
   - Yetersiz aydınlatma
   - Kaygan zemin""",
            
            "recommendations": """1. Acil Güvenlik Önlemleri:
   - Tüm çalışanlara koruyucu ekipman temini
   - İş güvenliği prosedürlerinin güncellenmesi
   
2. Eğitim Programı:
   - Haftalık güvenlik eğitimleri
   - Risk değerlendirme çalışmaları
   
3. Altyapı İyileştirmeleri:
   - Aydınlatma sistemlerinin güçlendirilmesi
   - Zemin kaplamalarının yenilenmesi""",
            
            "immediate_actions": """1. Olay bölgesinin güvenlik şeridi ile kapatılması
2. Benzer risklerin olduğu tüm alanlarda acil kontrol yapılması
3. İlgili çalışanların ek eğitime alınması
4. 24 saat içinde güvenlik komitesi toplantısı yapılması
5. Olayın tüm çalışanlara duyurulması"""
        }
        
        # Simüle edilmiş başarılı yanıt
        return RootCauseResponse(
            status="success",
            message="Root cause analysis completed successfully",
            report_id=f"RCA_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            analysis=mock_analysis,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        return RootCauseResponse(
            status="error",
            message=f"Root cause analysis failed: {str(e)}",
            report_id="N/A",
            analysis=None,
            timestamp=datetime.now().isoformat()
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 FastAPI Server başlatılıyor...")
    print("📍 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
