/**
 * CareerForge.AI - Core Frontend Controller & Personalized State Manager
 */

const API_BASE = (window.location && window.location.origin && window.location.origin.startsWith("http")) 
  ? window.location.origin 
  : "http://localhost:8000";

// Global State
let currentUser = null;
let currentProfile = null;
let matchedRoles = [];
let selectedRoleId = null;
let currentRoadmap = null;
let completedWeeks = [];

// Sample Resume Text
const SAMPLE_RESUME_TEXT = `
Rajatveer Singh Pasricha
Email: rajatveer1234@gmail.com | Phone: +91 9425654989
LinkedIn: https://linkedin.com/in/rajatveer | GitHub: https://github.com/rajatveer

Summary:
Aspiring Data Analyst and AI/ML Engineer with hands-on experience in building machine learning models, RAG retrieval pipelines, and interactive analytics dashboards.

Skills:
- Programming Languages: Python, SQL
- Machine Learning & Data Analytics: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, OpenCV, NLTK
- Generative AI & Vector Search: LangChain, Hugging Face Transformers, ChromaDB, FAISS, RAG
- Tools & Cloud: Power BI, Docker, Salesforce Administration, Git, Linux
- Databases: PostgreSQL, MySQL

Work Experience & Internships:
AI Engineer Intern | Kuberya AI | 04/2026 – 06/2026
- Built RAG solutions with vector DBs and embeddings, improving document retrieval accuracy by 22% across 5,000+ technical docs.
- Optimized model inference latency by 18% and automated 6 key analytical workflows with engineering teams.
- Developed AI applications with Python, FastAPI, and LangChain, cutting manual workflow time by 30%.

Data Analytics Trainee | NOKIA | 10/2025 – 11/2025
- Led end-to-end ML workflows on subscriber and network datasets, generating predictive insights for retention strategies.
- Built 3 Power BI dashboards translating operational analytics into strategies contributing to a 12% reduction in churn.

Salesforce Data & CRM Intern | TCS - SmartBridge | 07/2025 – 10/2025
- Managed user accounts, security roles, and permissions within an enterprise Salesforce environment.
- Automated 3 business workflows, reducing manual data-entry time by 25%.

Education:
Bachelor of Technology in Computer Science (AI & ML Specialization) | 2022 – 2026 | CGPA: 7.50
`;

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) window.lucide.createIcons();
  
  // Initialize Mermaid with dark theme
  if (window.mermaid) {
    try {
      window.mermaid.initialize({
        startOnLoad: false,
        theme: 'dark',
        themeVariables: {
          darkMode: true,
          background: '#0a0e18',
          primaryColor: '#6366f1',
          primaryTextColor: '#f8fafc',
          primaryBorderColor: '#06b6d4',
          lineColor: '#06b6d4',
          secondaryColor: '#1e293b',
          tertiaryColor: '#0f172a'
        }
      });
    } catch (e) {
      console.warn("Mermaid init notice:", e);
    }
  }

  checkApiHealth();
  setupAuthHandlers();
  setupUploadListeners();
  setupResetResumeListener();
  setupTabListeners();
  setupRoadmapControls();

  restoreUserSession();
});

// 1. API Health Check
async function checkApiHealth() {
  const statusEl = document.getElementById("apiStatusText");
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    if (res.ok) {
      statusEl.textContent = "AI Engine Online";
      statusEl.previousElementSibling.classList.add("online");
    }
  } catch (err) {
    statusEl.textContent = "Engine Offline (Run uvicorn app.main:app)";
    statusEl.previousElementSibling.classList.remove("online");
  }
}

