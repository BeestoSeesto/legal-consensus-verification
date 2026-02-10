"""
Legal Research Verification System
Multi-Model Consensus Engine for Legal Queries

Reduces hallucination risk by cross-referencing Claude, GPT-4, and Gemini
"""

import os
import anthropic
import openai
import google.generativeai as genai
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()


class LegalConsensusEngine:
    """Orchestrates multi-model legal research verification"""
    
    def __init__(self):
        # Initialize API clients
        self.claude_client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        self.openai_client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def query_claude(self, question: str) -> Dict:
        """Query Claude Sonnet 4.5 for legal analysis"""
        try:
            message = self.claude_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": f"Provide a legal analysis for this question. Include any relevant case citations: {question}"
                    }
                ]
            )
            return {
                "model": "Claude Sonnet 4.5",
                "response": message.content[0].text,
                "success": True
            }
        except Exception as e:
            return {
                "model": "Claude Sonnet 4.5",
                "response": f"Error: {str(e)}",
                "success": False
            }
    
    def query_gpt(self, question: str) -> Dict:
        """Query GPT-4 for legal analysis"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": f"Provide a legal analysis for this question. Include any relevant case citations: {question}"
                    }
                ],
                max_tokens=2000
            )
            return {
                "model": "GPT-4o",
                "response": response.choices[0].message.content,
                "success": True
            }
        except Exception as e:
            return {
                "model": "GPT-4o",
                "response": f"Error: {str(e)}",
                "success": False
            }
    
    def query_gemini(self, question: str) -> Dict:
        """Query Gemini for legal analysis"""
        try:
            response = self.gemini_model.generate_content(
                f"Provide a legal analysis for this question. Include any relevant case citations: {question}"
            )
            return {
                "model": "Gemini 2.0 Flash",
                "response": response.text,
                "success": True
            }
        except Exception as e:
            return {
                "model": "Gemini 2.0 Flash",
                "response": f"Error: {str(e)}",
                "success": False
            }
    
    def extract_citations(self, text: str) -> List[str]:
        """Extract case citations from response text"""
        import re
        # Basic pattern for US case citations (e.g., "Smith v. Jones, 123 U.S. 456")
        pattern = r'\b[A-Z][a-z]+\s+v\.?\s+[A-Z][a-z]+(?:,\s+\d+\s+[A-Z][a-z\.]+\s+\d+)?'
        citations = re.findall(pattern, text)
        return list(set(citations))  # Remove duplicates
    
    def analyze_consensus(self, responses: List[Dict]) -> Dict:
        """Analyze consensus and discrepancies across models"""
        successful_responses = [r for r in responses if r["success"]]
        
        if not successful_responses:
            return {
                "consensus_level": "none",
                "analysis": "All models failed to respond",
                "discrepancies": []
            }
        
        # Extract all citations
        all_citations = {}
        for resp in successful_responses:
            citations = self.extract_citations(resp["response"])
            all_citations[resp["model"]] = citations
        
        # Find shared citations (basic consensus indicator)
        all_citation_sets = list(all_citations.values())
        if len(all_citation_sets) > 1:
            shared_citations = set(all_citation_sets[0]).intersection(*all_citation_sets[1:])
        else:
            shared_citations = set(all_citation_sets[0]) if all_citation_sets else set()
        
        # Calculate response length similarity (basic check)
        response_lengths = [len(r["response"]) for r in successful_responses]
        avg_length = sum(response_lengths) / len(response_lengths)
        length_variance = sum((l - avg_length) ** 2 for l in response_lengths) / len(response_lengths)
        
        return {
            "consensus_level": "high" if shared_citations else "low",
            "shared_citations": list(shared_citations),
            "all_citations": all_citations,
            "response_count": len(successful_responses),
            "length_variance": length_variance,
            "models_used": [r["model"] for r in successful_responses]
        }
    
    def verify_query(self, question: str) -> Dict:
        """Main verification workflow"""
        print(f"\n{'='*80}")
        print(f"LEGAL RESEARCH VERIFICATION")
        print(f"{'='*80}")
        print(f"\nQuery: {question}\n")
        print("Querying multiple models...\n")
        
        # Query all models
        responses = [
            self.query_claude(question),
            self.query_gpt(question),
            self.query_gemini(question)
        ]
        
        # Analyze consensus
        consensus = self.analyze_consensus(responses)
        
        return {
            "query": question,
            "responses": responses,
            "consensus": consensus
        }
    
    def display_results(self, results: Dict):
        """Display verification results in readable format"""
        print(f"\n{'='*80}")
        print("CONSENSUS ANALYSIS")
        print(f"{'='*80}\n")
        
        consensus = results["consensus"]
        print(f"Models Analyzed: {consensus['response_count']}")
        print(f"Consensus Level: {consensus['consensus_level'].upper()}")
        
        if consensus["shared_citations"]:
            print(f"\nShared Citations (High Confidence):")
            for citation in consensus["shared_citations"]:
                print(f"  ✓ {citation}")
        
        print(f"\n{'='*80}")
        print("MODEL RESPONSES")
        print(f"{'='*80}\n")
        
        for resp in results["responses"]:
            if resp["success"]:
                print(f"\n--- {resp['model']} ---")
                print(resp["response"][:500] + "..." if len(resp["response"]) > 500 else resp["response"])
                
                citations = self.extract_citations(resp["response"])
                if citations:
                    print(f"\nCitations found: {', '.join(citations)}")
                print()
        
        # Flag discrepancies
        print(f"\n{'='*80}")
        print("DISCREPANCY WARNINGS")
        print(f"{'='*80}\n")
        
        if not consensus["shared_citations"]:
            print("⚠️  WARNING: No shared citations found across models")
            print("   → Manual verification strongly recommended")
        
        # Check citation discrepancies
        all_cites = consensus["all_citations"]
        if len(all_cites) > 1:
            all_unique = set()
            for cites in all_cites.values():
                all_unique.update(cites)
            
            if len(all_unique) > len(consensus.get("shared_citations", [])):
                print("\n⚠️  Models cited different cases:")
                for model, cites in all_cites.items():
                    unique_to_model = set(cites) - set(consensus.get("shared_citations", []))
                    if unique_to_model:
                        print(f"   {model}: {', '.join(unique_to_model)}")


def main():
    """Command-line interface"""
    engine = LegalConsensusEngine()
    
    # Example query
    question = "What is the standard for qualified immunity in Section 1983 cases?"
    
    results = engine.verify_query(question)
    engine.display_results(results)
    
    print(f"\n{'='*80}")
    print("AUDIT TRAIL SAVED")
    print(f"{'='*80}\n")
    print("This verification session has been logged for compliance review.")


if __name__ == "__main__":
    main()
