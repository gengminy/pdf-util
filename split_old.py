import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdfs(input_file_path):
    if not os.path.exists(input_file_path):
        print("[IOError] 존재하지 않는 파일 입니다.")
        return

    input_pdf = PdfReader(open(input_file_path, "rb"))
    out_paths = []
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    size = to_zerofill_number_str(len(input_pdf.pages), 3)
    for i, page in enumerate(input_pdf.pages):
        output = PdfWriter()
        page_number = to_zerofill_number_str(i, 3)
        output.add_page(page)
        out_file_path = f"outputs/{input_file_path[:-4]}_{page_number}.pdf"
        with open(out_file_path, "wb") as (output_stream, err):
            print(f"{page_number} 번 파일 저장중... ({page_number}/{size})")
            if err:
                print("[IOError] 파일 저장에 실패했습니다.")
            else:
                output.write(output_stream)
        out_paths.append(out_file_path)
    return out_paths


def to_zerofill_number_str(num, length):
    return str(num).zfill(length)


def is_valid_number_list(number_list, size):
    for number in number_list:
        if not str(number).isnumeric() or int(number) > size:
            return False
    return True


def request_path():
    while True:
        print("* 파일 경로를 입력해주세요.")
        _path = input("* 프로그램과 동일한 경로일 경우 [Enter]를 입력하세요.\n>> ")

        # 빈 문자열 입력 시 현재 디렉토리
        if not _path:
            return os.path.abspath('')

        # 디렉토리 검증
        if not os.path.exists(_path):
            print("[InputError] 존재하지 않는 경로입니다.\n")
            continue

        return os.path.abspath(_path)


def request_file(dir_path):
    # 경로 검증
    if not os.path.exists(dir_path):
        print("[InputError] 존재하지 않는 경로입니다.\n")
        return
    print(f"* 설정 경로 : {dir_path}")

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

    idx_list = request_idx(pdf_files_count)

    # 모든 파일 출력
    if idx_list == 0:
        for i, pdf_file in enumerate(pdf_files):
            print(f"* [{to_zerofill_number_str(i + 1, 3)}] {pdf_file} 변환중...")
            split_pdfs(pdf_file)
    # 특정 파일만 출력
    else:
        for idx in idx_list:
            print(f"* [{to_zerofill_number_str(idx, 3)}] {pdf_files[idx - 1]} 변환중...")
            split_pdfs(pdf_files[idx - 1])


def request_idx(max_size):
    # 변환할 파일 리스트
    while True:
        print("")
        print("* [Enter]: 모두 변환하기")
        print("* 숫자 + [Enter]: 특정 파일 1개만 변환하기")
        print("* 숫자, 숫자, 숫자 + [Enter]: 파일 여러 개 변환하기")
        input_idx = input(">> ")

        if not input_idx:
            return 0

        file_nums = input_idx.replace(' ', '').split(',')
        if is_valid_number_list(file_nums, max_size):
            return map(int, file_nums)
        else:
            print("[InputError] 잘못된 입력입니다.")


if __name__ == '__main__':
    req_path = request_path()
    file_numbers = request_file(req_path)