// 2. Authentication & Personalization Handlers
function setupAuthHandlers() {
  const modal = document.getElementById("authModal");
  const openBtn = document.getElementById("openAuthModalBtn");
  const closeBtn = document.getElementById("closeAuthModalBtn");
  const tabLogin = document.getElementById("tabLoginBtn");
  const tabRegister = document.getElementById("tabRegisterBtn");
  const loginForm = document.getElementById("loginForm");
  const regForm = document.getElementById("registerForm");
  const logoutBtn = document.getElementById("logoutBtn");

  openBtn.addEventListener("click", () => {
    modal.classList.remove("hidden");
    document.getElementById("authErrorMsg").classList.add("hidden");
  });

  closeBtn.addEventListener("click", () => modal.classList.add("hidden"));

  tabLogin.addEventListener("click", () => {
    tabLogin.classList.add("active");
    tabRegister.classList.remove("active");
    loginForm.classList.remove("hidden");
    regForm.classList.add("hidden");
    document.getElementById("authErrorMsg").classList.add("hidden");
  });

  tabRegister.addEventListener("click", () => {
    tabRegister.classList.add("active");
    tabLogin.classList.remove("active");
    regForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
    document.getElementById("authErrorMsg").classList.add("hidden");
  });

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    await handleAuthRequest("/api/auth/login", { email, password });
  });

  regForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const full_name = document.getElementById("regName").value;
    const email = document.getElementById("regEmail").value;
    const password = document.getElementById("regPassword").value;
    await handleAuthRequest("/api/auth/register", { full_name, email, password });
  });

  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("careerforge_token");
    currentUser = null;
    updateAuthNav(null);
  });
}

async function handleAuthRequest(endpoint, payload) {
  const errorEl = document.getElementById("authErrorMsg");
  errorEl.classList.add("hidden");

  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Authentication failed.");

    const userData = data.data;
    localStorage.setItem("careerforge_token", userData.token);
    currentUser = userData;

    document.getElementById("authModal").classList.add("hidden");
    updateAuthNav(userData);

    if (userData.state && userData.state.profile) {
      currentProfile = userData.state.profile;
      selectedRoleId = userData.state.target_role_id;
      completedWeeks = userData.state.completed_weeks || [];
      
      handleParsedSuccess(currentProfile, false);
      if (userData.state.roadmap) {
        currentRoadmap = userData.state.roadmap;
        renderRoadmapTimeline(currentRoadmap);
      }
    } else if (currentProfile) {
      saveUserState();
    }
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.remove("hidden");
  }
}

async function restoreUserSession() {
  const token = localStorage.getItem("careerforge_token");
  if (!token) return;

  try {
    const res = await fetch(`${API_BASE}/api/auth/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (!res.ok) return;

    const data = await res.json();
    if (data.success && data.user) {
      currentUser = data.user;
      updateAuthNav(currentUser);

      if (currentUser.state && currentUser.state.profile) {
        currentProfile = currentUser.state.profile;
        selectedRoleId = currentUser.state.target_role_id;
        completedWeeks = currentUser.state.completed_weeks || [];
        handleParsedSuccess(currentProfile, false);
        if (currentUser.state.roadmap) {
          currentRoadmap = currentUser.state.roadmap;
          renderRoadmapTimeline(currentRoadmap);
        }
      }
    }
  } catch (e) {
    console.log("Could not restore session:", e);
  }
}

function updateAuthNav(user) {
  const loggedOut = document.getElementById("authNavLoggedOut");
  const loggedIn = document.getElementById("authNavLoggedIn");

  if (user) {
    loggedOut.classList.add("hidden");
    loggedIn.classList.remove("hidden");
    const name = user.full_name || user.email.split("@")[0];
    document.getElementById("navUserName").textContent = name;
    document.getElementById("navUserInitials").textContent = name.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase();
  } else {
    loggedOut.classList.remove("hidden");
    loggedIn.classList.add("hidden");
  }
  if (window.lucide) window.lucide.createIcons();
}

async function saveUserState() {
  const token = localStorage.getItem("careerforge_token");
  if (!token || !currentUser) return;

  try {
    await fetch(`${API_BASE}/api/auth/save-state`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        profile: currentProfile,
        target_role_id: selectedRoleId,
        roadmap: currentRoadmap,
        completed_weeks: completedWeeks
      })
    });
  } catch (e) {
    console.error("Failed to auto-save state:", e);
  }
}

// 3. Upload & Ingestion Handlers
function setupUploadListeners() {
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("resumeFileInput");
  const browseBtn = document.getElementById("browseBtn");
  const sampleBtn = document.getElementById("sampleResumeBtn");

  browseBtn.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      uploadFile(e.target.files[0]);
    }
  });

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.add('drag-over');
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
    });
  });

  dropZone.addEventListener('drop', (e) => {
    if (e.dataTransfer.files.length > 0) {
      uploadFile(e.dataTransfer.files[0]);
    }
  });

  sampleBtn.addEventListener("click", () => {
    parseSampleText(SAMPLE_RESUME_TEXT);
  });
}

function showLoading(stageText) {
  document.getElementById("uploadPrompt").classList.add("hidden");
  const loadingEl = document.getElementById("uploadLoading");
  loadingEl.classList.remove("hidden");
  document.getElementById("loadingStageText").textContent = stageText;
}

function hideLoading() {
  document.getElementById("uploadPrompt").classList.remove("hidden");
  document.getElementById("uploadLoading").classList.add("hidden");
}

async function uploadFile(file) {
  showLoading(`Parsing ${file.name} with Layout-Aware NLP...`);

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/api/resume/parse-file`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to parse resume file.");
    }

    const data = await res.json();
    handleParsedSuccess(data.profile, true);
  } catch (err) {
    alert(`Error: ${err.message}`);
    hideLoading();
  }
}

