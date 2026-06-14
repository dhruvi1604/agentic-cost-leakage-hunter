import pytest

from src.llm.backends import GroqLLM, MockLLM


def test_mock_llm_returns_text():
    response = MockLLM().generate("any prompt")

    assert isinstance(response, str)
    assert len(response) > 0


def test_groq_llm_requires_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with pytest.raises(ValueError):
        GroqLLM()
        
        
#monkeypatch — a tool pytest hands you (just by naming it as an argument) to temporarily change the environment for one test. monkeypatch.delenv("GROQ_API_KEY") says "pretend the key doesn't exist for this test." After the test, pytest puts everything back. This lets us guarantee the no-key situation. (raising=False = "don't error if it was already missing" — which on this laptop, it is.)
#with pytest.raises(ValueError): — this flips the meaning of failure. Normally a crash = test fails. Here we're saying "I expect GroqLLM() to raise ValueError when there's no key. If it raises → ✅ pass. If it doesn't raise → ❌ fail." You're testing that your safety check actually fires.
#So test_groq_llm_requires_api_key reads as: "prove that my own guard rejects a missing key." That's testing your logic, not Groq's.
