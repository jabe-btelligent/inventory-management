<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>

      <!-- Success banner -->
      <div v-if="successMessage" class="success-banner">
        {{ successMessage }}
      </div>

      <!-- Error banner for order submission -->
      <div v-if="orderError" class="error">{{ orderError }}</div>

      <!-- Budget control card -->
      <div class="card budget-card">
        <div class="budget-header">
          <label class="budget-label">{{ t('restocking.budgetLabel') }}</label>
          <span class="budget-value">{{ formatCurrency(budget, currentCurrency) }}</span>
        </div>
        <input
          type="range"
          min="0"
          max="100000"
          step="1000"
          v-model.number="budget"
          class="budget-slider"
        />
        <div class="budget-range-labels">
          <span>{{ formatCurrency(0, currentCurrency) }}</span>
          <span>{{ formatCurrency(100000, currentCurrency) }}</span>
        </div>
      </div>

      <!-- Stats grid -->
      <div class="stats-grid">
        <div class="stat-card info">
          <div class="stat-label">{{ t('restocking.itemsRecommended') }}</div>
          <div class="stat-value">{{ itemCount }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t('restocking.estimatedCost') }}</div>
          <div class="stat-value">{{ formatCurrency(totalCost, currentCurrency) }}</div>
        </div>
        <div :class="['stat-card', budgetRemainingVariant]">
          <div class="stat-label">{{ t('restocking.budgetRemaining') }}</div>
          <div class="stat-value">{{ formatCurrency(budgetRemaining, currentCurrency) }}</div>
        </div>
      </div>

      <!-- Recommendations table -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommended') }}</h3>
          <button
            class="place-order-btn"
            :disabled="recommendations.length === 0 || submitting"
            @click="placeOrder"
          >
            {{ submitting ? t('restocking.placingOrder') : t('restocking.placeOrder') }}
          </button>
        </div>

        <div v-if="recommendations.length === 0" class="no-recommendations">
          {{ t('restocking.noRecommendations') }}
        </div>
        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('restocking.table.sku') }}</th>
                <th>{{ t('restocking.table.itemName') }}</th>
                <th>{{ t('restocking.table.trend') }}</th>
                <th class="col-num">{{ t('restocking.table.quantity') }}</th>
                <th class="col-num">{{ t('restocking.table.unitCost') }}</th>
                <th class="col-num">{{ t('restocking.table.lineCost') }}</th>
                <th class="col-num">{{ t('restocking.table.leadTime') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in recommendations" :key="item.item_sku">
                <td><strong>{{ item.item_sku }}</strong></td>
                <td>{{ item.item_name }}</td>
                <td>
                  <span :class="['badge', item.trend]">
                    {{ t('trends.' + item.trend) }}
                  </span>
                </td>
                <td class="col-num">{{ item.qty }}</td>
                <td class="col-num">{{ formatCurrencyWithDecimals(item.unit_cost, currentCurrency, 2) }}</td>
                <td class="col-num"><strong>{{ formatCurrency(item.lineCost, currentCurrency) }}</strong></td>
                <td class="col-num">{{ item.leadDays }} {{ t('dashboard.inventoryShortages.days') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'
import { formatCurrency, formatCurrencyWithDecimals } from '../utils/currency'

// Lead days by trend — increasing items are prioritized and arrive faster;
// decreasing items are never shown but defined for completeness.
const LEAD_DAYS = {
  increasing: 7,
  stable: 14,
  decreasing: 21
}

export default {
  name: 'Restocking',
  setup() {
    const { t, currentCurrency } = useI18n()
    const router = useRouter()

    const loading = ref(true)
    const error = ref(null)
    const allForecasts = ref([])
    const budget = ref(25000)
    const submitting = ref(false)
    const successMessage = ref(null)
    const orderError = ref(null)

    const loadForecasts = async () => {
      loading.value = true
      error.value = null
      try {
        allForecasts.value = await api.getDemandForecasts()
      } catch (err) {
        error.value = 'Failed to load demand forecasts: ' + err.message
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    /**
     * Recommendation algorithm:
     * 1. Drop decreasing-trend items (we only restock what's growing or stable).
     * 2. Compute qty = forecasted - current; drop items where qty <= 0.
     * 3. Sort: increasing group first, then stable; within each group sort by qty descending
     *    so highest-demand items get budget priority.
     * 4. Greedy fill: walk the sorted list and include each item if its lineCost fits within
     *    the remaining budget. We do NOT stop on first miss — we continue to smaller items
     *    that might still fit, maximising the number of items restocked.
     */
    const recommendations = computed(() => {
      const candidates = allForecasts.value
        .filter(f => f.trend !== 'decreasing')
        .map(f => ({
          ...f,
          qty: f.forecasted_demand - f.current_demand
        }))
        .filter(f => f.qty > 0)
        .sort((a, b) => {
          // increasing group before stable
          if (a.trend !== b.trend) {
            return a.trend === 'increasing' ? -1 : 1
          }
          // within group: highest qty first
          return b.qty - a.qty
        })

      const result = []
      let remaining = budget.value

      for (const item of candidates) {
        const lineCost = item.qty * item.unit_cost
        if (lineCost <= remaining) {
          result.push({
            ...item,
            lineCost,
            leadDays: LEAD_DAYS[item.trend]
          })
          remaining -= lineCost
        }
        // skip items that don't fit; continue to next (do not break)
      }

      return result
    })

    const totalCost = computed(() => recommendations.value.reduce((sum, r) => sum + r.lineCost, 0))
    const itemCount = computed(() => recommendations.value.length)
    const budgetRemaining = computed(() => budget.value - totalCost.value)

    // Show warning variant when remaining budget is less than 10% of the chosen budget
    // or when it reaches zero, to draw attention to a tight budget situation.
    const budgetRemainingVariant = computed(() => {
      if (budget.value === 0) return 'warning'
      return budgetRemaining.value / budget.value < 0.1 ? 'warning' : ''
    })

    const placeOrder = async () => {
      if (recommendations.value.length === 0 || submitting.value) return

      submitting.value = true
      orderError.value = null
      successMessage.value = null

      try {
        const payload = {
          items: recommendations.value.map(r => ({
            sku: r.item_sku,
            name: r.item_name,
            quantity: r.qty,
            unit_price: r.unit_cost,
            trend: r.trend
          })),
          total_value: totalCost.value
        }

        const order = await api.createRestockingOrder(payload)
        successMessage.value = t('restocking.orderSuccess', { orderNumber: order.order_number })

        // Navigate to /orders on the next tick so the success message is briefly visible
        await Promise.resolve()
        router.push('/orders')
      } catch (err) {
        orderError.value = t('restocking.orderError')
        console.error(err)
      } finally {
        submitting.value = false
      }
    }

    onMounted(loadForecasts)

    return {
      t,
      currentCurrency,
      loading,
      error,
      budget,
      submitting,
      successMessage,
      orderError,
      recommendations,
      totalCost,
      itemCount,
      budgetRemaining,
      budgetRemainingVariant,
      placeOrder,
      formatCurrency,
      formatCurrencyWithDecimals
    }
  }
}
</script>

<style scoped>
/* Budget control card */
.budget-card {
  margin-bottom: var(--sp-5);
}

.budget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--sp-4);
}

.budget-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.budget-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-strong);
  letter-spacing: -0.025em;
}

/* Slate-themed range slider */
.budget-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  background: var(--border);
  border-radius: 4px;
  outline: none;
  cursor: pointer;
  transition: background 0.15s ease;
}

.budget-slider:hover {
  background: #cbd5e1;
}

/* Filled track portion — browsers that support it natively */
.budget-slider::-webkit-slider-runnable-track {
  background: linear-gradient(to right, var(--accent) 0%, var(--accent) var(--fill, 50%), var(--border) var(--fill, 50%));
  height: 6px;
  border-radius: 4px;
}

.budget-slider::-moz-range-track {
  background: var(--border);
  height: 6px;
  border-radius: 4px;
}

.budget-slider::-moz-range-progress {
  background: var(--accent);
  height: 6px;
  border-radius: 4px;
}

/* Thumb */
.budget-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid var(--bg-surface);
  box-shadow: 0 1px 4px rgba(37, 99, 235, 0.4);
  cursor: pointer;
  transition: box-shadow 0.15s ease, transform 0.1s ease;
  margin-top: -7px;
}