async function parseSampleText(text) {
  showLoading("Parsing Sample Resume Profile...");

  try {
    const res = await fetch(`${API_BASE}/api/resume/parse-text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!res.ok) throw new Error("Failed to parse sample text.");

    const data = await res.json();
    handleParsedSuccess(data.profile, true);
  } catch (err) {
    alert(`Error: ${err.message}`);
    hideLoading();
  }
}

// 3.1 Reset / Delete Resume Handler
function setupResetResumeListener() {
  const resetBtn = document.getElementById("resetResumeBtn");
  if (!resetBtn) return;

  resetBtn.addEventListener("click", async () => {
    if (confirm("Are you sure you want to delete the uploaded resume and return to upload?")) {
      await deleteResumeAndReset();
    }
  });
}

async function deleteResumeAndReset() {
  // Clear in-memory state
  currentProfile = null;
  matchedRoles = [];
  selectedRoleId = null;
  currentRoadmap = null;
  completedWeeks = [];

  // Reset file input & UI sections
  const fileInput = document.getElementById("resumeFileInput");
  if (fileInput) fileInput.value = "";

  const resultsDashboard = document.getElementById("resultsDashboard");
  if (resultsDashboard) resultsDashboard.classList.add("hidden");

  const heroSection = document.getElementById("heroSection");
  if (heroSection) heroSection.classList.remove("hidden");

  const uploadSection = document.getElementById("uploadSection");
  if (uploadSection) uploadSection.classList.remove("hidden");

  hideLoading();

  // Reset tab to tab 1
  switchTab("rolesTab");

  // If user is authenticated, sync cleared state to database
  const token = localStorage.getItem("careerforge_token");
  if (token && currentUser) {
    try {
      await fetch(`${API_BASE}/api/auth/save-state`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          profile: null,
          target_role_id: null,
          roadmap: null,
          completed_weeks: []
        })
      });
      if (currentUser.state) {
        currentUser.state = { profile: null, target_role_id: null, roadmap: null, completed_weeks: [] };
      }
    } catch (e) {
      console.error("Failed to sync cleared state to server:", e);
    }
  }

  // Smooth scroll back to top
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// 4. Render Profile & Trigger Downstream Match
async function handleParsedSuccess(profile, shouldSave = true) {
  if (!profile) return;
  currentProfile = profile;
  hideLoading();

  // Render Candidate Banner
  renderCandidateBanner(profile);

  // Unhide Dashboard immediately
  const resultsDashboard = document.getElementById("resultsDashboard");
  if (resultsDashboard) {
    resultsDashboard.classList.remove("hidden");
  }

  // Scroll smoothly down to results
  setTimeout(() => {
    if (resultsDashboard) {
      resultsDashboard.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, 100);

  // Trigger downstream role matching
  await fetchMatchingRoles(profile);

  if (shouldSave) {
    saveUserState();
  }
}

function renderCandidateBanner(profile) {
  if (!profile) return;
  const contact = profile.contact || {};
  const name = contact.name || "Candidate Profile";
  
  // Safe initials extraction avoiding undefined charAt on empty strings
  const nameParts = name.trim().split(/\s+/).filter(Boolean);
  const initials = nameParts.length > 0 
    ? nameParts.map(n => n.charAt(0)).join("").slice(0, 2).toUpperCase() 
    : "CV";

  const nameEl = document.getElementById("candidateName");
  if (nameEl) nameEl.textContent = name;

  const avatarEl = document.getElementById("candidateAvatar");
  if (avatarEl) avatarEl.textContent = initials;

  const seniorityEl = document.getElementById("candidateSeniority");
  if (seniorityEl) seniorityEl.textContent = profile.detected_seniority || "Entry-Level";

  const emailEl = document.getElementById("candidateEmail");
  if (emailEl) emailEl.innerHTML = `<i data-lucide="mail"></i> ${contact.email || "Email Provided"}`;

  const expYears = profile.total_experience_years != null ? profile.total_experience_years : 1.5;
  const expEl = document.getElementById("candidateExp");
  if (expEl) expEl.innerHTML = `<i data-lucide="briefcase"></i> ${expYears} yrs experience`;
  
  const summaryEl = document.getElementById("candidateSummary");
  if (summaryEl) summaryEl.textContent = profile.summary || "Technical profile successfully parsed.";

  const gh = document.getElementById("candidateGithub");
  if (gh) {
    if (contact.github_url) {
      gh.href = contact.github_url;
      gh.classList.remove("hidden");
    } else {
      gh.classList.add("hidden");
    }
  }

  const li = document.getElementById("candidateLinkedin");
  if (li) {
    if (contact.linkedin_url) {
      li.href = contact.linkedin_url;
      li.classList.remove("hidden");
    } else {
      li.classList.add("hidden");
    }
  }

  const skills = profile.skills || {};
  renderChips("languagesChips", skills.languages || []);
  renderChips("frameworksChips", skills.frameworks || []);
  renderChips("databasesChips", skills.databases_and_storage || []);
  renderChips("devopsChips", skills.cloud_and_devops || []);
  renderChips("aimlChips", skills.ai_and_ml || []);
  renderChips("toolsChips", skills.tools_and_platforms || []);

  if (window.lucide) window.lucide.createIcons();
}

function renderChips(containerId, list) {
  const el = document.getElementById(containerId);
  if (!el) return;
  if (!list || list.length === 0) {
    el.innerHTML = `<span class="chip" style="opacity:0.35;">None detected</span>`;
    return;
  }
  el.innerHTML = list.map(item => `<span class="chip core">${item}</span>`).join("");
}

// 5. Role Matching (Enhanced Cards with Progress Rings and Action Flows)
async function fetchMatchingRoles(profile) {
  const rolesGrid = document.getElementById("rolesGrid");
  rolesGrid.innerHTML = `<div class="spinner"></div><p style="text-align:center; color:var(--text-secondary);">Querying ChromaDB Vector Store & Ranking Career Tracks...</p>`;

  try {
    const res = await fetch(`${API_BASE}/api/roles/match`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile, top_k: 6 })
    });

    if (!res.ok) throw new Error("Role matching request failed.");

    const data = await res.json();
    matchedRoles = data.top_matches;

    renderRoleCards(matchedRoles);
    populateRoadmapSelect(matchedRoles);

    if (matchedRoles.length > 0 && !selectedRoleId) {
      selectedRoleId = matchedRoles[0].role_id;
    }

    if (selectedRoleId) {
      document.getElementById("roadmapRoleSelect").value = selectedRoleId;
      await fetchRecommendedProjects(profile, selectedRoleId);
      if (!currentRoadmap) {
        await fetchPersonalizedRoadmap(profile, selectedRoleId);
      }
    }
  } catch (err) {
    rolesGrid.innerHTML = `<p style="color:var(--accent-rose);">Error matching roles: ${err.message}</p>`;
  }
}

let activeRoleCategory = 'all';

function filterRoleCategory(category, buttonEl) {
  activeRoleCategory = category;
  document.querySelectorAll(".filter-pill").forEach(btn => btn.classList.remove("active"));
  if (buttonEl) buttonEl.classList.add("active");

  const filtered = matchedRoles.filter(r => {
    if (category === "all") return true;
    const cat = (r.category || "").toLowerCase();
    const title = (r.title || "").toLowerCase();
    if (category === "ai") return cat.includes("ai") || cat.includes("intelligence") || cat.includes("machine") || title.includes("ml") || title.includes("llm");
    if (category === "data") return cat.includes("data") || cat.includes("analytic") || title.includes("data") || title.includes("bi");
    if (category === "software") return cat.includes("software") || cat.includes("backend") || cat.includes("engineering") || title.includes("software") || title.includes("backend");
    return true;
  });

  renderRoleCards(filtered);
}

function getCategoryIcon(category, title) {
  const c = ((category || "") + " " + (title || "")).toLowerCase();
  if (c.includes("ai") || c.includes("intelligence") || c.includes("machine") || c.includes("ml")) return "brain";
  if (c.includes("data") || c.includes("analytic") || c.includes("bi")) return "bar-chart-2";
  if (c.includes("cloud") || c.includes("devops") || c.includes("mlops")) return "cpu";
  return "code-2";
}

function renderRoleCards(roles) {
  const rolesGrid = document.getElementById("rolesGrid");
  if (!roles || roles.length === 0) {
    rolesGrid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding: 40px; color:var(--text-secondary);">No roles found in this category.</div>`;
    return;
  }

  rolesGrid.innerHTML = roles.map((r, idx) => {
    const scoreVal = Math.round(r.match_score_percentage);
    const ringClass = scoreVal >= 75 ? "high" : scoreVal >= 55 ? "mid" : "low";
    const isTopPick = (idx === 0 && activeRoleCategory === 'all') || r.role_id === selectedRoleId;
    const catIcon = getCategoryIcon(r.category, r.title);

    const matchedCount = r.key_strengths.length;
    const gapCount = r.critical_gaps.length;
    const totalCompetencies = matchedCount + gapCount;
    const competencyRatio = totalCompetencies > 0 ? Math.round((matchedCount / totalCompetencies) * 100) : scoreVal;

    const strengthPills = r.key_strengths.slice(0, 6).map(s => `
      <span class="modern-chip matched"><i data-lucide="check"></i> ${s}</span>
    `).join("");

    const gapPills = r.critical_gaps.length > 0 
      ? r.critical_gaps.map(g => `<span class="modern-chip gap"><i data-lucide="plus"></i> ${g}</span>`).join("")
      : `<div class="all-matched-banner"><i data-lucide="sparkles"></i> 100% Core Competency Matched!</div>`;

    return `
      <div class="role-card ${isTopPick ? 'highlight-top' : ''}">
        ${idx === 0 && activeRoleCategory === 'all' ? '<div class="top-pick-ribbon">Top Match</div>' : ''}
        
        <div>
          <div class="role-top-meta">
            <span class="category-badge">
              <i data-lucide="${catIcon}"></i> ${r.category}
            </span>
          </div>

          <div class="role-title-row">
            <div>
              <h3 class="role-title">${r.title}</h3>
              <div class="role-metrics-bar">
                <span class="metric-pill verdict-strong">${r.fit_verdict}</span>
                <span class="metric-pill"><i data-lucide="dollar-sign"></i> ${r.salary_range}</span>
                <span class="metric-pill"><i data-lucide="trending-up"></i> ${r.market_demand}</span>
              </div>
            </div>

            <!-- Sleek Circular Progress Gauge -->
            <div class="circular-score-wrapper" title="${scoreVal}% Fit Score">
              <svg class="score-ring" viewBox="0 0 36 36">
                <path class="ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path class="ring-val ${ringClass}" stroke-dasharray="${scoreVal}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              </svg>
              <div class="score-center-text">
                <span class="score-num">${scoreVal}%</span>
                <span class="score-lbl">Match</span>
              </div>
            </div>
          </div>

          <!-- Competency Progress Bar -->
          <div class="skill-progress-box">
            <div class="skill-progress-header">
              <span>Competency Coverage</span>
              <span>${matchedCount} of ${totalCompetencies || matchedCount} Skills (${competencyRatio}%)</span>
            </div>
            <div class="skill-progress-bar">
              <div class="skill-progress-fill ${scoreVal >= 75 ? 'high' : ''}" style="width: ${competencyRatio}%"></div>
            </div>
          </div>

          <!-- Matched Skills -->
          <div class="modern-chips-section">
            <div class="chips-title match">
              <i data-lucide="check-circle-2"></i> Matched Competencies (${matchedCount})
            </div>
            <div class="modern-chips-list">
              ${strengthPills}
            </div>
          </div>

          <!-- Missing Skills / Gaps -->
          <div class="modern-chips-section" style="margin-top: 10px;">
            <div class="chips-title gap">
              <i data-lucide="target"></i> ${gapCount > 0 ? `Target Growth Areas (${gapCount})` : 'Role Preparedness'}
            </div>
            <div class="modern-chips-list">
              ${gapPills}
            </div>
          </div>
        </div>

        <!-- Interactive Action Footer -->
        <div class="role-card-footer">
          <button class="btn-card-primary" onclick="selectTargetRole('${r.role_id}')">
            <span>Build Career Roadmap</span>
            <i data-lucide="arrow-right"></i>
          </button>
          <button class="btn-card-secondary" onclick="viewRoleProjects('${r.role_id}')" title="Explore Capstone Projects">
            <i data-lucide="folder-git-2"></i>
            <span>Projects</span>
          </button>
        </div>
      </div>
    `;
  }).join("");

  if (window.lucide) window.lucide.createIcons();
}

window.selectTargetRole = function(roleId) {
  selectedRoleId = roleId;
  const select = document.getElementById("roadmapRoleSelect");
  if (select) select.value = roleId;
  
  switchTab("roadmapTab");
  fetchRecommendedProjects(currentProfile, roleId);
  fetchPersonalizedRoadmap(currentProfile, roleId);
  saveUserState();
};

window.viewRoleProjects = function(roleId) {
  selectedRoleId = roleId;
  const select = document.getElementById("roadmapRoleSelect");
  if (select) select.value = roleId;
  
  switchTab("projectsTab");
  fetchRecommendedProjects(currentProfile, roleId);
};
};

