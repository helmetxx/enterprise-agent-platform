CREATE TABLE creative_projects (
  id VARCHAR(36) PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'draft',
  tags TEXT[], -- PostgreSQL数组类型
  members TEXT[],
  visibility VARCHAR(20) NOT NULL DEFAULT 'private',
  user_id VARCHAR(36) NOT NULL,
  enterprise_id VARCHAR(36) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (enterprise_id) REFERENCES enterprises(id)
);

CREATE TABLE document_analyses (
  id VARCHAR(36) PRIMARY KEY,
  project_id VARCHAR(36) NOT NULL,
  analysis_type VARCHAR(50) NOT NULL,
  content JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (project_id) REFERENCES creative_projects(id) ON DELETE CASCADE
);

-- 其他相关表... 