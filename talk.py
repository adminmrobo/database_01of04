# -*- coding: utf-8 -*-
"""캐릭터 대화 톤 정의
   박사   : ~입니다 / ~합니다        (격식체)
   조수   : ~일까요? / ~일까?        (질문형)
   M-Robo : 삐빅 + ~입니다, '박사님/조수님' 호칭, 사람은 '휴먼'으로 지칭
   초파리 : ~이다 / ~다              (평서 반말)
"""

def talk_html(lines):
    out = ['<div class="talk">']
    for who, role, src, txt in lines:
        out.append('  <div class="line %s"><img alt="%s" data-src="%s">'
                   '<div class="tb"><div class="who">%s<i>%s</i></div><p>%s</p></div></div>'
                   % (who, who, src, {"doc": "박사", "asst": "조수", "fly": "초파리 연구원", "robo": "M-Robo"}[who], role, txt))
    out.append('</div>')
    return "\n".join(out)

DIALOGUES = {
"week2/index.html": [
 ("doc","설계 원리","ch_doc_front","2주차입니다. 오늘은 <b>값</b>에서 출발해 데이터베이스까지 갑니다."),
 ("asst","실습·질문","ch_asst_front","값이랑 정보는 대체 <b>뭐가 다른 걸까요?</b>"),
 ("robo","DB 안내","ch_robo_front","삐빅 — 휴먼, 제 계산으로는 <b>가공 여부</b>입니다. 박사님, 보고드립니다."),
 ("fly","코드·데이터","ch_fly_arms","재료와 요리 차이다. 그 이상도 이하도 아니다."),
],
"week2/01_data_and_information.html": [
 ("asst","실습·질문","ch_asst_front","영수증 한 장으로 뭘 알 수 있을까요?"),
 ("doc","설계 원리","ch_doc_front","한 장은 값입니다. 백 장을 모으면 <b>'점심에 잘 팔린다'</b>가 됩니다."),
 ("robo","DB 안내","ch_robo_point","삐빅 — 데이터에서 정보를 뽑는 과정을 <b>정보처리</b>라고 합니다, 조수님."),
 ("fly","코드·데이터","ch_fly_keyboard","가공 안 하면 그냥 종이다."),
],
"week2/02_database_definition.html": [
 ("asst","실습·질문","ch_asst_smug","파일을 한 폴더에 모아 두면 데이터베이스일까요?"),
 ("doc","설계 원리","ch_doc_side","아닙니다. <b>공유·통합·저장·운영</b>, 네 조건을 모두 만족해야 합니다."),
 ("robo","DB 안내","ch_robo_warn","삐빅 — 휴먼, 조건 미달입니다. 박사님, 재검토를 요청드립니다."),
 ("fly","코드·데이터","ch_fly_clipboard","남들도 쓰고, 중복은 통제되고, 저장돼 있고, 계속 바뀌어야 한다."),
],
"week2/03_data_classification.html": [
 ("asst","실습·질문","ch_asst_front","혈액형이랑 키는 둘 다 값 아닌가요?"),
 ("fly","코드·데이터","ch_fly_pointing","아니다. 혈액형은 <b>이름</b>이다. 더하기가 안 된다."),
 ("doc","설계 원리","ch_doc_front","그 차이를 <b>척도</b>라고 부릅니다. 절대 영점이 있는지가 갈림길입니다."),
 ("robo","DB 안내","ch_robo_tablet","삐빅 — 휴먼, <b>'2배'가 말이 되는지</b> 확인하시면 됩니다."),
],
"week2/04_python_lab.html": [
 ("asst","실습·질문","ch_asst_determined","딕셔너리 하나면 충분하지 않을까요?"),
 ("fly","코드·데이터","ch_fly_keyboard","충분하지 않다. 순서도 없고 제약도 없다."),
 ("robo","DB 안내","ch_robo_stack","삐빅 — 휴먼, 리스트에는 순서가 있고 <b>릴레이션에는 없습니다</b>."),
 ("doc","설계 원리","ch_doc_magic","그 차이가 다음 주차의 주제입니다."),
],
"week3/index.html": [
 ("doc","설계 원리","ch_doc_front","3주차입니다. 파일 시스템이 왜 무너지는지부터 봅니다."),
 ("asst","실습·질문","ch_asst_panic","주소 하나 바꿨는데 <b>열 곳을 고쳐야 하는 걸까요?</b>"),
 ("fly","코드·데이터","ch_fly_arms","맞다. 그게 중복의 진짜 비용이다."),
 ("robo","DB 안내","ch_robo_front","삐빅 — 박사님, <b>저널 파일과 롤백 절차</b> 준비 완료했습니다."),
],
"week3/01_file_system.html": [
 ("asst","실습·질문","ch_asst_front","같은 값이 두 군데 있으면 그냥 하나 지우면 될까요?"),
 ("doc","설계 원리","ch_doc_front","그 전에 <b>'같은 값인지' 판단</b>해야 합니다. 그 판단이 계속 비용입니다."),
 ("robo","DB 안내","ch_robo_point","삐빅 — 휴먼, <b>위치 참조</b>와 <b>내용 참조</b>를 구분해 주십시오."),
 ("fly","코드·데이터","ch_fly_crying","사람이 중복을 관리하는 순간 실패한다."),
],
"week3/02_why_dbms.html": [
 ("asst","실습·질문","ch_asst_smug","다섯 문제가 다 따로 노는 문제일까요?"),
 ("doc","설계 원리","ch_doc_side","아닙니다. 중복·종속·동시 공유·보안·회복은 결국 <b>한 뿌리</b>에서 나옵니다."),
 ("robo","DB 안내","ch_robo_tablet","삐빅 — 조수님, 문제 <b>5건 접수</b>했습니다. 우선순위는 중복입니다."),
 ("fly","코드·데이터","ch_fly_arms","파일은 값을 저장한다. 규칙은 저장하지 않는다."),
],
"week3/03_dbms_functions.html": [
 ("asst","실습·질문","ch_asst_front","정의랑 조작은 뭐가 다른 걸까요?"),
 ("doc","설계 원리","ch_doc_front","정의(DDL)는 그릇을 만들고, 조작(DML)은 그릇에 담습니다."),
 ("robo","DB 안내","ch_robo_front","삐빅 — 제어(DCL)는 담긴 것을 지킵니다. 박사님, 정리 완료입니다."),
 ("fly","코드·데이터","ch_fly_keyboard","CREATE, SELECT, GRANT. 세 단어로 기억한다."),
],
"week3/04_dbms_values.html": [
 ("asst","실습·질문","ch_asst_smug","DBMS를 쓰면 무조건 좋은 걸까요?"),
 ("doc","설계 원리","ch_doc_front","아닙니다. 중복 통제를 얻는 대신 <b>비용과 복잡성</b>을 냅니다."),
 ("robo","DB 안내","ch_robo_warn","삐빅 — 휴먼, 중앙관리에는 <b>취약점</b>도 따릅니다."),
 ("fly","코드·데이터","ch_fly_coffee","공짜는 없다. 대신 무엇을 얻는지 정확히 알면 된다."),
],
"week3/05_dbms_generations.html": [
 ("asst","실습·질문","ch_asst_front","왜 계층형은 다대다를 못 그릴까요?"),
 ("fly","코드·데이터","ch_fly_pointing","트리라서 그렇다. <b>부모가 둘일 수 없다.</b>"),
 ("doc","설계 원리","ch_doc_front","그래서 네트워크형이 그래프로, 관계형이 표로, NoSQL이 유연한 스키마로 이어졌습니다."),
 ("robo","DB 안내","ch_robo_stack","삐빅 — 세대별 한계를 <b>순서대로</b> 기억하시면 됩니다, 박사님."),
],
"week4/index.html": [
 ("doc","설계 원리","ch_doc_front","4주차입니다. 시스템을 이해하고, 현실을 표로 옮깁니다."),
 ("asst","실습·질문","ch_asst_front","이름을 바꾸면 테이블을 다 고쳐야 할까요?"),
 ("robo","DB 안내","ch_robo_tablet","삐빅 — 아닙니다, 조수님. <b>사상 정보만</b> 수정하면 됩니다."),
 ("fly","코드·데이터","ch_fly_arms","그게 데이터 독립성이다."),
],
"week4/01_db_system.html": [
 ("asst","실습·질문","ch_asst_front","같은 데이터베이스를 왜 <b>세 눈</b>으로 볼까요?"),
 ("doc","설계 원리","ch_doc_side","사용자·설계자·시스템이 보는 층이 다르기 때문입니다. 그래서 스키마도 셋입니다."),
 ("robo","DB 안내","ch_robo_tablet","삐빅 — 휴먼, <b>외부/개념 사상</b>과 <b>개념/내부 사상</b>을 구분해 주십시오."),
 ("fly","코드·데이터","ch_fly_clipboard","층이 셋이면, 하나를 고쳐도 나머지가 안 흔들린다."),
],
"week4/02_data_modeling.html": [
 ("asst","실습·질문","ch_asst_determined","'고객이 상품을 주문한다'에서 뭘 먼저 찾아야 할까요?"),
 ("doc","설계 원리","ch_doc_front","명사부터 찾습니다. <b>고객</b>과 <b>상품</b>이 개체입니다."),
 ("robo","DB 안내","ch_robo_point","삐빅 — 동사는 관계입니다, 조수님. <b>주문</b>은 관계입니다."),
 ("fly","코드·데이터","ch_fly_keyboard","한 문장이 곧 스키마다."),
],
"week4/03_erd_practice.html": [
 ("asst","실습·질문","ch_asst_sparkle","다대다 관계는 어떻게 표로 옮길까요?"),
 ("fly","코드·데이터","ch_fly_pointing","쪼갠다. 가운데에 <b>표를 하나 더</b> 만든다."),
 ("doc","설계 원리","ch_doc_front","그 중간 테이블이 <b>관계의 속성</b>을 가집니다. 수량과 단가가 그렇습니다."),
 ("robo","DB 안내","ch_robo_stack","삐빅 — 휴먼, <b>order_item</b> 생성 준비 완료했습니다."),
],
"week4/04_relational_model.html": [
 ("asst","실습·질문","ch_asst_front","기본키가 없으면 무슨 일이 생길까요?"),
 ("doc","설계 원리","ch_doc_front","행을 구별할 수 없습니다. 같은 값이 두 번 들어가도 막을 방법이 없습니다."),
 ("robo","DB 안내","ch_robo_warn","삐빅 — <b>개체 무결성 위반</b>입니다, 박사님."),
 ("fly","코드·데이터","ch_fly_arms","키는 규칙이다. 규칙은 DBMS가 강제한다."),
],
"week4/05_rpg_case.html": [
 ("asst","실습·질문","ch_asst_front","인덱스를 많이 만들면 더 빠를까요?"),
 ("fly","코드·데이터","ch_fly_clipboard","아니다. 쓰기가 느려진다. <b>골라야 한다.</b>"),
 ("doc","설계 원리","ch_doc_front","조회 패턴을 먼저 보십시오. 활성 퀘스트 조회라면 <b>player_id + status</b>입니다."),
 ("robo","DB 안내","ch_robo_front","삐빅 — 휴먼, 응답시간 <b>3초에서 0.1초</b>로 단축되었습니다."),
],
}