// 6. Project Recommender
async function fetchRecommendedProjects(profile, roleId) {
  const projectsGrid = document.getElementById("projectsGrid");
  projectsGrid.innerHTML = `<div class="spinner"></div><p style="text-align:center; color:var(--text-secondary);">Synthesizing Production Project Architectures...</p>`;

  try {
    const res = await fetch(`${API_BASE}/api/projects/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile, target_role_id: roleId, max_recommendations: 3 })
    });

    if (!res.ok) throw new Error("Project recommendation failed.");

    const data = await res.json();
    renderProjectCards(data.recommendations);
  } catch (err) {
    projectsGrid.innerHTML = `<p style="color:var(--accent-rose);">Error loading projects: ${err.message}</p>`;
  }
}

function renderProjectCards(recommendations) {
  const projectsGrid = document.getElementById("projectsGrid");
  
  projectsGrid.innerHTML = recommendations.map((rec, idx) => {
    const p = rec.project;
    const bridgedChips = rec.skills_bridged.map(s => `<span class="chip-strength">Bridges: ${s}</span>`).join(" ");
    const bulletsHtml = p.resume_bullet_points.map(b => `<li>${b}</li>`).join("");
    const featuresHtml = p.core_features.map(f => `<li>${f}</li>`).join("");

    return `
      <div class="glass-card project-card">
        <div class="project-header">
          <div>
            <span class="badge" style="background:rgba(99,102,241,0.2); color:var(--accent-indigo); margin-bottom:6px; display:inline-block;">
              ⭐ Recommended Portfolio Capstone #${idx + 1}
            </span>
            <h3 class="project-title">${p.title}</h3>
            <p class="project-tagline">${p.tagline}</p>
          </div>
          <div class="score-badge" style="border-color:rgba(16,185,129,0.3); color:var(--accent-emerald);">
            ${rec.relevance_score}% Gap Fit
          </div>
        </div>

        <div style="margin-bottom: 14px;">${bridgedChips}</div>

        <div class="task-box">
          <strong>💡 Why this project:</strong> ${rec.why_recommended}
        </div>

        <div class="role-section-label" style="margin-top:16px;">System Architecture Flowchart:</div>
        <div class="mermaid-wrapper">
          <pre class="mermaid">${p.system_architecture_mermaid}</pre>
        </div>

        <div class="role-section-label">Core Implementation Modules:</div>
        <ul class="features-list">${featuresHtml}</ul>

        <div class="role-section-label" style="margin-top:14px;">Google XYZ Resume Bullet Points (Copy & Paste when completed):</div>
        <ul class="bullets-list">${bulletsHtml}</ul>
      </div>
    `;
  }).join("");

  if (window.lucide) window.lucide.createIcons();
  if (window.mermaid) {
    try {
      window.mermaid.run();
    } catch (e) {
      console.warn("Mermaid diagram rendering notice:", e);
    }
  }
}

// 7. Roadmap Generation & Milestone Tracking
function populateRoadmapSelect(roles) {
  const select = document.getElementById("roadmapRoleSelect");
  select.innerHTML = roles.map(r => `
    <option value="${r.role_id}" ${r.role_id === selectedRoleId ? 'selected' : ''}>${r.title} (${r.match_score_percentage}% Match)</option>
  `).join("");
}

async function fetchPersonalizedRoadmap(profile, roleId) {
  const container = document.getElementById("roadmapContainer");
  const weeks = parseInt(document.getElementById("roadmapWeeks").value) || 6;
  const hours = parseInt(document.getElementById("roadmapHours").value) || 10;

  container.innerHTML = `<div class="spinner"></div><p style="text-align:center; color:var(--text-secondary);">Pruning Mastered Concepts & Scheduling Personalized Milestones...</p>`;

  try {
    const res = await fetch(`${API_BASE}/api/roadmap/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        profile,
        target_role_id: roleId,
        duration_weeks: weeks,
        available_hours_per_week: hours
      })
    });

    if (!res.ok) throw new Error("Roadmap generation failed.");

    const data = await res.json();
    currentRoadmap = data.roadmap;
    renderRoadmapTimeline(currentRoadmap);
    saveUserState();
  } catch (err) {
    container.innerHTML = `<p style="color:var(--accent-rose);">Error generating roadmap: ${err.message}</p>`;
  }
}

