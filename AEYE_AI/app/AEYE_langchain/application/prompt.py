preprocess_pdf_prompt = """
You are an expert academic researcher skilled at parsing document information.
Your task is to extract the main category and keywords from the text of the first page of a research paper provided below.

Follow these rules carefully:
1. categorize the given document text into a single word. 
2. Extract keywords that describes the given document text well. There should be five keywords.
3. Format your response as a valid JSON object with two keys: "category" and "keywords".
4. The value for "category" must be a string and lowercase.
5. The value for "keywords" must be a list of strings and lowercase.
6. Do NOT add any introductory text, explanations, or markdown formatting like ```json. Your response must be ONLY the raw JSON object.

## JSON Output Format
{{
"category": "<Your generated concise category>",
"keywords": "<Your generated concise keywords>",
}}

---
DOCUMENT TEXT:
{abstract}
---

JSON OUTPUT:
"""

name_prompt = """
You are an expert academic researcher with a talent for abstraction and distillation.
Your task is to create a concise, alternative title for a research paper by analyzing its original title and abstract. The new title must capture the core subject and contribution of the paper.

## Rules
1.  Read the provided TITLE and ABSTRACT to understand the paper's main theme.
2.  Generate a new, shorter title that is clear, descriptive, and easy to understand.
3.  Your output MUST be a single, raw JSON object. Do NOT include any explanations, introductory text, or markdown formatting like ```json.

## JSON Output Format
{{
"title": "<Your generated concise title>"
}}

## Example
---
### INPUT:
- **TITLE**: "An Attention-Based Bidirectional Long Short-Term Memory Network with a Convolutional Neural Network for Sentence-Level Text Classification"
- **ABSTRACT**: "This paper proposes a novel deep learning model for sentence-level text classification. We combine a Convolutional Neural Network (CNN) to extract local features from words with a Bidirectional Long Short-Term Memory (Bi-LSTM) network to capture long-range dependencies. Furthermore, we introduce an attention mechanism that allows the model to focus on the most relevant parts of the sentence when making a prediction. Our experiments on several benchmark datasets show that the proposed model significantly outperforms previous state-of-the-art methods in accuracy and F1 score."

### EXPECTED JSON OUTPUT:
{{
"title": "Attention-based Bi-LSTM with CNN for Text Classification"
}}
---

## Your Task
---
### INPUT:
- **TITLE**: "{title}"
- **ABSTRACT**: "{abstract}"

### JSON OUTPUT:
"""