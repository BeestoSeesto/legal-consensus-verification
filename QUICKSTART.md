# Quick Start Guide

## Installation (2 minutes)

```bash
# 1. Clone this repo
git clone https://github.com/[your-username]/legal-consensus-verification
cd legal-consensus-verification

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up API keys
cp .env.example .env
# Edit .env and add your actual API keys
```

## Get API Keys

You'll need three API keys (all have free tiers):

1. **Anthropic API Key**
   - Sign up at: https://console.anthropic.com/
   - Free tier: $5 credit

2. **OpenAI API Key**
   - Sign up at: https://platform.openai.com/
   - Free tier: $5 credit

3. **Google API Key**
   - Sign up at: https://makersuite.google.com/
   - Free tier: Available

## Run Demo (No API Keys Required)

```bash
python demo.py
```

This shows example output without making API calls.

## Run Actual Verification

```bash
python verify.py
```

This queries all three models with your legal question.

## Customize Your Query

Edit `verify.py` line 129:

```python
question = "Your legal question here"
```

## Example Legal Questions

- "What is the standard for qualified immunity in Section 1983 cases?"
- "What are the elements of negligence in California?"
- "When does the statute of limitations begin for legal malpractice?"
- "What is the test for personal jurisdiction under International Shoe?"

## Understanding the Output

**High Consensus** = Models agree on citations → Higher confidence  
**Low Consensus** = Models disagree → Verify manually

Always review the actual responses and citations before relying on results.

## Need Help?

- Check the full README.md
- Open an issue on GitHub
- Review the code comments in verify.py