function renderRoadmapTimeline(roadmap) {
  const container = document.getElementById("roadmapContainer");

  const prunedHtml = roadmap.mastered_prerequisites_skipped.length > 0 ? `
    <div class="glass-card" style="padding:16px 20px; margin-bottom:24px; border-color:rgba(16,185,129,0.3);">
      <span style="color:var(--accent-emerald); font-weight:600; font-size:0.9rem;">
        ⚡ Pruned Mastered Concepts:
      </span>
      <span style="color:var(--text-secondary); font-size:0.85rem; margin-left:8px;">
        Skipped ${roadmap.mastered_prerequisites_skipped.join(", ")} from foundational modules to accelerate your graduation timeline.
      </span>
    </div>
  ` : "";

  const milestonesHtml = roadmap.milestones.map((m) => {
    const isCompleted = completedWeeks.includes(m.week_number);
    const resourcesHtml = m.curated_resources.map(r => `
      <a href="${r.url}" target="_blank" class="resource-btn">
        <i data-lucide="external-link"></i> ${r.title} (${r.resource_type})
      </a>
    `).join("");

    return `
      <div class="milestone-item ${isCompleted ? 'completed' : ''}" id="milestoneWeek${m.week_number}">
        <div class="milestone-dot">${isCompleted ? '✓' : m.week_number}</div>
        <div class="glass-card milestone-card">
          <div class="milestone-header">
            <div>
              <span class="milestone-badge">${m.phase_name}</span>
              <h3 class="milestone-title" style="margin-top:4px;">${m.title}</h3>
            </div>
            <span style="font-size:0.85rem; color:var(--text-muted); font-family:var(--font-mono);">
              ⏱️ ${m.estimated_hours} hrs
            </span>
          </div>

          <p class="milestone-objective"><strong>🎯 Objective:</strong> ${m.objective}</p>

          <div class="task-box">
            <strong>💻 Hands-On Coding Task:</strong> ${m.practical_coding_task}
          </div>

          <div class="interview-box">
            <strong>💡 Mock Interview Checkpoint:</strong> ${m.interview_checkpoint_question}
          </div>

          <div class="role-section-label" style="margin-top:14px;">Curated Documentation & Tutorial Resources:</div>
          <div class="resource-links">${resourcesHtml}</div>

          <div class="milestone-toggle-row">
            <label class="completion-label">
              <input type="checkbox" class="completion-checkbox" ${isCompleted ? 'checked' : ''} onchange="toggleWeekCompletion(${m.week_number}, this.checked)">
              <span>${isCompleted ? '✅ Completed Milestone' : 'Mark Week as Completed'}</span>
            </label>
          </div>
        </div>
      </div>
    `;
  }).join("");

  container.innerHTML = `
    ${prunedHtml}
    <div class="roadmap-timeline">
      ${milestonesHtml}
    </div>
  `;

  if (window.lucide) window.lucide.createIcons();
}

