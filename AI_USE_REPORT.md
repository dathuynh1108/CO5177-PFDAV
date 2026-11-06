# Khai báo sử dụng AI

**Nhóm** CTG

**Thành viên** Huỳnh Thành Đạt (2570161), Lương Minh Duy (2570083)

**Học phần** CO5177 · Học kỳ 261

AI được sử dụng để tra cứu tài liệu và API của scikit-learn, PyTorch, torchvision và Transformers, hỗ trợ hiện thực và kiểm tra mã, đối chiếu số liệu, biên tập báo cáo và notebook.

| Bài | Nội dung có hỗ trợ |
| --- | --- |
| Tabular | Hỗ trợ xây dựng quy trình xử lý dữ liệu thiếu, mã hóa và chuẩn hóa thuộc tính, chia tập và so sánh các bộ phân loại trên UCI Adult. Đối chiếu chỉ số và phân tích sự đánh đổi giữa precision và recall. |
| Text | Hỗ trợ tra cứu API PhoBERT, chuẩn bị đối chứng TF-IDF và embedding, tách tập xác thực và tập kiểm tra, đối chiếu ma trận nhầm lẫn và phân tích hiệu chỉnh. Dữ liệu được Huỳnh Thành Đạt thu thập bằng crawling từ URL công khai của VietnamNet. |
| Image | Hỗ trợ sử dụng API trọng số tiền huấn luyện, kiểm tra ảnh trùng pixel, triển khai quy trình huấn luyện trong notebook và đối chiếu các chỉ số với dự đoán kiểm tra. Kết quả 18 lượt của notebook được lưu riêng với hồ sơ A1 CO5085. |
| Trình bày | Hỗ trợ biên tập Markdown, LaTeX, PDF và nội dung GitHub Pages. Phần phân công do nhóm cung cấp. |

Bảng và hình sử dụng số liệu từ các lượt thực nghiệm có lưu cấu hình và lịch sử. Hai thí nghiệm Text hiện tại dùng chung danh sách bài kiểm tra độc lập. Lượt toàn văn Kaggle trước đó được lưu riêng vì dùng chung tập đánh giá để chọn checkpoint và hiệu chỉnh.

## Tài liệu đối chiếu

- [UCI Adult](https://archive.ics.uci.edu/dataset/2/adult), [VietnamNet News](https://huggingface.co/datasets/dathuynh1108/vietnamnet-news) và [CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html)
- [Tài liệu scikit-learn](https://scikit-learn.org/stable/), [PyTorch](https://docs.pytorch.org/docs/stable/), [torchvision](https://docs.pytorch.org/vision/stable/models.html) và [PhoBERT](https://huggingface.co/vinai/phobert-base-v2)
- [Nguồn thí nghiệm Image](docs/IMAGE_REUSE.md) và [nguồn thí nghiệm PhoBERT toàn văn](docs/TEXT_REUSE.md)
