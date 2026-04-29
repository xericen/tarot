"""
타로 78장 RAG 지식 베이스 구축 스크립트
- DB의 fortunes(card_id, message) 테이블에서 키워드 데이터 로드
- 78장 카드별로 정방향/역방향/영역(love/finance/health/work) 청크 생성
- ChromaDB(/opt/app/project/main/data/rag)에 저장

실행:
    python3 /opt/app/project/main/scripts/build_rag_db.py
"""

import os
import sys
import pymysql
import chromadb

DB_DIR = "/opt/app/project/main/data/rag"
COLLECTION = "tarot_knowledge"

# 78장 영문 카드 이름
TAROT_CARDS = [
    "The Fool","The Magician","The High Priestess","The Empress","The Emperor",
    "The Hierophant","The Lovers","The Chariot","Strength","The Hermit",
    "Wheel of Fortune","Justice","The Hanged Man","Death","Temperance",
    "The Devil","The Tower","The Star","The Moon","The Sun","Judgement","The World",
    "Ace of Wands","Two of Wands","Three of Wands","Four of Wands","Five of Wands",
    "Six of Wands","Seven of Wands","Eight of Wands","Nine of Wands","Ten of Wands",
    "Page of Wands","Knight of Wands","Queen of Wands","King of Wands",
    "Ace of Cups","Two of Cups","Three of Cups","Four of Cups","Five of Cups",
    "Six of Cups","Seven of Cups","Eight of Cups","Nine of Cups","Ten of Cups",
    "Page of Cups","Knight of Cups","Queen of Cups","King of Cups",
    "Ace of Swords","Two of Swords","Three of Swords","Four of Swords","Five of Swords",
    "Six of Swords","Seven of Swords","Eight of Swords","Nine of Swords","Ten of Swords",
    "Page of Swords","Knight of Swords","Queen of Swords","King of Swords",
    "Ace of Pentacles","Two of Pentacles","Three of Pentacles","Four of Pentacles","Five of Pentacles",
    "Six of Pentacles","Seven of Pentacles","Eight of Pentacles","Nine of Pentacles","Ten of Pentacles",
    "Page of Pentacles","Knight of Pentacles","Queen of Pentacles","King of Pentacles"
]

# 한국어 카드명 (간단 매핑 — 타로 표준)
TAROT_NAMES_KO = [
    "바보","마법사","여사제","여황제","황제","교황","연인","전차","힘","은둔자",
    "운명의 수레바퀴","정의","매달린 사람","죽음","절제","악마","탑","별","달","태양","심판","세계",
    "완드 에이스","완드 2","완드 3","완드 4","완드 5","완드 6","완드 7","완드 8","완드 9","완드 10",
    "완드 페이지","완드 기사","완드 여왕","완드 왕",
    "컵 에이스","컵 2","컵 3","컵 4","컵 5","컵 6","컵 7","컵 8","컵 9","컵 10",
    "컵 페이지","컵 기사","컵 여왕","컵 왕",
    "소드 에이스","소드 2","소드 3","소드 4","소드 5","소드 6","소드 7","소드 8","소드 9","소드 10",
    "소드 페이지","소드 기사","소드 여왕","소드 왕",
    "펜타클 에이스","펜타클 2","펜타클 3","펜타클 4","펜타클 5","펜타클 6","펜타클 7","펜타클 8","펜타클 9","펜타클 10",
    "펜타클 페이지","펜타클 기사","펜타클 여왕","펜타클 왕"
]


# 슈트별 일반 의미 (Minor Arcana)
SUIT_MEANING = {
    "Wands": {"element": "불", "domain": "열정·창의·행동·일", "energy": "능동성과 추진력"},
    "Cups": {"element": "물", "domain": "감정·관계·사랑·직관", "energy": "감수성과 흐름"},
    "Swords": {"element": "공기", "domain": "사고·소통·갈등·지성", "energy": "결단과 명료함"},
    "Pentacles": {"element": "흙", "domain": "물질·재정·일·건강", "energy": "안정과 결실"},
}


def get_suit(card_name):
    if "Wands" in card_name: return "Wands"
    if "Cups" in card_name: return "Cups"
    if "Swords" in card_name: return "Swords"
    if "Pentacles" in card_name: return "Pentacles"
    return None


def gen_reversed(keywords_ko):
    """정방향 키워드를 역방향 의미로 자동 생성"""
    return f"역방향에서는 '{keywords_ko}' 에너지가 억압·왜곡·지연되거나 내면으로 향합니다. 균형이 깨지거나 회피·집착·과잉의 양상으로 나타날 수 있습니다."


