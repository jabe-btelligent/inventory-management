<template>
  <div class="app" :class="{ 'sidebar-collapsed': collapsed }">

    <!-- Sidebar -->
    <aside class="sidebar">
      <!-- Brand -->
      <div v-if="collapsed" class="sidebar-brand sidebar-brand--collapsed" :title="t('nav.companyName')" :aria-label="t('nav.companyName')">
        <span class="sidebar-brand-monogram" aria-hidden="true">{{ brandInitials }}</span>
      </div>
      <div v-else class="sidebar-brand">
        <span class="sidebar-brand-name">{{ t('nav.companyName') }}</span>
        <span class="sidebar-brand-subtitle">{{ t('nav.subtitle') }}</span>
      </div>

      <!-- Navigation -->
      <nav class="side-nav" aria-label="Main navigation">

        <router-link
          to="/"
          :class="{ active: $route.path === '/' }"
          :title="t('nav.overview')"
          :aria-label="t('nav.overview')"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" /><rect x="3" y="14" width="7" height="7" /><rect x="14" y="14" width="7" height="7" />
          </svg>
          <span class="nav-label">{{ t('nav.overview') }}</span>
        </router-link>

        <router-link
          to="/inventory"
          :class="{ active: $route.path === '/inventory' }"
          :title="t('nav.inventory')"
          :aria-label="t('nav.inventory')"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" /><polyline points="3.27 6.96 12 12.01 20.73 6.96" /><line x1="12" y1="22.08" x2="12" y2="12" />
          </svg>
          <span class="nav-label">{{ t('nav.inventory') }}</span>
        </router-link>

        <router-link
          to="/orders"
          :class="{ active: $route.path === '/orders' }"
          :title="t('nav.orders')"
          :aria-label="t('nav.orders')"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="9" cy="21" r="1" /><circle cx="20" cy="21" r="1" /><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" />
          </svg>
          <span class="nav-label">{{ t('nav.orders') }}</span>
        </router-link>

        <router-link
          to="/spending"
          :class="{ active: $route.path === '/spending' }"
          :title="t('nav.finance')"
          :aria-label="t('nav.finance')"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <line x1="12" y1="1" x2="12" y2="23" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
          </svg>
          <span class="nav-label">{{ t('nav.finance') }}</span>
        </router-link>

        <router-link
          to="/demand"
          :class="{ active: $route.path === '/demand' }"
          :title="t('nav.demandForecast')"
          :aria-label="t('nav.demandForecast')"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" /><polyline points="17 6 23 6 23 12" />
          </svg>
          <span class="nav-label">{{ t('nav.demandForecast') }}</span>
        </router-link>

        <router-link
          to="/restocking"
          :class="{ active: $route.path === '/restocking' }"
          :title="t('nav.restocking')"
          :aria-label="t('nav.restocking')"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="1 4 1 10 7 10" /><polyline points="23 20 23 14 17 14" /><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15" />
          </svg>
          <span class="nav-label">{{ t('nav.restocking') }}</span>
        </router-link>

        <router-link
          to="/reports"
          :class="{ active: $route.path === '/reports' }"
          title="Reports"
          aria-label="Reports"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" />
          </svg>
          <span class="nav-label">Reports</span>
        </router-link>

      </nav>

      <!-- Sidebar bottom: ProfileMenu -->
      <div class="sidebar-bottom">
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </aside>

    <!-- Main area -->
    <div class="layout-main">

      <!-- Topbar -->
      <header class="topbar">
        <button
          class="collapse-btn"
          @click="collapsed = !collapsed"
          :aria-label="collapsed ? 'Expand sidebar' : 'Collapse sidebar'"
          :title="collapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        >
          <svg v-if="!collapsed" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="18" x2="21" y2="18" />
          </svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>

        <span class="topbar-page-title">{{ pageTitle }}</span>

        <div class="topbar-right">
          <button
            class="theme-toggle"
            @click="toggleTheme"
            :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
            :title="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
          >
            <!-- Moon: shown in light mode — clicking switches to dark -->
            <svg v-if="theme !== 'dark'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
            </svg>
            <!-- Sun: shown in dark mode — clicking switches to light -->
            <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="12" cy="12" r="5" />
              <line x1="12" y1="1" x2="12" y2="3" />
              <line x1="12" y1="21" x2="12" y2="23" />
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
              <line x1="1" y1="12" x2="3" y2="12" />
              <line x1="21" y1="12" x2="23" y2="12" />
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
            </svg>
          </button>
          <LanguageSwitcher />
        </div>
      </header>

      <FilterBar />

      <main class="main-content">
        <router-view />
      </main>
    </div>

    <!-- Modals (unchanged) -->
    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const route = useRoute()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const apiTasks = ref([])

    // Sidebar collapse state — persisted to localStorage (guarded against SSR/errors)
    const collapsed = ref(false)
    try {
      const stored = localStorage.getItem('sidebar-collapsed')
      if (stored !== null) collapsed.value = stored === 'true'
    } catch (_) { /* ignore */ }

    // Persist collapse preference
    const toggleCollapsed = () => {
      collapsed.value = !collapsed.value
      try { localStorage.setItem('sidebar-collapsed', String(collapsed.value)) } catch (_) { /* ignore */ }
    }

    // Theme state — persisted to localStorage, falls back to OS preference
    const theme = ref('light')
    try {
      const stored = localStorage.getItem('theme')
      if (stored !== null) {
        theme.value = stored
      } else {
        theme.value = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      }
    } catch (_) { /* ignore */ }

    const applyTheme = (t) => {
      try {
        document.documentElement.setAttribute('data-theme', t)
      } catch (_) { /* ignore */ }
    }

    const toggleTheme = () => {
      theme.value = theme.value === 'dark' ? 'light' : 'dark'
      try { localStorage.setItem('theme', theme.value) } catch (_) { /* ignore */ }
      applyTheme(theme.value)
    }

    // Apply theme immediately (before mount) so there's no flash
    applyTheme(theme.value)

    // Page title derived from current route
    const pageTitle = computed(() => {
      const map = {
        '/': t('nav.overview'),
        '/inventory': t('nav.inventory'),
        '/orders': t('nav.orders'),
        '/spending': t('nav.finance'),
        '/demand': t('nav.demandForecast'),
        '/restocking': t('nav.restocking'),
        '/reports': 'Reports'
      }
      return map[route.path] || ''
    })

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(() => {
      loadTasks()
      // Re-apply theme on mount to handle any SSR/hydration edge cases
      applyTheme(theme.value)
    })

    // Derive initials from the first letter of each of the first two words
    const brandInitials = computed(() => {
      const name = t('nav.companyName') || ''
      const words = name.trim().split(/\s+/).filter(Boolean)
      if (words.length === 0) return ''
      if (words.length === 1) return words[0][0].toUpperCase()
      return (words[0][0] + words[1][0]).toUpperCase()
    })

    return {
      t,
      collapsed,
      toggleCollapsed,
      theme,
      toggleTheme,
      pageTitle,
      brandInitials,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>

<style>
/* ============================================================
   Design tokens
   ============================================================ */
:root {
  --bg-app: #f8fafc;
  --bg-surface: #ffffff;
  --bg-sidebar: #0f172a;
  --bg-sidebar-hover: #1e293b;
  --border: #e2e8f0;
  --text-strong: #0f172a;
  --text: #334155;
  --text-muted: #64748b;
  --text-on-dark: #cbd5e1;
  --accent: #2563eb;
  --accent-soft: #eff6ff;
  --success: #16a34a;
  --warning: #d97706;
  --danger: #dc2626;
  --info: #2563eb;
  --sp-1: 0.25rem;
  --sp-2: 0.5rem;
  --sp-3: 0.75rem;
  --sp-4: 1rem;
  --sp-5: 1.5rem;
  --sp-6: 2rem;
  --sp-8: 3rem;
  --radius: 8px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);
  --sidebar-w: 260px;
  --sidebar-w-collapsed: 72px;
  --topbar-h: 64px;
}

