# Đối chiếu bài nộp CO5177

Căn cứ đề v4.0 ngày 14/09/2026, mục 3–7. Nhóm CTG gồm Huỳnh Thành Đạt (2570161) và Lương Minh Duy (2570083), mỗi người đóng góp 50% theo thông tin nhóm cung cấp. Nhóm thực hiện Tabular, Text và bài tự chọn Image.

Notebook là điểm truy cập thực nghiệm từ landing page. Các notebook hiện tại có phần trình bày tiếng Anh và đầu ra Jupyter thực tế; báo cáo viết bằng tiếng Việt. Bằng chứng thực thi hiện có được phân biệt với việc chạy lại trên Google Colab và nộp bài bên ngoài kho mã.

| Tiêu chí | Bằng chứng và trạng thái |
| --- | --- |
| Tabular | Dùng toàn bộ 48.780 dòng UCI Adult sau làm sạch, 14 thuộc tính, dữ liệu thiếu và biến số/phân loại. Chia 34.146/7.317/7.317 mẫu; EDA số và IQR chỉ trên train; fit bốn mô hình. Histogram gradient boosting đạt accuracy 87,4812% và macro-F1 0,818526. [Notebook](../notebooks/tabular.ipynb) · [PDF](../reports/tabular/tabular.pdf). |
| Text · toàn bài | Dùng toàn bộ 207.375 bài hợp lệ từ 212.705 dòng nguồn. Nhóm các đầu vào token tiêu đề hoặc Head–Tail trùng nhau thành 207.108 nhóm, không loại thêm dòng; split 145.162/31.107/31.106 bằng 20-fold StratifiedGroupKFold, seed 2026, phân bổ 14/3/3 fold. Chạy đủ bảy epoch trên RTX 5090, effective batch 64, chọn epoch 7 bằng validation. Sau hiệu chỉnh trên validation, test đạt accuracy 91,892239% và macro-F1 0,911448. Nguồn là [VietnamNet News](https://huggingface.co/datasets/dathuynh1108/vietnamnet-news), công bố trên tài khoản Hugging Face của học viên Huỳnh Thành Đạt. [Notebook](../notebooks/text.ipynb) · [Metrics](../reports/text/notebook-evidence/metrics.json) · [PDF](../reports/text/text.pdf). |
| Text · baseline tiêu đề | Bốn bộ phân loại được fit mới trên CPU với toàn bộ 207.375 tiêu đề, dùng cùng ID và split với toàn bài; đặc trưng PhoBERT đóng băng dùng cache đã kiểm tra từ lượt mã hóa trên RTX 5090. PhoBERT đóng băng + logistic regression đạt accuracy 80,981161% và macro-F1 0,794315; TF-IDF từ/ký tự đạt 80,190317%/80,251398%. Đầu vào khác nhau nên so sánh không xác định riêng ảnh hưởng của fine-tuning. [Notebook](../notebooks/text_baselines.ipynb) · [PDF baseline](../reports/text/baselines.pdf). |
| Text · lưu trữ lịch sử | [Notebook Kaggle/Tesla T4 bảy epoch](../notebooks/text_historical.ipynb) giữ nguyên byte và đầu ra cũ. Lượt cũ dùng chung tập đánh giá cho chọn checkpoint và hiệu chỉnh; không phải test độc lập hay kết quả hiện tại. [Nguồn và giới hạn](TEXT_REUSE.md). |
| Image | Sáu cấu hình pretrained × ba seed, mỗi lượt đủ 20 epoch trên RTX 5090; sau loại trùng pixel có 44.976/5.000/9.998 ảnh. Hoàn tất 18 lượt; notebook có 21 cell mã, sáu PNG và không có đầu ra lỗi. Swin-T full đạt trung bình accuracy 86,81% và macro-F1 0,8681. [Notebook](../notebooks/image.ipynb) · [PDF](../reports/image/image.pdf) · [Biên nhận thực thi](../reports/image/notebook-evidence/execution-receipt.json). |
| Google Colab | Có liên kết Colab cho notebook; chưa xác minh Run all trong một runtime Google Colab mới. Thực thi Jupyter cục bộ hoặc trên RTX 5090 không thay thế bước này. |
| Báo cáo và landing page | Có PDF riêng và các trang bài con. Landing page dùng notebook làm điểm truy cập; báo cáo và evidence được liên kết ở trang bài tương ứng. [Landing page](https://dathuynh1108.github.io/CO5177-PFDAV/) · [PDF tổng hợp](../reports/overview/CTG-report.pdf). |
| Video YouTube | Cả ba trường liên kết để trống theo lựa chọn của người dùng. Đề yêu cầu video Public hoặc Unlisted cho từng bài; chưa có bằng chứng đáp ứng mục này. |
| GroupLink và LMS | Chưa xác minh sheet GroupLink hoặc trạng thái nộp PDF tổng hợp trên LMS. |

Các mục chưa xác minh gồm ba video, Run all trên Google Colab mới, GroupLink và việc gửi PDF tổng hợp lên LMS. Các lượt huấn luyện và kiểm tra trong kho mã không xác nhận thay cho các mục này.
