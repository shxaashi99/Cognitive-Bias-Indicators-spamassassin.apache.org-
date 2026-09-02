Bias-Based Phishing Risk Scoring Model (BPRSM) – Artefact Documentation
Author: Ibrahim Abdullahi Sheikh_25006888
Institution: University of the West of England (UWE)
Programme: MSc Project
Email: Shxaashi99@gmail.com

1. Overview and Purpose
This repository contains the implementation artefacts for the Bias‑Based Phishing Risk Scoring Model (BPRSM), developed as part of a Masters research project at UWE. The overarching aim of this work is to bridge the gap between psycholinguistic theory and automated phishing detection by providing a computational framework that identifies and quantifies cognitive bias indicators in email text.

The research adopts a Design Science Research (DSR) paradigm, combining a PRISMA‑governed systematic literature review with empirical validation using the SpamAssassin Public Corpus. The artefacts included here serve two primary purposes: (1) to validate the theoretical framework through machine learning, and (2) to provide a functional dashboard that demonstrates how the model can be applied in practice to assess the psychological risk of email content.

It is important to note that the artefacts are research‑grade prototypes rather than production‑ready security tools. They are designed to illustrate the principles and performance of the BPRSM framework, and to support further academic exploration rather than to serve as a definitive detection solution. The repository includes scripts for data ingestion, feature engineering, model training and evaluation, as well as two different HTML dashboards that offer alternative interfaces for visualising risk scores and forensic narratives.

2. Repository Contents and File Descriptions
2.1 The SpamAssassin Corpus Archives
The repository contains nine compressed archive files named according to the original SpamAssassin Public Corpus distribution conventions. These files are:

20021010_easy_ham.tar.bz2

20021010_hard_ham.tar.bz2

20021010_spam.tar.bz2

20030228_easy_ham.tar.bz2

20030228_easy_ham_2.tar.bz2

20030228_hard_ham.tar.bz2

20030228_spam.tar.bz2

20030228_spam_2.tar.bz2

20050311_spam_2.tar.bz2

Each archive contains a collection of email messages in plain text format, organised into sub‑directories that correspond to their classification as either "ham" (legitimate email) or "spam" (unwanted or malicious email). The "easy_ham" and "hard_ham" designations reflect the relative difficulty of distinguishing those legitimate messages from spam using traditional filtering techniques. The corpus is widely used in academic research as a benchmark for email classification and phishing detection studies.

For the artefact to function correctly, these archives must be extracted into folders matching their base names (e.g., 20021010_easy_ham, 20021010_hard_ham, 20021010_spam, and so on). The scripts described below assume that these extracted folders exist within the working directory. Users are responsible for extracting the archives prior to running the analysis pipeline.

2.2 process_emails.py – Data Ingestion Script
This Python script provides a data ingestion pipeline that reads email messages from the extracted SpamAssassin folders and loads them into a pandas DataFrame for further analysis. The script defines a function extract_and_load() that iterates over a predefined list of folder names – easy_ham, hard_ham, and spam – and, for each email file found within those folders, parses the message using Python's built‑in email library.

For each email, the script extracts the plain text body by walking through any multipart MIME structure and decoding the payload using Latin‑1 encoding. It assigns a binary label to each message: 1 for messages found in the spam folder, and 0 for messages found in the easy_ham or hard_ham folders. The resulting DataFrame contains two columns: text (the extracted email body) and label (the binary classification).

Current limitations of this script: The script does not, in its current form, save the DataFrame to disk as a pickle file. It only prints the total number of emails loaded and returns the DataFrame in memory. It does not handle the full range of folder names present in the extracted archives, nor does it process the archived files directly without prior manual extraction. Users should be aware that this script is primarily a demonstration of the ingestion logic rather than a complete preprocessing pipeline. To use it effectively, one would need to modify the folder list to match the extracted archive names and add a serialisation step to persist the DataFrame for subsequent analysis.

