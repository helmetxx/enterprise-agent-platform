// Composer沟通步骤和提示词

/* 第一步：项目现状了解 */
const step1_prompt = `
我需要你先了解当前项目的情况：
1. 项目已经完成了基础框架搭建，包括：
   - 前端Vue3 + TypeScript框架
   - 后端FastAPI框架
   - MySQL数据库
   - 基础依赖组件

2. 已实现的功能：
   - 用户注册功能已完成并测试通过
   - 登录页面已实现但功能未调通

3. 代码位置：
   请扫描当前工程目录，了解现有代码结构和实现。

请确认你已了解现有代码，并告诉我是否需要更多信息。
`;

/* 第二步：UI规范更新 */
const step2_prompt = `
基于现有代码，需要更新UI样式：
1. 请参考design0122.js中的uiStyleGuide规范
2. 主要更新内容：
   - 应用深色太空主题
   - 更新组件样式（按钮、输入框、卡片等）
   - 添加动画效果（火箭、星星等装饰元素）

3. 优先更新：
   - 注册页面（参考reg.png）
   - 登录页面
   - 工作台页面（参考desktop.png）

请生成更新后的CSS和相关组件代码。
`;

/* 第三步：数据库扩展 */
const step3_prompt = `
需要扩展数据库设计：
1. 请参考design0122.js中的databaseSchema
2. 需要创建的新表：
   - creative_projects
   - document_analysis
   - market_analysis
   - idea_generations
   - generated_images
   - solution_designs

请生成建表SQL语句和相关的数据模型代码。
`;

/* 第四步：智能体功能实现 */
const step4_prompt = `
需要实现产品创意助手的功能：
1. 前端实现：
   - 10个工作页面（A1-A10）的组件代码
   - 页面路由配置
   - 状态管理

2. 后端实现：
   - 6个智能体服务的API接口
   - 与Dify平台的集成
   - 数据处理逻辑

请分模块生成代码，并说明部署步骤。
`;

/* 执行建议 */
const executionGuide = {
  step1: {
    action: "代码扫描",
    expectation: "了解现有代码结构和实现",
    output: "项目现状确认"
  },
  step2: {
    action: "UI更新",
    expectation: "统一的深色太空主题风格",
    output: "样式代码和组件更新"
  },
  step3: {
    action: "数据库扩展",
    expectation: "新增所需数据表",
    output: "SQL语句和模型代码"
  },
  step4: {
    action: "功能实现",
    expectation: "完整的智能体功能",
    output: "前后端代码"
  }
};

/* 注意事项 */
const notes = `
1. 每个步骤完成后需要确认再进行下一步
2. 保持与现有代码的一致性
3. 注意代码复用
4. 保留已实现的功能
5. 提供清晰的部署说明
`;

/* 成功标准 */
const successCriteria = {
  step1: "完全理解现有代码",
  step2: "UI风格统一且符合设计规范",
  step3: "数据库结构完整且兼容现有数据",
  step4: "功能完整且与平台无缝集成"
}; 


composer的建议,用于后续改进  

建议添加以下改进：
添加错误处理中间件
添加请求/响应拦截器
添加数据加载状态管理
添加表单验证
5. 添加文件上传进度提示
添加操作确认提示
添加权限控制
添加数据缓存机制
添加主题切换功能
添加国际化支持