window.toggleWeekCompletion = function(weekNumber, isChecked) {
  if (isChecked) {
    if (!completedWeeks.includes(weekNumber)) completedWeeks.push(weekNumber);
  } else {
    completedWeeks = completedWeeks.filter(w => w !== weekNumber);
  }

  const milestoneEl = document.getElementById(`milestoneWeek${weekNumber}`);
  if (milestoneEl) {
    if (isChecked) {
      milestoneEl.classList.add("completed");
      milestoneEl.querySelector(".milestone-dot").textContent = "✓";
    } else {
      milestoneEl.classList.remove("completed");
      milestoneEl.querySelector(".milestone-dot").textContent = weekNumber;
    }
  }

  saveUserState();
};

// 8. Tab Switching Logic
function setupTabListeners() {
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetId = tab.dataset.tab;
      switchTab(targetId);
    });
  });
}

function switchTab(targetId) {
  document.querySelectorAll(".tab-btn").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

  const activeBtn = document.querySelector(`.tab-btn[data-tab="${targetId}"]`);
  const activeContent = document.getElementById(targetId);

  if (activeBtn) activeBtn.classList.add("active");
  if (activeContent) activeContent.classList.add("active");
}

function setupRoadmapControls() {
  document.getElementById("regenerateRoadmapBtn").addEventListener("click", () => {
    const roleId = document.getElementById("roadmapRoleSelect").value;
    if (currentProfile && roleId) {
      fetchPersonalizedRoadmap(currentProfile, roleId);
    }
  });
}
