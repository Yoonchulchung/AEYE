from typing import List
import json

def create_table(conn):
    paper_query="""
    CREATE TABLE IF NOT EXISTS paper (
        id SERIAL PRIMARY KEY,
        title TEXT,
        authors JSONB,
        published TIMESTAMPTZ,
        abstract TEXT,
        language TEXT,
        keywords JSONB,
        category JSONB,
        
        db_status BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS paper_chunk (
        id SERIAL PRIMARY KEY,
        paper_id INT REFERENCES paper(id) ON DELETE CASCADE,

        chunk_index INT,
        section_title TEXT,
        page_start INT,
        page_end   INT,

        content TEXT,

        embedding VECTOR(768),
        
        db_status BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(paper_query)
    
    except Exception as e:
        conn.rollback()
        print(f"Soemthing wrong while creating table : {e}")
        raise e
    
def insert_paper(conn, title : str, authors : List, published : str, 
                 abstract : str, language : str, keywords : List, category : List):
    
    query = """
        INSERT INTO paper (title, authors, published, abstract, 
                            language, keywords, category)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    
    data_tuple = (title, json.dumps(authors), published, 
                  abstract, language, json.dumps(keywords), json.dumps(category))
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, data_tuple)
            
            result = cur.fetchone()
            
            if result:
                paper_id = result[0]
    
    except Exception as e:
        print(f"Something wrong while inerting paper : {e}")
        raise e

    return paper_id

def insert_paper_chunk(conn, paper_id : int, chunk_index : int, section_title :str,
                       char_start : int, char_end : int, content : str, embedding):
    
    query = """
        INSERT INTO paper_chunk (paper_id, chunk_index, section_title,
                                 char_start, char_end, content, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    
    data_tuple = (paper_id, chunk_index, section_title,
                  char_start, char_end, content, embedding)
    
    try:    
        with conn.cursor() as cur:
            cur.execute(query, data_tuple)
    
    except Exception as e:
        conn.rollback()
        print(f"Something wrong while insrting chunks : {e}")
        raise e