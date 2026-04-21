-- Initialize database for EduRAG system
-- This script runs when MySQL container starts

USE subjects_kg;

-- Create conversations table for storing chat history
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    INDEX idx_session_id (session_id),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create knowledge base table for BM25 search (if needed)
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_subject (subject),
    FULLTEXT idx_question_answer (question, answer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data for testing (optional)
INSERT IGNORE INTO knowledge_base (subject, question, answer) VALUES
('ai', '什么是人工智能？', '人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。'),
('ai', '机器学习的类型有哪些？', '机器学习主要分为监督学习、无监督学习和强化学习三大类。'),
('java', 'Java的特点是什么？', 'Java具有平台无关性、面向对象、安全性、多线程、分布式等特点。'),
('java', '什么是Java虚拟机？', 'Java虚拟机是一个可以执行Java字节码的虚拟计算机系统。'),
('test', '软件测试的目的是什么？', '软件测试的目的是发现软件中的缺陷，确保软件质量满足用户需求。'),
('ops', '什么是DevOps？', 'DevOps是一种软件开发方法，强调开发（Dev）和运维（Ops）团队之间的协作与沟通。'),
('bigdata', '大数据的特点是什么？', '大数据具有Volume（大量）、Velocity（高速）、Variety（多样）、Value（价值）四个特点。');

-- Create user for application (optional, for production)
-- CREATE USER IF NOT EXISTS 'eduraq_user'@'%' IDENTIFIED BY 'eduraq_password';
-- GRANT ALL PRIVILEGES ON subjects_kg.* TO 'eduraq_user'@'%';
-- FLUSH PRIVILEGES;

SELECT 'Database initialization completed successfully!' AS message;