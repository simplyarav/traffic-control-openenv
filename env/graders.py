def grade(avg_queue):
    score = 1 - (avg_queue / 25)
    return max(0.0, min(1.0, score))