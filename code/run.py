from crawl import crawl_all_urls
from make_embedding import make_embedding_db
# from make_answer import answer_question
from rag_answer import answer_question
from test_similarity import compute_val

if __name__ == "__main__":
    crawl_all_urls()
    make_embedding_db()
    answer_question()
    compute_val()