2.3 comprehensive_analysis.py – Main Analysis Pipeline
This script is the core of the quantitative validation component of the research. It performs all steps of the BPRSM analysis, from loading email data through to generating visualisation outputs. The script is organised into several distinct sections, each corresponding to a specific research objective.

2.3.1 Psychological Taxonomy Definition
The script begins by defining a TAXONOMY dictionary that maps four cognitive bias categories to regular expression patterns. These categories are:

Authority: Patterns such as ceo, admin, official, director, management, department, and security are used to detect language that invokes institutional hierarchy or official status.

Urgency: Patterns including immediat, now, deadline, urgent, asap, expir, limit, and quick capture temporal pressure and time‑sensitive language.

Fear: Patterns such as suspend, risk, unauthoriz, breach, lock, warn, legal, and compromis identify threat‑based and anxiety‑inducing terms.

Elicitation: Patterns like click, login, updat, submit, download, confirm, verify, and access detect language that prompts the recipient to take a specific action.

These patterns were derived from the systematic literature review and taxonomic calibration described in the research write‑up, and they represent the linguistic markers most strongly associated with cognitive manipulation in phishing emails.

2.3.2 Data Loading
The load_extracted_data() function iterates over a hard‑coded list of folder names – spam, spam_2, easy_ham, easy_ham_2, and hard_ham – and reads each email file found in those directories. For each file, it reads the entire contents as a string (using Latin‑1 encoding) and appends a record consisting of the full email text and its label (1 for spam folders, 0 for ham folders) to a list. This list is then converted into a pandas DataFrame.

Important limitation: This script does not load data from the process_emails.py script or from any intermediate serialised file. It reads directly from the extracted archive folders, meaning that both scripts are independent of each other. The README description suggesting that process_emails.py feeds into comprehensive_analysis.py is therefore not accurate in the current implementation.

2.3.3 Feature Extraction
The extract_features() function applies the taxonomy patterns to each email body. For each of the four bias categories, it counts the number of matches found using regular expressions, and then sums these counts to calculate a Density metric, defined as the total number of bias indicators divided by the total word count, multiplied by 100. This Density feature is intended to capture the overall concentration of affective and manipulative language in the message.

2.3.4 Model Training and Evaluation
The script separates the feature columns – the four bias category counts plus the Density metric – from the target label column. It then splits the data into training and test sets using a 80/20 split (the default for train_test_split when test_size=0.3), trains a Random Forest classifier with 100 estimators, and evaluates the model using the classification report and ROC‑AUC score. The results are printed to the terminal.

2.3.5 Visualisation Generation
The script generates five PNG visualisation files, which are saved directly to the working directory:

synergy_matrix.png : A heatmap showing the correlation matrix of the four bias category counts, computed only on the spam (phishing) subset. This visualises how strongly different biases co‑occur within malicious emails.

feature_importance.png : A bar chart displaying the relative importance of each feature (Authority, Urgency, Fear, Elicitation, and Density) as determined by the Random Forest model.

trigger_density.png : A violin plot comparing the distribution of the Density metric between ham and spam classes.

synergy_co_occurrence.png : A heatmap of the co‑occurrence matrix, showing the frequency with which each pair of bias categories co‑occur in the same email (i.e., both categories having at least one detected indicator).

confusion_matrix.png : A heatmap of the confusion matrix from the model's predictions on the test set.

Missing functionality: The script does not, in its current form, save any JSON file for the dashboard. The dashboard_data.json file mentioned in the README is not generated by this script, meaning that the HTML dashboard cannot load pre‑computed sample data without manual intervention.

2.4 HTML Dashboards
The repository contains two HTML dashboard files, both of which are standalone web applications that can be opened directly in a browser. They are designed to demonstrate the BPRSM framework by allowing users to paste email text and receive a risk assessment based on the detection of cognitive bias indicators.

