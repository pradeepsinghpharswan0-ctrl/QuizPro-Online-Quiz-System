#include <stdio.h>

__declspec(dllexport) int calculate_score(int answers[], int correct[], int n) {
    int score = 0;

    for (int i = 0; i < n; i++) {
        if (answers[i] == correct[i]) {
            score++;
        }
    }

    return score;
}