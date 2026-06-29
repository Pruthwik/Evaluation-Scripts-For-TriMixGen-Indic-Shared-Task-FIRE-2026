"""
Evaluation Script for Token-Level Classification Tasks (CoNLL format)
Compatible with Codabench

This script calculates the Macro F1 score and writes it to a scores.json 
file using the exact column keys defined in the Codabench leaderboard UI.
"""
# How to run the code
# python3 evaluate_subtask_B.py
import os
import json
from sklearn.metrics import classification_report, f1_score


def read_conll_sentences(path):
    """Read a CoNLL-style file and return sentence-level language tags."""
    sentences = []
    curr_tags = []

    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip():
                if curr_tags:
                    sentences.append(curr_tags)
                    curr_tags = []
                continue

            parts = line.split("\t")
            tag = parts[1] if len(parts) >= 2 else ""
            curr_tags.append(tag)

    if curr_tags:
        sentences.append(curr_tags)

    return sentences


def evaluate_macro_f1(pred_file, true_file):
    pred_sentences = read_conll_sentences(pred_file)
    true_sentences = read_conll_sentences(true_file)

    # Verify sentence counts match
    if len(pred_sentences) != len(true_sentences):
        raise ValueError(
            f"Sentence count mismatch: predicted={len(pred_sentences)}, "
            f"ground-truth={len(true_sentences)}"
        )

    # Verify token counts match for each sentence
    for sent_id, (true_tags, pred_tags) in enumerate(zip(true_sentences, pred_sentences)):
        if len(true_tags) != len(pred_tags):
            raise ValueError(
                f"Token count mismatch for sentence {sent_id} "
                f"(true={len(true_tags)}, pred={len(pred_tags)})"
            )

    # Flatten all tags across all sentences
    y_true = [tag for sentence_tags in true_sentences for tag in sentence_tags]
    y_pred = [tag for sentence_tags in pred_sentences for tag in sentence_tags]

    # Calculate metrics
    macro_f1 = f1_score(y_true, y_pred, average="macro")
    
    print(f"\nPer-class metrics for current file:")
    print(classification_report(y_true, y_pred, digits=4))

    return macro_f1


def main():
    """Main function to evaluate predictions against ground truth and write scores to a JSON file."""
    input_dir = 'Input Directory Path'  # Update this path to your input directory
    output_dir = 'Output Directory Path'  # Update this path to your output directory
    # Save two folders in the input directory: 'res' for predicted labels and 'ref' for gold/reference labels
    submit_dir = os.path.join(input_dir, 'res') # Gold/Reference Labels
    truth_dir = os.path.join(input_dir, 'ref') # Predicted Labels

    # Mapping your Leaderboard "Column Keys" to the expected filenames
    # Update the values here if your files are named differently!
    TASKS = {
        'guj': 'eng-hin-guj.conll',  # Score for Macro F1 ENG-HIN-GUJ
        'ben': 'eng-hin-ben.conll'   # Score for Macro F1 ENG-HI-BEN
    }

    scores = {}

    for key, filename in TASKS.items():
        pred_file = os.path.join(submit_dir, filename)
        true_file = os.path.join(truth_dir, filename)

        if os.path.exists(pred_file) and os.path.exists(true_file):
            print(f"Evaluating {key} from {filename}...")
            # if there is an error in evaluation, the code will crash
            # which will result in Failed Submission rather than giving -1 score
            score = evaluate_macro_f1(pred_file, true_file)
            scores[key] = score
        else:
            print(f"Warning: Could not find files for {key} ({filename}).")
            scores[key] = -1

    # Write the results to scores.json for Codabench to parse
    score_file = os.path.join(output_dir, 'scores.json')
    with open(score_file, 'w') as f:
        json.dump(scores, f)
    
    print(f"\nFinal scores written to Codabench: {scores}")


if __name__ == "__main__":
    # Call the main function to execute the evaluation
    main()