2.4.1 risk_dashboard old.html
This is the earlier version of the dashboard. It uses a simplified taxonomy with four categories – Authority, Urgency, Fear, and Elicitation – each associated with a short list of keywords. The script embedded in this dashboard counts keyword occurrences, calculates a raw score by multiplying each count by 25, and then applies a synergy multiplier of 1.4 if at least two categories are detected, and a further multiplier of 1.2 if both Authority and Urgency are present. The final score is capped at 100%.

The dashboard provides a risk gauge, a list of detected categories with their marker counts, and a set of methodological citations that correspond to the detected biases. The scoring logic is entirely independent of the Python model and uses a different weighting scheme, meaning that the risk scores generated by this dashboard are not directly comparable to those from the Random Forest classifier.

2.4.2 new risk_dashboard.html
This is the updated and more visually polished version of the dashboard. It defines four cognitive categories – Authority_Heuristic, Affective_Urgency, Trait_Exploitation, and Linguistic_Deception – each with its own set of keywords, insight text, findings, and tags derived from the research literature.

The scoring logic in this dashboard is as follows: each detected keyword contributes 12 points to the total score. If both Authority and Urgency are detected, an additional 25‑point synergy bonus is applied. If both Linguistic Deception and Urgency are detected, a further 20‑point bonus is added. The score is then capped at 100%.

The dashboard displays a colour‑coded risk gauge, a detailed linguistic profile for each detected category (including the number of matches, research insights, and findings), a forensic narrative that synthesises the detected triggers into a coherent explanation, and a prescriptive recommendation section that suggests defensive actions based on the risk level.

Key differences from the Python model: The keyword lists, category names, weights, and synergy logic in the new dashboard differ substantially from those used in the Random Forest model. For example, the dashboard uses a broader set of keywords and a different score calculation that does not include the Density metric. As a result, the risk scores generated by the dashboard are not calibrated to the same scale as the model's predictions, and the dashboard does not benefit from the machine learning validation applied to the Python pipeline.

2.5 Visualisation Output Files
The five PNG files – confusion_matrix.png, feature_importance.png, trigger_density.png, synergy_matrix.png, and synergy_co_occurrence.png – are generated by comprehensive_analysis.py and provide a visual summary of the model's performance and the relationships between bias indicators. These images are intended for inclusion in the research write‑up and for use in presentations. They are not used by any other component of the artefact.

2.6 Risk Mails.docx
This Word document contains the full research write‑up, including the abstract, introduction, literature review, methodology, results, discussion, and conclusions. It also includes several example email cases that illustrate how the BPRSM framework classifies different types of phishing and legitimate messages. The document serves as the primary reference for the theoretical and methodological foundations of the artefact.

3. How to Use the Artefact
3.1 Setting Up the Environment
The Python scripts require Python 3.8 or later. The following packages must be installed:

bash
pip install pandas numpy scikit-learn matplotlib seaborn
All other modules used (os, re, email, tarfile, json) are part of the Python standard library and do not require separate installation.

3.2 Preparing the Corpus
Before running either of the Python scripts, the SpamAssassin archive files must be extracted. Each .tar.bz2 file should be extracted into a folder with the same base name. For example:

bash
tar -xjf 20021010_easy_ham.tar.bz2
tar -xjf 20021010_hard_ham.tar.bz2
tar -xjf 20021010_spam.tar.bz2
# ... and so on for all nine archives
The extracted folders should be placed in the same directory as the Python scripts.

3.3 Running the Data Ingestion Script
To load the email data into a DataFrame:

bash
python process_emails.py
This will print the total number of emails loaded and return the DataFrame. However, as noted above, the script does not save the DataFrame to disk. To make use of this script in a pipeline, users would need to modify it to serialise the DataFrame (e.g., using df.to_pickle('email_data.pkl')).

3.4 Running the Comprehensive Analysis
To run the full analysis pipeline and generate the visualisation files:

bash
python comprehensive_analysis.py
The script will read from the extracted folders, compute features, train the Random Forest model, and produce the five PNG files. The classification report and ROC‑AUC score will be printed to the terminal.

3.5 Using the Dashboards
Both HTML dashboards are self‑contained and can be opened directly in any modern web browser. No web server is required. To use a dashboard:

