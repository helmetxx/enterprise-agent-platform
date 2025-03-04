<template>
  <el-avatar :size="size" :src="avatarSrc" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { config } from '@/config'

const props = defineProps({
  src: {
    type: String,
    default: ''
  },
  size: {
    type: [Number, String],
    default: 'default'
  }
})

const avatarSrc = computed(() => {
  // 如果提供了src并且不是avatar-default.png，则使用它
  if (props.src && !props.src.includes('avatar-default.png')) {
    return props.src
  }
  // 否则使用配置中的默认头像
  return config.defaultAvatar
})
</script> 