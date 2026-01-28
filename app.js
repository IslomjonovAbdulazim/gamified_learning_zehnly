// Word Islands - Vocabulary Learning App with Spaced Repetition

// ============ CONFIGURATION ============
const CATEGORIES = [
    { id: 1, folder: '01_animals', name: 'Animals' },
    { id: 2, folder: '02_food_and_drinks', name: 'Food & Drinks' },
    { id: 3, folder: '03_family_and_people', name: 'Family & People' },
    { id: 4, folder: '04_body_parts', name: 'Body Parts' },
    { id: 5, folder: '05_colors', name: 'Colors' },
    { id: 6, folder: '06_numbers_and_time', name: 'Numbers & Time' },
    { id: 7, folder: '07_house_and_furniture', name: 'House & Furniture' },
    { id: 8, folder: '08_clothes_and_accessories', name: 'Clothes & Accessories' },
    { id: 9, folder: '09_weather_and_nature', name: 'Weather & Nature' },
    { id: 10, folder: '10_transportation', name: 'Transportation' },
    { id: 11, folder: '11_school_and_education', name: 'School & Education' },
    { id: 12, folder: '12_sports_and_games', name: 'Sports & Games' },
    { id: 13, folder: '13_technology', name: 'Technology' },
    { id: 14, folder: '14_work_and_office', name: 'Work & Office' },
    { id: 15, folder: '15_health_and_medicine', name: 'Health & Medicine' },
    { id: 16, folder: '16_emotions_and_feelings', name: 'Emotions & Feelings' },
    { id: 17, folder: '17_actions_and_verbs', name: 'Actions & Verbs' },
    { id: 18, folder: '18_places_and_locations', name: 'Places & Locations' },
    { id: 19, folder: '19_kitchen_and_cooking', name: 'Kitchen & Cooking' },
    { id: 20, folder: '20_music_and_entertainment', name: 'Music & Entertainment' },
];

// SRS intervals in minutes (for demo: short intervals, in production use days)
const SRS_INTERVALS = {
    0: 1,      // New word: review in 1 min
    1: 5,      // Level 1: review in 5 min
    2: 30,     // Level 2: review in 30 min
    3: 120,    // Level 3: review in 2 hours
    4: 1440,   // Level 4: review in 1 day
    5: 4320,   // Level 5: review in 3 days
    6: 10080,  // Level 6: review in 1 week
};

const FORGET_THRESHOLD = 10; // Minutes until word starts to "decay"

// ============ OPTIONS COUNT ============
function getOptionCount() {
    return parseInt(localStorage.getItem('wordIslands_optionCount') || '2');
}

function setOptionCount(count) {
    localStorage.setItem('wordIslands_optionCount', count);
}

// ============ STATE ============
let currentCategory = null;
let currentTests = [];
let currentTestIndex = 0;
let practiceResults = { correct: 0, wrong: 0 };
let categoryData = {};

// ============ LOCAL STORAGE ============
function getProgress() {
    const saved = localStorage.getItem('wordIslands_progress');
    return saved ? JSON.parse(saved) : {};
}

function saveProgress(progress) {
    localStorage.setItem('wordIslands_progress', JSON.stringify(progress));
}

function getWordProgress(category, word) {
    const progress = getProgress();
    const key = `${category}_${word}`;
    return progress[key] || {
        level: 0,
        lastReview: null,
        nextReview: null,
        correct: 0,
        wrong: 0
    };
}

function updateWordProgress(category, word, correct) {
    const progress = getProgress();
    const key = `${category}_${word}`;
    const wordProg = progress[key] || {
        level: 0,
        lastReview: null,
        nextReview: null,
        correct: 0,
        wrong: 0
    };

    const now = Date.now();
    wordProg.lastReview = now;

    if (correct) {
        wordProg.level = Math.min(wordProg.level + 1, 6);
        wordProg.correct++;
    } else {
        wordProg.level = Math.max(wordProg.level - 2, 0);
        wordProg.wrong++;
    }

    // Calculate next review time
    const intervalMinutes = SRS_INTERVALS[wordProg.level];
    wordProg.nextReview = now + (intervalMinutes * 60 * 1000);

    progress[key] = wordProg;
    saveProgress(progress);
    return wordProg;
}

function getStats() {
    const saved = localStorage.getItem('wordIslands_stats');
    return saved ? JSON.parse(saved) : { streak: 0, lastPractice: null, totalWords: 0 };
}

