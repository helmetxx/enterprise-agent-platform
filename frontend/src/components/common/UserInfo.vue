<template>
  <div class="user-info">
    <common-avatar :src="user?.avatar" :size="size" />
    <div v-if="showName" class="user-name">{{ user?.name || 'User' }}</div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import CommonAvatar from './Avatar.vue'

defineProps({
  user: {
    type: Object,
    default: () => ({})
  },
  size: {
    type: [Number, String],
    default: 'default'
  },
  showName: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-name {
  font-size: 14px;
  color: #606266;
}
</style> 