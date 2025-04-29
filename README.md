# Chess AI Agent

A Python-based Chess AI Agent implementing both Minimax and Alpha-Beta Pruning algorithms. The agent can play games, record gameplay videos, and log moves for later analysis.

## Features

- Play chess using Minimax or Alpha-Beta Pruning algorithms.
- Record games as MP4 videos.
- Log all moves in text files for review.

## Installation

1. **Clone the repository:**
   ```bash
    git clone https://github.com/i-apex/Chess_AI_Agent.git
    cd Chess_AI_Agent
   ```


3. **Install dependencies:**
   ```bash
    pip install -r requirements.txt
   ```

## Usage

### Minimax Algorithm

1. **Run the Minimax AI:**
   ```bash
   python Minimax.py
   ```
3. **Record the game:**
   ```bash
   python record.py
   ```


- The recorded video will be saved as `output_video.mp4`.
- The move log will be saved as `game_log.txt`.

### Alpha-Beta Pruning Algorithm

1. **Run the Alpha-Beta Pruning AI:**
   ```bash
   python alpha_beta_pruning.py
   ```

3. **Record the game:**
   ```bash
   python record_ab.py
   ```

- The recorded video will be saved as `output_video_ab.mp4`.
- The move log will be saved as `ab_game_log.txt`.

## Output Files

| Algorithm      | Video Output          | Move Log           |
| -------------- | -------------------- | ------------------ |
| Minimax        | output_video.mp4      | game_log.txt       |
| Alpha-Beta     | output_video_ab.mp4   | ab_game_log.txt    |

## Notes

- Ensure all dependencies are installed as specified in `requirements.txt`.
- The scripts must be run in the order shown above for each algorithm to generate the correct outputs.

## License

This project is licensed under the MIT License.

---