function updateStats() {
    const stats = getStats();
    const today = new Date().toDateString();
    const lastPractice = stats.lastPractice ? new Date(stats.lastPractice).toDateString() : null;

    if (lastPractice !== today) {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        if (lastPractice === yesterday.toDateString()) {
            stats.streak++;
        } else if (lastPractice !== today) {
            stats.streak = 1;
        }
        stats.lastPractice = Date.now();
    }

    // Count total learned words
    const progress = getProgress();
    stats.totalWords = Object.values(progress).filter(p => p.level >= 1).length;

    localStorage.setItem('wordIslands_stats', JSON.stringify(stats));
    return stats;
}

// ============ CATEGORY STATUS ============
function getCategoryStatus(category) {
    const progress = getProgress();
    const now = Date.now();
    let totalWords = 0;
    let learnedWords = 0;
    let needsReview = 0;
    let forgotten = 0;

    // Check words in this category
    Object.keys(progress).forEach(key => {
        if (key.startsWith(category.name + '_')) {
            totalWords++;
            const wordProg = progress[key];

            if (wordProg.level >= 1) learnedWords++;

            if (wordProg.nextReview && now > wordProg.nextReview) {
                const overdueMinutes = (now - wordProg.nextReview) / (60 * 1000);
                if (overdueMinutes > FORGET_THRESHOLD * 3) {
                    forgotten++;
                } else if (overdueMinutes > 0) {
                    needsReview++;
                }
            }
        }
    });

    // Determine status
    let status = 'new';
    let imageState = 'locked';

    if (learnedWords > 0) {
        if (forgotten > learnedWords * 0.5) {
            status = 'forgotten';
            imageState = 'locked';
        } else if (needsReview > learnedWords * 0.3) {
            status = 'needs-practice';
            imageState = 'damaged';
        } else {
            status = 'active';
            imageState = 'active';
        }
    }

    return {
        totalWords: 50, // Each category has 50 words
        learnedWords,
        needsReview,
        forgotten,
        status,
        imageState,
        progress: Math.round((learnedWords / 50) * 100)
    };
}

// ============ LOAD DATA ============
async function loadCategoryData(category) {
    if (categoryData[category.folder]) {
        return categoryData[category.folder];
    }

    try {
        const [wordsRes, testsRes] = await Promise.all([
            fetch(`data/${category.folder}/words.json`),
            fetch(`data/${category.folder}/tests.json`)
        ]);

        const words = await wordsRes.json();
        const tests = await testsRes.json();

        categoryData[category.folder] = { words, tests };
        return categoryData[category.folder];
    } catch (error) {
        console.error('Error loading category data:', error);
        return null;
    }
}

// ============ RENDER FUNCTIONS ============
function renderCategories() {
    const grid = document.getElementById('categoriesGrid');
    grid.innerHTML = '';

    CATEGORIES.forEach(category => {
        const status = getCategoryStatus(category);
        const card = document.createElement('div');
        card.className = `category-card ${status.status === 'needs-practice' ? 'needs-practice' : ''} ${status.status === 'forgotten' ? 'forgotten' : ''}`;

        card.innerHTML = `
            <img class="category-icon" src="data/${category.folder}/images/${status.imageState}.png" alt="${category.name}">
            <h3>${category.name}</h3>
            <p class="category-status ${status.status === 'active' ? 'active' : status.status === 'needs-practice' ? 'warning' : status.status === 'forgotten' ? 'danger' : ''}">
                ${status.status === 'new' ? '🔒 Locked' :
                  status.status === 'forgotten' ? '💀 Forgotten!' :
                  status.status === 'needs-practice' ? '⚠️ Needs Practice' :
                  `✨ ${status.learnedWords}/50 words`}
            </p>
            <div class="progress-mini">
                <div class="progress-mini-fill" style="width: ${status.progress}%"></div>
            </div>
        `;

        card.onclick = () => showCategory(category);
        grid.appendChild(card);
    });

    // Update header stats
    const stats = getStats();
    document.getElementById('streak').textContent = stats.streak;
    document.getElementById('totalWords').textContent = stats.totalWords;

    // Show/hide floating practice button
    let totalNeedReview = 0;
    CATEGORIES.forEach(cat => {
        const catStatus = getCategoryStatus(cat);
        totalNeedReview += catStatus.needsReview + catStatus.forgotten;
    });

    const floatingBtn = document.getElementById('floatingPracticeBtn');
    if (totalNeedReview > 0) {
        document.getElementById('totalNeedReview').textContent = totalNeedReview;
        floatingBtn.style.display = 'block';
    } else {
        floatingBtn.style.display = 'none';
    }
}

function showView(viewId) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');
}

function showCategories() {
    renderCategories();
    showView('categoriesView');
}

