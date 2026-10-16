# Image: phạm vi và nguồn thực nghiệm

Image dùng lại thí nghiệm A1 của CO5085 tại commit `1250e569c6ce055391b5670e2f9a31faedb44b20`. Đây là cùng 24 lượt chạy, không phải 24 phép đo độc lập mới. `reports/image/reuse-manifest.json` ghi repository, commit, hash config/source, ánh xạ code được chuyển và SHA256 từng tệp evidence được nhập. Không lấy Fashion-MNIST của E1–E3 làm bài chính.

| Yêu cầu Image trong brief v4.0 | Đối chiếu |
| --- | --- |
| Ít nhất 5.000 ảnh, ít nhất 3 lớp | Đủ 60.000 ảnh CIFAR-100, 100 lớp |
| Không MNIST, Fashion-MNIST, CIFAR-10 làm dữ liệu chính | CIFAR-100 là tập khác, không nằm trong ba tập bị loại |
| Khuyến nghị cạnh ngắn 128px | Ảnh gốc 32px, input đã đo 96px. Giữ nguyên setting để tái sử dụng phép đo; không gọi resize là thêm thông tin. Đây là giới hạn phải giải thích |
| Pretrained khi dùng deep learning | Sáu cấu hình chính đều pretrained IMAGENET1K_V1; hai scratch là đối chứng bổ sung |
| Split, tránh leakage, augmentation | Train/validation/test 45k/5k/10k; split phân tầng seed 2026, crop/flip chỉ train; validation chọn checkpoint |
| Khám phá, trực quan và giải thích | Notebook kiểm tra dữ liệu và phân tích prediction/confusion; báo cáo Image riêng |

Căn cứ hiện có là bản tóm tắt brief trong `requirements.html` và `assignments/image.html`, không phải PDF đề gốc chưa có trong repo. Nếu LMS bổ sung ràng buộc khác, cần đối chiếu lại; không coi reuse là tự động được công nhận bởi giảng viên.

## Bố cục

- `src/image/`: data, mô hình, training loop và phân tích; module được chuyển từ A1, thay import/path.
- `configs/image.json`: protocol gốc byte-identical.
- `reports/image/`: PDF, LaTeX, figures và evidence riêng của track Image.
- `notebooks/image.ipynb`: notebook phân tích từ trên xuống, không tự thuê GPU hay chạy lại training.
- `reports/image/reuse-manifest.json`: provenance bất biến; `python -m image.analysis` kiểm tra hash và tính lại 24 confusion/accuracy/macro-F1 từ predictions.

## Chạy

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install --no-deps -e .
.venv/bin/python -m image.analysis
.venv/bin/python -m image.run_suite --list
.venv/bin/python -m pytest -q
```

Training mới là lệnh riêng: `python -m image.run_suite --device cuda --num-workers 8 --output-root runs/image-new`. Cần chuẩn bị CIFAR-100 trước; code không tự tải dữ liệu khi train. Chỉ đánh giá test sau khi cố định protocol bằng `--phase test --confirm-test`. Không dùng source identity mới để resume checkpoint của CO5085.

Nguồn raw data có tình trạng license chưa rõ; không phân phối raw data hoặc checkpoint trong Git. Bộ notebook có nguồn tải public và kiểm tra pixel/label hashes khớp dữ liệu của phép đo gốc. Không tuning sau khi xem test. Video và PDF tổng hợp toàn môn vẫn cần các phần Tabular/Text; không đánh dấu đã hoàn thành toàn bộ học phần.

## Kết quả kiểm tra bổ sung

Notebook đã chạy trọn 19 cell trên CPU, với đầy đủ 60.000 ảnh qua mirror revision cố định và pixel/label hashes khớp archive Toronto. Exact-pixel audit: 2 nội dung chung train–validation, 10 nội dung chung train–test, không có validation–test. Chỉ số phụ trên 9.990 prediction giữ lại không phải thí nghiệm train mới hay bảo đảm loại hết leakage. `reports/image/analysis/` lưu kết quả, danh sách indices và đồ thị. Các unit/protocol checks được chuyển theo source và kiểm tra lại ở module `image`.
