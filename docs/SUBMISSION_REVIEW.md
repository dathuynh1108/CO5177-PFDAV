# Đối chiếu bài nộp CO5177

Căn cứ theo đề v4.0 ngày 14/09/2026, mục 3–7. Nhóm CTG có hai thành viên, mỗi người đóng góp 50% theo thông tin nhóm cung cấp. Khối lượng yêu cầu gồm Tabular, Text và một bài tự chọn. CTG chọn Image.

| Tiêu chí | Bằng chứng và trạng thái |
| --- | --- |
| Tabular | UCI Adult có 48.842 bản ghi nguồn, 14 thuộc tính, dữ liệu thiếu và cả biến số lẫn biến phân loại. Thí nghiệm gồm điền thiếu, mã hóa, chuẩn hóa, chia ba tập và so sánh bốn mô hình. [Notebook](../notebooks/tabular.ipynb) · [PDF](../reports/tabular/tabular.pdf). |
| Text | Bộ VietnamNet do nhóm thu thập có 212.705 bài. Thí nghiệm trên 7.600 tiêu đề so sánh TF-IDF với đặc trưng PhoBERT và có ba tập riêng. Notebook PhoBERT toàn văn là bằng chứng của lần chạy Kaggle, với tập đánh giá kiêm chọn checkpoint và hiệu chỉnh. [Notebook tiêu đề](../notebooks/text_baselines.ipynb) · [Notebook toàn văn](../notebooks/text.ipynb) · [PDF](../reports/text/text.pdf). |
| Image | CIFAR-100 có 60.000 ảnh, 100 lớp và sáu cấu hình tiền huấn luyện. Báo cáo giải thích đầu vào 96 px thấp hơn mức khuyến nghị 128 px. Hai ảnh xác thực và mười ảnh kiểm tra trùng pixel với tập huấn luyện trong lượt chạy gốc. Có kiểm tra độ nhạy trên 9.990 dự đoán kiểm tra. [Notebook](../notebooks/image.ipynb) · [PDF](../reports/image/image.pdf). |
| Notebook | Tabular, Image và Text tiêu đề đã chạy hết các ô trong bản sao cục bộ. Colab mới chưa được xác nhận. Image tính lại kết quả từ dự đoán đã lưu. Mã huấn luyện Image nằm riêng ngoài notebook, nên Run all của notebook chỉ kiểm chứng phần phân tích và đánh giá. Text toàn văn giữ đầu ra gốc và chưa chạy lại. |
| Hình hoặc bảng so sánh | Tabular đối chiếu precision và recall khi cân bằng lớp. Text so sánh ba biểu diễn trên cùng tập tiêu đề và phân tích thay đổi F1 theo lớp sau hiệu chỉnh toàn văn. Image so sánh độ chính xác, thời gian và bộ nhớ giữa các mức tinh chỉnh. |
| Website | Có trang chủ và ba trang bài con với liên kết đến notebook và PDF. Bản rà soát bổ sung thông tin CTG, tỷ lệ đóng góp và khai báo AI. |
| PDF tổng hợp | Có [CTG-report.pdf](../reports/overview/CTG-report.pdf). Trạng thái nộp trên LMS chưa được xác nhận. |
| YouTube | Ba trường liên kết để trống theo thông tin nhóm cung cấp. Đề yêu cầu mỗi bài có video Public hoặc Unlisted. |
| GroupLink | Tệp đăng ký yêu cầu đăng nhập khi kiểm tra. Trạng thái ghi link và hạn nộp theo LMS chưa được xác nhận. |
