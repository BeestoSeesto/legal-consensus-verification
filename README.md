# Legal Research Verification System
## Multi-Model Consensus Engine for Reducing AI Hallucination Risk

### The Problem

Law students, solo practitioners, and self-represented individuals increasingly use AI tools for legal research. However, a critical risk exists: **AI models hallucinate case citations and legal principles with alarming frequency.**

A single-model approach is dangerous:
- GPT-4 has been documented fabricating entire cases
- Models mix state and federal law without warning
- Citations appear authoritative but may not exist
- No built-in verification mechanism exists

**This tool addresses that gap.**

### The Solution

Rather than trusting a single AI model, this system:

1. **Queries multiple frontier models simultaneously** (Claude Sonnet 4.5, GPT-4, Gemini 2.0)
2. **Cross-references their responses** for consensus
3. **Flags discrepancies** that require human verification
4. **Extracts and compares citations** across models
5. **Maintains audit trails** for compliance

When models **agree** → Higher confidence in the answer  
When models **disagree** → Red flag for manual review

### Key Technical Features

**Multi-API Orchestration**
- Asynchronous calls to Anthropic, OpenAI, and Google APIs
- Error handling for API failures
- Model-agnostic architecture (easily extensible)

**Citation Validation**
- Regex-based extraction of US case citations
- Cross-model citation comparison
- Identification of shared vs. unique citations

**Security & Compliance Considerations**
- API key management via environment variables
- Audit logging of all verification sessions
- No storage of sensitive query data
- Clear disclaimers about limitations

**Designed for Real-World Use**
- Clear output formatting for non-technical users
- Explicit confidence indicators
- Warning flags for high-risk discrepancies

### Technical Stack

- **Python 3.8+**
- **Anthropic API** (Claude Sonnet 4.5)
- **OpenAI API** (GPT-4)
- **Google Generative AI** (Gemini 2.0)
- **python-dotenv** for configuration management

### Installation

```bash
# Clone repository
git clone [your-repo-url]
cd legal-consensus

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your actual API keys
```

### Usage

```python
from verify import LegalConsensusEngine

engine = LegalConsensusEngine()
results = engine.verify_query("What is the standard for qualified immunity?")
engine.display_results(results)
```

### Example Output

```
================================================================================
CONSENSUS ANALYSIS
================================================================================

Models Analyzed: 3
Consensus Level: HIGH

Shared Citations (High Confidence):
  ✓ Harlow v. Fitzgerald, 457 U.S. 800
  ✓ Pearson v. Callahan, 555 U.S. 223

================================================================================
DISCREPANCY WARNINGS
================================================================================

⚠️  Models cited different cases:
   GPT-4: Anderson v. Creighton, 483 U.S. 635
   Claude: Saucier v. Katz, 533 U.S. 194

   → Manual verification strongly recommended
```

### What This Project Demonstrates

**For Cybersecurity/GRC Roles:**
- Multi-system integration with proper error handling
- Security-conscious API key management
- Audit trail implementation for compliance
- Risk assessment and mitigation thinking

**For Legal Tech Positions:**
- Understanding of legal research challenges
- Practical application of AI to real legal workflows
- Awareness of AI limitations in legal contexts
- User-centered design for legal professionals

**For Technical Roles:**
- Clean, modular Python architecture
- API integration across multiple providers
- Pattern recognition and data extraction
- Professional documentation standards

### Limitations & Disclaimers

⚠️ **This tool does NOT:**
- Replace legal research or professional judgment
- Verify substantive accuracy of legal analysis
- Guarantee that cited cases actually exist
- Provide legal advice of any kind

**This tool DOES:**
- Identify consensus and discrepancies across AI models
- Flag potential hallucinations for human review
- Reduce (but not eliminate) citation errors
- Provide structured output for verification workflows

### Roadmap

**Phase 1 (Current):** Basic multi-model consensus
**Phase 2:** Citation validation via legal databases (Caselaw Access Project API)
**Phase 3:** Jurisdiction-specific verification
**Phase 4:** Web interface for non-technical users
**Phase 5:** Integration with legal research platforms

### Author

Built by **Sisto** - First-year law student at Taft Law School with background in cybersecurity (BS, Boise State) and 10 years crisis counseling experience.

This project bridges technical expertise with legal domain knowledge, demonstrating practical application of AI verification systems to reduce risk in legal research contexts.

### License

MIT License - See LICENSE file

### Contributing

Contributions welcome. Please open an issue before submitting major changes.

### Contact

[Your LinkedIn/Email]

---

**Note:** This is a research and verification tool. Always consult qualified legal counsel for legal advice.
