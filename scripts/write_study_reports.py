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
    title = track.title()
    subject = {
        "tabular": "Phân loại thu nhập trên UCI Adult",
        "text": "Phân loại tiêu đề VietnamNet với TF-IDF và PhoBERT",
    }[track]
    preamble = r"""\documentclass[12pt,a4paper]{report}
\input{../course-report.tex}
\CourseReportHeader{CO5177 · @TRACK@}
\hypersetup{pdftitle={CO5177 - Bao cao @TRACK@},pdfauthor={Huynh Thanh Dat, Luong Minh Duy}}

\begin{document}
\CourseCover{assets/hcmut-logo.png}
  {BÁO CÁO @LABEL@}
  {CO5177 · Nền tảng lập trình cho phân tích và trực quan dữ liệu}
  {@SUBJECT@}
  {Nhóm CTG}
  {Huỳnh Thành Đạt & 2570161 · 50\%\\
   Lương Minh Duy & 2570083 · 50\%\\[0.5em]
   Giảng viên & Lê Thành Sách}
  {tháng 10 năm 2026}

""".replace("@TRACK@", title).replace("@LABEL@", track.upper()).replace("@SUBJECT@", subject)
    best = max(summary["models"], key=lambda model: model["validation"]["macro_f1"])
    accuracy = f"{100 * best['test']['accuracy']:.2f}".replace(".", ",")
    macro_f1 = f"{best['test']['macro_f1']:.4f}".replace(".", ",")
    test_size = f"{data['split_sizes']['test']:,}".replace(",", ".")
    best_name = (
        "PhoBERT đóng băng kết hợp hồi quy logistic"
        if best["id"] == "phobert"
        else best["name"]
    )
    best_result = (
        f"{best_name} đạt độ chính xác {accuracy}\\% và macro-F1 {macro_f1} "
        f"trên {test_size} mẫu kiểm tra."
    )
    if track == "tabular":
        abstract = (
            "Thực nghiệm dự đoán thu nhập trên 50.000 USD mỗi năm từ 14 thuộc tính trong UCI Adult. "
            "Sau khi loại các bản ghi trùng và nhóm có nhãn mâu thuẫn, dữ liệu được chia thành ba tập. "
            "Bốn cấu hình so sánh gồm dự đoán lớp đa số, hồi quy logistic thường, hồi quy logistic "
            "cân bằng lớp và histogram gradient boosting.\n\n"
            + best_result
            + " Thêm trọng số cân bằng lớp giúp hồi quy logistic nhận ra nhiều bản ghi thu nhập cao hơn, "
            "đồng thời làm tăng số bản ghi được xếp nhầm vào nhóm này."
        )
        overview = [
            ("Dữ liệu", "UCI Adult với 14 thuộc tính số và phân loại."),
            ("Tiền xử lý", "Loại trùng trước khi chia tập, điền giá trị thiếu và mã hóa thuộc tính phân loại."),
            ("Đối chứng", "Dự đoán lớp đa số, hồi quy logistic và histogram gradient boosting."),
            ("Kết quả chính", best_result),
        ]
    else:
        abstract = (
            "Thực nghiệm so sánh các cách biểu diễn trên cùng tập 7.600 tiêu đề VietnamNet thuộc 19 chuyên mục. "
            "TF-IDF theo từ và theo ký tự được kết hợp với SVM tuyến tính. Đặc trưng từ PhoBERT đóng băng "
            "được đưa vào hồi quy logistic. Bộ phân loại được chọn bằng macro-F1 trên tập xác thực.\n\n"
            + best_result
            + " Kết quả phản ánh hiệu quả của từng cặp biểu diễn và bộ phân loại. "
            "Tập tiêu đề cân bằng và cách chia riêng xác định phạm vi của phép so sánh."
        )
        overview = [
            ("Dữ liệu", "7.600 tiêu đề được chọn từ bộ dữ liệu VietnamNet do nhóm thu thập."),
            ("Biểu diễn", "TF-IDF theo từ, TF-IDF theo ký tự và đặc trưng PhoBERT đóng băng."),
            ("Phép đo", "Độ chính xác, macro-F1 và lỗi theo chuyên mục trên tập kiểm tra giữ riêng."),
            ("Kết quả chính", best_result),
        ]
    overview_rows = "".join(f"{label} & {value}" + r"\\" + "\n" for label, value in overview)
    parts = [
        preamble,
        "\\CourseAbstract{\n" + abstract + "\n}\n\n",
        "\\CourseOverview{\n" + overview_rows + "}\n\n",
        "\\CourseContents\n",
    ]
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
\caption{Số giá trị thiếu theo thuộc tính trong toàn bộ dữ liệu nguồn trước khi chia tập và imputation.}\end{figure}
\begin{figure}[htbp]\centering\includegraphics[width=.8\textwidth]{generated/class_counts.png}
\caption{Số bản ghi theo nhãn thu nhập sau khi loại nhóm nhãn mâu thuẫn và bản ghi trùng.}\end{figure}
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
Các thuộc tính số được chuẩn hóa cho logistic regression; histogram gradient boosting dùng chúng ở thang đo gốc.
Phân bố số liệu có thể chứa giá trị cực đoan, nhưng thí nghiệm không áp dụng bước phát hiện hoặc loại ngoại lệ riêng.
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
Dữ liệu thô và trọng số mô hình không được đưa vào Git \cite{vietnamnet}.
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
Đo accuracy, macro-F1 và F1 theo chuyên mục trên cùng 1.140 tiêu đề; không chọn mô hình theo test.
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
Mô hình & C & Val macro-F1 & Test accuracy & Test macro-F1\\\midrule
""")
    for model in summary["models"]:
        name = model["name"].replace(" + ", " + ")
        c = "--" if model["selected_C"] is None else str(model["selected_C"])
        parts.append(
            f"{name} & {c} & {model['validation']['macro_f1']:.4f} & {100 * model['test']['accuracy']:.2f}\\% & {model['test']['macro_f1']:.4f} \\\\\n"
        )
    parts.append(r"""\bottomrule\end{tabularx}
