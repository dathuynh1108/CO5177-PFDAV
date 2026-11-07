# Khai báo sử dụng AI

**Nhóm** CTG

**Thành viên** Huỳnh Thành Đạt (2570161), Lương Minh Duy (2570083)

**Học phần** CO5177 · Học kỳ 261

AI được sử dụng để tra cứu tài liệu và API của scikit-learn, PyTorch, torchvision và Transformers, hỗ trợ hiện thực và kiểm tra mã, đối chiếu số liệu, biên tập báo cáo và notebook.

| Bài | Nội dung có hỗ trợ |
| --- | --- |
| Tabular | Hỗ trợ hiện thực xử lý dữ liệu thiếu, mã hóa, chuẩn hóa, chia tập, khảo sát phân bố và IQR trên train, so sánh bốn bộ phân loại trên toàn bộ 48.780 dòng hợp lệ. Đối chiếu chỉ số và phân tích đánh đổi giữa precision và recall. |
| Text | Hỗ trợ hiện thực và kiểm tra tiền xử lý, nhóm các đầu vào token trùng nhau trước khi chia tập, fine-tuning PhoBERT đủ bảy epoch trên 207.375 bài hợp lệ, bốn đối chứng tiêu đề và hiệu chỉnh bằng validation. Hỗ trợ thực thi notebook, đối chiếu dự đoán, ma trận nhầm lẫn và số liệu báo cáo. Bộ VietnamNet News được công bố trên tài khoản Hugging Face của học viên Huỳnh Thành Đạt; thông tin này không xác định người thu thập bài báo. |
| Image | Hỗ trợ sử dụng API trọng số tiền huấn luyện, kiểm tra ảnh trùng pixel, hiện thực và thực thi 18 lượt huấn luyện đủ 20 epoch trên RTX 5090, kiểm tra checkpoint và đối chiếu chỉ số với dự đoán test. Notebook thực thi có 21 cell mã và sáu hình PNG; kết quả được lưu riêng với hồ sơ A1 CO5085. |
| Trình bày | Hỗ trợ chuyển phần trình bày notebook hiện tại sang tiếng Anh, chia cell, biên tập Markdown, LaTeX, PDF và nội dung GitHub Pages. Phần phân công do nhóm cung cấp. |

Bảng và hình sử dụng số liệu từ các lượt thực nghiệm có lưu cấu hình, lịch sử và đầu ra Jupyter. Hai thí nghiệm Text hiện tại dùng chung split 145.162/31.107/31.106; nhóm đầu vào token được giữ trong cùng một tập. Lượt toàn văn Kaggle bảy epoch trước đó được lưu nguyên byte riêng vì dùng chung tập đánh giá để chọn checkpoint và hiệu chỉnh. Các kiểm tra hiện có không xác nhận thay cho Run all trên Google Colab hoặc việc nộp bài trên LMS.

## Tài liệu đối chiếu

- [UCI Adult](https://archive.ics.uci.edu/dataset/2/adult), [VietnamNet News](https://huggingface.co/datasets/dathuynh1108/vietnamnet-news) và [CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html)
- [Tài liệu scikit-learn](https://scikit-learn.org/stable/), [PyTorch](https://docs.pytorch.org/docs/stable/), [torchvision](https://docs.pytorch.org/vision/stable/models.html) và [PhoBERT](https://huggingface.co/vinai/phobert-base-v2)
- [Nguồn thí nghiệm Image](docs/IMAGE_REUSE.md) và [nguồn thí nghiệm PhoBERT toàn văn](docs/TEXT_REUSE.md)