/* ============================================================
   Dark mode token overrides
   ============================================================ */
:root[data-theme="dark"] {
  --bg-app: #0b1120;
  --bg-surface: #111c30;
  --bg-sidebar: #0a0f1d;
  --bg-sidebar-hover: #1e293b;
  --border: #283449;
  --text-strong: #f1f5f9;
  --text: #cbd5e1;
  --text-muted: #94a3b8;
  --text-on-dark: #cbd5e1;
  --accent: #3b82f6;
  --accent-soft: #1e293b;
  --success: #22c55e;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.5);
}

/* ============================================================
   Reset
   ============================================================ */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--bg-app);
  color: var(--text);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* ============================================================
   App shell
   ============================================================ */
.app {
  display: flex;
  min-height: 100vh;
}

/* ============================================================
   Sidebar
   ============================================================ */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: var(--sidebar-w);
  background: var(--bg-sidebar);
  color: var(--text-on-dark);
  display: flex;
  flex-direction: column;
  padding: var(--sp-4);
  z-index: 200;
  overflow: hidden;
  transition: width 0.2s ease;
}

.app.sidebar-collapsed .sidebar {
  width: var(--sidebar-w-collapsed);
}

/* Brand */
.sidebar-brand {
  display: flex;
  flex-direction: column;
  gap: var(--sp-1);
  padding: var(--sp-2) var(--sp-2) var(--sp-5);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: var(--sp-4);
  white-space: nowrap;
  overflow: hidden;
}

.sidebar-brand-name {
  font-size: 1rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.02em;
}

.sidebar-brand-subtitle {
  font-size: 0.75rem;
  color: var(--text-on-dark);
  opacity: 0.7;
}

.sidebar-brand--collapsed {
  align-items: center;
  justify-content: center;
  padding: var(--sp-2) 0 var(--sp-5);
}

.sidebar-brand-monogram {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius);
  background: var(--accent);
  color: #ffffff;
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}

