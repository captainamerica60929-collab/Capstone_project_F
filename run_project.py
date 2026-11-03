"""Run all project stages in sequence. Use this after installing requirements."""
from src.data_pipeline import audit,clean_data,validate
from src.customer_models import rfm_and_segments,build_lapse_model
from src.triage import run_pipeline,FEW
from src.policy_rag import PolicyRAG,evaluate,compare_chunking
from src.refund_agent import run_agent
def main():
    print("\n=== PART A: AUDIT / CLEAN / VALIDATE ===")
    audit(); clean_data(); validate()
    print("\n=== PART B: SEGMENTS & LAPSE MODEL ===")
    rfm,diagnostics,profile,pca=rfm_and_segments()
    print("K-means diagnostics:\n",diagnostics.to_string(index=False))
    print("Segment profile:\n",profile.to_string(index=False)); print("PCA explained variance:",pca)
    print("Lapse model summary:",build_lapse_model())
    print("\n=== PART C: PRIVACY GUARDRAILS & TRIAGE ===")
    triage,summary=run_pipeline(prompt=FEW,token_budget=100000)
    print(summary); print(triage.head().to_string(index=False))
    print("\n=== PART D: POLICY RAG & REFUND AGENT ===")
    rag=PolicyRAG(); print("chunks:",len(rag.chunks)); print(evaluate(rag).to_string(index=False))
    print("\nChunking strategy comparison:\n", compare_chunking().to_string(index=False))
    print("\nRunning Refund Agent Scenarios:")
    print("1. Eligible auto-refund (ORD-100048):", run_agent("Please refund order ORD-100048", scenario_id="cli-auto"))
    print("2. Idempotent re-refund (ORD-100048):", run_agent("Please refund order ORD-100048", scenario_id="cli-idempotent"))
    print("3. High-value escalation (ORD-100145):", run_agent("Please refund order ORD-100145", scenario_id="cli-escalate"))
    print("4. Ineligible on-time delivery (ORD-100008):", run_agent("Please refund order ORD-100008", scenario_id="cli-denied"))
    print("\nProject pipeline finished. Review outputs/ and data/instamart.db.")
if __name__=="__main__": main()
