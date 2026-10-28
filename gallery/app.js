let libraryData = null;
let activeCategory = 'all';
let searchQuery = '';
const selectedCards = new Set();
let activeModalCard = null;

// DOM Elements
const elements = {
  categoryList: document.getElementById('categoryList'),
  cardGrid: document.getElementById('cardGrid'),
  searchInput: document.getElementById('searchInput'),
  btnClearSearch: document.getElementById('btnClearSearch'),
  emptyState: document.getElementById('emptyState'),
  currentCategoryTitle: document.getElementById('currentCategoryTitle'),
  activeCardCount: document.getElementById('activeCardCount'),
  statHolymoly: document.getElementById('statHolymoly'),
  statShotcraft: document.getElementById('statShotcraft'),
  statTotal: document.getElementById('statTotal'),
  selectionDock: document.getElementById('selectionDock'),
  dockSelectedCount: document.getElementById('dockSelectedCount'),
  dockSelectedNames: document.getElementById('dockSelectedNames'),
  btnDockClear: document.getElementById('btnDockClear'),
  btnDockRaw: document.getElementById('btnDockRaw'),
  btnDockPrompt: document.getElementById('btnDockPrompt'),
  modalOverlay: document.getElementById('modalOverlay'),
  modalClose: document.getElementById('modalClose'),
  modalVideo: document.getElementById('modalVideo'),
  modalTitle: document.getElementById('modalTitle'),
  modalSummary: document.getElementById('modalSummary'),
  modalDirective: document.getElementById('modalDirective'),
  modalTags: document.getElementById('modalTags'),
  btnModalSelect: document.getElementById('btnModalSelect'),
  toast: document.getElementById('toast'),
};

// Toast notification helper
function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add('show');
  setTimeout(() => {
    elements.toast.classList.remove('show');
  }, 3200);
}

// Copy to clipboard helper
async function copyToClipboard(text, successMsg) {
  try {
    await navigator.clipboard.writeText(text);
    showToast(successMsg || '✅ Berhasil disalin ke clipboard!');
  } catch (err) {
    // Fallback
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showToast(successMsg || '✅ Berhasil disalin ke clipboard!');
  }
}