/* Side nav */
.side-nav {
  display: flex;
  flex-direction: column;
  gap: var(--sp-1);
  flex: 1;
  overflow: hidden;
}

.side-nav a {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: 0.625rem var(--sp-2);
  border-radius: var(--radius);
  color: var(--text-on-dark);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  transition: background 0.15s ease, color 0.15s ease;
  position: relative;
  /* Left accent bar placeholder */
  border-left: 3px solid transparent;
}

.side-nav a:hover {
  background: var(--bg-sidebar-hover);
  color: #ffffff;
}

.side-nav a.active {
  background: var(--bg-sidebar-hover);
  color: #ffffff;
  border-left-color: var(--accent);
}

.side-nav a svg {
  flex-shrink: 0;
}

.nav-label {
  transition: opacity 0.15s ease;
}

.app.sidebar-collapsed .nav-label {
  opacity: 0;
  pointer-events: none;
}

/* Sidebar bottom */
.sidebar-bottom {
  margin-top: auto;
  padding-top: var(--sp-4);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
}

/* ============================================================
   Layout main area
   ============================================================ */
.layout-main {
  margin-left: var(--sidebar-w);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  transition: margin-left 0.2s ease;
}

.app.sidebar-collapsed .layout-main {
  margin-left: var(--sidebar-w-collapsed);
}

/* ============================================================
   Topbar
   ============================================================ */
.topbar {
  position: sticky;
  top: 0;
  height: var(--topbar-h);
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 var(--sp-6);
  gap: var(--sp-4);
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.collapse-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  background: none;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text-muted);
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

.collapse-btn:hover {
  background: var(--bg-app);
  color: var(--text-strong);
}

.topbar-page-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-strong);
  letter-spacing: -0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.topbar-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: var(--sp-2);
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  background: none;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text-muted);
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

.theme-toggle:hover {
  background: var(--bg-app);
  color: var(--text-strong);
}

/* ============================================================
   Main content
   ============================================================ */
.main-content {
  flex: 1;
  padding: var(--sp-6);
}

/* ============================================================
   Shared component styles (used by all views — must stay global)
   ============================================================ */
.page-header {
  margin-bottom: var(--sp-5);
}

.page-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--text-strong);
  margin-bottom: 0.375rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: var(--text-muted);
  font-size: 0.938rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: var(--sp-5);
}

.stat-card {
  background: var(--bg-surface);
  padding: 1.25rem;
  border-radius: 10px;
  border: 1px solid var(--border);
  transition: background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  border-color: #cbd5e1;
  box-shadow: var(--shadow-md);
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--text-strong);
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value {
  color: #ea580c;
}

.stat-card.success .stat-value {
  color: #059669;
}

.stat-card.danger .stat-value {
  color: var(--danger);
}

.stat-card.info .stat-value {
  color: var(--accent);
}

.card {
  background: var(--bg-surface);
  border-radius: 10px;
  padding: 1.25rem;
  border: 1px solid var(--border);
  margin-bottom: 1.25rem;
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--sp-4);
  padding-bottom: 0.875rem;
  border-bottom: 1px solid var(--border);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-strong);
  letter-spacing: -0.025em;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--bg-app);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

th {
  text-align: left;
  padding: 0.5rem 0.75rem;
  font-weight: 600;
  color: #475569;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid #f1f5f9;
  color: var(--text);
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: var(--bg-app);
}

.badge {
  display: inline-block;
  padding: 0.313rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success {
  background: #d1fae5;
  color: #065f46;
}

.badge.warning {
  background: #fed7aa;
  color: #92400e;
}

.badge.danger {
  background: #fecaca;
  color: #991b1b;
}

.badge.info {
  background: #dbeafe;
  color: #1e40af;
}

.badge.increasing {
  background: #d1fae5;
  color: #065f46;
}

.badge.decreasing {
  background: #fecaca;
  color: #991b1b;
}

.badge.stable {
  background: #e0e7ff;
  color: #3730a3;
}

.badge.high {
  background: #fecaca;
  color: #991b1b;
}

.badge.medium {
  background: #fed7aa;
  color: #92400e;
}

.badge.low {
  background: #dbeafe;
  color: #1e40af;
}

.loading {
  text-align: center;
  padding: var(--sp-8);
  color: var(--text-muted);
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: var(--sp-4);
  border-radius: var(--radius);
  margin: var(--sp-4) 0;
  font-size: 0.938rem;
}

/* ============================================================
   Responsive: force icon-rail at narrow viewports
   ============================================================ */
@media (max-width: 900px) {
  .sidebar {
    width: var(--sidebar-w-collapsed);
  }

  .sidebar-brand-subtitle,
  .nav-label {
    opacity: 0;
    pointer-events: none;
  }

  .layout-main {
    margin-left: var(--sidebar-w-collapsed);
  }

  /* Override any JS-driven expanded state on small screens */
  .app .sidebar {
    width: var(--sidebar-w-collapsed) !important;
  }

  .app .layout-main {
    margin-left: var(--sidebar-w-collapsed) !important;
  }
}
</style>
