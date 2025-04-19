# PPL-Project

A simple Python + ANTLR4 project to parse natural language commands for scheduling.

## Installation
1. Clone the repository: `git clone <repo-url>`
2. Create virtual environment: `python3 -m venv venv`
3. Activate environment: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. Install dependencies: `pip install -r requirements.txt`
5. Generate parser: `./scripts/generate_parser.sh`

**Note**: The ANTLR4 JAR file is included in `lib/antlr-4.9.2-complete.jar`. Ensure Java is installed (`java -version`) to run the parser generation script.

## Usage
Run: `python src/interfaces/cli.py`
Enter commands like:
- `đặt lịch hẹn vào thứ Hai lúc 10 giờ sáng`
- `hủy lịch hẹn vào thứ Ba`
Type `thoát` to exit.