def gen_love(card_name_ko, keywords):
    base = f"애정운: '{keywords}' 에너지가 관계에 미치는 영향. "
    return base + "솔로는 새로운 만남의 신호일 수 있고, 커플은 관계의 현재 흐름을 비춥니다. 진솔함과 교감이 핵심입니다."


def gen_finance(card_name_ko, keywords):
    return f"재정운: '{keywords}' 흐름이 금전 영역에 적용됩니다. 큰 결정 전 정보 수집이 필요하며, 작은 변화가 누적되어 큰 차이를 만듭니다."


def gen_health(card_name_ko, keywords):
    return f"건강운: '{keywords}' 카드는 심신의 균형을 권합니다. 충분한 휴식과 규칙적 생활, 감정 정화가 도움됩니다."


def gen_work(card_name_ko, keywords):
    return f"일·진로운: '{keywords}' 에너지가 직업 영역에 적용됩니다. 동료와의 협업·자기 신뢰·꾸준한 노력이 결실을 만듭니다."


def main():
    print("[1/4] DB에서 78장 키워드 로드...")
    conn = pymysql.connect(host='172.21.64.212', port=3306, user='root', password='qwer', database='tarot', charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("SELECT card_id, message FROM fortunes ORDER BY card_id")
    rows = cur.fetchall()
    keywords_map = {r[0]: r[1] or "" for r in rows}
    conn.close()
    print(f"    DB에서 {len(keywords_map)}장 로드")

    print("[2/4] ChromaDB 초기화...")
    os.makedirs(DB_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=DB_DIR)
    # 기존 컬렉션 제거 후 재구축
    try:
        client.delete_collection(name=COLLECTION)
    except Exception:
        pass
    col = client.create_collection(name=COLLECTION)

    print("[3/4] 78장 청크 생성...")
    docs = []
    metas = []
    ids = []

    for card_id in range(78):
        card_en = TAROT_CARDS[card_id] if card_id < len(TAROT_CARDS) else f"Card #{card_id}"
        card_ko = TAROT_NAMES_KO[card_id] if card_id < len(TAROT_NAMES_KO) else card_en
        kw = keywords_map.get(card_id, "")
        suit = get_suit(card_en)

        # 청크 1: 정방향 핵심 의미
        upright = f"{card_en} ({card_ko}) — 정방향 키워드: {kw}. "
        if suit:
            sm = SUIT_MEANING[suit]
            upright += f"{suit} 슈트({sm['element']}, {sm['domain']})로서 {sm['energy']}을 상징합니다."
        docs.append(upright)
        metas.append({"card_id": card_id, "card_name": card_en, "card_name_ko": card_ko, "chunk_type": "upright"})
        ids.append(f"c{card_id}_upright")

        # 청크 2: 역방향
        reversed_text = f"{card_en} ({card_ko}) — 역방향: {gen_reversed(kw)}"
        docs.append(reversed_text)
        metas.append({"card_id": card_id, "card_name": card_en, "card_name_ko": card_ko, "chunk_type": "reversed"})
        ids.append(f"c{card_id}_reversed")

        # 청크 3~6: 4영역
        for area, gen_fn in [("love", gen_love), ("finance", gen_finance), ("health", gen_health), ("work", gen_work)]:
            text = f"{card_en} ({card_ko}) — {gen_fn(card_ko, kw)}"
            docs.append(text)
            metas.append({"card_id": card_id, "card_name": card_en, "card_name_ko": card_ko, "chunk_type": area})
            ids.append(f"c{card_id}_{area}")

    print(f"    생성된 청크: {len(docs)}개 (78장 × 6 = 468)")

    print("[4/4] ChromaDB 임베딩 및 저장...")
    # 배치로 추가 (기본 임베딩: all-MiniLM-L6-v2)
    BATCH = 100
    for i in range(0, len(docs), BATCH):
        col.add(
            documents=docs[i:i+BATCH],
            metadatas=metas[i:i+BATCH],
            ids=ids[i:i+BATCH]
        )
        print(f"    {i+BATCH if i+BATCH < len(docs) else len(docs)}/{len(docs)}")

    final_count = col.count()
    print(f"\n✅ 완료: {final_count}개 청크 저장")
    print(f"   DB 위치: {DB_DIR}")

    # 샘플 검색 테스트
    print("\n[테스트] 'The Fool 사랑' 검색...")
    res = col.query(query_texts=["The Fool 사랑"], n_results=3)
    for d, m in zip(res["documents"][0], res["metadatas"][0]):
        print(f"  - [{m['card_name']}/{m['chunk_type']}] {d[:80]}...")


if __name__ == "__main__":
    main()
