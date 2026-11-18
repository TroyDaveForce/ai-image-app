import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [negativePrompt, setNegativePrompt] = useState(''); // NEW
  const [aspectRatio, setAspectRatio] = useState('1:1'); // NEW
  const [imageUrl, setImageUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedModel, setSelectedModel] = useState('pollinations-flux');
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/history');
      const data = await response.json();
      if (response.ok) setHistory(data);
    } catch (err) {
      console.error("Failed to fetch history", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setIsLoading(true);
    setError('');
    setImageUrl('');

    // Calculate width and height based on aspect ratio
    let width = 1024;
    let height = 1024;
    if (aspectRatio === '16:9') { width = 1344; height = 768; }
    if (aspectRatio === '9:16') { width = 768; height = 1344; }

    try {
      const response = await fetch('http://localhost:3001/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: prompt,
          negative_prompt: negativePrompt,
          model_id: selectedModel,
          width: width,
          height: height,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate image');
      }

      setImageUrl(data.image_url);
      fetchHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!imageUrl) return;
    try {
      const response = await fetch(imageUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ai-image-${Date.now()}.jpg`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Failed to download image.");
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>AI Image Generator</h1>
      </header>

      <main className="main-content">
        {error && <div className="error-message">{error}</div>}
        
        {isLoading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Generating...</p>
          </div>
        )}

        {imageUrl && !isLoading && (
          <div className="image-container">
            <img src={imageUrl} alt={prompt} className="generated-image" style={{ maxHeight: '60vh', objectFit: 'contain' }} />
            <div className="button-group">
              <button className="download-btn" onClick={handleDownload}>⬇️ Download</button>
              <button className="download-btn" onClick={() => setImageUrl('')}>🔄 Gallery</button>
            </div>
          </div>
        )}

        {!imageUrl && !isLoading && history.length > 0 && (
          <div className="history-section">
            <h2>Recent Creations</h2>
            <div className="history-grid">
              {history.map((item) => (
                <div key={item.id} className="history-item" onClick={() => setImageUrl(item.image_url)}>
                  <img src={item.image_url} alt={item.prompt} />
                  <div className="history-prompt">{item.prompt}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className="input-area">
        <form onSubmit={handleGenerate} className="input-form-advanced">
          {/* TOP ROW: Model and Aspect Ratio */}
          <div className="form-row">
            <select className="model-select" value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)} disabled={isLoading}>
              <option value="pollinations-flux">Pollinations (Free)</option>
              <option value="cloudflare-flux">Cloudflare FLUX</option> {/* <--- ADDED THIS LINE */}
              <option value="huggingface-flux">Hugging Face</option>
              <option value="fal-flux-2-flash">FAL FLUX 2 Flash</option>
              <option value="ideogram-4-5">Ideogram 4.5</option>
              <option value="openai-gpt-image-1">OpenAI GPT-Image</option>
            </select>

            <select className="model-select" value={aspectRatio} onChange={(e) => setAspectRatio(e.target.value)} disabled={isLoading}>
              <option value="1:1">Square (1:1)</option>
              <option value="16:9">Landscape (16:9)</option>
              <option value="9:16">Portrait (9:16)</option>
            </select>
          </div>

          {/* MIDDLE ROW: Main Prompt */}
          <div className="form-row">
            <input type="text" placeholder="Describe the image you want to create..." value={prompt} onChange={(e) => setPrompt(e.target.value)} disabled={isLoading} className="prompt-input" />
            <button type="submit" disabled={isLoading || !prompt.trim()} className="send-btn">
              {isLoading ? 'Wait...' : 'Generate'}
            </button>
          </div>

          {/* BOTTOM ROW: Negative Prompt */}
          <div className="form-row">
             <input type="text" placeholder="Negative prompt (what to avoid: blurry, ugly, extra limbs...)" value={negativePrompt} onChange={(e) => setNegativePrompt(e.target.value)} disabled={isLoading} className="prompt-input small-input" />
          </div>
        </form>
      </footer>
    </div>
  );
}

export default App;