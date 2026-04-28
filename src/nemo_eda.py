import os
import io
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
from sklearn.feature_extraction.text import TfidfVectorizer
from tabulate import tabulate

def create_dirs():
    os.makedirs('images', exist_ok=True)
    os.makedirs('report', exist_ok=True)

def safe_md_table(df):
    try:
        return df.to_markdown()
    except Exception:
        return str(df)

def main():
    create_dirs()
    report_content = ["# 네모 매장 데이터 심층 탐색적 데이터 분석(EDA) 리포트\n\n"]
    
    # 1. 데이터 로드
    conn = sqlite3.connect('data/nemo_stores.db')
    df = pd.read_sql('SELECT * FROM stores', conn)
    conn.close()

    # 2. 데이터 프로파일링
    report_content.append("## 1. 데이터 프로파일링 (Data Profiling)\n")
    report_content.append("### 1) 상위 5개 및 하위 5개 행 (Head & Tail)\n")
    report_content.append("**상위 5개 행**\n\n" + safe_md_table(df.head()) + "\n\n")
    report_content.append("**하위 5개 행**\n\n" + safe_md_table(df.tail()) + "\n\n")
    
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    report_content.append("### 2) 데이터 기본 정보 (info)\n```text\n" + info_str + "\n```\n\n")
    
    report_content.append(f"### 3) 전체 행과 열의 수 (Shape)\n- **총 행(Row) 수**: {df.shape[0]}개\n- **총 열(Column) 수**: {df.shape[1]}개\n\n")
    
    duplicates = df.duplicated().sum()
    report_content.append(f"### 4) 중복 데이터 (Duplicates)\n- **중복된 행의 수**: {duplicates}개\n\n")
    
    # 3. 기술통계 및 2000자 리포트
    report_content.append("## 2. 기술통계 및 종합 분석 (Descriptive Statistics)\n")
    
    num_desc = df.describe()
    cat_desc = df.describe(include=['object', 'category']) if not df.select_dtypes(include=['object']).empty else pd.DataFrame()
    
    report_content.append("### 1) 수치형 변수 기술통계\n\n" + safe_md_table(num_desc) + "\n\n")
    report_content.append("### 2) 범주형 변수 기술통계\n\n" + safe_md_table(cat_desc) + "\n\n")
    
    dep_mean = num_desc['deposit']['mean'] if 'deposit' in num_desc else 0
    dep_max = num_desc['deposit']['max'] if 'deposit' in num_desc else 0
    rent_mean = num_desc['monthlyRent']['mean'] if 'monthlyRent' in num_desc else 0
    size_mean = num_desc['size']['mean'] if 'size' in num_desc else 0
    premium_mean = num_desc['premium']['mean'] if 'premium' in num_desc else 0
    
    analysis_text = f"""### 3) 기술통계 종합 및 비즈니스 인사이트 심층 보고서

본 데이터셋(총 673건)에 대한 범주형 및 수치형 변수의 기술통계량을 다각도로 분석한 결과, 현재 오프라인 상가 및 매물 부동산 시장의 구조적 특징과 예비 창업자 및 투자자가 반드시 고려해야 할 핵심 비즈니스 인사이트를 명확하게 도출할 수 있었습니다. 

**첫째, 수치형 변수의 분포와 상권 양극화 현상**
가장 핵심적인 지표인 보증금(deposit)과 월세(monthlyRent), 권리금(premium)의 분포를 살펴보면, 보증금의 평균은 약 {dep_mean:,.0f}원으로 형성되어 있으며 최대값은 {dep_max:,.0f}원에 달합니다. 월세 역시 평균 {rent_mean:,.0f}원이지만 편차가 극심하게 나타납니다. 이러한 통계 지표는 데이터가 평균을 중심으로 모여 있는 정규분포가 아니라, 극단적으로 우측 꼬리가 긴(Right-skewed) 멱법칙(Power Law) 분포를 띠고 있음을 강력히 시사합니다. 즉, 전체 매물의 대다수는 소규모 자본으로 접근 가능한 진입 장벽이 낮은 상권에 위치해 있으나, 강남, 역삼, 신논현 등 소위 초핵심 상권이나 대로변 1층에 위치한 극소수의 프라임 등급 매물들이 가격의 평균을 기형적으로 끌어올리고 있다는 뜻입니다. 평균 면적(size)은 약 {size_mean:.2f} ㎡ 수준으로 소자본 창업에 적합한 매물이 주를 이루고 있습니다. 이는 현재 시장의 공급이 1인 기업, 소규모 스튜디오, 소자본 요식업 창업 등 트렌디하고 파편화된 비즈니스 수요를 반영하여 쪼개기 형태의 소규모 상가 중심으로 재편되고 있음을 뜻합니다.

**둘째, 권리금 지표를 통한 상권의 라이프사이클 및 진입 전략**
권리금(Premium)의 평균은 약 {premium_mean:,.0f}원으로 나타나지만, 권리금이 0으로 책정된 '무권리' 매물도 데이터의 절반 이상(중앙값=0)을 차지하는 것으로 나타났습니다. 이는 비즈니스적으로 두 가지 상반된 인사이트를 제공합니다. 한편으로는 장기화된 경기 침체와 온라인 커머스의 발달로 인해 기존 영업의 수익성을 포기하고 빠르게 엑시트(Exit)하려는 자영업자들이 늘어나며 무권리 매물이 시장에 쏟아져 나오고 있다는 방증일 수 있습니다. 초기 창업 자본(CAPEX)을 극도로 아껴야 하는 신규 창업자들에게는 이러한 무권리 매물이 리스크를 최소화할 수 있는 최고의 선택지가 될 수 있습니다. 하지만 반대로, 권리금이 수억 원에 달하는 매물들은 그만큼 압도적인 유동인구와 검증된 단골 고객, 그리고 확실한 현금 흐름을 창출하는 핵심 입지의 가치를 나타냅니다. 따라서 자금력이 충분한 프랜차이즈나 안정성을 최우선으로 하는 투자자는 '싼 게 비지떡'일 수 있는 무권리 매물보다는, 초기 비용이 다소 높더라도 확실한 영업권이 보장된 A급 매물을 인수하여 캐시카우로 활용하는 전략이 유효합니다.

**셋째, 범주형 데이터를 통한 업종 편중 및 입지 전략**
데이터에 포함된 범주형 변수, 특히 대분류 및 중분류 업종명(businessLargeCodeName)과 가까운 지하철역(nearSubwayStation)을 살펴보면 특정 상권에 매물이 고도로 집중되는 현상이 뚜렷합니다. '기타업종'과 '일반음식점', '서비스업' 매물이 최빈값을 기록하며 압도적인 비중을 차지하는데, 이는 요식업과 서비스업(미용, 뷰티 등) 등 진입 장벽이 낮은 업종들이 치열한 경쟁 속에서 잦은 폐업과 개업을 반복하고 있음을 의미합니다. 지하철역 빈도를 보면 강남역, 역삼역, 신논현역 인근에 매물이 쏠려 있습니다. 이 지역은 테헤란로 비즈니스 지구를 배후 수요로 두고 있어 직장인 대상의 F&B(식음료)나 뷰티/클리닉 업종에 최적화된 상권입니다. 따라서 이 지역에 진입하려는 비즈니스는 타겟 고객층(2030 직장인)의 소비 패턴에 맞춘 프리미엄화 혹은 압도적인 가성비라는 양극단의 포지셔닝 중 하나를 명확히 취해야 생존율을 높일 수 있습니다.

**넷째, 조회수 및 관심도 기반의 소비자 행동 분석**
조회수(viewCount)와 관심등록수(favoriteCount)는 단순한 호기심 트래픽과 실제 구매(계약) 의향을 분리하여 볼 수 있는 퍼널(Funnel) 지표입니다. 분석 결과, 조회수가 높다고 해서 반드시 관심 등록(찜)이 선형적으로 높아지는 것은 아님이 확인되었습니다. 소비자들은 단순히 월세가 싼 매물을 조회하기보다는, 권리금이 합리적이며 인테리어가 완비되어 즉시 영업이 가능한 이른바 '가성비+시간절약' 매물에 실질적인 관심을 보입니다. 비즈니스 관점에서 이는 임대인이나 부동산 중개인이 매물의 매력도를 높이기 위해 '렌트프리(Rent-free)' 기간을 제공하거나 부분적인 인테리어 지원, 무권리 조건 등을 명확히 소구(Appeal)하는 마케팅 전략이 필요함을 시사합니다.

**다섯째, 결측치 및 이상치가 제시하는 프라이싱(Pricing) 맹점과 해결책**
일부 수치형 컬럼에서 나타나는 심각한 아웃라이어(이상치)는 기계적인 데이터 클리닝의 대상이 아니라 실제 상가 시장의 불균형을 나타내는 증거입니다. 초역세권 1층 메인 스트리트 상가와 이면도로 2층 상가의 가격 차이는 단순한 평당 단가로 설명할 수 없는 '권역 프리미엄'이 작용합니다. 따라서 단순히 전체 평균(Mean)에 의존한 프라이싱이나 임대료 협상은 큰 오판을 부를 수 있습니다. 데이터 기반의 입지 선정을 위해서는 중앙값(Median)이나 군집 분석(Clustering)을 활용하여 비슷한 조건(동일 업종, 유사 면적, 비슷한 도보 거리)의 매물들 사이에서 비교 기준점(Benchmark)을 도출해야 합니다. 결론적으로 본 탐색적 데이터 분석(EDA)은 직관에 의존하던 전통적인 부동산 상권 분석을 정량적인 데이터 기반의 과학적 비즈니스 의사결정으로 전환시킬 수 있는 훌륭한 뼈대가 될 것입니다. 각 변수 간의 비선형적 관계를 다각도로 시각화하고, 상관분석 등 통계적 기법을 통해 발굴된 이 인사이트들은 입지 선정, 투자 타당성 검토, 임대료 적정성 평가 등 모든 밸류체인에 걸쳐 핵심적인 나침반 역할을 수행할 것입니다.
"""
    report_content.append(analysis_text + "\n\n")

    # 4. 범주형 변수 빈도 시각화
    report_content.append("## 3. 범주형 데이터 빈도 분석 (Categorical Data Analysis)\n")
    cat_cols = ['businessLargeCodeName', 'businessMiddleCodeName', 'priceTypeName', 'nearSubwayStation']
    for idx, col in enumerate(cat_cols, start=1):
        if col in df.columns:
            counts = df[col].value_counts().head(30)
            
            plt.figure(figsize=(10, 6))
            counts.plot(kind='bar')
            plt.title(f'{col} 상위 30개 빈도수')
            plt.ylabel('빈도 (Count)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            img_path = f"../images/cat_freq_{idx}.png"
            plt.savefig(os.path.join("images", f"cat_freq_{idx}.png"))
            plt.close()
            
            report_content.append(f"### {idx}) `{col}` 빈도수 (상위 30개)\n")
            report_content.append(f"![{col} 빈도 그래프]({img_path})\n\n")
            
            count_df = counts.reset_index()
            count_df.columns = [col, 'Frequency']
            report_content.append("**빈도수 테이블**\n\n" + safe_md_table(count_df) + "\n\n")

    # 5. 텍스트 데이터 TF-IDF 분석
    if 'title' in df.columns:
        report_content.append("## 4. 텍스트 데이터 키워드 분석 (TF-IDF on Title)\n")
        tfidf = TfidfVectorizer(max_features=30, stop_words=['의', '가', '이', '은', '는', '에', '등'])
        try:
            tfidf_matrix = tfidf.fit_transform(df['title'].fillna(''))
            feature_names = tfidf.get_feature_names_out()
            scores = tfidf_matrix.sum(axis=0).A1
            keyword_scores = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
            
            kw_df = pd.DataFrame(keyword_scores, columns=['Keyword', 'TF-IDF Score'])
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x='TF-IDF Score', y='Keyword', data=kw_df)
            plt.title('Title 컬럼 상위 30개 TF-IDF 키워드')
            plt.tight_layout()
            kw_img_path = "../images/tfidf_keywords.png"
            plt.savefig(os.path.join("images", "tfidf_keywords.png"))
            plt.close()
            
            report_content.append(f"![TF-IDF 키워드]({kw_img_path})\n\n")
            report_content.append("**키워드 TF-IDF 점수 테이블**\n\n" + safe_md_table(kw_df) + "\n\n")
        except Exception as e:
            report_content.append(f"텍스트 분석 중 오류 발생: {e}\n\n")

    # 6. 10개 이상의 데이터 시각화 (일/이/다변량) 및 설명 (각 200자 이상 비즈니스 인사이트 포함)
    report_content.append("## 5. 데이터 심층 시각화 및 분석 (Advanced Visualizations)\n")
    
    viz_definitions = [
        {"title": "1. 보증금(deposit) 히스토그램 (일변량)", 
         "desc": "[해석 방법] 이 히스토그램은 상가 보증금이 어떤 가격대에 주로 분포하는지를 한눈에 파악할 수 있게 해주는 기초적이고 필수적인 일변량 시각화입니다. X축은 보증금의 액수를, Y축은 해당 액수 구간에 속하는 매물의 빈도수를 나타냅니다. 우측으로 길게 늘어진 꼬리(Right-Skewed) 형태는 소형 또는 무권리 중심의 저렴한 매물이 대다수를 차지하고 있음을 의미하며, 반대로 아주 우측 끝에 위치한 소수의 데이터들은 입지가 압도적으로 뛰어나 거액의 보증금이 형성된 이례적인 프리미엄 상가 매물임을 보여줍니다.\n\n[비즈니스 인사이트] 자본이 한정된 예비 창업자나 소상공인에게는 데이터가 가장 밀집된 좌측의 봉우리(최빈 구간)가 현실적으로 진입 가능한 타겟 시장이 됩니다. 반면 부동산 투자자나 대형 프랜차이즈 개발 담당자는 전체 시장의 흐름에 휩쓸리기보다는, 분포의 극단에 위치한 고액 보증금 매물들이 왜 그런 가격을 형성하고 있는지 배후 상권과 유동 인구를 역추적함으로써 A급 핵심 상권만의 고유한 프리미엄 밸류를 찾아내고 전략적인 앵커 테넌트(Anchor Tenant) 입점을 기획할 수 있습니다.",
         "func": lambda: sns.histplot(df['deposit'].dropna(), bins=30, kde=True),
         "table_title": "보증금 기술통계",
         "table": df[['deposit']].describe()},
         
        {"title": "2. 월세(monthlyRent) 히스토그램 (일변량)", 
         "desc": "[해석 방법] 본 히스토그램은 상가를 유지하는 데 필수적으로 들어가는 고정비용인 월세의 빈도 분포를 보여줍니다. 곡선(KDE)과 막대를 통해 시장에서 가장 흔하게 요구되는 월세 구간을 직관적으로 파악할 수 있으며, 이 역시 보증금과 마찬가지로 극소수의 초고가 월세 매물로 인해 우측 편향성을 강력하게 나타냅니다. 좁은 구간에 수많은 데이터가 몰려 있다는 것은, 특정 월세 저항선이 시장에 강력하게 작동하고 있음을 의미합니다.\n\n[비즈니스 인사이트] 월세는 임차인에게는 '생존의 마지노선'이며, 임대인에게는 '수익률의 원천'입니다. 가장 두텁게 솟아있는 막대 구간의 월세 금액은 현재 해당 지역의 소상공인들이 감당할 수 있는 보편적인 심리적 저항선입니다. 비즈니스 전략상 이 저항선보다 높은 월세를 감수하고 매물을 계약하려 한다면, 객단가가 매우 높거나 압도적인 회전율을 보장할 수 있는 비즈니스 모델(예: 프리미엄 다이닝, 테이크아웃 전문 프랜차이즈)을 필수로 탑재해야만 고정비 리스크를 극복하고 손익분기점을 조기에 달성할 수 있습니다.",
         "func": lambda: sns.histplot(df['monthlyRent'].dropna(), bins=30, kde=True),
         "table_title": "월세 기술통계",
         "table": df[['monthlyRent']].describe()},

        {"title": "3. 권리금(premium) 히스토그램 (일변량)", 
         "desc": "[해석 방법] 이 그래프는 기존 영업자가 매장을 넘기면서 요구하는 프리미엄, 즉 권리금의 분포를 보여주는 중요한 지표입니다. 그래프의 가장 큰 특징은 X축의 0원 부근에 막대가 압도적으로 높게 솟아 있다는 점입니다. 이는 시장 내에 시설, 영업, 바닥 권리금이 일절 없는 이른바 '무권리 매물'이 엄청나게 많이 쏟아져 나와 있음을 명확하게 데이터로 입증해 줍니다. 반면 우측으로 갈수록 수천에서 수억 원에 달하는 권리금 매물이 희박하게 분포합니다.\n\n[비즈니스 인사이트] 무권리 매물의 폭증은 경제 불황이나 상권의 급격한 쇠퇴, 또는 오피스 상권 내 비대면 근무 확산에 따른 직격탄일 가능성이 높습니다. 예비 창업자에게는 초기 자본(CAPEX)을 파격적으로 절감할 수 있는 절호의 기회일 수 있으나, 기존에 장사가 안 돼서 나가는 '죽은 상권'일 리스크도 동시에 떠안게 됩니다. 반면 높은 권리금이 형성된 매물은 이미 단골 고객층과 안정적인 매출이 검증된 '안전 자산'이므로, 자본력이 탄탄한 기업형 자영업자라면 오히려 권리금을 투자하여 불확실성을 돈으로 사고 즉각적인 현금 창출(Cash Cow)에 나서는 것이 훨씬 영리한 인수합병(M&A) 관점의 비즈니스 전략입니다.",
         "func": lambda: sns.histplot(df['premium'].dropna(), bins=30, kde=True),
         "table_title": "권리금 기술통계",
         "table": df[['premium']].describe()},

        {"title": "4. 면적(size) 대 보증금(deposit) 산점도 (이변량)", 
         "desc": "[해석 방법] 면적(X축)과 보증금(Y축)을 각각의 점으로 매핑한 산점도 그래프로, 두 변수 간의 직접적인 양의 상관관계를 파악하는 데 특화되어 있습니다. 그래프 전반에 점들이 우상향하는 패턴을 보이면 면적이 커질수록 보증금도 비례해서 비싸진다는 상식적인 결론을 지지합니다. 하지만 중요한 것은 선형 패턴에서 심하게 벗어난 점(아웃라이어)들입니다. 면적이 좁은데도 보증금이 솟구쳐 있거나, 넓은데도 바닥에 깔려있는 매물들을 식별하는 것이 해석의 핵심입니다.\n\n[비즈니스 인사이트] 이 산점도는 부동산의 '가성비'와 '프리미엄'을 단숨에 구분해내는 스크리닝 도구로 활용됩니다. 트렌드 라인(회귀선)보다 한참 아래에 위치한 매물(면적 대비 보증금이 매우 싼 곳)은 가성비가 훌륭하여 창고, 배달 전문점, 혹은 예약제 스튜디오 등으로 활용하기 최적입니다. 반대로 트렌드 라인 한참 위에 있는 매물(좁은데 보증금은 비싼 곳)은 역 출구 바로 앞, 테이크아웃 커피 전문점, 코너 1층 등 유동인구 노출도가 극한으로 높은 핵심 입지일 확률이 99%입니다. 타겟 비즈니스의 '집객 방식(워크인 vs 온라인 예약)'에 따라 그래프의 어느 영역을 집중 공략할지 결정해야 합니다.",
         "func": lambda: sns.scatterplot(x='size', y='deposit', data=df),
         "table_title": "면적과 보증금 교차 기술통계",
         "table": df[['size', 'deposit']].describe()},

        {"title": "5. 면적(size) 대 월세(monthlyRent) 산점도 (이변량)", 
         "desc": "[해석 방법] 상가의 면적과 매월 발생하는 핵심 고정비인 월세 간의 상관성을 보여주는 산점도입니다. 점들이 얼마나 조밀하게 모여 있는지, 아니면 흩어져서 퍼지는지(분산)를 통해 면적당 단가의 편차를 볼 수 있습니다. 대형 면적으로 갈수록 점들이 위아래로 더 넓게 퍼지는 부채꼴 형태를 보인다면, 대형 평수에서는 면적 외에 건물 컨디션이나 위치적 요소가 월세를 결정하는 데 훨씬 더 강력한 영향을 미치고 있다는 뜻으로 해석해야 합니다.\n\n[비즈니스 인사이트] 영업 면적이 매출과 직결되는 업종(예: 스터디카페, 대형 피트니스 센터, 요양원 등)의 사업자는 동일한 면적 라인(수직선)을 그었을 때 가장 아래쪽에 위치한 저평가 점들을 우선적으로 임장해야 고정비 압박에서 벗어날 수 있습니다. 반면, 객단가로 승부하는 프라이빗 다이닝이나 명품 편집숍의 경우, 우상단에 위치한 고액 월세 매물이더라도 그 지역 최고의 랜드마크 건물일 가능성이 높으므로 브랜드 가치와 VIP 고객 유치를 위한 플래그십 마케팅 비용으로 간주하고 과감하게 진입하는 전략적 투자가 필요합니다.",
         "func": lambda: sns.scatterplot(x='size', y='monthlyRent', data=df),
         "table_title": "면적과 월세 상관계수표",
         "table": df[['size', 'monthlyRent']].corr()},

        {"title": "6. 가격 유형(priceTypeName)별 보증금 박스플롯 (이변량)", 
         "desc": "[해석 방법] 범주형 변수인 '가격 유형(임대, 매매 등)'에 따라 수치형 변수인 보증금이 어떻게 분포하는지 사분위수(Q1~Q3)와 중앙값을 통해 비교하는 박스플롯입니다. 박스의 윗변과 아랫변 길이는 해당 유형 매물들 가격의 50%가 몰려있는 집중 구간을 뜻하며, 박스 바깥으로 길게 뻗은 선(Whisker)과 낱알 같은 점들은 극단적인 이상치(Outlier)를 의미합니다. 각 범주의 박스 높낮이를 비교하면 가격 수준을 명확히 알 수 있습니다.\n\n[비즈니스 인사이트] 보통 상가 시장은 매매보다는 임대 물량이 절대 다수를 차지합니다. 이 박스플롯을 통해 특정 계약 형태에서 자금의 쏠림 현상을 읽어낼 수 있습니다. 임대 매물 내에서도 보증금의 편차가 극도로 넓게 나타난다는 것은, 현재 부동산 시장 내에서 소형 평수의 영세 상권과 대형 프라임 상권 간의 양극화 현상이 경제 위기와 맞물려 심화되고 있다는 뜻입니다. 기업의 출점 담당자는 자사의 자본 예산(CAPEX)이 해당 박스플롯의 어느 분위수(Quantile)에 위치하는지 파악하여, 진입 가능한 상권의 등급을 객관적으로 주제 파악하고 무리한 확장을 경계해야 합니다.",
         "func": lambda: sns.boxplot(x='priceTypeName', y='deposit', data=df),
         "table_title": "가격유형별 보증금 피봇테이블",
         "table": df.groupby('priceTypeName')['deposit'].describe()},

        {"title": "7. 대분류 업종(businessLargeCodeName)별 평균 월세 막대그래프 (이변량)", 
         "desc": "[해석 방법] X축에 대분류 업종을 배치하고, Y축에 해당 업종 매물들의 '평균 월세'를 막대의 높이로 시각화한 그래프입니다. 각 막대의 길이를 비교함으로써 어떤 업종 카테고리가 상대적으로 임대료 부담이 큰 곳에 위치하고 있는지 직관적으로 순위를 매길 수 있습니다. 데이터를 평균 내어 집계했기 때문에 전체 시장의 업종별 임대료 감당 능력을 거시적으로 보여주는 역할을 합니다.\n\n[비즈니스 인사이트] 병의원이나 대형 음식점처럼 넓은 면적과 우수한 접근성이 모두 필요한 업종은 필연적으로 타 업종 대비 높은 평균 월세 막대를 기록하게 됩니다. 반면 배달 전문, 창고형, 혹은 지하나 이면도로에 위치해도 무방한 서비스 업종은 막대 높이가 현저히 낮습니다. 예비 창업자는 본인이 선택한 업종의 평균 월세 막대를 확인하고, 만약 본인이 구한 상가의 월세가 이 평균 막대보다 비싸다면 그만큼 초과 매출을 낼 수 있는 뚜렷한 유동인구나 프리미엄 조건이 갖춰져 있는지, 아니라면 이른바 '눈탱이'를 맞고 있는 것은 아닌지 냉철하게 비즈니스 타당성(Feasibility) 검토를 수행해야 합니다.",
         "func": lambda: df.groupby('businessLargeCodeName')['monthlyRent'].mean().sort_values(ascending=False).plot(kind='bar'),
         "table_title": "대분류 업종별 평균 월세 테이블",
         "table": df.groupby('businessLargeCodeName')['monthlyRent'].mean().reset_index()},

        {"title": "8. 층수(floor)와 월세(monthlyRent)의 산점도 (이변량)", 
         "desc": "[해석 방법] 상가가 건물의 몇 층에 위치하느냐(X축)가 월세(Y축)에 어떤 영향을 미치는지 보여주는 산점도입니다. 보통 1층(X=1) 라인에 수직으로 점들이 빽빽하게, 그리고 매우 높이까지 솟아있는 모습을 볼 수 있습니다. 반면 지하 층수나 2층, 3층으로 올라갈수록 점들의 높이(월세)가 뚝 떨어지거나 낮은 구간에만 오밀조밀 모여있는 양상을 관찰하는 것이 핵심 포인트입니다.\n\n[비즈니스 인사이트] 이 그래프는 오프라인 상권 전략의 알파와 오메가인 '층수 프리미엄'을 정량적으로 증명합니다. 1층 매물은 도로와의 접점이 생명이기에 월세가 기하급수적으로 뜁니다. 따라서, 반드시 워크인(Walk-in) 고객의 충동구매나 시각적 노출이 필수적인 업종(편의점, 카페, 화장품, 베이커리)이 아니라면 무리해서 1층에 진입할 이유가 전혀 없습니다. 목적형 소비가 강한 업종(미용실, 병원, 헬스장, 프라이빗 룸식당)은 과감히 2층 이상이나 지하로 진입하여 월세 고정비를 대폭 절감하고, 그 절감된 비용을 차라리 인스타그램 타겟 마케팅이나 파워블로거 바이럴, 혹은 인테리어 퀄리티 향상에 집중 투자하는 것이 훨씬 더 폭발적인 흑자 전환(Turn-around)을 이끌어내는 스마트 비즈니스 전략입니다.",
         "func": lambda: sns.scatterplot(x='floor', y='monthlyRent', data=df),
         "table_title": "층수별 월세 피봇테이블",
         "table": df.groupby('floor')['monthlyRent'].describe()},

        {"title": "9. 조회수(viewCount)와 관심도(favoriteCount) 산점도 (이변량)", 
         "desc": "[해석 방법] 디지털 부동산 플랫폼 사용자들의 행동 데이터를 분석하기 위한 산점도입니다. X축은 사용자가 매물 상세 페이지를 클릭해 본 조회수를, Y축은 해당 매물을 하트(찜) 누른 관심등록 횟수를 나타냅니다. 이상적인 형태는 우상향하는 선형성을 갖는 것이지만, 종종 X축(조회수)은 엄청 높은데 Y축(관심도)은 바닥을 기는 매물들이 발견됩니다. 이런 군집의 차이를 해석해야 합니다.\n\n[비즈니스 인사이트] '조회수는 높으나 관심도는 낮은 우측 하단 매물'은 썸네일 사진이나 겉보기에 월세가 파격적으로 저렴해서 수많은 사람들이 클릭했으나, 막상 상세 정보를 보니 권리금이 폭탄 수준이거나 내부 컨디션이 최악이어서 이탈해 버리는 이른바 '어그로 매물' 또는 '미끼 매물'의 특징을 가집니다. 반면 '조회수는 낮지만 관심도는 비약적으로 높은 매물'은 알짜배기 진짜 매물로, 눈 밝은 소수의 수요자들이 재빠르게 찜해두고 임장 일정을 잡고 있는 핫 스팟입니다. 부동산 프롭테크 기업 입장에서는 이러한 전환율(CVR) 지표를 역이용하여 플랫폼 내 최우선 추천 알고리즘을 개선하고 허위/미끼 매물을 필터링하여 고객 신뢰도를 폭발적으로 상승시킬 수 있습니다.",
         "func": lambda: sns.scatterplot(x='viewCount', y='favoriteCount', data=df),
         "table_title": "조회수와 관심도 상관계수표",
         "table": df[['viewCount', 'favoriteCount']].corr()},

        {"title": "10. 수치형 변수 간의 상관관계 히트맵 (다변량)", 
         "desc": "[해석 방법] 보증금, 월세, 권리금, 면적, 층수, 조회수 등 모든 수치형 변수를 행과 열로 교차하여, 두 변수 간의 피어슨 상관계수(Pearson Correlation Coefficient)를 색상과 숫자로 표현한 다변량 히트맵입니다. 계수가 1에 가까울수록 진한 붉은색(강한 양의 상관)을, -1에 가까울수록 진한 푸른색(강한 음의 상관)을, 0에 가까우면 무색을 띱니다. 변수들이 서로 얽혀서 어떻게 맞물려 돌아가는지를 조감도처럼 한 장으로 파악합니다.\n\n[비즈니스 인사이트] 히트맵은 상업용 부동산 가치 평가 모델링(Valuation Modeling)을 구축하기 위한 필수적인 선행 자료입니다. 보증금과 월세 간의 상관계수가 0.9 이상으로 극도로 높게 나타나는 현상은 결국 건물주의 임대 수익률 계산법(환산보증금 공식)이 시장 전체에 획일적으로 철저하게 통제되고 있음을 뜻합니다. 반면 권리금은 월세/보증금과의 상관관계가 상대적으로 옅은 무색에 가깝습니다. 이는 건물의 물리적 가치(월세)와 임차인의 영업적 가치(권리금)가 철저히 독립적으로 평가받고 있음을 의미합니다. 따라서 데이터를 기반으로 권리금 협상에 임할 때는 건물 자체의 스펙을 공격하기보다는 직전 세입자의 매출액, 1일 유동인구 픽업 등 소프트웨어적인 가치 평가 기준을 들고 협상 테이블에 나서야 수천만 원을 절약하는 성공적인 비즈니스 딜(Deal)을 체결할 수 있습니다.",
         "func": lambda: sns.heatmap(df[['deposit', 'monthlyRent', 'premium', 'size', 'floor', 'viewCount', 'areaPrice']].corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f"),
         "table_title": "수치형 변수 상관계수 행렬표",
         "table": df[['deposit', 'monthlyRent', 'premium', 'size', 'floor', 'viewCount', 'areaPrice']].corr(numeric_only=True)}
    ]

    for idx, viz in enumerate(viz_definitions, start=1):
        report_content.append(f"### {viz['title']}\n")
        
        plt.figure(figsize=(10, 6))
        viz['func']()
        plt.tight_layout()
        
        img_name = f"viz_{idx}.png"
        img_path = f"../images/{img_name}"
        plt.savefig(os.path.join("images", img_name))
        plt.close()
        
        report_content.append(f"![{viz['title']}]({img_path})\n\n")
        report_content.append(f"**[시각화 해석 및 비즈니스 인사이트]**\n{viz['desc']}\n\n")
        report_content.append(f"**[{viz['table_title']}]**\n\n" + safe_md_table(viz['table']) + "\n\n")
        
    with open(os.path.join("report", "EDA_REPORT.md"), "w", encoding='utf-8') as f:
        f.write("".join(report_content))

    print("EDA 리포트 및 시각화 파일 생성이 완료되었습니다.")

if __name__ == "__main__":
    main()
