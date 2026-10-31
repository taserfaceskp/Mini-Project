import requests
import json

def analyze_threat(detected_brand, domain_match, urgency_score, email_text):
    url = "http://localhost:11434/api/generate"
    
    # Construct a technical analysis prompt
    prompt = f"System Prompt: You are a professional, technical security analyst. Analyze the following indicators and text to generate a concise summary explaining why this is a credential harvesting attempt.\n\nIndicators:\n- Detected Brand Logo: {detected_brand}\n- Logo Domain Matches Host: {domain_match}\n- Text Urgency Score: {urgency_score}/1.0\n\nEmail Text:\n{email_text}\n\nWrite a concise summary explaining the social engineering and deceptive tactics used in under 100 words."
    
    payload = {
        "model": "qwen2.5:3b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No explanation generated.")
        else:
            return f"Error from Ollama API: Status {response.status_code}"
    except Exception as e:
        return f"Failed to connect to local Ollama server: {str(e)}"

if __name__ == "__main__":
    # Test case representing a credential harvesting mock scenario
    test_explanation = analyze_threat(
        detected_brand="Microsoft",
        domain_match=False,
        urgency_score=0.95,
        email_text="URGENT: Your password expires in 2 hours. Reset at: http://suspicious-update-microsoft.net"
    )
    print("\n--- Test Threat Analysis Explanation ---\n")
    print(test_explanation)
