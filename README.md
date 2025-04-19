Hướng Dẫn Cấu Trúc Dự Án Python + ANTLR4

Đây là tài liệu hướng dẫn cho một dự án Python sử dụng ANTLR4, được thiết kế với cấu trúc chung, linh hoạt và dễ mở rộng. Dự án này phù hợp cho các ứng dụng như công cụ phân tích cú pháp, chatbot, hoặc hệ thống xử lý ngôn ngữ tự nhiên. Tài liệu bao gồm cách clone và thiết lập môi trường, cấu trúc thư mục dự án kèm bảng giải thích chi tiết, và cách chạy chương trình.

## Table of Contents
- [Cách Clone và Thiết Lập Môi Trường](#cach-clone-va-thiet-lap-moi-truong)
- [Cấu Trúc Dự Án](#cau-truc-du-an)
  - [Cây Thư Mục](#cay-thu-muc)
  - [Giải Thích Cấu Trúc](#giai-thich-cau-truc)
- [Cách Chạy](#cach-chay)

## Cách Clone và Thiết Lập Môi Trường
1. **Clone kho mã nguồn**
```bash
git clone <repo-url>
cd project_name
```
2. **Tạo và kích hoạt môi trường ảo**
```bash
python3 -m venv venv
```
- Trên Windows:
```bash
venv\Scripts\activate
```
- Trên Linux/macOS:
```bash
source venv/bin/activate
```
3. **Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```
4. **Đảm bảo Java đã được cài đặt**
```bash
java -version
```
5. **Tạo mã nguồn từ file ngữ pháp**
```bash
./scripts/generate_parser.sh
```
- Trên Windows:
```bash
bash scripts/generate_parser.sh
```
- Hoặc chạy trực tiếp:
```bash
java -jar lib/antlr-4.9.2-complete.jar -Dlanguage=Python3 -visitor -o src/generated src/grammar/Command.g4
```

## Cấu Trúc Dự Án
### Cây Thư Mục
```
project_name/
├── lib/
│   └── antlr-4.9.2-complete.jar
├── src/
│   ├── grammar/
│   │   └── Command.g4
│   ├── generated/
│   │   ├── CommandLexer.py
│   │   ├── CommandParser.py
│   │   ├── CommandListener.py
│   │   ├── CommandVisitor.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── processor.py
│   │   ├── models.py
│   │   └── utils.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   └── gui.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── schema.sql
│   └── tests/
│       ├── __init__.py
│       ├── test_parser.py
│       ├── test_processor.py
│       └── test_integration.py
├── config/
│   ├── settings.py
│   └── logging.conf
├── scripts/
│   ├── generate_parser.sh
│   └── setup_env.sh
├── docs/
│   ├── api.md
│   └── architecture.md
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

### Giải Thích Cấu Trúc
| Đường dẫn | Mô tả |
|-----------|-------|
| `lib/` | Chứa file JAR của ANTLR4 để tạo mã Python từ file ngữ pháp `.g4`. |
| `src/grammar/Command.g4` | Định nghĩa ngữ pháp của dự án sử dụng ANTLR4. |
| `src/generated/` | Chứa mã Python được tạo từ file ngữ pháp, không nên chỉnh sửa thủ công. |
| `src/core/` | Gồm parser, processor và các logic xử lý trung tâm. |
| `src/interfaces/` | Giao diện CLI và GUI (GUI chưa triển khai). |
| `src/storage/` | Xử lý lưu trữ bằng SQLite và schema cơ sở dữ liệu. |
| `src/tests/` | Chứa các unit test và integration test sử dụng `pytest`. |
| `config/` | Chứa cấu hình settings và logging. |
| `scripts/` | Script tiện ích cho việc setup và tạo parser. |
| `docs/` | Tài liệu mô tả API và kiến trúc (đặt chỗ). |
| `requirements.txt` | Danh sách thư viện yêu cầu. |
| `README.md` | Tài liệu hướng dẫn chính. |
| `LICENSE` | Giấy phép sử dụng mã nguồn. |
| `.gitignore` | Loại trừ các file không cần thiết cho git. |

## Cách Chạy
1. **Thiết lập môi trường**: Làm theo phần "Cách Clone và Thiết Lập Môi Trường"
2. **Chạy giao diện CLI**
```bash
python -m src.interfaces.cli
```
- Trên Windows (nếu lỗi):
```bash
set PYTHONPATH=%PYTHONPATH%;%CD%
python src/interfaces/cli.py
```
3. **Tương tác**: Nhập các lệnh theo ngữ pháp (ví dụ: `đặt lịch hẹn vào thứ Hai lúc 10 giờ sáng`).
4. **Chạy kiểm tra**:
```bash
pytest src/tests/
```

## Ghi Chú
- Đảm bảo các thư mục đều có file `__init__.py`
- ANTLR4 cần Java để chạy
- Tạo parser với `-visitor` để sinh `CommandVisitor.py`
- `cli.py` là giao diện chính hiện tại
- Các thành phần khác như GUI, cấu hình, tài liệu chi tiết vẫn là chỗ đặt chỗ cho mở rộng

