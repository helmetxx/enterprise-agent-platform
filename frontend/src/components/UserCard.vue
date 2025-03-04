<template>
  <div class="user-card">
    <div class="avatar">
      <common-avatar :src="user.avatar" :size="64" />
    </div>
    <div class="info">
      <h3 class="name">{{ user.name }}</h3>
      <p class="email">{{ user.email }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import CommonAvatar from './common/Avatar.vue'

defineProps({
  user: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.user-card {
  display: flex;
  align-items: center;
  padding: 16px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.avatar {
  margin-right: 16px;
}

.name {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 500;
}

.email {
  margin: 0;
  color: #909399;
}
</style> 