<template>
  <el-avatar :size="size" :src="avatarSrc" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { config } from '@/config'

const props = defineProps({
  avatar: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'default'
  }
})

const avatarSrc = computed(() => props.avatar || config.defaultAvatar)
</script> 