import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# READ JOB DESCRIPTION
# =========================

with open("job_description.txt", "r", encoding="utf-8") as f:
    job_description = f.read()

# =========================
# READ RESUMES
# =========================

resume_folder = "resumes"

resume_texts = []
resume_names = []

for file in os.listdir(resume_folder):

    if file.endswith(".txt"):

        path = os.path.join(resume_folder, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

            resume_texts.append(text)
            resume_names.append(file)

# =========================
# TF-IDF
# =========================

documents = [job_description] + resume_texts

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(documents)

# =========================
# SIMILARITY
# =========================

job_vector = tfidf_matrix[0]

resume_vectors = tfidf_matrix[1:]

scores = cosine_similarity(job_vector, resume_vectors)

# =========================
# RESULTS
# =========================

results = []

for i in range(len(resume_names)):

    score = round(scores[0][i] * 100, 2)

    status = "Shortlisted" if score >= 30 else "Rejected"

    results.append({
        "Resume": resume_names[i],
        "Score": score,
        "Status": status
    })

# =========================
# DATAFRAME
# =========================

df = pd.DataFrame(results)

df = df.sort_values(by="Score", ascending=False)

print("\n===== Resume Screening Results =====\n")

print(df)

# =========================
# SAVE CSV
# =========================

os.makedirs("outputs", exist_ok=True)

df.to_csv("outputs/results.csv", index=False)

print("\nCSV Report Saved Successfully!")

print("\nFile Location: outputs/results.csv")