# Khai báo sử dụng AI

**Nhóm** CTG

**Thành viên** Huỳnh Thành Đạt (2570161), Lương Minh Duy (2570083)

**Học phần** CO5177 · Học kỳ 261

AI được sử dụng để tra cứu tài liệu và API của scikit-learn, PyTorch, torchvision và Transformers, hỗ trợ hiện thực và kiểm tra mã, đối chiếu số liệu, biên tập báo cáo và notebook.

| Bài | Nội dung có hỗ trợ |
| --- | --- |
| Tabular | Hỗ trợ xây dựng quy trình xử lý dữ liệu thiếu, mã hóa và chuẩn hóa thuộc tính, chia tập và so sánh các bộ phân loại trên UCI Adult. Đối chiếu chỉ số và phân tích sự đánh đổi giữa precision và recall. |
| Text | Hỗ trợ hiện thực thí nghiệm đối chứng trên tiêu đề bằng TF-IDF và PhoBERT đóng băng. Với thí nghiệm toàn văn đã có, AI hỗ trợ đối chiếu notebook và kết quả huấn luyện, kiểm tra chỉ số từ ma trận nhầm lẫn và biên tập phần phân tích hiệu chỉnh. Bộ dữ liệu VietnamNet do nhóm thu thập. |
| Image | Hỗ trợ chuyển mã và kết quả CIFAR-100 từ A1 của CO5085, tra cứu API trọng số tiền huấn luyện và phân tích đường cong, lỗi phân loại và ảnh trùng. Các số liệu chính thuộc cùng 24 lượt thực nghiệm của CO5085. |
| Trình bày | Hỗ trợ biên tập Markdown, LaTeX, PDF và nội dung GitHub Pages. Phần phân công do nhóm cung cấp. |

Bảng và hình sử dụng số liệu từ các lượt chạy có lưu kết quả. Thí nghiệm tiêu đề có tập kiểm tra riêng. Lượt PhoBERT toàn văn dùng chung tập đánh giá cho chọn checkpoint và hiệu chỉnh, nên báo cáo ghi riêng phạm vi của các chỉ số này.

## Tài liệu đối chiếu

- [UCI Adult](https://archive.ics.uci.edu/dataset/2/adult), [VietnamNet News](https://huggingface.co/datasets/dathuynh1108/vietnamnet-news) và [CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html)
- [Tài liệu scikit-learn](https://scikit-learn.org/stable/), [PyTorch](https://docs.pytorch.org/docs/stable/), [torchvision](https://docs.pytorch.org/vision/stable/models.html) và [PhoBERT](https://huggingface.co/vinai/phobert-base-v2)
- [Nguồn thí nghiệm Image](docs/IMAGE_REUSE.md) và [nguồn thí nghiệm PhoBERT toàn văn](docs/TEXT_REUSE.md)
