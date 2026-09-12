import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.database import SessionLocal, engine, Base
from backend.app.models.case import CaseModel
from backend.app.models.evidence import EvidenceModel
from backend.app.config import STORAGE_DIR, UPLOADS_DIR
from backend.app.services.rag_service import rag_service

def compute_sha256(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    print("[Seed] Initializing ProofForge database seed...")

    # 1. Project Riverstone
    c1_id = "case-riverstone"
    existing_c1 = db.query(CaseModel).filter(CaseModel.id == c1_id).first()
    if not existing_c1:
        c1 = CaseModel(
            id=c1_id,
            title="Project Riverstone: Multi-Jurisdiction Evidence Intelligence",
            case_number="SPL/2026/RIV-01",
            case_type="Criminal",
            court="Special CBI / High Court Division",
            court_location="Vijayawada / Hyderabad",
            filing_date="2026-01-20",
            status="Trial",
            description="Multi-jurisdictional evidence inquiry tracking alleged conspiratorial meeting between Ravi Kumar and Suresh Reddy in Vijayawada, contradictory alibi audio recordings, and cross-border digital exhibits.",
            parties=[
                {"id": "rp1", "name": "Directorate of Forensic Investigation", "role": "Complainant"},
                {"id": "rp2", "name": "Ravi Kumar", "role": "Accused"},
                {"id": "rp3", "name": "Suresh Reddy", "role": "Accused"},
                {"id": "rp4", "name": "Priya Sharma", "role": "Witness"}
            ],
            tags=["Cross-Border", "Alibi Conflict", "Section 65B Certified", "Financial Fraud"]
        )
        db.add(c1)
        db.commit()
        print(f"[Seed] Created case: {c1.title}")

    # Evidence for Riverstone
    riverstone_exhibits = [
        {
            "id": "E-RIV-001",
            "file_name": "FIR_Riverstone_01_2026.txt",
            "title": "Certified First Information Report (FIR No. 12/2026)",
            "category": "document",
            "criticality": "Mandatory",
            "content": (
                "DIRECTORATE OF FORENSIC INVESTIGATION - SPECIAL DOCKET\n"
                "FIR Number: 12/2026 | Police Station: Cyber & Economic Offences Wing\n"
                "Date of Registration: 18-Jan-2026 | Investigating Officer: DySP M. V. Raman\n\n"
                "SUMMARY OF OCCURRENCE:\n"
                "Between 14-Jan-2026 and 16-Jan-2026, suspect Ravi Kumar allegedly engaged in an unauthorized "
                "conspiracy session with Suresh Reddy at Hotel Fortune, Vijayawada at 20:00 IST to divert corporate assets.\n"
                "Complainant audit logs indicate irregular escrow clearance of INR 14.5 Crore.\n"
                "Accused claimed under preliminary inquiry that he never visited Vijayawada during that period and was in Hyderabad."
            )
        },
        {
            "id": "E-RIV-002",
            "file_name": "Vijayawada_Hotel_Fortune_CCTV_Log.txt",
            "title": "Hotel Fortune Grand - Visitor Register & ANPR Vehicle Log",
            "category": "physical",
            "criticality": "Supporting",
            "content": (
                "HOTEL FORTUNE GRAND - SECURITY & VISITOR LOG EXTRACT\n"
                "Location: MG Road, Vijayawada, Andhra Pradesh\n"
                "Date: 14-Jan-2026\n\n"
                "20:05 IST: White Toyota Fortuner (Reg: AP 16 BK 4421) enters basement parking P2.\n"
                "20:12 IST: Two individuals matching description of Ravi Kumar and Suresh Reddy enter Private Dining Suite 4.\n"
                "21:45 IST: Both individuals exit lobby towards basement parking.\n"
                "Physical entry register signed with initials 'R.K.'."
            )
        },
        {
            "id": "E-RIV-003",
            "file_name": "Telugu_Audio_Alibi_Intercept.txt",
            "title": "Audio Intercept Transcript - Accused Alibi Statement",
            "category": "digital",
            "criticality": "Mandatory",
            "content": (
                "FORENSIC TRANSCRIPTION OF INTERCEPTED CALL RECORDING\n"
                "Target Device: +91 98490 XXXXX (Ravi Kumar)\n"
                "Date & Timestamp: 14-Jan-2026 at 20:30 IST\n"
                "Language: Telugu & English (Certified Translation)\n\n"
                "Ravi Kumar: 'I am currently at Rajiv Gandhi International Airport in Hyderabad waiting at Gate 14.\n"
                "My flight to Bengaluru is delayed by 45 minutes. I have not left Hyderabad all evening.'\n\n"
                "FORENSIC NOTE: Tower cell triangulation conflicts with background ambient noise signature."
            )
        },
        {
            "id": "E-RIV-004",
            "file_name": "WhatsApp_Shamshabad_Location_Export.txt",
            "title": "WhatsApp Message & Location Pin Export",
            "category": "digital",
            "criticality": "Recommended",
            "content": (
                "DIGITAL FORENSIC EXTRACTION - WHATSAPP CHAT DATABASE\n"
                "Exported Device: OnePlus 12 (Belonging to Accused Ravi Kumar)\n"
                "Timestamp: 14-Jan-2026 20:18:22 IST\n"
                "Recipient: Suresh Reddy\n"
                "Content: Sent live GPS location coordinates pointing to Shamshabad Airport, Hyderabad.\n"
                "Analysis: Device spoofing application 'FakeGPS Pro' package detected in device application cache."
            )
        },
        {
            "id": "E-RIV-005",
            "file_name": "Section_65B_Certificate_Digital_Records.txt",
            "title": "Statutory Section 65B (IEA) / Section 63 (BSA) Certificate",
            "category": "certificate",
            "criticality": "Mandatory",
            "content": (
                "CERTIFICATE UNDER SECTION 65B OF THE INDIAN EVIDENCE ACT, 1872 / SECTION 63 OF BHARATIYA SAKSHYA ADHINIYAM, 2023\n\n"
                "I, K. N. Sastry, System Administrator and Head of Technical Operations at Cyber Forensics Lab, do hereby certify:\n"
                "1. That the electronic records consisting of CCTV logs, digital extracts, and server logs produced herein were generated during the ordinary course of business.\n"
                "2. The recording systems were operating properly at all material times.\n"
                "3. The SHA-256 hash verified copy matches bit-by-bit with the master storage media.\n"
                "Executed on: 22-Jan-2026 | Signature & Seal attached."
            )
        }
    ]

    for ex in riverstone_exhibits:
        existing_ev = db.query(EvidenceModel).filter(EvidenceModel.id == ex["id"]).first()
        raw_bytes = ex["content"].encode("utf-8")
        file_hash = compute_sha256(raw_bytes)
        file_path = UPLOADS_DIR / ex["file_name"]

        # Write actual file to storage
        with open(file_path, "wb") as f:
            f.write(raw_bytes)

        if not existing_ev:
            ev = EvidenceModel(
                id=ex["id"],
                case_id=c1_id,
                title=ex["title"],
                file_name=ex["file_name"],
                file_path=str(file_path),
                file_size=len(raw_bytes),
                file_type="text/plain",
                sha256_hash=file_hash,
                category=ex["category"],
                criticality=ex["criticality"],
                extracted_text=ex["content"],
                page_count=1,
                status="Ingested",
                metadata_json={"source": "Forensic Seeder", "integrity_verified": True}
            )
            db.add(ev)
            print(f"[Seed] Added evidence: {ex['title']} (Hash: {file_hash[:12]}...)")
        else:
            existing_ev.extracted_text = ex["content"]
            existing_ev.sha256_hash = file_hash
            existing_ev.file_path = str(file_path)

        # Index in RAG service memory
        rag_service.index_evidence(
            case_id=c1_id,
            evidence_id=ex["id"],
            file_name=ex["file_name"],
            chunks=[{"page": 1, "text": ex["content"]}]
        )

    # 2. State vs Kumar Case
    c2_id = "case-001"
    existing_c2 = db.query(CaseModel).filter(CaseModel.id == c2_id).first()
    if not existing_c2:
        c2 = CaseModel(
            id=c2_id,
            title="State vs. Kumar & Quantum Tech Ltd.",
            case_number="CR/2026/001",
            case_type="Cybercrime",
            court="High Court of Judicature",
            court_location="New Delhi",
            filing_date="2026-02-10",
            status="Pre-Trial",
            description="Alleged cyber intrusion into corporate treasury, exfiltration of encrypted proprietary source code, and illegal offshore remittance.",
            parties=[
                {"id": "p1", "name": "State NCT of Delhi", "role": "Prosecution"},
                {"id": "p2", "name": "John Kumar", "role": "Accused"},
                {"id": "p3", "name": "Quantum Tech Ltd.", "role": "Co-Accused"}
            ],
            tags=["Data Theft", "Cybercrime", "Financial Fraud"]
        )
        db.add(c2)
        print(f"[Seed] Created case: {c2.title}")

    db.commit()
    db.close()
    print("[Seed] Database successfully seeded with cases, exhibits, and forensic files!")

if __name__ == "__main__":
    seed_database()
