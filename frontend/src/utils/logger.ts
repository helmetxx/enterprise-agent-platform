interface ImportMetaEnv {
  DEV: boolean
  // 其他环境变量...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

const isDev = import.meta.env.DEV || true  // 默认启用日志

class Logger {
  static log(...args: any[]) {
    if (isDev) {
      console.log('[App]', ...args)
    }
  }

  static error(...args: any[]) {
    if (isDev) {
      console.error('[App]', ...args)
    }
  }

  static warn(...args: any[]) {
    if (isDev) {
      console.warn('[App]', ...args)
    }
  }

  static info(...args: any[]) {
    if (isDev) {
      console.info('[App]', ...args)
    }
  }
}

export default Logger 