async function showCategory(category) {
    currentCategory = category;
    const data = await loadCategoryData(category);
    if (!data) return;

    const status = getCategoryStatus(category);

    document.getElementById('categoryIcon').src = `data/${category.folder}/images/${status.imageState}.png`;
    document.getElementById('categoryTitle').textContent = category.name;
    document.getElementById('categoryProgress').textContent =
        `${status.learnedWords} words learned • ${status.needsReview} need review`;

    // Show practice button if needsReview > 0 OR learnedWords > 0
    const practiceBtn = document.getElementById('practiceBtn');
    practiceBtn.style.display = (status.needsReview > 0 || status.learnedWords > 0) ? 'inline-block' : 'none';

    // Hide learn button if all words learned
    const learnBtn = document.getElementById('learnBtn');
    learnBtn.style.display = status.learnedWords < 50 ? 'inline-block' : 'none';

    // Render words list
    const wordsList = document.getElementById('wordsList');
    wordsList.innerHTML = '';

    data.words.words.forEach(word => {
        const wordProg = getWordProgress(category.name, word);
        const now = Date.now();
        let wordStatus = 'new';

        if (wordProg.level >= 4) wordStatus = 'mastered';
        else if (wordProg.level >= 1) {
            if (wordProg.nextReview && now > wordProg.nextReview) {
                wordStatus = 'weak';
            } else {
                wordStatus = 'learning';
            }
        }

        const chip = document.createElement('div');
        chip.className = `word-chip ${wordStatus}`;
        chip.innerHTML = `
            <span>${wordStatus === 'mastered' ? '⭐' : wordStatus === 'learning' ? '📖' : wordStatus === 'weak' ? '⚠️' : '🔒'}</span>
            <span>${word}</span>
        `;
        wordsList.appendChild(chip);
    });

    showView('categoryView');
}

// ============ PRACTICE ============
async function startGlobalPractice() {
    const now = Date.now();
    const progress = getProgress();
    let allWordsToReview = [];

    // Gather words needing review from ALL categories
    for (const category of CATEGORIES) {
        const data = await loadCategoryData(category);
        if (!data) continue;

        data.words.words.forEach(word => {
            const key = `${category.name}_${word}`;
            const wordProg = progress[key];

            if (wordProg && wordProg.nextReview && now >= wordProg.nextReview) {
                allWordsToReview.push({
                    word,
                    category,
                    priority: now - wordProg.nextReview
                });
            }
        });
    }

    if (allWordsToReview.length === 0) {
        return;
    }

    // Sort by most overdue first
    allWordsToReview.sort((a, b) => b.priority - a.priority);

    // Take up to 15 words
    const selectedWords = allWordsToReview.slice(0, 15);

    // Get tests for selected words
    currentTests = [];
    for (const item of selectedWords) {
        const data = await loadCategoryData(item.category);
        const wordTests = data.tests.tests.filter(t => t.word === item.word);
        if (wordTests.length > 0) {
            const test = wordTests[Math.floor(Math.random() * wordTests.length)];
            test._category = item.category;
            currentTests.push(test);
        }
    }

    // Shuffle
    currentTests.sort(() => Math.random() - 0.5);

    currentCategory = { name: 'Mixed Practice', folder: null };
    currentTestIndex = 0;
    practiceResults = { correct: 0, wrong: 0 };

    showView('practiceView');
    showQuestion();
}

async function startPractice() {
    const data = await loadCategoryData(currentCategory);
    if (!data) return;

    const now = Date.now();
    const progress = getProgress();

    // Get words that need review (SRS)
    let wordsToReview = [];

    data.words.words.forEach(word => {
        const key = `${currentCategory.name}_${word}`;
        const wordProg = progress[key];

        if (wordProg && wordProg.nextReview && now >= wordProg.nextReview) {
            wordsToReview.push({ word, priority: now - wordProg.nextReview });
        }
    });

    // Sort by most overdue first
    wordsToReview.sort((a, b) => b.priority - a.priority);

    // If no words to review, get random learned words
    if (wordsToReview.length === 0) {
        data.words.words.forEach(word => {
            const key = `${currentCategory.name}_${word}`;
            const wordProg = progress[key];
            if (wordProg && wordProg.level >= 1) {
                wordsToReview.push({ word, priority: 0 });
            }
        });
        // Shuffle
        wordsToReview.sort(() => Math.random() - 0.5);
    }

    // Take up to 10 words
    const selectedWords = wordsToReview.slice(0, 10).map(w => w.word);

    if (selectedWords.length === 0) {
        alert('No words to practice! Learn some new words first.');
        return;
    }

    // Get tests for selected words
    currentTests = data.tests.tests.filter(t => selectedWords.includes(t.word));

    // Shuffle and limit
    currentTests.sort(() => Math.random() - 0.5);
    currentTests = currentTests.slice(0, Math.min(15, currentTests.length));

    currentTestIndex = 0;
    practiceResults = { correct: 0, wrong: 0 };

    showView('practiceView');
    showQuestion();
}

