<template>
  <div class="user-avatar">
    <el-avatar :src="userStore.user?.avatar || config.defaultAvatar" />
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { config } from '@/config'
</script> 