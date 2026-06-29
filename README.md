- This GitHub repository consists of the evaluation scripts for both subtask A and subtask B of the `Code-Mixed Text Generation and Identification in Low-Resource Indian Languages (TriMixGen-Indic)` shared task in FIRE 2026.
- There are two separate evaluation scripts for each subtask, which can be found in the respective directories: `Evaluation_Scripts/Subtask-A` and `Evaluation_Scripts/Subtask-B`.
- The first script, `evaluate_subtask_A.py`, is used to score the code mixed sentences for subtask A, while the second script, `evaluate_subtask_B.py`, is used to evaluate the predictions for subtask B.
- The scoring for subtask A uses multiple transformer models and multiple evaluation metrics. The submissions for subtask A will take upto 24 hours to get reflected on the codabench leaderboard. The scoring for subtask B uses the macro F1-score metric and the submissions will be reflected on the codabench leaderboard instantly.
- How to run the evaluation scripts:
  - For subtask A, run the following command:
    ```
    python3 evaluate_subtask_A.py
    ```
  - For subtask B, run the following command:
    ```
    python3 evaluate_subtask_B.py
    ```