async function startLearnNew() {
    const data = await loadCategoryData(currentCategory);
    if (!data) return;

    const progress = getProgress();

    // Get words not yet learned
    let newWords = data.words.words.filter(word => {
        const key = `${currentCategory.name}_${word}`;
        return !progress[key] || progress[key].level === 0;
    });

    // Take 5 new words
    newWords = newWords.slice(0, 5);

    if (newWords.length === 0) {
        return;
    }

    // Get tests for new words
    currentTests = data.tests.tests.filter(t => newWords.includes(t.word));
    currentTests.sort(() => Math.random() - 0.5);
    currentTests = currentTests.slice(0, Math.min(15, currentTests.length));

    currentTestIndex = 0;
    practiceResults = { correct: 0, wrong: 0 };

    showView('practiceView');
    showQuestion();
}

function showQuestion() {
    if (currentTestIndex >= currentTests.length) {
        showResults();
        return;
    }

    const test = currentTests[currentTestIndex];

    document.getElementById('practiceProgress').style.width =
        `${(currentTestIndex / currentTests.length) * 100}%`;
    document.getElementById('practiceCount').textContent =
        `${currentTestIndex + 1}/${currentTests.length}`;

    document.getElementById('questionText').textContent = test.question;

    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';

    // Limit options based on setting
    const optionCount = getOptionCount();
    const correctAnswer = test.options[test.correct_answer];
    let displayOptions = [...test.options];

    // If we need fewer options, keep correct + random wrong ones
    if (optionCount < displayOptions.length) {
        const wrongOptions = displayOptions.filter((_, i) => i !== test.correct_answer);
        const selectedWrong = wrongOptions.slice(0, optionCount - 1);
        displayOptions = [correctAnswer, ...selectedWrong];
        // Shuffle
        displayOptions.sort(() => Math.random() - 0.5);
    }

    // Find new correct index
    const newCorrectIndex = displayOptions.indexOf(correctAnswer);
    test._displayOptions = displayOptions;
    test._displayCorrectIndex = newCorrectIndex;

    displayOptions.forEach((option, index) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = option;
        btn.onclick = () => selectAnswer(index);
        optionsContainer.appendChild(btn);
    });

    document.getElementById('questionCard').classList.remove('hidden');
    document.getElementById('feedbackCard').classList.add('hidden');
}

function selectAnswer(selectedIndex) {
    const test = currentTests[currentTestIndex];
    const correctIndex = test._displayCorrectIndex !== undefined ? test._displayCorrectIndex : test.correct_answer;
    const displayOptions = test._displayOptions || test.options;
    const correct = selectedIndex === correctIndex;

    // Update word progress (use test's category for global practice)
    const categoryName = test._category ? test._category.name : currentCategory.name;
    updateWordProgress(categoryName, test.word, correct);

    // Show feedback on buttons
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach((btn, index) => {
        btn.disabled = true;
        if (index === correctIndex) {
            btn.classList.add('correct');
        } else if (index === selectedIndex && !correct) {
            btn.classList.add('wrong');
        }
    });

    // Update results
    if (correct) {
        practiceResults.correct++;
        createConfetti();
    } else {
        practiceResults.wrong++;
    }

    // Auto-advance after delay
    setTimeout(() => {
        currentTestIndex++;
        showQuestion();
    }, correct ? 800 : 1500);
}

function nextQuestion() {
    currentTestIndex++;
    showQuestion();
}

function showResults() {
    updateStats();

    document.getElementById('correctCount').textContent = practiceResults.correct;
    document.getElementById('wrongCount').textContent = practiceResults.wrong;

    showView('resultsView');
}

function exitPractice() {
    if (confirm('Exit practice? Your progress will be saved.')) {
        showCategory(currentCategory);
    }
}

// ============ CONFETTI ============
function createConfetti() {
    const colors = ['#6366f1', '#22c55e', '#f59e0b', '#ec4899', '#8b5cf6'];
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDuration = (Math.random() * 1 + 1) + 's';
        confetti.style.animationDelay = Math.random() * 0.5 + 's';
        document.body.appendChild(confetti);

        setTimeout(() => confetti.remove(), 2000);
    }
}

// ============ INIT ============
document.addEventListener('DOMContentLoaded', () => {
    // Set saved option count in dropdown
    const optionCount = getOptionCount();
    document.getElementById('optionCount').value = optionCount;

    renderCategories();
});
