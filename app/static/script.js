document.addEventListener('DOMContentLoaded', () => {
  const linkIn      = document.getElementById('youtubeLink');
  const fetchBtn    = document.getElementById('fetchVideoInfoBtn');
  const infoDiv     = document.getElementById('videoInfo');
  const thumbImg    = document.getElementById('videoThumbnail');
  const titleH2     = document.getElementById('videoTitle');
  const selectEl    = document.getElementById('resolutionSelect');
  const downloadBtn = document.getElementById('downloadBtn');
  const statusEl    = document.getElementById('statusMessage');
  const themeBtn    = document.getElementById('themeToggleBtn');
  let currentUrl = null;

  // Theme toggle
  function applyTheme(mode) {
    document.body.classList.toggle('dark-mode', mode === 'dark');
  }
  const saved = localStorage.getItem('theme') || 'light';
  applyTheme(saved);
  themeBtn.addEventListener('click', () => {
    const next = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
    applyTheme(next);
    localStorage.setItem('theme', next);
  });

  // Fetch info
  fetchBtn.addEventListener('click', async () => {
    const url = linkIn.value.trim();
    if (!url) return showStatus('Paste a URL first', 'error');
    showStatus('Fetching info…', 'info');
    try {
      const resp = await fetch(`/api/info/?url=${encodeURIComponent(url)}`);
      if (!resp.ok) throw new Error(await resp.text());
      const data = await resp.json();
      currentUrl = url;
      thumbImg.src = data.thumbnailUrl;
      titleH2.textContent = data.title;
      selectEl.innerHTML = data.resolutions
        .map(r => `<option value="${r.quality}|${r.container}">${r.qualityLabel}</option>`)
        .join('');
      infoDiv.classList.remove('hidden');
      showStatus('Select resolution and click Download', 'success');
    } catch (e) {
      showStatus(e.message, 'error');
    }
  });

  // Download
  downloadBtn.addEventListener('click', () => {
    if (!currentUrl) return showStatus('Fetch info first', 'error');
    const [quality, container] = selectEl.value.split('|');
    showStatus('Starting download…', 'info');
    window.location.href =
      `/api/download/?url=${encodeURIComponent(currentUrl)}&quality=${quality}&container=${container}`;
  });

  function showStatus(msg, type = 'info') {
    statusEl.textContent = msg;
    statusEl.className = `status-${type}`;
  }
});
