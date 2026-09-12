# ProofForge AI — Legal Case Intelligence & Management Platform

**ProofForge AI** is a fully functional legal case-management and AI intelligence SaaS platform designed for advocates, senior partners, legal assistants, and clients.

The platform follows a complete end-to-end user workflow:

$$\text{Login} \longrightarrow \text{Dashboard} \longrightarrow \text{Create Case} \longrightarrow \text{Case Information} \longrightarrow \text{Upload Materials} \longrightarrow \text{Processing Pipeline} \longrightarrow \text{Case Workspace} \longrightarrow \text{Lawyer Review} \longrightarrow \text{Intelligence Reports (PDF)}$$

---

## 🌟 Key Features & Capabilities

### 1. First Screen — Secure Login & Registration
- **Login Screen**: Logo, tagline (*"AI-Powered Legal Case Intelligence & Preparation"*), email/password validation, show/hide password toggle, remember me, forgot password, role selector (**Lawyer, Junior Lawyer, Legal Assistant, Client, Administrator**), credentials authentication, and JWT session handling.
- **Registration Screen**: Organization registration with 4-digit OTP verification simulation.
- **Quick Demo Launch**: Instant Senior Partner & Associate demo access buttons.

### 2. Main Dashboard & Portfolio
- **8 Workload Summary Cards**: Active Cases, Total Cases, Evidence Items, Pending Tasks, Upcoming Hearings, Potential Evidence Gaps, Potential Contradictions, Reports Generated.
- **Case Portfolio**: Status badges, court jurisdiction, client name, hearing date, evidence count, and AI index.
- **Quick Actions**: *Open Workspace*, *View Contradictions*, *View Evidence*, *Generate Report*.
- **Reload Demo Data**: One-click reset to reload pre-loaded legal sample data.

### 3. Multi-Step Case Creation Wizard (`/cases/new`)
1. **Select Case Type**: 12 selectable cards (*Criminal, Civil, Family, Property, Corporate, Labour, Consumer, Cybercrime, Constitutional, Financial, Traffic, Other*).
2. **Basic Case Information**: Case ID, Title, Case #, Court, Location, FIR #, Police Station, Filing Date, Status, Judge, Client, Opposing Party & Counsel, Description.
3. **Party Information**: Add multiple parties with roles (*Plaintiff, Defendant, Petitioner, Respondent, Complainant, Accused, Witness, Expert, IO*).
4. **Case Facts Ingestion**: Manual fact entry & AI fact extraction labeled `"AI-generated — Lawyer verification required"`.
5. **Upload Case Materials**: Drag & drop uploader for **PDF, DOCX, TXT, XLSX, CSV, JPG, PNG, MP3, WAV, MP4, MOV**. Metadata tagging (*FIR, Contract, Bank Statement, Chat, CCTV, Audio*), SHA-256 file hashing, file size & progress.

### 4. Background Processing Pipeline Screen (`"Analyzing Your Case"`)
- Real-time visual progress tracker: *Upload → Validation → Security Scan → OCR → Text Extraction → Audio Transcription → Video Processing → Entity Extraction → Timeline → Claims → Contradictions → Gaps → Legal RAG Indexing*.
- Non-blocking UI allows exploring the workspace while background processing completes.

### 5. Central Case Workspace (`/cases/{id}`) & 16 Interactive Workspace Tabs
1. **Overview Tab**: Executive AI Summary, key facts, contradiction & gap highlights, clickable citations.
2. **Evidence Manager Tab**: Table & Card grid, category filter, search, upload metadata editor.
3. **Evidence Viewer Modal**: Previews PDF documents, audio wiretaps with speaker transcripts, video CCTV keyframes, and image OCR.
4. **Chronology & Timeline Tab**: Chronological event feed with dates, confidence levels, add/edit modal, and direct source evidence triggers.
5. **Claim-Evidence Matrix Tab**: Claims mapped to supporting & contradicting evidence and witnesses with clickable evidence triggers.
6. **Contradictions Dashboard**: Side-by-side Source A vs Source B comparison, date/fact differences, AI rationale, and lawyer verification safety disclaimers.
7. **Evidence Gap Dashboard**: Proof gap scan with missing evidence warnings and requisition recommendations.
8. **Legal Research RAG Tab**: Natural language query engine returning verified Supreme Court precedents, ratio decidendi, and citations.
9. **Case AI Assistant Tab**: Context-aware chatbot restricted to case docs, providing clickable citation pills (`Source: Agreement.pdf, Page 4, Evidence ID: E-023`) that open the Evidence Viewer Modal.
10. **Witnesses Tab**: Statement summaries, contradiction alerts, AI interview clarification topics & cross-examination prep.
11. **Hearings Tab**: Hearing schedule, court purpose, orders summary, post-hearing notes.
12. **Knowledge Graph Tab**: Interactive graphical node map connecting Party → Event → Evidence → Claim → Legal Issue → Judgment.
13. **What-If Analysis Tab**: Dependency analyzer simulating impact of excluding specific evidence items.
14. **Reports Tab**: 21-section Case Intelligence Report previewer & instant PDF exporter using `jsPDF` / `html2canvas`.
15. **Tasks Tab**: Action item task board with priority badges and completion toggle.
16. **Audit Log Tab**: Security audit trail logging authentication, evidence ingestion, RAG queries, and report exports.

---

## 🛠️ Installation & Running Locally

### Prerequisites
- Node.js (v18+)
- npm (v9+)

### Running All Services (Unified)
To launch **Frontend**, **Backend API**, and **Swagger API Docs** all at once with a single command:

```bash
# Option 1: Using npm
npm start
# or: npm run dev:all

# Option 2: Using the Python launcher
python run_all.py

# Option 3: On Windows (Double-click or run)
run_all.bat
```

### Accessing the Combined Services:
- **Combined Web App**: [http://localhost:8080](http://localhost:8080)
- **Combined Backend API**: [http://localhost:8080/api](http://localhost:8080/api)
- **Combined Swagger API Docs**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **Direct Backend**: [http://127.0.0.1:8000](http://127.0.0.1:8000) (Docs: `http://127.0.0.1:8000/docs`)

### Individual Development Servers:
```bash
# Frontend only
npm run dev

# Backend only
backend\venv\Scripts\python.exe backend/run_server.py
```

### Production Build
```bash
# Compile production bundle
npm run build
```

---

## 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t proofforge-ai .

# Run Docker container
docker run -p 8080:80 proofforge-ai
```
Access the containerized application at [`http://localhost:8080`](http://localhost:8080).

---

## 🔒 Security & AI Safety Guarantees
- **RBAC & Audit Trails**: Access levels for Lawyer, Associate, Assistant, Client, and Admin. All security actions logged to local audit store.
- **Lawyer Verification**: All AI-extracted facts, contradiction alerts, and witness strategies are clearly labeled `"AI-generated — Lawyer verification required"`.
- **No Speculative Judgments**: The AI strictly provides factual dependency analysis and source citations without computing fake win probabilities or guilt assertions.
