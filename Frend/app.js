const API_BASE = "http://127.0.0.1:5000";

let username = "";
let selectedCategory = "";
let selectedDifficulty = "";
let questions = [];
let currentIndex = 0;
let answers = {};
let timer;
let timeLeft = 60;

const sections = document.querySelectorAll(".section");

function showSection(id) {
  sections.forEach(section => section.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

document.getElementById("loginBtn").onclick = function () {
  username = document.getElementById("username").value.trim();

  if (username === "") {
    alert("Please enter your name");
    return;
  }

  document.getElementById("welcomeText").innerText = `Hi, ${username} 👋`;
  showSection("homeSection");
};

document.querySelectorAll(".category-card").forEach(card => {
  card.onclick = function () {
    selectedCategory = card.dataset.category;
    document.getElementById("difficultyBox").classList.remove("hidden");
  };
});

document.querySelectorAll(".difficulty-btn").forEach(btn => {
  btn.onclick = function () {
    selectedDifficulty = btn.dataset.level;
    startQuiz();
  };
});

async function startQuiz() {
  currentIndex = 0;
  answers = {};

  const res = await fetch(
    `${API_BASE}/api/questions?category=${selectedCategory}&difficulty=${selectedDifficulty}&limit=10`
  );

  questions = await res.json();

  if (questions.length === 0) {
    alert("No questions found for this category.");
    return;
  }

  document.getElementById("quizHeading").innerText =
    `${selectedCategory.toUpperCase()} - ${selectedDifficulty.toUpperCase()} Quiz`;

  showSection("quizSection");
  showQuestion();
}

function showQuestion() {
  clearInterval(timer);
  timeLeft = 60;

  const q = questions[currentIndex];

  document.getElementById("timer").innerText = `${timeLeft}s`;
  document.getElementById("questionText").innerText =
    `${currentIndex + 1}. ${q.question}`;

  document.getElementById("progress").style.width =
    `${((currentIndex + 1) / questions.length) * 100}%`;

  const optionsContainer = document.getElementById("optionsContainer");
  optionsContainer.innerHTML = "";

  ["A", "B", "C", "D"].forEach(letter => {
    const optionDiv = document.createElement("div");
    optionDiv.className = "option";
optionDiv.addEventListener("click", () => {

    document.querySelectorAll(".option").forEach(opt => {
        opt.classList.remove("selected");
    });

    optionDiv.classList.add("selected");

    optionDiv.querySelector("input").checked = true;

});

    optionDiv.innerHTML = `
      <label>
        <input type="radio" name="answer" value="${letter}">
        ${letter}. ${q["opt" + letter]}
      </label>
    `;

    optionsContainer.appendChild(optionDiv);
  });

  timer = setInterval(() => {
    timeLeft--;
    document.getElementById("timer").innerText = `${timeLeft}s`;

    if (timeLeft <= 0) {
      saveAnswer();
      nextQuestion();
    }
  }, 1000);
}

function saveAnswer() {
  const selected = document.querySelector('input[name="answer"]:checked');

  if (selected) {
    answers[questions[currentIndex].id] = selected.value;
  } else {
    answers[questions[currentIndex].id] = "N";
  }
}

document.getElementById("nextBtn").onclick = function () {
  saveAnswer();
  nextQuestion();
document.getElementById("submitBtn").onclick = function () {

  saveAnswer();

  clearInterval(timer);

  submitQuiz();

};
};

function nextQuestion() {
  clearInterval(timer);

  if (currentIndex < questions.length - 1) {
    currentIndex++;
    showQuestion();
  } else {
    submitQuiz();
  }
}

async function submitQuiz() {
  const res = await fetch(`${API_BASE}/api/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: username,
      answers: answers
    })
  });

  const data = await res.json();

  document.getElementById("scoreText").innerText =
    `Your Score: ${data.score}/${data.total}`;

  showReview(data.review);
  await loadLeaderboard();

  showSection("resultSection");
}

function showReview(review) {
  const reviewContainer = document.getElementById("reviewContainer");
  reviewContainer.innerHTML = "";

  review.forEach((item, index) => {
    const div = document.createElement("div");
    div.className = "review-box";

    const isCorrect = item.user === item.correct;

    div.innerHTML = `
      <h3>Q${index + 1}. ${item.question}</h3>
      <p class="${isCorrect ? "correct" : "wrong"}">
        Your Answer: ${item.user === "N" ? "Not Attempted" : item.user}
      </p>
      <p class="correct">Correct Answer: ${item.correct}</p>
      <p>Explanation: ${item.explanation}</p>
    `;

    reviewContainer.appendChild(div);
  });
}

async function loadLeaderboard() {
  const res = await fetch(`${API_BASE}/api/leaderboard`);
  const data = await res.json();

  const leaderboard1 = document.getElementById("leaderboardContainer");
  const leaderboard2 = document.getElementById("leaderboardPageContainer");

  const html = data.map((item, index) => `
    <div class="leaderboard-item">
      <span>${index + 1}. ${item.username}</span>
      <span>${item.score}/${item.total}</span>
    </div>
  `).join("");

  if (leaderboard1) leaderboard1.innerHTML = html;
  if (leaderboard2) leaderboard2.innerHTML = html;
}
document.getElementById("backHomeBtn").onclick = function () {
  showSection("homeSection");
};

document.getElementById("adminBtn").onclick = function () {
  showSection("adminSection");
};

document.getElementById("closeAdminBtn").onclick = function () {
  showSection("homeSection");
};

document.getElementById("adminLoginBtn").onclick = function () {
  const password = document.getElementById("adminPassword").value;

  if (password === "admin123") {
    document.getElementById("adminLoginBox").classList.add("hidden");
    document.getElementById("adminForm").classList.remove("hidden");
  } else {
    alert("Wrong admin password");
  }
};

document.getElementById("addQuestionBtn").onclick = async function () {
  const questionData = {
    category: document.getElementById("questionCategory").value,
    difficulty: document.getElementById("questionDifficulty").value,
    question: document.getElementById("questionInput").value,
    optA: document.getElementById("optionA").value,
    optB: document.getElementById("optionB").value,
    optC: document.getElementById("optionC").value,
    optD: document.getElementById("optionD").value,
    correct: document.getElementById("correctAnswer").value,
    explanation: document.getElementById("explanation").value
  };

  const res = await fetch(`${API_BASE}/api/admin/add-question`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Admin-Password": "admin123"
    },
    body: JSON.stringify(questionData)
  });

  const data = await res.json();

  if (data.message) {
    alert("Question added successfully");
  } else {
    alert("Error adding question");
  }
};

const homeNav = document.getElementById("homeNav");
if (homeNav) {
  homeNav.onclick = function () {
    showSection("homeSection");
  };
}

const aboutNav = document.getElementById("aboutNav");
if (aboutNav) {
  aboutNav.onclick = function () {
    showSection("aboutSection");
  };
}
const leaderboardNav = document.getElementById("leaderboardNav");

if (leaderboardNav) {
  leaderboardNav.onclick = async function () {
    await loadLeaderboard();
    showSection("leaderboardSection");
  };
}
const leaderboardBackBtn = document.getElementById("leaderboardBackBtn");

if (leaderboardBackBtn) {
  leaderboardBackBtn.onclick = function () {
    showSection("homeSection");
  };
}