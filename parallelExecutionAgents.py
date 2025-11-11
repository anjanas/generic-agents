import os
from openai import OpenAI
from dotenv import load_dotenv
import threading
import re  

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI(
    #base_url = "https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

# Thread lock for thread-safe operations
outputs_lock = threading.Lock()

def llm_call(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Basic LLM call wrapper."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def extract_xml(text: str, tag: str) -> str:
    """Extract content between XML-style tags."""
    pattern = rf"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

 

# Example contract text (in a real application, this would be loaded from a file)
contract_text = """
CONSULTING AGREEMENT

This Consulting Agreement (the "Agreement") is made effective as of January 1, 2025 (the "Effective Date"), by and between ABC Corporation, a Delaware corporation ("Client"), and XYZ Consulting LLC, a California limited liability company ("Consultant").

1. SERVICES. Consultant shall provide Client with the following services: strategic business consulting, market analysis, and technology implementation advice (the "Services").

2. TERM. This Agreement shall commence on the Effective Date and shall continue for a period of 12 months, unless earlier terminated.

3. COMPENSATION. Client shall pay Consultant a fee of $10,000 per month for Services rendered. Payment shall be made within 30 days of receipt of Consultant's invoice.

4. CONFIDENTIALITY. Consultant acknowledges that during the engagement, Consultant may have access to confidential information. Consultant agrees to maintain the confidentiality of all such information.

5. INTELLECTUAL PROPERTY. All materials developed by Consultant shall be the property of Client. Consultant assigns all right, title, and interest in such materials to Client.

6. TERMINATION. Either party may terminate this Agreement with 30 days' written notice. Client shall pay Consultant for Services performed through the termination date.

7. GOVERNING LAW. This Agreement shall be governed by the laws of the State of Delaware.

8. LIMITATION OF LIABILITY. Consultant's liability shall be limited to the amount of fees paid by Client under this Agreement.

9. INDEMNIFICATION. Client shall indemnify Consultant against all claims arising from use of materials provided by Client.

10. ENTIRE AGREEMENT. This Agreement constitutes the entire understanding between the parties and supersedes all prior agreements.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.
"""

# Agent classes for contract analysis

class LegalTermsChecker:
    """Agent that checks for problematic legal terms and clauses in contracts."""
    def run(self, contract_text):
        prompt = f"""
        You are a legal terms checker. Your task is to analyze the following contract text and check for problematic legal terms and clauses.
        
        Contract Text:
        {contract_text}
        
        Return your response in the following format:
        <response>
        - Identify any problematic legal terms and clauses.
        - Provide a brief explanation for each problematic term or clause.
        - Suggest alternative terms or clauses that are more compliant with the law.
        </response>
        """
        raw_output = llm_call(prompt)
        print("\n[Raw Legal Terms Checker Output]\n", raw_output)
        return extract_xml(raw_output, "response")

class ComplianceValidator:
    """Agent that validates regulatory and industry compliance of contracts."""
    def run(self, contract_text):
        prompt = f"""
        You are a compliance validator. Your task is to analyze the following contract text and check for regulatory and industry compliance.
        
        Contract Text:
        {contract_text}
        
        Return your response in the following format:
        <response>
        - Identify any regulatory or industry compliance issues.
        - Provide a brief explanation for each compliance issue.
        - Suggest alternative terms or clauses that are more compliant with the law.
        </response>
        """
        raw_output = llm_call(prompt)
        print("\n[Raw Compliance Validator Output]\n", raw_output)
        return extract_xml(raw_output, "response")

class FinancialRiskAssessor:
    """Agent that assesses financial risks and liabilities in contracts."""
    def run(self, contract_text):
        prompt = f"""
        You are a financial risk assessor. Your task is to analyze the following contract text and assess the financial risks and liabilities.
        
        Contract Text:
        {contract_text}
        
        Return your response in the following format:
        <response>
        - Identify any financial risks or liabilities.
        - Provide a brief explanation for each financial risk or liability.
        - Suggest alternative terms or clauses that are more compliant with the law.
        </response>
        """
        raw_output = llm_call(prompt)
        print("\n[Raw Financial Risk Assessor Output]\n", raw_output)
        return extract_xml(raw_output, "response")


class SummaryAgent:
    """Agent that synthesizes findings from all specialized agents."""
    def run(self, contract_text, inputs):
        legal_terms_output = inputs[0] if len(inputs) > 0 else ""
        compliance_output = inputs[1] if len(inputs) > 1 else ""
        financial_risk_output = inputs[2] if len(inputs) > 2 else ""
        
        prompt = f"""
        You are a summary agent. Your task is to synthesize the findings from all specialized agents and create a comprehensive summary.
        
        Contract Text:
        {contract_text}
        
        Legal Terms Checker Findings:
        {legal_terms_output}
        
        Compliance Validator Findings:
        {compliance_output}
        
        Financial Risk Assessor Findings:
        {financial_risk_output}
        
        Return your response in the following format:
        <response>
        - Summarize the findings from all specialized agents.
        - Provide a brief explanation for each finding.
        - Suggest alternative terms or clauses that are more compliant with the law.
        </response>
        """
        raw_output = llm_call(prompt)
        print("\n[Raw Summary Agent Output]\n", raw_output)
        return extract_xml(raw_output, "response")

# Main function to run all agents in parallel
def analyze_contract(contract_text):
    """Run all agents in parallel and summarize their findings."""
    # Local dictionary for thread-safe collection of agent outputs
    agent_outputs = {}
    
    legal_terms_checker = LegalTermsChecker()
    compliance_validator = ComplianceValidator()
    financial_risk_assessor = FinancialRiskAssessor()
    summary_agent = SummaryAgent()

    # Wrapper functions to capture results in thread-safe manner
    def run_legal_terms_checker():
        result = legal_terms_checker.run(contract_text)
        with outputs_lock:
            agent_outputs['legal_terms'] = result
    
    def run_compliance_validator():
        result = compliance_validator.run(contract_text)
        with outputs_lock:
            agent_outputs['compliance'] = result
    
    def run_financial_risk_assessor():
        result = financial_risk_assessor.run(contract_text)
        with outputs_lock:
            agent_outputs['financial_risk'] = result

    # Start all agent threads
    legal_terms_checker_thread = threading.Thread(target=run_legal_terms_checker)
    compliance_validator_thread = threading.Thread(target=run_compliance_validator)
    financial_risk_assessor_thread = threading.Thread(target=run_financial_risk_assessor)
   
    legal_terms_checker_thread.start()
    compliance_validator_thread.start()
    financial_risk_assessor_thread.start()
   
    # Wait for all threads to complete
    legal_terms_checker_thread.join()
    compliance_validator_thread.join()
    financial_risk_assessor_thread.join()

    # Collect results from thread-safe dictionary
    legal_terms_checker_output = agent_outputs.get('legal_terms', '')
    compliance_validator_output = agent_outputs.get('compliance', '')
    financial_risk_assessor_output = agent_outputs.get('financial_risk', '')

    # Run summary agent with collected outputs
    summary_agent_output = summary_agent.run(contract_text, [legal_terms_checker_output, compliance_validator_output, financial_risk_assessor_output])
    return summary_agent_output

if __name__ == "__main__":
    print("Enterprise Contract Analysis System")
    print("Analyzing contract...")
    
    final_analysis = analyze_contract(contract_text)
    print("\n=== FINAL CONTRACT ANALYSIS ===\n")
    print(final_analysis)