# ── 1주차 (오리엔테이션) ──────────────────────────────
DIALOGUES.update({
"week1/index.html": [
 ("doc","설계 원리","ch_doc_front","1주차입니다. 오늘은 코드를 한 줄도 쓰지 않습니다. 대신 <b>어디에나 있는 데이터베이스</b>를 찾아봅니다."),
 ("asst","실습·질문","ch_asst_front","데이터베이스가 저희 주변에 정말 있을까요?"),
 ("robo","DB 안내","ch_robo_point","삐빅 — 조수님, 편의점·은행·도서관 전부입니다. 박사님, 사례 <b>8건</b> 수집 완료했습니다."),
 ("fly","코드·데이터","ch_fly_arms","도구를 배우기 전에 쓰임을 봐야 한다. 순서다."),
],
"week1/01_everyday_database.html": [
 ("asst","실습·질문","ch_asst_front","콜라 몇 개 남았는지, 그건 어디에 적혀 있는 걸까요?"),
 ("doc","설계 원리","ch_doc_front","바코드를 찍는 순간 기록됩니다. 사람이 장부를 고치는 게 아닙니다."),
 ("robo","DB 안내","ch_robo_front","삐빅 — 판매 기록 저장 → 재고 차감 → 3개 미만이면 발주 목록. 휴먼, 자동입니다."),
 ("fly","코드·데이터","ch_fly_clipboard","규칙을 기계에 적어 두면, 알바생이 바뀌어도 발주는 안 빠진다."),
],
"week1/02_db_vs_spreadsheet.html": [
 ("asst","실습·질문","ch_asst_smug","엑셀이면 충분하지 않을까요? 저는 잘 쓰고 있는데요."),
 ("doc","설계 원리","ch_doc_side","혼자 쓸 때는 충분합니다. 여럿이 오래 쓰면 <b>보장</b>이 없어서 무너집니다."),
 ("robo","DB 안내","ch_robo_warn","삐빅 — 경고. 휴먼, 엑셀은 1,048,576행이 상한입니다."),
 ("fly","코드·데이터","ch_fly_pointing","형식도 중복도 못 막는다. 사람이 지켜야 한다. 사람은 잊는다."),
],
"week1/03_db_tools.html": [
 ("asst","실습·질문","ch_asst_front","MySQL이랑 MariaDB는 이름이 왜 이렇게 비슷할까요?"),
 ("fly","코드·데이터","ch_fly_keyboard","한 뿌리다. 같은 사람이 만들었다. 딸 이름이다."),
 ("robo","DB 안내","ch_robo_tablet","삐빅 — 휴먼, SQL은 공통어입니다. 도구가 달라도 묻는 말은 같습니다."),
 ("doc","설계 원리","ch_doc_front","그래서 하나를 제대로 배우면 나머지로 옮기는 비용이 작습니다."),
],
"week1/04_habits_and_security.html": [
 ("asst","실습·질문","ch_asst_determined","선배, 저는 코딩을 잘 못하는데 괜찮을까요?"),
 ("doc","설계 원리","ch_doc_front","괜찮습니다. 필요한 것은 <b>수집·분류·정리</b> 습관입니다. 문법은 따라옵니다."),
 ("robo","DB 안내","ch_robo_warn","삐빅 — 단, 보안은 타협하지 마십시오. 휴먼, 개인정보는 무기입니다."),
 ("fly","코드·데이터","ch_fly_clipboard","중복은 적게, 이름은 하나로, 빈 값의 뜻은 정해 둔다. 그게 전부다."),
],
})
