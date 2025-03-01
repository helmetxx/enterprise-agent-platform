/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module 'vue-router'
declare module 'pinia'
declare module 'axios'
declare module '@vueuse/core'
declare module 'element-plus'

// Element Plus 组件类型
declare module 'element-plus/dist/types' {
  export * from 'element-plus/es/components'
}

// 全局组件类型
declare module '@vue/runtime-core' {
  export interface GlobalComponents {
    ElButton: typeof import('element-plus')['ElButton']
    ElInput: typeof import('element-plus')['ElInput']
    ElForm: typeof import('element-plus')['ElForm']
    ElFormItem: typeof import('element-plus')['ElFormItem']
    // ... 其他使用的组件
  }
} 