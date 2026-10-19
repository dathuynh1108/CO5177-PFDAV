"""Compose separate Vietnamese reports from verified Tabular/Text measurements."""

import json
import shutil

from studies.evidence import ROOT, audit


def code(value):
    return r"\code{" + str(value) + "}"


def write(track):
    audit(track, check_models=True)
    directory = ROOT / "reports" / track
    data = json.loads((directory / "generated/data-audit.json").read_text())
    summary = json.loads((directory / "generated/summary.json").read_text())
    assets = directory / "assets"
    assets.mkdir(exist_ok=True)
    shutil.copyfile(
        ROOT / "reports/image/assets/hcmut-logo.png", assets / "hcmut-logo.png"
    )
    preamble = (
        (ROOT / "reports/image/report.tex").read_text().split(r"\begin{document}", 1)[0]
    )
    title = track.title()
    preamble = (
        preamble.replace("Nhóm Image", title)
        .replace("CO5177 · Image", f"CO5177 · {title}")
        .replace("CO5177 - Bao cao Image", f"CO5177 - Bao cao {title}")
    )
    subject = {
        "tabular": "Phân tích và phân loại dữ liệu UCI Adult",
        "text": "Phân loại tiêu đề VietnamNet với TF-IDF và PhoBERT",
    }[track]
    cover = r"""
\begin{document}
\hypersetup{pageanchor=false}
\begin{titlepage}\centering
{\large ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH\par}
{\large\bfseries TRƯỜNG ĐẠI HỌC BÁCH KHOA\par}
{\large KHOA KHOA HỌC VÀ KỸ THUẬT MÁY TÍNH\par}
\vspace{1cm}\includegraphics[width=3cm]{assets/hcmut-logo.png}\par
\vspace{.8cm}{\large\bfseries NỀN TẢNG LẬP TRÌNH CHO PHÂN TÍCH\par}
{\large\bfseries VÀ TRỰC QUAN DỮ LIỆU\par}{\large Mã môn học: CO5177\par}
\vspace{1cm}\rule{\textwidth}{.6pt}\par\vspace{.4cm}
{\Huge\bfseries BÁO CÁO @TRACK@\par}\vspace{.5cm}
{\Large @SUBJECT@\par}\vspace{.4cm}\rule{\textwidth}{.6pt}\par
\vspace{.8cm}{\large Học kỳ 261 · Năm học 2026–2027\par}\vspace{.7cm}
\begin{tabular}{ll}Giảng viên: & Lê Thành Sách\\[.5em]
Thành viên: & Huỳnh Thành Đạt · 2570161\\ & Lương Minh Duy · 2570083\end{tabular}
\vfill{\small Thành phố Hồ Chí Minh, tháng 10 năm 2026\par}
\end{titlepage}\hypersetup{pageanchor=true}
\pagenumbering{roman}{\small\tableofcontents}\clearpage\pagenumbering{arabic}
""".replace("@TRACK@", track.upper()).replace("@SUBJECT@", subject)
    parts = [preamble, cover]
    if track == "tabular":
        parts.append(r"""
\chapter{Bài toán và dữ liệu}
\section{Mục tiêu}
Bài toán dự đoán nhãn thu nhập lớn hơn 50.000 USD/năm từ các thuộc tính trong UCI Adult.
Phần phân tích tập trung vào dữ liệu thiếu, mã hóa thuộc tính phân loại, chuẩn hóa thuộc tính số
và đánh đổi giữa accuracy với chất lượng dự đoán lớp ít mẫu. Bốn đối chứng gồm dự đoán lớp đa số,
logistic regression, logistic regression cân bằng lớp và histogram gradient boosting.
\section{Nguồn và cấu trúc}
Adult gồm 48.842 bản ghi và 14 thuộc tính từ dữ liệu Census năm 1994, do Barry Becker và Ronny Kohavi cung cấp.
Trang UCI công bố license CC BY 4.0 \cite{adult}. Các thuộc tính số là tuổi, fnlwgt, số năm học,
capital gain, capital loss và số giờ làm mỗi tuần. Tám thuộc tính còn lại là phân loại.
Dấu hỏi được đọc thành giá trị thiếu. Không tạo thiếu nhân tạo.
\section{Chất lượng dữ liệu và chia tập}
Hai tệp official train/test được gộp trước khi tạo một split mới. Nhóm có cùng 14 thuộc tính
nhưng nhãn mâu thuẫn bị loại toàn bộ; nhóm trùng còn lại giữ một bản ghi.
Quy tắc được áp dụng trước khi chia tập, nhằm tránh cùng một vector thuộc tính xuất hiện ở hai phía.
Đây không phải phép đánh giá trên official test gốc, nên điểm số không so trực tiếp với các benchmark dùng split đó.
""")
        parts.append(
            f"Loại {data['conflicting_label_rows_removed']} dòng có nhãn mâu thuẫn và {data['duplicate_rows_removed_after_conflicts']} dòng trùng còn lại; giữ {data['retained_rows']:,} dòng. Các cột thiếu gồm workclass (2.799), occupation (2.809) và native-country (857).\n"
        )
        parts.append(r"""
\begin{figure}[htbp]\centering\includegraphics[width=.95\textwidth]{generated/missing.png}
\caption{Giá trị thiếu trong dữ liệu nguồn, trước bước imputation.}\end{figure}
\begin{figure}[htbp]\centering\includegraphics[width=.8\textwidth]{generated/class_counts.png}
\caption{Phân bố hai lớp sau xử lý trùng.}\end{figure}
\chapter{Phương pháp và thiết lập}
\section{Tiền xử lý}
Split phân tầng theo nhãn với tỷ lệ 70/15/15 và seed 2026; phần 30\% còn lại được chia validation/test bằng seed 2027.
Median imputer cho cột số và most-frequent imputer cho cột phân loại chỉ fit trên train.
Logistic regression dùng StandardScaler và one-hot encoding, với lớp mới ở validation/test được bỏ qua trong encoder.
Gradient boosting dùng ordinal encoding cho biến phân loại và khai báo đúng các vị trí categorical;
mã -1 biểu diễn hạng chưa gặp. Không chuẩn hóa các cột số cho cây.
\section{Các mô hình}
Baseline luôn dự đoán lớp phổ biến nhất. Logistic regression thường và bản có class weight balanced
chọn $C\in\{0.1,1,10\}$ theo macro-F1 validation; khi hòa giữ ứng viên xuất hiện trước.
Giới hạn optimizer là 2.000 vòng. Histogram gradient boosting dùng 150 vòng, tối đa 31 lá,
L2 bằng 1 và không early stopping. Các cấu hình cố định trước khi mở test; không refit trên train cộng validation.
\section{Phép đo}
Accuracy, macro-F1, confusion và precision/recall/F1 từng lớp được tính từ prediction test.
Thời gian fit/validation cộng các ứng viên của từng mô hình, không gồm tải dữ liệu và xuất báo cáo.
Chỉ một split và model seed 42 được đo, không báo độ lệch chuẩn hoặc khoảng tin cậy từ một lượt.
""")
    else:
        parts.append(r"""
\chapter{Bài toán và dữ liệu}
\section{Mục tiêu}
Bài toán phân loại chuyên mục của bài báo từ tiêu đề tiếng Việt. Các cách biểu diễn được so sánh
trên cùng dữ liệu và split: TF-IDF từ, TF-IDF ký tự và đặc trưng PhoBERT đóng băng.
Baseline lớp đa số cung cấp mức đối chứng; mô hình không dùng URL, body hoặc tên chuyên mục làm input.
\section{Nguồn VietnamNet}
Bộ \code{dathuynh1108/vietnamnet-news} do nhóm thu thập chứa 212.705 bài trong 19 tệp chuyên mục.
Bài này dùng các tệp parquet gốc, không dùng config NER có nhãn thực thể.
Revision nguồn được cố định ở \code{d70a9601f36dcb1e5c534d30e2d3921c2ba16284}; SHA256 từng tệp nằm trong config.
Dataset card không nêu license phân phối nội dung báo chí; tình trạng license được ghi là chưa rõ.
Raw corpus và checkpoint không được đưa vào Git \cite{vietnamnet}.
\section{Làm sạch và tập mô hình}
Tiêu đề được chuẩn hóa NFC và khoảng trắng. URL được bỏ query/fragment để nhận diện bài.
Các bản ghi có cùng URL hoặc cùng tiêu đề đã casefold được nối thành nhóm liên thông;
nhóm có nhiều chuyên mục bị loại toàn bộ, nhóm còn lại giữ một bản ghi.
Quy tắc loại trùng được áp dụng trước bước lấy mẫu và chia tập.
""")
        parts.append(
            f"Có {data['empty_headlines_removed']:,} tiêu đề rỗng, {data['conflicting_category_rows_removed']:,} dòng thuộc nhóm chuyên mục mâu thuẫn và {data['duplicate_rows_removed_after_conflicts']} dòng trùng còn lại bị loại. Corpus còn {data['unique_usable_rows']:,} bài có thể sử dụng.\n"
        )
        parts.append(r"""
Chọn tối đa 400 bài mỗi lớp bằng thứ tự SHA256 của ID với seed 2026, trước khi xem chỉ số mô hình.
Tập mô hình có 7.600 tiêu đề, đủ 19 lớp. Đây là một cohort cân bằng từ corpus đã kiểm tra đầy đủ,
không phải huấn luyện trên toàn bộ 212.705 bài. Lựa chọn này giới hạn chi phí mã hóa và cho phép so sánh
các cách biểu diễn trên cùng dữ liệu. Phân bố nguồn vốn không cân bằng được lưu trong audit.
\begin{figure}[htbp]\centering\includegraphics[width=.95\textwidth]{generated/class_counts.png}
\caption{Mỗi lớp có 400 tiêu đề trong tập mô hình.}\end{figure}
\chapter{Biểu diễn và mô hình}
\section{Split và tách từ}
Split phân tầng 70/15/15 dùng seed 2026, tiếp tục chia validation/test bằng seed 2027.
Ba tập có 5.320/1.140/1.140 tiêu đề; mỗi lớp có 280/60/60 mẫu.
PyVi tách từ cho cùng chuỗi đầu vào của mọi mô hình. Sau tách từ còn kiểm tra tính duy nhất của input.
\section{TF-IDF và Linear SVM}
TF-IDF từ dùng unigram/bigram; bản ký tự dùng char-within-word n-gram 3--5.
Mỗi vectorizer có tối đa 80.000 đặc trưng, min-df 2, max-df 0,98 và sublinear TF.
Từ vựng và IDF chỉ fit trên train. Linear SVM chọn $C\in\{0.5,1,2\}$ bằng macro-F1 validation,
tối đa 5.000 vòng, model seed 42.
\section{PhoBERT đóng băng}
Dùng \code{vinai/phobert-base-v2}. Revision model:

\code{86cd7fd4c148980922ac11a2cf5e257f2ba639e1}.

PhoBERT yêu cầu input đã tách từ \cite{phobert}.
Encoder ở eval, mọi trọng số requires-grad bằng false; không cập nhật backbone bằng corpus.
Đặc trưng 768 chiều được mean-pool theo attention mask, gồm token BOS/EOS và không gồm padding.
Input tối đa 128 token, batch 16, FP32. Không có tiêu đề nào bị cắt trong cohort đã đo.
Logistic regression trên đặc trưng cố định chọn cùng tập C bằng macro-F1 validation, tối đa 2.000 vòng.
Các vector test được tạo bằng encoder cố định, không dùng để học từ vựng, thống kê chuẩn hóa hoặc tham số classifier.
\section{Đánh giá}
Tất cả lựa chọn classifier hoàn tất bằng validation trước khi dự đoán test.
Đo accuracy, macro-F1 và F1 theo chuyên mục trên cùng 1.140 tiêu đề; không chọn model hoặc checkpoint theo test.
Thời gian classifier gồm toàn bộ fit/validation của các ứng viên, tách khỏi thời gian mã hóa PhoBERT.
""")
        info = summary["pretrained"]
        parts.append(
            f"Lần mã hóa đã đo dùng {code(info['device'])} trên Apple M1 Pro, mất {info['encoding_seconds']:.2f} giây cho 7.600 tiêu đề. Các feature được cache cùng hash; tải model, tách từ và fit classifier nằm ngoài khoảng thời gian này.\n"
        )
    sizes = data["split_sizes"]
    parts.append(
        f"Số mẫu train/validation/test là {sizes['train']:,}/{sizes['validation']:,}/{sizes['test']:,}. Indices/ID và chữ ký nguồn được lưu cùng kết quả.\n"
    )
    parts.append(r"""
\chapter{Kết quả và phân tích}
\section{So sánh mô hình}
\begin{table}[htbp]\centering\small\setlength{\tabcolsep}{4pt}
\begin{tabularx}{\textwidth}{Xrrrr}\toprule
Mô hình & C & Val F1 & Test acc. & Test F1\\\midrule
""")
    for model in summary["models"]:
        name = model["name"].replace(" + ", " + ")
        c = "--" if model["selected_C"] is None else str(model["selected_C"])
        parts.append(
            f"{name} & {c} & {model['validation']['macro_f1']:.4f} & {100 * model['test']['accuracy']:.2f}\\% & {model['test']['macro_f1']:.4f} \\\\\n"
        )
    parts.append(r"""\bottomrule\end{tabularx}
\caption{C được chọn theo validation macro-F1. Test accuracy theo phần trăm; F1 theo thang 0--1.}\end{table}
\begin{figure}[htbp]\centering\includegraphics[width=.95\textwidth]{generated/scores.png}
\caption{Accuracy và macro-F1 trên cùng tập test. Không có error bar vì chỉ đo một split/seed.}\end{figure}
\section{Nhận xét}
""")
    models = {m["id"]: m for m in summary["models"]}
    if track == "tabular":
        base = models["logistic"]
        balanced = models["balanced"]
        strong = models["histogram"]
        parts.append(
            f"Gradient boosting đạt accuracy {100 * strong['test']['accuracy']:.2f}\\% và macro-F1 {strong['test']['macro_f1']:.4f}, cao hơn logistic regression {100 * (strong['test']['accuracy'] - base['test']['accuracy']):.2f} điểm phần trăm accuracy. Cây phân nhánh biểu diễn được các quan hệ phi tuyến và tương tác giữa thuộc tính trong thiết lập này. Đây là diễn giải từ đối chứng đã đo, chưa tách riêng đóng góp từng tương tác.\n\n"
        )
        p = base["test"]["per_class"][">50K"]
        q = balanced["test"]["per_class"][">50K"]
        parts.append(
            f"Cân bằng class weight thay đổi recall lớp >50K từ {p['recall']:.4f} lên {q['recall']:.4f}, trong khi precision đổi từ {p['precision']:.4f} xuống {q['precision']:.4f}. Vì vậy, tăng khả năng nhận diện lớp ít mẫu đi kèm nhiều false positive hơn; không thể chỉ đọc accuracy để đánh giá lựa chọn này.\n"
        )
    else:
        phi = models["phobert"]
        char = models["character"]
        word = models["word"]
        parts.append(
            f"PhoBERT đóng băng với logistic regression đạt accuracy {100 * phi['test']['accuracy']:.2f}\\% và macro-F1 {phi['test']['macro_f1']:.4f}. So với TF-IDF ký tự, accuracy tăng {100 * (phi['test']['accuracy'] - char['test']['accuracy']):.2f} điểm phần trăm. Kết quả phù hợp với lợi ích của biểu diễn ngữ cảnh pretrained khi tiêu đề ngắn và nhiều cách diễn đạt khác nhau. Thực nghiệm chưa tách riêng ảnh hưởng của encoder, pooling và classifier.\n\n"
        )
        parts.append(
            f"TF-IDF ký tự đạt {100 * char['test']['accuracy']:.2f}\\%, so với {100 * word['test']['accuracy']:.2f}\\% của TF-IDF từ. Chênh lệch quan sát được nhỏ hơn mức tăng từ PhoBERT; một split chưa đủ để suy ra ưu thế ổn định giữa hai baseline.\n"
        )
        chosen = max(summary["models"], key=lambda m: m["validation"]["macro_f1"])
        weakest = sorted(
            summary["classes"], key=lambda c: chosen["test"]["per_class"][c]["f1-score"]
        )[:3]
        parts.append(
            "Ba lớp có F1 thấp nhất của mô hình chọn bằng validation là "
            + ", ".join(
                code(c) + f" ({chosen['test']['per_class'][c]['f1-score']:.3f})"
                for c in weakest
            )
            + ". Các chuyên mục gần nhau hoặc chuyên mục rộng có thể gây nhầm lẫn; cần đối chiếu nhãn và bài nguồn trước khi gán nguyên nhân cho mô hình.\n"
        )
    parts.append(r"""
\begin{figure}[htbp]\centering\includegraphics[width=.9\textwidth]{generated/confusion.png}
\caption{Confusion test của mô hình có validation macro-F1 cao nhất; hàng là nhãn thực, cột là dự đoán.}\end{figure}
\chapter{Kết luận và tái lập}
\section{Giới hạn}
""")
    if track == "tabular":
        parts.append(r"""Một split và seed chỉ mô tả thiết lập cụ thể; chưa có đánh giá biến thiên hoặc kiểm định thống kê.
Dữ liệu Census lịch sử không đại diện cho thu nhập hiện tại. Đã loại trùng vector thuộc tính nhưng chưa có khóa hộ gia đình
để chia theo nhóm tự nhiên. Fnlwgt được dùng như một feature, không làm sample weight; kết quả không phải ước lượng tỷ lệ dân số.
Chưa khảo sát riêng ảnh hưởng của từng chiến lược imputation hay hiệu quả trên từng nhóm nhân khẩu.
""")
    else:
        parts.append(r"""Chỉ dùng tiêu đề trên cohort cân bằng, nên kết quả không mô tả việc đọc toàn bài hoặc phân bố triển khai tự nhiên.
Chuyên mục nguồn có thể giao nhau; 3.628 dòng có mâu thuẫn trong nhóm trùng đã bị loại, nhưng chưa kiểm tra nhãn từng bài.
Đã xử lý exact URL/headline duplicates; near duplicates và split theo thời gian chưa được khảo sát.
Không có nhiều split/seed để mô tả độ bất định. PhoBERT không được fine-tune trong thực nghiệm này.
""")
    parts.append(r"\section{Mã nguồn và lệnh chạy}" + "\n")
    parts.append(
        f"Mã nguồn ở {code('src/studies/' + track + '.py')}; cấu hình ở {code('configs/' + track + '.json')}.\n\n"
    )
    parts.append(
        f"{code('python -m studies.' + track)} chạy lại toàn bộ thí nghiệm.\n\nNotebook {code('notebooks/' + ('text_baselines' if track == 'text' else track) + '.ipynb')} thực hiện cùng quy trình.\n\n"
    )
    parts.append(r"""\code{python -m studies.audit --models} kiểm tra checksum và tính lại chỉ số từ predictions,
đồng thời kiểm tra classifier đã lưu ngoài Git. Chữ ký nguồn/config được kiểm tra không đổi trong lúc đo.
JSON/CSV, split IDs và biểu đồ nằm trong thư mục generated; dữ liệu nguồn, feature cache và model ở data/runs ngoài Git.
Các unit checks kiểm tra loại trùng liên thông, nhãn mâu thuẫn, biến phân loại chưa gặp, thống kê imputer và sửa đổi evidence.

Báo cáo sử dụng AI được đính kèm tại tệp \code{AI_USE_REPORT.md} trong repository.
\begin{thebibliography}{9}\addcontentsline{toc}{chapter}{Tài liệu tham khảo}
""")
    if track == "tabular":
        parts.append(r"""\bibitem{adult} B. Becker và R. Kohavi. \emph{Adult}. UCI Machine Learning Repository, 1996. DOI: 10.24432/C5XW20. \url{https://archive.ics.uci.edu/dataset/2/adult}. License CC BY 4.0.
""")
    else:
        parts.append(r"""\bibitem{vietnamnet} Nhóm thực hiện. \emph{VietnamNet News}. \url{https://huggingface.co/datasets/dathuynh1108/vietnamnet-news}. Revision và checksums trong config.
\bibitem{phobert} D. Q. Nguyen và A. T. Nguyen. \emph{PhoBERT: Pre-trained language models for Vietnamese}. Findings of EMNLP, 2020. \url{https://huggingface.co/vinai/phobert-base-v2}. Model card nêu license AGPL-3.0 cho phiên bản base-v2.
\bibitem{pyvi} PyVi 0.1.1. Vietnamese word segmentation. \url{https://pypi.org/project/pyvi/}.
""")
    parts.append(r"""\bibitem{sklearn} Scikit-learn documentation: Pipeline, ColumnTransformer, TfidfVectorizer và classification metrics. \url{https://scikit-learn.org/stable/}.
\end{thebibliography}\end{document}
""")
    filename = "report.tex" if track == "tabular" else "baselines.tex"
    (directory / filename).write_text("".join(parts))
    print(directory / filename)


if __name__ == "__main__":
    for track in ["tabular", "text"]:
        write(track)
    from text_reuse.analysis import export_tables

    export_tables()
