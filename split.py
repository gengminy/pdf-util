import os
from PyPDF2 import PdfReader, PdfWriter


def split_pdfs(input_file_path):
    if not os.path.exists(input_file_path):
        print("[IOError] 존재하지 않는 파일 입니다.")
        return

    input_pdf = PdfReader(input_file_path)
    out_paths = []
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    size = to_zerofill_number_str(len(input_pdf.pages), 3)
    for i, page in enumerate(input_pdf.pages):
        page_number = to_zerofill_number_str(i + 1, 3)
        output = PdfWriter()
        output.add_page(page)
        out_file_path = f"outputs/{input_file_path[:-4]}_{page_number}.pdf"
        with open(out_file_path, "wb") as output_stream:
            print(f"{page_number} 번 파일 저장중... ({page_number}/{size})")
            output.write(output_stream)
        out_paths.append(out_file_path)
    return out_paths


def to_zerofill_number_str(num, length):
    return str(num).zfill(length)


def request_file(dir_path):
    # 경로 검증
    if not os.path.exists(dir_path):
        print("[InputError] 존재하지 않는 경로입니다.\n")
        return
    print(f"* 현재 디렉토리 경로 : {dir_path}")

    # 현재 디렉토리 pdf 파일 출력
    pdf_files = [filename for filename in os.listdir(dir_path) if filename.endswith(".pdf")]
    pdf_files_count = len(pdf_files)
    print(f"총 {pdf_files_count} 개의 파일을 발견했습니다")
    for i, pdf_file in enumerate(pdf_files):
        print(f"* [{to_zerofill_number_str(i + 1, 3)}] {pdf_file}")
    # 현재 디렉토리에 pdf 파일이 없음
    if pdf_files_count <= 0:
        print("* 현재 디렉토리에 pdf 파일이 없습니다")
        return

    print("")
    print("* pdf 파일 분할을 시작합니다.")
    for i, pdf_file in enumerate(pdf_files):
        print(f"* [{to_zerofill_number_str(i + 1, 3)}] {pdf_file} 변환중...")
        try:
            split_pdfs(pdf_file)
            print("* 완료\n")
        except Exception as e:
            print(e)
            print("* [IOError] 파일 변환에 실패하였습니다.")


if __name__ == '__main__':
    req_path = os.path.abspath('')
    request_file(req_path)
