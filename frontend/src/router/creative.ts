import type { RouteRecordRaw } from 'vue-router'

export const creativeRoutes: Array<RouteRecordRaw> = [
  {
    path: '/creative',
    component: () => import('@/layouts/CreativeLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'projects',
        name: 'ProjectList',
        component: () => import('@/views/creative/A1-ProjectList.vue'),
      },
      {
        path: 'projects/new',
        name: 'NewProject',
        component: () => import('@/views/creative/A2-NewProject.vue'),
      },
      {
        path: 'projects/:id/document',
        name: 'DocumentAnalysis',
        component: () => import('@/views/creative/A3-DocumentAnalysis.vue'),
      },
      {
        path: 'projects/:id/market',
        name: 'MarketAnalysis',
        component: () => import('@/views/creative/A4-MarketAnalysis.vue'),
      },
      {
        path: 'projects/:id/ideas',
        name: 'IdeaGeneration',
        component: () => import('@/views/creative/A5-IdeaGeneration.vue'),
      },
      {
        path: 'projects/:id/images',
        name: 'ImageGeneration',
        component: () => import('@/views/creative/A6-ImageGeneration.vue'),
      },
      {
        path: 'projects/:id/solution',
        name: 'SolutionDesign',
        component: () => import('@/views/creative/A7-SolutionDesign.vue'),
      },
      {
        path: 'projects/:id/evaluation',
        name: 'ProjectEvaluation',
        component: () => import('@/views/creative/A8-ProjectEvaluation.vue'),
      },
      {
        path: 'projects/:id/export',
        name: 'ProjectExport',
        component: () => import('@/views/creative/A9-ProjectExport.vue'),
      },
      {
        path: 'projects/:id/settings',
        name: 'ProjectSettings',
        component: () => import('@/views/creative/A10-ProjectSettings.vue'),
      }
    ]
  }
] 