.budget-slider::-webkit-slider-thumb:hover {
  box-shadow: 0 0 0 6px rgba(37, 99, 235, 0.15);
  transform: scale(1.05);
}

.budget-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid var(--bg-surface);
  box-shadow: 0 1px 4px rgba(37, 99, 235, 0.4);
  cursor: pointer;
}

.budget-range-labels {
  display: flex;
  justify-content: space-between;
  margin-top: var(--sp-2);
  font-size: 0.75rem;
  color: var(--text-muted);
}

/* Place order button */
.place-order-btn {
  background: var(--accent);
  color: var(--bg-surface);
  border: none;
  padding: var(--sp-2) var(--sp-5);
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.place-order-btn:hover:not(:disabled) {
  background: #1d4ed8;
  box-shadow: var(--shadow-md);
}

.place-order-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* Numeric columns: right-align for readability */
.col-num {
  text-align: right;
}

/* Empty state */
.no-recommendations {
  padding: var(--sp-6);
  text-align: center;
  color: var(--text-muted);
  font-size: 0.938rem;
}

/* Success banner */
.success-banner {
  background: #d1fae5;
  border: 1px solid #6ee7b7;
  color: #065f46;
  padding: var(--sp-4) var(--sp-5);
  border-radius: var(--radius);
  margin-bottom: var(--sp-5);
  font-size: 0.938rem;
  font-weight: 500;
}
</style>
