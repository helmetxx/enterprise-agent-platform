// 设计文档修订建议

/* 1. 第3章 页面设计补充 */
const uiStyleGuide = {
  // 3.4 统一UI规范（新增章节）
  theme: {
    // Lobe Chat风格
    colors: {
      primary: '#1E1E1E',
      secondary: '#2D2D2D',
      accent: '#6B7280',
      text: {
        primary: '#FFFFFF',
        secondary: '#9CA3AF'
      }
    },
    spacing: {
      base: '16px',
      large: '24px'
    },
    borderRadius: {
      small: '8px',
      medium: '12px',
      large: '16px'
    },
    // 深色太空主题
    background: {
      primary: 'linear-gradient(180deg, #1A1A1A 0%, #0D0D0D 100%)',
      secondary: '#1E1E1E',
      elements: {
        rocket: true,
        stars: true,
        planets: true
      }
    }
  },
  
  components: {
    // 统一组件样式
    button: {
      primary: {
        background: '#3B82F6',
        hover: '#2563EB',
        text: '#FFFFFF'
      },
      secondary: {
        background: '#374151',
        hover: '#4B5563',
        text: '#FFFFFF'
      }
    },
    input: {
      background: '#2D2D2D',
      border: '1px solid #4B5563',
      text: '#FFFFFF'
    },
    card: {
      background: 'rgba(45, 45, 45, 0.7)',
      backdropFilter: 'blur(10px)'
    }
  }
};

/* 2. 第4章 数据设计补充 */
const databaseSchema = {
  // 4.1.4 产品创意相关表（新增章节）
  tables: {
    // 创意项目表
    creative_projects: `
      CREATE TABLE creative_projects (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36) NOT NULL,
        enterprise_id VARCHAR(36) NOT NULL,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status ENUM('draft', 'in_progress', 'completed') DEFAULT 'draft',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (enterprise_id) REFERENCES enterprises(id)
      );
    `,
    
    // 文档分析结果表
    document_analysis: `
      CREATE TABLE document_analysis (
        id VARCHAR(36) PRIMARY KEY,
        project_id VARCHAR(36) NOT NULL,
        analysis_type ENUM('core_features', 'feature_relations', 'key_insights'),
        content JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES creative_projects(id)
      );
    `,
    
    // 市场分析结果表
    market_analysis: `
      CREATE TABLE market_analysis (
        id VARCHAR(36) PRIMARY KEY,
        project_id VARCHAR(36) NOT NULL,
        analysis_data JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES creative_projects(id)
      );
    `,
    
    // 创意生成结果表
    idea_generations: `
      CREATE TABLE idea_generations (
        id VARCHAR(36) PRIMARY KEY,
        project_id VARCHAR(36) NOT NULL,
        idea_content JSON,
        evaluation_score DECIMAL(3,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES creative_projects(id)
      );
    `,
    
    // 图片生成结果表
    generated_images: `
      CREATE TABLE generated_images (
        id VARCHAR(36) PRIMARY KEY,
        project_id VARCHAR(36) NOT NULL,
        idea_id VARCHAR(36) NOT NULL,
        image_url VARCHAR(255),
        prompt_used TEXT,
        style_config JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES creative_projects(id),
        FOREIGN KEY (idea_id) REFERENCES idea_generations(id)
      );
    `,
    
    // 方案设计结果表
    solution_designs: `
      CREATE TABLE solution_designs (
        id VARCHAR(36) PRIMARY KEY,
        project_id VARCHAR(36) NOT NULL,
        technical_solution JSON,
        feasibility_study JSON,
        implementation_path JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES creative_projects(id)
      );
    `
  }
};

/* 3. 代码生成状态确认 */
const codeGenerationStatus = {
  phase1: {
    // 基础平台代码
    status: 'GENERATED',
    tested: {
      registration: 'PASSED',
      login: 'IN_PROGRESS'
    },
    location: 'current_project_directory'
  },
  
  phase2: {
    // 智能体代码
    status: 'PENDING',
    required: {
      frontend: [
        'A1-A10页面组件',
        'UI组件库更新',
        'CSS样式更新'
      ],
      backend: [
        '6个智能体服务',
        '新增数据库表',
        'API接口实现'
      ]
    }
  }
};

// 建议执行顺序
const implementationSteps = [
  '1. 更新现有代码的UI样式以符合新的设计规范',
  '2. 创建新的数据库表',
  '3. 生成智能体相关的后端代码',
  '4. 生成智能体相关的前端代码',
  '5. 集成测试'
]; 