\caption{Siêu tham số $C$ được chọn theo macro-F1 trên validation; các cột test là kết quả trên tập giữ riêng. Accuracy trình bày theo phần trăm, macro-F1 theo thang 0--1.}\end{table}
\begin{figure}[htbp]\centering\includegraphics[width=.95\textwidth]{generated/scores.png}
\caption{Độ chính xác và macro-F1 của bốn mô hình trên cùng tập kiểm tra. Kết quả tính trên một cách chia và một hạt giống.}\end{figure}
\section{Nhận xét}
""")
    models = {m["id"]: m for m in summary["models"]}
    if track == "tabular":
        base = models["logistic"]
        balanced = models["balanced"]
        strong = models["histogram"]
        parts.append(
            f"Histogram gradient boosting đạt accuracy {100 * strong['test']['accuracy']:.2f}\\% và macro-F1 {strong['test']['macro_f1']:.4f}, cao hơn logistic regression {100 * (strong['test']['accuracy'] - base['test']['accuracy']):.2f} điểm phần trăm accuracy và {strong['test']['macro_f1'] - base['test']['macro_f1']:.4f} macro-F1. Kết quả cho thấy mô hình boosting có hiệu quả cao hơn trong split và cấu hình đã thử; phép so sánh không xác định riêng vai trò của phi tuyến tính, tương tác hay cách mã hóa.\n\n"
        )
        p = base["test"]["per_class"][">50K"]
        q = balanced["test"]["per_class"][">50K"]
        parts.append(
            f"Thêm trọng số cân bằng lớp làm recall của nhóm thu nhập trên 50.000 USD tăng từ {p['recall']:.4f} lên {q['recall']:.4f}, trong khi precision giảm từ {p['precision']:.4f} xuống {q['precision']:.4f}. Số dự đoán dương tính giả tăng từ 363 với hồi quy logistic thông thường lên {balanced['test']['confusion'][0][1]:,} với bản cân bằng lớp. Trọng số lớp giúp bỏ sót ít bản ghi thu nhập cao hơn và làm tăng số bản ghi được xếp nhầm vào nhóm này.\n"
        )
    else:
        phi = models["phobert"]
        char = models["character"]
        word = models["word"]
        parts.append(
            f"PhoBERT đóng băng với logistic regression đạt accuracy {100 * phi['test']['accuracy']:.2f}\\% và macro-F1 {phi['test']['macro_f1']:.4f}. So với TF-IDF ký tự, accuracy tăng {100 * (phi['test']['accuracy'] - char['test']['accuracy']):.2f} điểm phần trăm và macro-F1 tăng {phi['test']['macro_f1'] - char['test']['macro_f1']:.4f}. Đây là so sánh giữa toàn bộ pipeline đã đo; thí nghiệm chưa cô lập ảnh hưởng của encoder, pooling hoặc classifier.\n\n"
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
\caption{Ma trận nhầm lẫn trên test của mô hình có macro-F1 validation cao nhất; hàng là nhãn thực, cột là nhãn dự đoán.}\end{figure}
\chapter{Kết luận và giới hạn}
\section{Giới hạn}
""")
    if track == "tabular":
        parts.append(r"""Các kết quả phản ánh một cách chia dữ liệu và một hạt giống.
Nguồn điều tra năm 1994 giới hạn khả năng áp dụng cho thu nhập hiện nay. Sau khi gộp các bản ghi trùng thuộc tính, dữ liệu còn thiếu mã hộ gia đình để chia theo hộ. Fnlwgt được dùng làm biến đầu vào. Các chỉ số mô tả tập mẫu đã chia.
Chưa khảo sát riêng ảnh hưởng của từng chiến lược imputation, xử lý giá trị cực đoan hay hiệu quả trên từng nhóm nhân khẩu.
""")
    else:
        parts.append(r"""Chỉ dùng tiêu đề trên cohort cân bằng, nên kết quả không mô tả việc đọc toàn bài hoặc phân bố triển khai tự nhiên.
Chuyên mục nguồn có thể giao nhau; 3.628 dòng có mâu thuẫn trong nhóm trùng đã bị loại, nhưng chưa kiểm tra nhãn từng bài.
Đã xử lý exact URL/headline duplicates; near duplicates và split theo thời gian chưa được khảo sát.
Không có nhiều split/seed để mô tả độ bất định. PhoBERT không được fine-tune trong thực nghiệm này.
""")
    parts.append(r"""
Phạm vi hỗ trợ của AI được trình bày trong \href{https://github.com/dathuynh1108/CO5177-PFDAV/blob/main/AI\_USE\_REPORT.md}{AI\_USE\_REPORT.md}.
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