// Fetch library data
async function initGallery() {
  try {
    const res = await fetch('./data/library.json');
    libraryData = await res.json();

    // Set stats
    elements.statHolymoly.textContent = libraryData.holymolyCount;
    elements.statShotcraft.textContent = libraryData.shotcraftCount;
    elements.statTotal.textContent = libraryData.totalCards;

    renderCategories();
    renderCards();
    setupEventListeners();
  } catch (error) {
    console.error('Failed to load library data:', error);
    elements.cardGrid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #EF4444;">
        ⚠️ Gagal memuat data katalog jurus. Pastikan file <code>data/library.json</code> ada.
      </div>
    `;
  }
}

// Render Categories
function renderCategories() {
  const cats = libraryData.categories;
  elements.categoryList.innerHTML = '';

  for (const [key, info] of Object.entries(cats)) {
    let count = 0;
    if (key === 'all') {
      count = libraryData.totalCards;
    } else if (key === 'holymoly') {
      count = libraryData.holymolyCount;
    } else {
      count = libraryData.cards.filter(c => c.category === key).length;
    }

    const pill = document.createElement('button');
    pill.type = 'button';
    pill.className = `category-pill ${activeCategory === key ? 'is-active' : ''}`;
    pill.dataset.category = key;
    pill.innerHTML = `
      <span>${info.icon || '📁'}</span>
      <span>${info.label}</span>
      <span class="pill-badge">${count}</span>
    `;

    pill.addEventListener('click', () => {
      activeCategory = key;
      document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('is-active'));
      pill.classList.add('is-active');
      renderCards();
    });

    elements.categoryList.appendChild(pill);
  }
}

// Filter Cards
function getFilteredCards() {
  if (!libraryData) return [];
  return libraryData.cards.filter(card => {
    // Category match
    const matchesCategory = (activeCategory === 'all') || (card.category === activeCategory);

    // Search query match
    if (!matchesCategory) return false;
    if (!searchQuery) return true;

    const q = searchQuery.toLowerCase();
    const matchName = card.name.toLowerCase().includes(q);
    const matchTitle = (card.title || '').toLowerCase().includes(q);
    const matchSummary = (card.summary || '').toLowerCase().includes(q);
    const matchTags = (card.tags || []).some(t => t.toLowerCase().includes(q));

    return matchName || matchTitle || matchSummary || matchTags;
  });
}

// Render Cards
function renderCards() {
  const cards = getFilteredCards();
  const currentCatInfo = libraryData.categories[activeCategory] || { label: 'Kategori' };

  elements.currentCategoryTitle.textContent = `${currentCatInfo.icon || ''} ${currentCatInfo.label}`;
  elements.activeCardCount.textContent = `Menampilkan ${cards.length} dari ${libraryData.totalCards} jurus`;

  if (cards.length === 0) {
    elements.cardGrid.innerHTML = '';
    elements.emptyState.hidden = false;
    return;
  }

  elements.emptyState.hidden = true;
  elements.cardGrid.innerHTML = '';

  cards.forEach(card => {
    const isSelected = selectedCards.has(card.name);
    const isHolymoly = card.category === 'holymoly';

    const cardEl = document.createElement('article');
    cardEl.className = `recipe-card ${isSelected ? 'is-selected' : ''} ${isHolymoly ? 'is-holymoly' : ''}`;
    cardEl.dataset.cardName = card.name;

    // Media element (GIF or Video)
    let mediaHtml = '';
    const firstStyle = card.styles && card.styles[0];
    const mediaUrl = firstStyle?.media?.url || card.preview_url || '';
    const isGif = mediaUrl.endsWith('.gif');

    if (isGif) {
      mediaHtml = `<img src="${mediaUrl}" alt="${card.title}" loading="lazy">`;
    } else {
      mediaHtml = `
        <video 
          data-src="${mediaUrl}" 
          muted 
          loop 
          playsinline 
          preload="none"
          poster=""
        ></video>
      `;
    }

    cardEl.innerHTML = `
      <div class="card-preview">
        ${mediaHtml}
        <div class="card-preview-overlay"></div>
        <div class="selection-check">✓</div>
        <span class="badge-category ${isHolymoly ? 'badge-holymoly' : ''}">
          ${isHolymoly ? '🌟 Holymoly' : card.category}
        </span>
        <button type="button" class="btn-expand-preview" title="Preview Fullscreen" data-expand="${card.name}">⤢</button>
      </div>

      <div class="card-body">
        <div class="card-title-row">
          <h4 class="card-title">${card.title}</h4>
          <span class="card-directive">${card.directive || card.name}</span>
        </div>
        <p class="card-summary">${card.summary}</p>
        <div class="card-footer">
          <span class="card-duration">${card.duration || 'Dinamis'}</span>
          <button type="button" class="btn-card-select">
            ${isSelected ? 'Dipilih' : '+ Pilih'}
          </button>
        </div>
      </div>
    `;

    // Click on expand button
    const expandBtn = cardEl.querySelector('.btn-expand-preview');
    expandBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      openModal(card);
    });

    // Click anywhere on card to toggle selection
    cardEl.addEventListener('click', () => {
      toggleCardSelection(card);
    });

    // Hover video autoplay
    if (!isGif) {
      const video = cardEl.querySelector('video');
      cardEl.addEventListener('mouseenter', () => {
        if (!video.src && video.dataset.src) {
          video.src = video.dataset.src;
        }
        video.play().catch(() => {});
      });
      cardEl.addEventListener('mouseleave', () => {
        video.pause();
      });
    }

    elements.cardGrid.appendChild(cardEl);
  });

  // Setup Lazy Video Loading with IntersectionObserver
  setupVideoObserver();
  updateDock();
}

// Lazy Video Observer
let videoObserver = null;
function setupVideoObserver() {
  if (videoObserver) videoObserver.disconnect();

  videoObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const video = entry.target;
      if (entry.isIntersecting) {
        if (!video.src && video.dataset.src) {
          video.src = video.dataset.src;
        }
      }
    });
  }, { rootMargin: '200px' });

  document.querySelectorAll('video[data-src]').forEach(video => {
    videoObserver.observe(video);
  });
}

// Toggle Selection
function toggleCardSelection(card) {
  if (selectedCards.has(card.name)) {
    selectedCards.delete(card.name);
  } else {
    selectedCards.add(card.name);
  }

  // Update card DOM
  const cardEl = document.querySelector(`.recipe-card[data-card-name="${card.name}"]`);
  if (cardEl) {
    const isNowSelected = selectedCards.has(card.name);
    cardEl.classList.toggle('is-selected', isNowSelected);
    const selectBtn = cardEl.querySelector('.btn-card-select');
    if (selectBtn) {
      selectBtn.textContent = isNowSelected ? 'Dipilih' : '+ Pilih';
    }
  }

  updateDock();
}

// Update Floating Selection Dock
function updateDock() {
  const count = selectedCards.size;
  if (count === 0) {
    elements.selectionDock.hidden = true;
    return;
  }

  elements.selectionDock.hidden = false;
  elements.dockSelectedCount.textContent = count;

  // Selected names formatted
  const selectedList = libraryData.cards.filter(c => selectedCards.has(c.name));
  const namesStr = selectedList.map(c => c.directive || c.name).join(', ');
  elements.dockSelectedNames.textContent = namesStr;
}

// Generate Structured Antigravity Prompt
function generateAntigravityPrompt() {
  const selectedList = libraryData.cards.filter(c => selectedCards.has(c.name));
  if (!selectedList.length) return '';

  let prompt = `Tolong buatkan video [NUSA Kasir / Topik: ...] menggunakan alur shot pilihan berikut:\n\n`;

  selectedList.forEach((c, idx) => {
    const directive = c.directive || c.name;
    const desc = c.summary ? c.summary.split('.')[0] : c.title;
    prompt += `${idx + 1}. ${directive} — ${desc}\n`;
  });

  prompt += `\nInstruksi Sutradara & Editor (@hm-editor-persona):\n`;
  prompt += `- Durasi 100% dinamis mengikuti ritme voiceover 1.0x native speed (zero slowmo/dead silence).\n`;
  prompt += `- Subtitle wajib menggunakan Standar Universal Tipografi Murni melayang putih tebal dengan multi-layer shadow, dilarang keras container box hitam (Rule 15).\n`;
  prompt += `- Jalankan pre-delivery audit mandiri, upload master ke Google Drive, dan kirim video preview ke WhatsApp.`;

  return prompt;
}

// Fullscreen Modal
function openModal(card) {
  activeModalCard = card;
  const firstStyle = card.styles && card.styles[0];
  const mediaUrl = firstStyle?.media?.url || card.preview_url || '';

  elements.modalTitle.textContent = card.title;
  elements.modalSummary.textContent = card.summary;
  elements.modalDirective.textContent = card.directive || card.name;

  elements.modalTags.innerHTML = (card.tags || []).map(t => `<span class="badge-category">${t}</span>`).join('');

  elements.modalVideo.src = mediaUrl;
  elements.modalVideo.play().catch(() => {});

  const isSelected = selectedCards.has(card.name);
  elements.btnModalSelect.textContent = isSelected ? 'Hapus dari Pilihan' : '+ Pilih Jurus Ini';
  elements.btnModalSelect.style.background = isSelected ? '#EF4444' : '#10B981';

  elements.modalOverlay.hidden = false;
}

function closeModal() {
  elements.modalOverlay.hidden = true;
  elements.modalVideo.pause();
  elements.modalVideo.src = '';
  activeModalCard = null;
}

// Event Listeners
function setupEventListeners() {
  // Search input with debounce
  let searchTimer;
  elements.searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      searchQuery = e.target.value.trim();
      renderCards();
    }, 180);
  });

  // Clear search
  elements.btnClearSearch.addEventListener('click', () => {
    elements.searchInput.value = '';
    searchQuery = '';
    activeCategory = 'all';
    document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('is-active'));
    document.querySelector('.category-pill[data-category="all"]')?.classList.add('is-active');
    renderCards();
  });

  // Keyboard shortcut Ctrl+K / Cmd+K
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      elements.searchInput.focus();
    }
    if (e.key === 'Escape') {
      if (!elements.modalOverlay.hidden) {
        closeModal();
      } else if (document.activeElement === elements.searchInput) {
        elements.searchInput.blur();
      }
    }
  });

  // Dock Actions
  elements.btnDockClear.addEventListener('click', () => {
    selectedCards.clear();
    document.querySelectorAll('.recipe-card.is-selected').forEach(el => el.classList.remove('is-selected'));
    document.querySelectorAll('.btn-card-select').forEach(btn => btn.textContent = '+ Pilih');
    updateDock();
  });

  elements.btnDockRaw.addEventListener('click', () => {
    const selectedList = libraryData.cards.filter(c => selectedCards.has(c.name));
    const rawTags = selectedList.map(c => c.directive || c.name).join(', ');
    copyToClipboard(rawTags, `📋 ${selectedList.length} tag jurus disalin!`);
  });

  elements.btnDockPrompt.addEventListener('click', () => {
    const promptText = generateAntigravityPrompt();
    copyToClipboard(promptText, `✨ Prompt Antigravity siap paste disalin!`);
  });

  // Modal Actions
  elements.modalClose.addEventListener('click', closeModal);
  elements.modalOverlay.addEventListener('click', (e) => {
    if (e.target === elements.modalOverlay) closeModal();
  });

  elements.btnModalSelect.addEventListener('click', () => {
    if (activeModalCard) {
      toggleCardSelection(activeModalCard);
      const isNowSelected = selectedCards.has(activeModalCard.name);
      elements.btnModalSelect.textContent = isNowSelected ? 'Hapus dari Pilihan' : '+ Pilih Jurus Ini';
      elements.btnModalSelect.style.background = isNowSelected ? '#EF4444' : '#10B981';
    }
  });
}

// Start
initGallery();