Navigate to the repository folder in your file explorer.

Double‑click on either risk_dashboard old.html or new risk_dashboard.html.

Paste an email or any text into the text area.

Click the analysis button to generate the risk assessment.

The dashboards perform all analysis client‑side and do not send any data to external servers. They are suitable for testing individual email samples but do not provide batch processing capabilities.

4. Known Limitations and Discrepancies
4.1 Inconsistent Pipeline and Data Flow
The README describes a sequential pipeline where process_emails.py feeds data to comprehensive_analysis.py, and comprehensive_analysis.py produces dashboard_data.json for the dashboard. In the current implementation, this is not the case:

process_emails.py does not save any file to disk.

comprehensive_analysis.py does not load data from any file produced by process_emails.py; it reads directly from the extracted folders.

comprehensive_analysis.py does not generate dashboard_data.json.

Users should therefore treat the two Python scripts as independent demonstration scripts rather than as parts of a fully integrated pipeline.

4.2 Discrepant Scoring Logic
The research defines a BPRSM scoring formula in the write‑up:

text
Sfinal = Σ(hits × weight) + Wsynergy
where weights are Authority=4, Urgency=5, Fear=4, Elicitation=3, and Wsynergy=2.5 if both Authority and Urgency are present.

However, the actual implementations differ:

The Random Forest model in comprehensive_analysis.py does not use the weighted additive formula at all. It learns feature importances through the classification process, which are not directly comparable to the manually defined weights.

The old dashboard uses a base weight of 25 per hit, with a 1.4 multiplier for any co‑occurrence and an additional 1.2 multiplier for Authority‑Urgency synergy.

The new dashboard uses a base weight of 12 per hit, with a 25‑point bonus for Authority‑Urgency synergy and a 20‑point bonus for Linguistic Deception‑Urgency synergy.

These differences mean that the same email text can receive very different risk scores depending on which component of the artefact is used.

4.3 Keyword and Category Variations
The taxonomy categories and keyword lists also vary across components:

comprehensive_analysis.py uses four categories (Authority, Urgency, Fear, Elicitation) with regular expression patterns.

risk_dashboard old.html uses the same four category names but different keyword lists.

new risk_dashboard.html uses four different category names (Authority_Heuristic, Affective_Urgency, Trait_Exploitation, Linguistic_Deception) with yet another set of keywords.

These variations reflect the exploratory nature of the research and the evolution of the framework during development, but they also mean that the artefact does not provide a single, consistent implementation of the CBI Taxonomy.

4.4 Absence of Validation for Dashboard Scores
While the Random Forest model in comprehensive_analysis.py is validated against the SpamAssassin corpus (with reported accuracy of 0.90 and ROC‑AUC of 0.9269), the dashboards are not validated in the same way. The dashboard scores are based on hand‑coded heuristics rather than on the learned model, and their performance against ground truth labels has not been systematically evaluated.

5. Recommendations for Use
Given the limitations described above, users are advised to approach the artefact with the following considerations:

For replicating the quantitative results: Use comprehensive_analysis.py to reproduce the Random Forest evaluation. This script provides the most rigorous validation of the cognitive bias indicators and their predictive power.

For exploring the concept interactively: Use the new risk_dashboard.html dashboard. It offers a more polished user interface and richer forensic narratives, but its scores should be understood as illustrative rather than as validated predictions.

For understanding the theoretical framework: Read Risk Mails.docx, which provides the full research context, literature review, and methodological rationale.

For extending the work: Consider unifying the taxonomy and scoring logic across components. The TAXONOMY dictionary in comprehensive_analysis.py can be modified to include additional or alternative keywords. The dashboard scoring functions can also be updated to match the weighted formula defined in the research write‑up.

6. Contact and Citation
For questions about the artefact or the research, please contact:

Ibrahim Abdullahi Sheikh_25006888
Email: Shxaashi99@gmail.com
Institution: University of the West of England (UWE Bristol)

