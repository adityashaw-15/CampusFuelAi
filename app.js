const STORAGE_KEY = "campusfuel-ai-log-v1";

const SAMPLE_LOGS = {
  hostel: `poha\nchai\n2 rotis\ndal\nrice\ncurd\nbanana\nsamosa`,
  exam: `coffee\nbiscuits\nmaggi\nburger\ncola\nchips\nchocolate`,
  gym: `oats with milk\nbanana\n4 eggs\nrice\nchicken curry\ncurd\npeanut butter toast`
};

const foodForm = document.querySelector("#foodForm");
const foodInput = document.querySelector("#foodInput");
const entryCount = document.querySelector("#entryCount");

const heightInput = document.querySelector("#heightInput");
const weightInput = document.querySelector("#weightInput");
const workoutInput = document.querySelector("#workoutInput");
const bmiValue = document.querySelector("#bmiValue");
const bmiStatus = document.querySelector("#bmiStatus");

const calorieValue = document.querySelector("#calorieValue");
const proteinValue = document.querySelector("#proteinValue");
const carbValue = document.querySelector("#carbValue");
const junkValue = document.querySelector("#junkValue");
const ratingValue = document.querySelector("#ratingValue");
const heartScoreValue = document.querySelector("#heartScoreValue");
const scoreValue = document.querySelector("#scoreValue");
const summaryText = document.querySelector("#summaryText");

const suggestionList = document.querySelector("#suggestionList");
const habitList = document.querySelector("#habitList");
const recipeList = document.querySelector("#recipeList");
const foodList = document.querySelector("#foodList");
const matchBadge = document.querySelector("#matchBadge");
const ratingBadge = document.querySelector("#ratingBadge");

const proteinNote = document.querySelector("#proteinNote");
const carbNote = document.querySelector("#carbNote");
const junkNote = document.querySelector("#junkNote");

const proteinBar = document.querySelector("#proteinBar");
const carbBar = document.querySelector("#carbBar");
const junkBar = document.querySelector("#junkBar");

const clearLogButton = document.querySelector("#clearLog");
const loadHostelDay = document.querySelector("#loadHostelDay");
const loadGymDay = document.querySelector("#loadGymDay");

let inputTimer = null;

initialize();

function initialize() {
  foodInput.value = readStoredLog() || SAMPLE_LOGS.hostel;
  bindEvents();
  updateBmi();
  analyzeLog();
}

function bindEvents() {
  foodForm.addEventListener("submit", (event) => {
    event.preventDefault();
    analyzeLog();
  });

  foodInput.addEventListener("input", () => {
    writeStoredLog(foodInput.value);
    window.clearTimeout(inputTimer);
    inputTimer = window.setTimeout(analyzeLog, 600);
  });

  heightInput.addEventListener("input", updateBmi);
  weightInput.addEventListener("input", updateBmi);
  workoutInput.addEventListener("change", analyzeLog);

  clearLogButton.addEventListener("click", () => {
    foodInput.value = "";
    writeStoredLog("");
    analyzeLog();
    foodInput.focus();
  });

  loadHostelDay.addEventListener("click", () => loadSample("hostel"));
  loadGymDay.addEventListener("click", () => loadSample("gym"));

  document.querySelectorAll("[data-sample]").forEach((button) => {
    button.addEventListener("click", () => loadSample(button.dataset.sample));
  });

  document.querySelectorAll("[data-food]").forEach((button) => {
    button.addEventListener("click", () => appendFood(button.dataset.food || ""));
  });
}

