# CO5177 · PFDAV

Website bài tập lớn học phần **Nền tảng lập trình cho phân tích và trực quan dữ liệu**.

**[Truy cập website](https://dathuynh1108.github.io/CO5177-PFDAV/)**

## Thông tin học phần

| Nội dung | Thông tin |
| --- | --- |
| Trường | Đại học Bách Khoa – ĐHQG-HCM |
| Khoa | Khoa Khoa học và Kỹ thuật Máy tính |
| Mã học phần | CO5177 |
| Giảng viên | Lê Thành Sách |
| Học kỳ | 261 · Năm học 2026–2027 |

## Thành viên

| MSSV | Họ và tên |
| --- | --- |
| 2570161 | Huỳnh Thành Đạt |
| 2570083 | Lương Minh Duy |

## Các bài tập lớn

| Bài | Loại dữ liệu | Hình thức | Nội dung |
| --- | --- | --- | --- |
| 01 | Tabular | Bắt buộc | Khám phá, tiền xử lý và mô hình hóa dữ liệu bảng. |
| 02 | Text | Bắt buộc | Xử lý văn bản, biểu diễn đặc trưng và phân tích dữ liệu ngôn ngữ. |
| 03 | Image | Tự chọn | Khám phá dữ liệu ảnh, trích xuất đặc trưng và đánh giá mô hình. |

Website hiện giới thiệu học phần, thành viên và yêu cầu của ba bài tập. Tập dữ liệu cụ thể, notebook, báo cáo và video sẽ được bổ sung trong quá trình thực hiện.

## Công nghệ

HTML5, CSS3 và JavaScript thuần. Website tĩnh, không cần backend hoặc bước build; triển khai bằng GitHub Pages.

## Cấu trúc thư mục

```text
.
├── index.html                # Trang giới thiệu
├── requirements.html         # Yêu cầu bài tập lớn
├── assignments/
│   ├── tabular.html          # Bài 01 · Tabular
│   ├── text.html             # Bài 02 · Text
│   └── image.html            # Bài 03 · Image
├── assets/
│   ├── styles.css            # Giao diện và responsive
│   ├── site-config.js        # Thông tin nhóm và liên kết tài liệu
│   ├── app.js                # Điều hướng và tương tác
│   └── favicon.svg
└── .nojekyll
```

## Chạy cục bộ

```bash
git clone https://github.com/dathuynh1108/CO5177-PFDAV.git
cd CO5177-PFDAV
python3 -m http.server 8000
```

Mở `http://localhost:8000` trên trình duyệt.

## Triển khai

Trong **Settings → Pages**, cấu hình:

```text
Source: Deploy from a branch
Branch: main
Folder: / (root)
```

GitHub Pages xuất bản website từ nhánh `main`. Các đường dẫn tài nguyên sử dụng dạng tương đối để hoạt động tại `/CO5177-PFDAV/`.

## Cập nhật nội dung

- Chỉnh thông tin nhóm, phân công và liên kết tài liệu trong `assets/site-config.js`.
- Chỉnh nội dung giới thiệu và yêu cầu tại các trang HTML tương ứng.
- Liên kết notebook, báo cáo PDF và video từ trang của từng bài tập khi tài liệu sẵn sàng.
- Để trống các trường chưa có tài liệu; website hiển thị trạng thái chờ cập nhật.

## Yêu cầu học phần

Nội dung yêu cầu được tổng hợp từ **Đề bài bài tập lớn v4.0, ngày 14/09/2026**. Thông báo và thời hạn chính thức theo LMS của học phần.
