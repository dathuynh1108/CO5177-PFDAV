# Đối chiếu bài nộp CO5177

Căn cứ đề v4.0 ngày 14/09/2026, mục 3–7. Nhóm CTG gồm Huỳnh Thành Đạt (2570161) và Lương Minh Duy (2570083), mỗi người đóng góp 50% theo thông tin nhóm cung cấp. Nhóm thực hiện Tabular, Text và bài tự chọn Image.

Notebook Colab **Run all** là quy trình chính để tái lập từng nghiên cứu. Mỗi notebook trình bày dữ liệu, cấu hình và seed, các bước huấn luyện/chọn mô hình, kết quả định lượng và biểu đồ. Chỉ xem Colab là đã xác minh sau khi chạy hết notebook trong runtime mới; bằng chứng thực thi hiện có được tách rõ dưới đây.

| Tiêu chí | Bằng chứng và trạng thái |
| --- | --- |
| Tabular | UCI Adult có 48.842 dòng và 14 thuộc tính, bao gồm dữ liệu thiếu, biến số và biến phân loại. Notebook xử lý thiếu, mã hóa, chuẩn hóa, chia train/validation/test và fit bốn mô hình. Chạy cục bộ mới đã hoàn tất: 34.146/7.317/7.317 mẫu; histogram gradient boosting đạt accuracy 87,4812% và macro-F1 0,818526. [Notebook](../notebooks/tabular.ipynb) · [Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/tabular.ipynb) · [PDF](../reports/tabular/tabular.pdf). |
| Text · toàn bài | 7.600 bài VietnamNet được phân loại bằng PhoBERT fine-tuning với split phân tầng chung 5.320/1.140/1.140. Từ tập kiểm tra, accuracy là 0,837719 và macro-F1 là 0,835296; hiệu chỉnh tham số trên validation cho kết quả accuracy 0,832456 và macro-F1 0,829602 trên cùng test. Lượt chạy mới thực hiện trên RTX 5090. Dữ liệu được Huỳnh Thành Đạt thu thập từ URL công khai của VietnamNet và công bố tại [VietnamNet News](https://huggingface.co/datasets/dathuynh1108/vietnamnet-news); trạng thái giấy phép nội dung bài báo chưa được nêu trong thẻ dữ liệu. [Notebook](../notebooks/text.ipynb) · [Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/text.ipynb). |
| Text · baseline tiêu đề | Cohort 7.600 tiêu đề, TF-IDF từ/ký tự và PhoBERT đóng băng, dùng cùng split 5.320/1.140/1.140. Chạy cục bộ mới đã hoàn tất; PhoBERT + logistic regression đạt accuracy 0,775439 và macro-F1 0,773780. Đây là thí nghiệm riêng, không gộp với kết quả fine-tuning toàn bài. [Notebook](../notebooks/text_baselines.ipynb) · [Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/text_baselines.ipynb) · [PDF baseline](../reports/text/baselines.pdf). |
| Text · lưu trữ lịch sử | Notebook Kaggle/Tesla T4 và đầu ra cũ được giữ nguyên riêng tại [text_historical.ipynb](../notebooks/text_historical.ipynb), cùng hồ sơ nguồn và giới hạn trong [TEXT_REUSE.md](TEXT_REUSE.md). Số liệu lưu trữ không phải phép đo mới của notebook hiện tại. |
| Image | CIFAR-100, sáu cấu hình pretrained × ba seed, 20 epoch; ảnh trùng pixel được loại sau khi chia phân tầng, ưu tiên giữ tập kiểm tra. Đã hoàn tất 18 lượt trên RTX 5090. Sau đối chiếu pixel, ba tập có 44.976/5.000/9.998 ảnh. Swin-T tinh chỉnh toàn bộ đạt 86,81% accuracy và 0,8681 macro-F1. [Notebook](../notebooks/image.ipynb) · [Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb) · [PDF](../reports/image/image.pdf) · [Nhật ký và kết quả](../reports/image/notebook-evidence/summary.json). |
| Notebook và Colab | Tabular và baseline tiêu đề đã chạy hết từ kernel cục bộ mới, có lưu seed, cấu hình, nhật ký fit, metrics, dự đoán, mô hình và biểu đồ vào thư mục output mới. Text toàn bài và Image đã chạy từ đầu đến cuối bằng kernel Jupyter mới trên RTX 5090. Chưa xác nhận Run all trên Google Colab cho các notebook. |
| Báo cáo và landing page | Có PDF riêng và landing page cho ba bài. Các trang bài dẫn đến notebook và PDF. Báo cáo Text, Image và PDF tổng hợp dùng kết quả của các lượt notebook mới. [Landing page](https://dathuynh1108.github.io/CO5177-PFDAV/) · [PDF tổng hợp](../reports/overview/CTG-report.pdf). |
| Video YouTube | Cả ba trường liên kết đang để trống theo chỉ dẫn; đề yêu cầu video cho từng bài ở chế độ Public hoặc Unlisted. Cần thêm và kiểm tra ba liên kết trước khi nộp. |
| GroupLink và LMS | Nhóm CTG và tỷ lệ đóng góp 50/50 đã được xác nhận, nhưng chưa xác minh được sheet GroupLink và trạng thái nộp PDF tổng hợp trên LMS. Cần kiểm tra đường dẫn landing page, tên nhóm và trạng thái nộp trên hệ thống môn học. |

## Các hạng mục còn thiếu hoặc cần cập nhật

- Bổ sung ba video trình bày và kiểm tra quyền xem Public/Unlisted.
- Xác minh GroupLink, tên nhóm trên biểu mẫu đăng ký và trạng thái gửi PDF tổng hợp lên LMS.
- Chạy thử Run all trong Google Colab mới; kiểm tra thiết bị, tải dữ liệu/mô hình và toàn bộ output trước khi coi đường dẫn Colab là đã xác minh.

Các phép đo Tabular/Text baseline cục bộ và lượt Text RTX 5090 không xác nhận thay cho các mục còn thiếu ở trên.
