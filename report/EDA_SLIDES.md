---
marp: true
theme: gaia
backgroundColor: #fff
paginate: true
header: '네모 상가 데이터 EDA 리포트'
footer: 'Nemo Stores Analysis Dashboard'
---

# 네모 상가 데이터 심층 분석
## Premium Business Insights

**작성일**: 2026-04-29
**데이터 수**: 673건

---

# 1. 데이터 프로파일링 요약

| 항목 | 수치 |
| :--- | :--- |
| **총 행(Row) 수** | 673개 |
| **총 열(Column) 수** | 40개 |
| **중복 데이터** | 0개 |
| **평균 보증금** | 약 6,895만 원 |
| **평균 권리금** | 약 4,640만 원 |

---

# 2. 핵심 비즈니스 인사이트 💡

1. **상권 양극화**: 강남/역삼 등 핵심 상권의 프라임 매물이 평균 가격을 견인하는 멱법칙 분포 확인.
2. **무권리 매물 급증**: 데이터의 절반 이상이 무권리. 소자본 창업의 기회이자 상권 쇠퇴 리스크 공존.
3. **입지 편중**: 강남역, 역삼역 인근에 매물이 고도로 집중. 2030 직장인 타겟 전략 필수.

---

# 3. 업종별 빈도 분석

![w:800](../images/cat_freq_1.png)

- **기타업종**(325건), **일반음식점**(96건) 순으로 비중이 높음.
- 요식업 및 서비스업의 치열한 경쟁 환경 시사.

---

# 4. 키워드 분석 (TF-IDF)

![w:700](../images/tfidf_keywords.png)

- **주요 키워드**: 역삼동, 강남역, 인테리어, 무권리, 초역세권.
- 수요자들은 '입지'와 '즉시 영업 가능성'을 최우선으로 고려함.

---

# 5. 임대료 분포 분석 (보증금/월세)

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
  <img src="../images/viz_1.png" width="400">
  <img src="../images/viz_2.png" width="400">
</div>

- **Right-Skewed**: 대다수는 저렴한 매물이나, 일부 프라임 매물이 가격 평균을 높임.

---

# 6. 상권 가치: 권리금 및 층수

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
  <img src="../images/viz_3.png" width="400">
  <img src="../images/viz_8.png" width="400">
</div>

- **1층 프리미엄**: 도로 접점인 1층의 월세가 압도적으로 높음.
- 목적형 업종은 2층 이상으로 진입하여 고정비 절감 권장.

---

# 7. 면적 대비 가성비 분석

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
  <img src="../images/viz_4.png" width="400">
  <img src="../images/viz_5.png" width="400">
</div>

- 회귀선 하단 매물을 공략하여 효율적인 공간 확보 가능.

---

# 8. 소비자 행동 분석

![w:800](../images/viz_9.png)

- **조회수 vs 관심도**: 단순히 싼 매물보다 '가성비+시설 완비' 매물에 실질적인 찜(Favorite)이 집중됨.

---

# 9. 결론 및 제안

1. **데이터 기반 입지 선정**: 평균값보다 중앙값(Median)을 활용한 정밀한 프라이싱 필요.
2. **전략적 출점**: 업종 특성에 맞는 층수 선택(1층 vs 2층 이상)으로 ROI 극대화.
3. **리스크 관리**: 무권리 매물의 함정을 피하고 검증된 상권을 선별하는 혜안 필요.

---

# 감사합니다!
## Q&A
