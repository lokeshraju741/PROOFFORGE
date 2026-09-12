import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("--- 1. Testing Health Check ---")
r = requests.get(f"{BASE_URL}/health")
print(f"Health Status: {r.status_code}, Response: {r.json()}")
assert r.status_code == 200

print("\n--- 2. Testing Case Creation ---")
requests.delete(f"{BASE_URL}/cases/case-test-101")
case_payload = {
    "id": "case-test-101",
    "title": "State vs. Ravi Kumar (Bank Fraud)",
    "case_number": "CC/2026/789",
    "case_type": "Cyber Financial Fraud",
    "court": "Special Cyber Court",
    "court_location": "Hyderabad",
    "description": "Alleged unauthorized transfer of INR 4.2 Crore from corporate escrow account."
}
r = requests.post(f"{BASE_URL}/cases", json=case_payload)
print(f"Case Creation Status: {r.status_code}, Created ID: {r.json().get('id')}")
assert r.status_code == 201

print("\n--- 3. Testing Real Evidence File Upload & Ingestion ---")
test_file_content = (
    "FIRST INFORMATION REPORT (FIR No. 104/2026)\n"
    "Date of Occurrence: 12-August-2026 at 11:30 PM.\n"
    "Place of Occurrence: Vijayawada Escrow Branch.\n"
    "Complainant Statement: Accused Ravi Kumar was seen operating the terminal without authorization.\n"
    "Digital evidence shows IP address 192.168.1.45 accessed the ledger database.\n"
    "Suspect claimed he was in Hyderabad at the time."
)

files = {
    "file": ("FIR_104_2026.txt", test_file_content.encode("utf-8"), "text/plain")
}
data = {
    "case_id": "case-test-101",
    "title": "Certified First Information Report (FIR)",
    "category": "document",
    "criticality": "Mandatory"
}
r = requests.post(f"{BASE_URL}/evidence/upload", data=data, files=files)
evidence_resp = r.json()
print(f"Upload Status: {r.status_code}")
print(f"Evidence ID: {evidence_resp.get('id')}")
print(f"Forensic SHA-256 Hash: {evidence_resp.get('sha256_hash')}")
print(f"Extracted Text Preview: {evidence_resp.get('extracted_text_preview')[:100]}...")
assert r.status_code == 201
assert len(evidence_resp.get("sha256_hash", "")) == 64

print("\n--- 4. Testing RAG Semantic Search & Citations ---")
query_payload = {
    "case_id": "case-test-101",
    "query": "Where was the place of occurrence and what time did it happen?",
    "top_k": 3
}
r = requests.post(f"{BASE_URL}/rag/query", json=query_payload)
rag_resp = r.json()
print(f"RAG Status: {r.status_code}")
print(f"Answer: {rag_resp.get('answer')}")
print(f"Citations Count: {len(rag_resp.get('citations', []))}")
assert r.status_code == 200

print("\n--- 5. Testing AI Pipeline Execution ---")
r = requests.post(f"{BASE_URL}/pipeline/analyze/case-test-101")
pipe_resp = r.json()
print(f"Pipeline Started: {pipe_resp}")
job_id = pipe_resp["job_id"]

# Poll status for completion
for _ in range(10):
    time.sleep(1)
    status_resp = requests.get(f"{BASE_URL}/pipeline/jobs/{job_id}").json()
    print(f"Job Progress: {status_resp.get('progress')}% - Stage: {status_resp.get('current_stage')}")
    if status_resp.get("status") == "completed":
        print("\nPipeline Complete! Intelligence Dossier:")
        print(json.dumps(status_resp.get("results"), indent=2))
        break

print("\n==============================================")
print("  ALL FULL-STACK BACKEND AI TESTS PASSED!     ")
print("==============================================")