function loadSample(name) {
  if (!SAMPLE_LOGS[name]) return;
  foodInput.value = SAMPLE_LOGS[name];
  writeStoredLog(foodInput.value);
  analyzeLog();
  document.querySelector("#analyzer")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function appendFood(food) {
  const nextValue = foodInput.value.trim() ? `${foodInput.value.trim()}\n${food}` : food;
  foodInput.value = nextValue;
  writeStoredLog(nextValue);
  analyzeLog();
  foodInput.focus();
}

function updateBmi() {
  const h = parseFloat(heightInput.value);
  const w = parseFloat(weightInput.value);
  if (h > 0 && w > 0) {
    const hm = h / 100;
    const bmi = w / (hm * hm);
    bmiValue.textContent = bmi.toFixed(1);
    
    let status = "";
    let color = "";
    if (bmi < 18.5) { status = "(Underweight)"; color = "orange"; }
    else if (bmi < 25) { status = "(Normal)"; color = "green"; }
    else if (bmi < 30) { status = "(Overweight)"; color = "orange"; }
    else { status = "(Obese)"; color = "red"; }
    
    bmiStatus.textContent = status;
    bmiStatus.style.color = color;
  } else {
    bmiValue.textContent = "--";
    bmiStatus.textContent = "";
  }
}

async function analyzeLog() {
  const text = foodInput.value.trim();
  const entries = text.split(/\n|,/g).map(i => i.trim()).filter(Boolean);
  entryCount.textContent = `${entries.length} item${entries.length === 1 ? "" : "s"}`;

  if (!entries.length) {
    renderEmptyState();
    return;
  }

  summaryText.textContent = "Analyzing your food with Google Gemini AI...";
  summaryText.parentElement.classList.add("loading-pulse");
  ratingBadge.textContent = "...";

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        foods: text,
        height: heightInput.value,
        weight: weightInput.value,
        workout: workoutInput.value
      })
    });

    if (!response.ok) {
      throw new Error("Failed to reach AI");
    }

    const data = await response.json();
    renderReport(data);
  } catch (err) {
    console.error(err);
    summaryText.textContent = "Could not connect to the AI analyzer. Make sure the Java backend is running and Gemini API key is set.";
  } finally {
    summaryText.parentElement.classList.remove("loading-pulse");
  }
}

function renderReport(analysis) {
  calorieValue.textContent = String(analysis.calories);
  proteinValue.textContent = `${analysis.protein}g`;
  carbValue.textContent = `${analysis.carbs}g`;
  junkValue.textContent = `${analysis.junkLevel}/10`;
  ratingValue.textContent = analysis.rating;
  heartScoreValue.textContent = `${analysis.heartScore}/100`;
  scoreValue.textContent = (analysis.dailyScore || 0).toFixed(1);
  summaryText.textContent = analysis.summary;

  ratingBadge.textContent = analysis.rating;
  ratingBadge.className = `score-pill ${analysis.rating.toLowerCase()}`;

  proteinNote.textContent = analysis.proteinNote || "Estimated";
  carbNote.textContent = analysis.carbNote || "Estimated";
  junkNote.textContent = analysis.junkNote || "Estimated";

  proteinBar.style.width = `${Math.min(100, (analysis.protein / 75) * 100)}%`;
  carbBar.style.width = `${Math.min(100, (analysis.carbs / 280) * 100)}%`;
  junkBar.style.width = `${Math.min(100, (analysis.junkLevel / 10) * 100)}%`;

  suggestionList.innerHTML = (analysis.suggestions || [])
    .map(s => `<li>${escapeHTML(s)}</li>`).join("");

  habitList.innerHTML = (analysis.habits || [])
    .map(h => `<li>${escapeHTML(h)}</li>`).join("");

  recipeList.innerHTML = (analysis.recipes || [])
    .map(r => `<li>${escapeHTML(r)}</li>`).join("");

  matchBadge.textContent = "AI Analysed";
  foodList.innerHTML = ""; // Gemini gives an overall summary, not per-item breakdown
}

function renderEmptyState() {
  calorieValue.textContent = "0";
  proteinValue.textContent = "0g";
  carbValue.textContent = "0g";
  junkValue.textContent = "0/10";
  ratingValue.textContent = "Average";
  heartScoreValue.textContent = "--/100";
  scoreValue.textContent = "0.0";
  ratingBadge.textContent = "Average";
  ratingBadge.className = "score-pill average";
  summaryText.textContent = "Add a few foods to see your daily calories, macros, and AI health score.";
  
  proteinNote.textContent = "Needs data";
  carbNote.textContent = "Needs data";
  junkNote.textContent = "Needs data";
  
  proteinBar.style.width = "0%";
  carbBar.style.width = "0%";
  junkBar.style.width = "0%";
  
  suggestionList.innerHTML = "";
  habitList.innerHTML = "";
  recipeList.innerHTML = "";
  foodList.innerHTML = "";
  matchBadge.textContent = "0 matched";
}

function readStoredLog() {
  try { return window.localStorage.getItem(STORAGE_KEY) || ""; }
  catch (e) { return ""; }
}

function writeStoredLog(value) {
  try { window.localStorage.setItem(STORAGE_KEY, value); }
  catch (e) {}
}

function escapeHTML(str) {
  const div = document.createElement('div');
  div.innerText = str;
  return div.innerHTML;
}
