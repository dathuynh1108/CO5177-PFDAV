# Báo cáo sử dụng AI

AI được sử dụng để chuyển phần Image phù hợp từ CO5085 sang CO5177 theo yêu cầu của Huỳnh Thành Đạt, tổ chức source/config/report và bổ sung notebook, trực quan, kiểm tra provenance, báo cáo LaTeX và liên kết website.

Phần mô hình và vòng lặp PyTorch được kế thừa từ A1 CO5085, vốn được AI hỗ trợ hiện thực theo prompt, thông số và định hướng của người học, tham khảo API PyTorch/torchvision. Trong lần chuyển này, AI điều chỉnh import và đường dẫn; kết quả GPU được dùng lại nguyên vẹn, không được trình bày thành một lượt train mới.

AI hỗ trợ tính lại accuracy/macro-F1 từ prediction, kiểm tra hash và chữ ký nguồn/checkpoint, phân tích đường cong và lỗi phân loại, soạn rồi rà văn phong báo cáo. Notebook phân tích và các kiểm tra tự động được thực thi; trạng thái kiểm tra được ghi trong tài liệu repo. Không gán phần việc hoặc xác nhận đóng góp chưa được cung cấp cho thành viên còn lại.

Các yêu cầu về dữ liệu, protocol và pretrained được đối chiếu với nội dung brief hiện có trong repo. Việc sử dụng lại kết quả giữa hai môn được nêu trong `reports/image/reuse-manifest.json` và báo cáo Image; không tạo số liệu hoặc video chưa có.

Trong lần rà soát ngày 19/10/2026, AI đối chiếu E1–E3/A1/A2 với ba track CO5177, bổ sung sáu hình đường cong pretrained từ commit gốc có kiểm tra SHA256, cập nhật notebook, báo cáo và trang Image. Code huấn luyện và các kết quả đo không thay đổi; không phát sinh lượt huấn luyện GPU mới.

Theo yêu cầu bổ sung, AI hiện thực hai bài Tabular và Text bằng scikit-learn, PyTorch và Transformers; chọn UCI Adult cho Tabular và sử dụng corpus VietnamNet đã thu thập cho Text. AI viết quy trình làm sạch, loại trùng, chia tập, chọn cấu hình theo validation, huấn luyện, tính chỉ số, lưu classifier và kiểm tra bằng chứng. PhoBERT VinAI được dùng làm encoder đóng băng vì repo PhoBERT cũ chưa có trọng số. Các mô hình mới được chạy trên máy hiện tại, không thuê GPU hoặc phát sinh phép đo giả.

AI hỗ trợ viết hai notebook, báo cáo LaTeX/PDF riêng, phần phân tích kết quả và rà lại nội dung UI theo văn phong trực tiếp của báo cáo. Notebook được chạy từ đầu; báo cáo và website được kiểm tra sau khi tạo. Nguồn dữ liệu/model, cấu hình và giới hạn được ghi trong `docs/STUDIES_PROTOCOL.md` cùng manifest từng bài.
