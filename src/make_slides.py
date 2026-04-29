import os
import re

def main():
    report_path = os.path.join('report', 'EDA_REPORT.md')
    slides_path = os.path.join('report', 'slides.md')

    if not os.path.exists(report_path):
        print(f"오류: {report_path} 파일이 존재하지 않습니다.")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Marp 헤더 설정
    slides = [
        "---",
        "marp: true",
        "theme: default",
        "paginate: true",
        "header: '네모 매장 데이터 EDA 리포트'",
        "footer: 'Wiset Inflearn Nemo Project'",
        "style: |",
        "  section { font-family: 'Malgun Gothic', sans-serif; font-size: 20px; }",
        "  h1 { color: #2c3e50; font-size: 50px; }",
        "  h2 { color: #34495e; border-bottom: 2px solid #3498db; font-size: 35px; }",
        "  img { max-width: 70%; max-height: 350px; display: block; margin: 0 auto; }",
        "  table { font-size: 15px; margin-left: auto; margin-right: auto; }",
        "---\n"
    ]

    # 제목 추출 및 첫 슬라이드 작성
    title_match = re.search(r'^# (.*)', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "EDA 리포트"
    slides.append(f"# {title}\n\n인프런 니모 프로젝트 데이터 분석 결과 발표\n")

    # 섹션 분리 (## 또는 ### 기준으로 슬라이드 분할 고려)
    # 너무 긴 내용은 슬라이드를 쪼개야 함
    sections = re.split(r'\n(## |### )', content)
    
    current_header = ""
    for i in range(1, len(sections), 2):
        header_type = sections[i]
        section_content = sections[i+1]
        
        lines = section_content.split('\n')
        sub_title = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        
        # 새로운 슬라이드 시작
        slides.append("---\n")
        
        if header_type == "## ":
            current_header = sub_title
            slides.append(f"## {sub_title}\n\n")
        else:
            slides.append(f"## {current_header}\n### {sub_title}\n\n")
        
        # 이미지 경로 수정 및 크기 조절 (Marp 문법)
        # EDA_REPORT.md의 이미지 경로: ![제목](../images/name.png)
        # 리포트 폴더에서 실행 시 그대로 사용 가능하거나 경로 조정 필요
        body = body.replace('../images/', '../images/') 
        
        # 내용이 너무 길면 자르기 (슬라이드 한계를 넘지 않도록)
        if len(body) > 800:
            body = body[:800] + "...\n\n**(내용이 길어 요약되었습니다. 리포트 본문을 참조하세요.)**"
            
        slides.append(body + "\n")

    with open(slides_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(slides))

    print(f"Marp 슬라이드 마크다운 생성 완료: {slides_path}")

if __name__ == "__main__":
    main()
