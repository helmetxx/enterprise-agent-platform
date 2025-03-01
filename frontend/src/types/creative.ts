export interface CreativeProject {
  id: string
  title: string
  description: string
  status: 'draft' | 'in_progress' | 'completed'
  created_at: string
  updated_at: string
  user_id: string
  enterprise_id: string
  tags: string[]
  members: string[]
  visibility: 'private' | 'team' | 'public'
}

export interface DocumentAnalysis {
  id: string
  project_id: string
  analysis_type: 'core_features' | 'feature_relations' | 'key_insights'
  content: Record<string, any>
  created_at: string
}

export interface MarketAnalysis {
  id: string
  project_id: string
  analysis_type: 'market_size' | 'competitor' | 'trend'
  analysis_data: Record<string, any>
  created_at: string
}

export interface IdeaGeneration {
  id: string
  project_id: string
  idea_content: Record<string, any>
  evaluation_score: number
  created_at: string
}

export interface GeneratedImage {
  id: string
  project_id: string
  idea_id: string
  image_url: string
  prompt_used: string
  style_config: Record<string, any>
  created_at: string
}

export type TimelineStatus = 'pending' | 'completed' | 'in_progress' | 'blocked'

export interface SolutionDesign {
  id: string
  project_id: string
  technical_solution: {
    architecture: Record<string, any>
    core_tech: Record<string, any>
    tech_stack: string[]
  }
  feasibility_study: {
    technical: Record<string, any>
    cost: Record<string, any>
    risks: Record<string, any>
  }
  implementation_path: {
    phases: Array<{
      name: string
      time: string
      status: TimelineStatus
      tasks: string[]
    }>
    resources: Record<string, any>
  }
  created_at: string
}

export interface ProjectMember {
  id: string
  name: string
  role: 'owner' | 'editor' | 'viewer'
} 