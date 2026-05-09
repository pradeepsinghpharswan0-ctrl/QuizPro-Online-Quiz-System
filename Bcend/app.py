from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import db

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE ----------------

db.init_db()
db.seed_questions()


def letter_to_int(letter):
    mapping = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "N": -1
    }

    return mapping.get(letter, -1)


# ---------------- GET QUESTIONS ----------------

@app.route("/api/questions")
def get_questions():

    category = request.args.get("category")
    difficulty = request.args.get("difficulty")
    limit = int(request.args.get("limit", 10))

    conn = db.get_connection()

    # AI QUIZ: mixed questions from all categories
    if category == "ai":

        rows = conn.execute(
            """
            SELECT id, question, optA, optB, optC, optD
            FROM questions
            ORDER BY RANDOM()
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

        conn.close()

        return jsonify([dict(row) for row in rows])

    # NORMAL QUIZ
    rows = conn.execute(
        """
        SELECT id, question, optA, optB, optC, optD
        FROM questions
        WHERE category = ?
        AND difficulty = ?
        ORDER BY RANDOM()
        LIMIT ?
        """,
        (category, difficulty, limit)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# ---------------- SUBMIT QUIZ ----------------

@app.route("/api/submit", methods=["POST"])
def submit_quiz():

    data = request.json

    username = data.get("username")
    answers_dict = data.get("answers")

    if not username:
        username = "Anonymous"

    if not answers_dict:
        return jsonify({"error": "No answers submitted"}), 400

    question_ids = list(map(int, answers_dict.keys()))
    placeholders = ",".join(["?"] * len(question_ids))

    conn = db.get_connection()

    rows = conn.execute(
        f"""
        SELECT id, question, optA, optB, optC, optD,
               correct, explanation, category, difficulty
        FROM questions
        WHERE id IN ({placeholders})
        """,
        question_ids
    ).fetchall()

    if not rows:
        conn.close()
        return jsonify({"error": "No matching questions found"}), 404

    rows_by_id = {row["id"]: row for row in rows}

    answers = []
    correct = []
    review = []

    for qid in question_ids:

        if qid not in rows_by_id:
            continue

        row = rows_by_id[qid]

        user_answer = answers_dict.get(str(qid), "N")
        correct_answer = row["correct"]

        answers.append(letter_to_int(user_answer))
        correct.append(letter_to_int(correct_answer))

        review.append({
            "question": row["question"],
            "user": user_answer,
            "correct": correct_answer,
            "explanation": row["explanation"]
        })

    n = len(answers)

    # Python score calculation for online deployment
    score = sum(1 for i in range(n) if answers[i] == correct[i])

    category = rows[0]["category"]
    difficulty = rows[0]["difficulty"]

    conn.execute(
        """
        INSERT INTO results
        (username, score, total, category, difficulty, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            score,
            n,
            category,
            difficulty,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "score": score,
        "total": n,
        "review": review
    })


# ---------------- LEADERBOARD ----------------

@app.route("/api/leaderboard")
def leaderboard():

    conn = db.get_connection()

    rows = conn.execute(
        """
        SELECT username, score, total, category,
               difficulty, created_at
        FROM results
        ORDER BY score DESC, created_at ASC
        LIMIT 10
        """
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# ---------------- ADMIN ADD QUESTION ----------------

@app.route("/api/admin/add-question", methods=["POST"])
def add_question():

    admin_password = request.headers.get("Admin-Password")

    if admin_password != "admin123":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    required_fields = [
        "category",
        "difficulty",
        "question",
        "optA",
        "optB",
        "optC",
        "optD",
        "correct",
        "explanation"
    ]

    for field in required_fields:
        if field not in data or data[field] == "":
            return jsonify({"error": f"{field} is required"}), 400

    conn = db.get_connection()

    conn.execute(
        """
        INSERT INTO questions
        (
            category,
            difficulty,
            question,
            optA,
            optB,
            optC,
            optD,
            correct,
            explanation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["category"],
            data["difficulty"],
            data["question"],
            data["optA"],
            data["optB"],
            data["optC"],
            data["optD"],
            data["correct"],
            data["explanation"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Question added successfully"
    })


# ---------------- HEALTH CHECK ----------------

@app.route("/")
def home():
    return jsonify({
        "message": "QuizPro Backend is running successfully"
    })


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run()