# CO5177 · PFDAV

Landing page giới thiệu bài tập lớn môn **Nền tảng lập trình cho phân tích và trực quan dữ liệu**. HTML/CSS/JavaScript thuần, không cần npm hoặc build.

- Huỳnh Thành Đạt — **2570161**
- Lương Minh Duy — **2570083**

Ba bài đã chọn: **Tabular** (bắt buộc), **Text** (bắt buộc), **Image** (tự chọn).

## GitHub Pages

Website: https://dathuynh1108.github.io/CO5177-PFDAV/

Trong repo: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: main → /(root) → Save**.

Không cần custom domain, Jekyll, backend hay token. Đường dẫn tài nguyên nội bộ là đường dẫn tương đối, tương thích project site `/CO5177-PFDAV/`.

Tài liệu GitHub: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Chạy tại máy

Mở `index.html` trực tiếp, hoặc chạy từ thư mục dự án:

```bash
python3 -m http.server 8000
```

Truy cập `http://localhost:8000`.

## Cấu trúc

```text
index.html                  # Landing page
requirements.html           # Tóm lược đề bài v4.0
assignments/
  tabular.html              # Bài 01
  text.html                 # Bài 02
  image.html                # Bài 03
assets/
  styles.css                # Design tokens, responsive, print
  site-config.js            # Tên nhóm, phân công, link tài liệu
  app.js                    # Menu mobile, điều hướng, liên kết
  favicon.svg
.nojekyll
```

## Cập nhật nội dung

Chỉnh `assets/site-config.js` để thêm tên nhóm đã đăng ký, phân công, GitHub của Duy, dataset, notebook, báo cáo và video. Để trống các trường chưa có dữ liệu; website hiện “Sẽ cập nhật” thay vì tạo liên kết giả.

Link ngoài dùng URL HTTPS đầy đủ. Link nội bộ dùng đường dẫn tương đối như `reports/tabular.pdf`, không bắt đầu bằng `/`. Không đưa token hoặc thông tin bí mật vào file cấu hình công khai.

Các tiêu đề và mô tả chính nằm trong HTML: trang vẫn có nội dung và điều hướng khi tắt JavaScript. Khi chốt nội dung, cập nhật phần HTML tương ứng để giữ trạng thái no-JS đồng bộ với cấu hình.

## Thiết kế

Editorial hiện đại: nền giấy sáng, xanh rừng, cam đất; Manrope và Lora từ Google Fonts. Có font hệ thống dự phòng khi offline, không đính kèm font. Hỗ trợ menu mobile, bàn phím, Escape, skip link, reduced motion và kiểu in. Không có analytics, cookie, ảnh thành viên giả, metric giả hoặc link tài liệu giả.

## Nguồn

Yêu cầu dựa trên `assignment-vne-v4.pdf` người dùng cung cấp: v4.0 ngày 14/09/2026, học kỳ 261. `requirements.html` là bản tóm lược, không thay thế đề bài gốc hoặc cập nhật trên LMS.

Trang tham khảo do người dùng cung cấp: https://cuong111111.github.io/PF4DS — công cụ không truy cập được trang trong lần thực hiện, nên nội dung dựa trên PDF và giao diện được thiết kế mới.
