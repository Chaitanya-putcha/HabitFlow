// HabitFlow Dashboard JavaScript

let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let selectedHabitId = null;
let charts = {};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    if (!currentUser) {
        window.location.href = '/';
        return;
    }

    await loadInitialData();
    await showDashboard();
});

async function loadInitialData() {
    await loadHabits();
    await loadCategories();
    updateCategoryFilters();
}

async function loadHabits() {
    const response = await HabitFlow.api.fetchAPI('/habits');
    if (response?.ok) {
        habits = await response.json();
        updateStatHabitSelect();
    }
}

async function loadCategories() {
    const response = await HabitFlow.api.fetchAPI('/categories');
    if (response?.ok) {
        categories = await response.json();
        updateCategorySelects();
    }
}

// ==================== Navigation ====================

async function showDashboard(event) {
    if (event) event.preventDefault();
    
    document.getElementById('dashboardView').classList.remove('hidden');
    document.getElementById('habitsView').classList.add('hidden');
    document.getElementById('calendarView').classList.add('hidden');
    document.getElementById('statisticsView').classList.add('hidden');
    document.getElementById('categoriesView').classList.add('hidden');
    document.getElementById('profileView').classList.add('hidden');
    
    await loadDashboardData();
}

async function showHabits(event) {
    if (event) event.preventDefault();
    
    document.getElementById('dashboardView').classList.add('hidden');
    document.getElementById('habitsView').classList.remove('hidden');
    document.getElementById('calendarView').classList.add('hidden');
    document.getElementById('statisticsView').classList.add('hidden');
    document.getElementById('categoriesView').classList.add('hidden');
    document.getElementById('profileView').classList.add('hidden');
    
    await renderHabits();
}

async function showCalendar(event) {
    if (event) event.preventDefault();
    
    document.getElementById('dashboardView').classList.add('hidden');
    document.getElementById('habitsView').classList.add('hidden');
    document.getElementById('calendarView').classList.remove('hidden');
    document.getElementById('statisticsView').classList.add('hidden');
    document.getElementById('categoriesView').classList.add('hidden');
    document.getElementById('profileView').classList.add('hidden');
    
    await renderCalendar();
}

async function showStatistics(event) {
    if (event) event.preventDefault();
    
    document.getElementById('dashboardView').classList.add('hidden');
    document.getElementById('habitsView').classList.add('hidden');
    document.getElementById('calendarView').classList.add('hidden');
    document.getElementById('statisticsView').classList.remove('hidden');
    document.getElementById('categoriesView').classList.add('hidden');
    document.getElementById('profileView').classList.add('hidden');
    
    await loadStatisticsData();
}

async function showCategories(event) {
    if (event) event.preventDefault();
    
    document.getElementById('dashboardView').classList.add('hidden');
    document.getElementById('habitsView').classList.add('hidden');
    document.getElementById('calendarView').classList.add('hidden');
    document.getElementById('statisticsView').classList.add('hidden');
    document.getElementById('categoriesView').classList.remove('hidden');
    document.getElementById('profileView').classList.add('hidden');
    
    await renderCategories();
}

async function showProfile(event) {
    if (event) event.preventDefault();
    
    document.getElementById('dashboardView').classList.add('hidden');
    document.getElementById('habitsView').classList.add('hidden');
    document.getElementById('calendarView').classList.add('hidden');
    document.getElementById('statisticsView').classList.add('hidden');
    document.getElementById('categoriesView').classList.add('hidden');
    document.getElementById('profileView').classList.remove('hidden');
    
    await loadProfileData();
}

// ==================== Dashboard ====================

async function loadDashboardData() {
    const data = await HabitFlow.api.loadDashboard();
    if (!data) return;

    // Update welcome message
    const fullName = currentUser.full_name || currentUser.username;
    document.getElementById('welcomeText').textContent = `Welcome back, ${fullName}!`;

    // Update stats
    document.getElementById('activHabitsCount').textContent = data.active_habits;
    document.getElementById('todayLogsCount').textContent = data.today_logs_count;
    document.getElementById('totalLogsCount').textContent = data.total_logs;
    
    // Current streak (max from all habits)
    const maxStreak = Math.max(...data.streaks.map(s => s.current_streak), 0);
    document.getElementById('currentStreakMax').textContent = maxStreak;

    // Render favorite habits
    renderFavoriteHabits(data.favorite_habits);

    // Render recent activities
    renderRecentActivities(data.recent_activities);

    // Load and render weekly chart
    await loadWeeklyChart();
}

function renderFavoriteHabits(habits) {
    const container = document.getElementById('favoriteHabitsContainer');
    
    if (habits.length === 0) {
        container.innerHTML = '<p class="text-gray-500">No favorite habits yet</p>';
        return;
    }

    container.innerHTML = habits.map(habit => `
        <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:shadow-md transition">
            <div class="flex items-center gap-3">
                <span class="text-2xl">${habit.icon || '📌'}</span>
                <div>
                    <h3 class="font-semibold">${habit.name}</h3>
                    <p class="text-sm text-gray-600">${habit.goal_value ? habit.goal_value + ' ' + habit.goal_unit : 'Track'}</p>
                </div>
            </div>
            <button onclick="showLogActivityModal(${habit.id})" class="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">Log</button>
        </div>
    `).join('');
}

function renderRecentActivities(logs) {
    const container = document.getElementById('recentActivitiesContainer');
    
    if (logs.length === 0) {
        container.innerHTML = '<p class="text-gray-500">No activities logged yet</p>';
        return;
    }

    container.innerHTML = logs.map(log => {
        const habit = habits.find(h => h.id === log.habit_id);
        const date = new Date(log.logged_date);
        return `
            <div class="p-4 border border-gray-200 rounded-lg">
                <div class="flex items-center justify-between mb-2">
                    <span class="font-semibold">${habit?.name || 'Unknown Habit'}</span>
                    <span class="text-sm text-gray-600">${date.toLocaleDateString()}</span>
                </div>
                ${log.value ? `<p class="text-sm text-gray-600">Value: ${log.value}</p>` : ''}
                ${log.notes ? `<p class="text-sm text-gray-600">Note: ${log.notes}</p>` : ''}
            </div>
        `;
    }).join('');
}

async function loadWeeklyChart() {
    const data = await HabitFlow.api.getWeeklyProgress();
    if (!data) return;

    const labels = data.daily_progress.map(d => {
        const date = new Date(d.date);
        return date.toLocaleDateString('en', { weekday: 'short' });
    });
    const values = data.daily_progress.map(d => d.logs_count);

    // Destroy existing chart if it exists
    if (charts.weekly) {
        charts.weekly.destroy();
    }

    charts.weekly = HabitFlow.chart.createProgressChart('weeklyChart', 'Activities', {
        labels,
        values
    }, '#3b82f6');
}

// ==================== Habits Management ====================

async function renderHabits() {
    const container = document.getElementById('habitsContainer');
    
    if (habits.length === 0) {
        container.innerHTML = '<p class="text-gray-500 col-span-full">No habits yet. Create your first habit!</p>';
        return;
    }

    container.innerHTML = habits.map(habit => `
        <div class="card cursor-pointer hover:shadow-lg" onclick="openHabitDetails(${habit.id})">
            <div class="flex items-start justify-between mb-3">
                <span class="text-4xl">${habit.icon || '📌'}</span>
                <div class="flex gap-2">
                    <button onclick="event.stopPropagation(); toggleFavorite(${habit.id})" class="text-yellow-400">
                        ${habit.is_favorite ? '⭐' : '☆'}
                    </button>
                    <button onclick="event.stopPropagation(); showHabitMenu(${habit.id})" class="text-gray-400">⋮</button>
                </div>
            </div>
            <h3 class="font-bold text-lg mb-1">${habit.name}</h3>
            <p class="text-sm text-gray-600 mb-3">${habit.description || ''}</p>
            <div class="flex justify-between text-sm">
                <span class="badge badge-primary">${habit.frequency}</span>
                <span class="text-gray-600">${habit.status}</span>
            </div>
            <button onclick="event.stopPropagation(); showLogActivityModal(${habit.id})" class="w-full mt-4 px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm font-semibold">
                Log Activity
            </button>
        </div>
    `).join('');
}

async function openHabitDetails(habitId) {
    const response = await HabitFlow.api.fetchAPI(`/habits/${habitId}`);
    if (!response?.ok) return;
    
    const data = await response.json();
    // For now, just show logs count
    HabitFlow.ui.showToast(`${data.name} has ${data.logs?.length || 0} activities`, 'info');
}

async function toggleFavorite(habitId) {
    if (await HabitFlow.api.toggleFavorite(habitId)) {
        await loadHabits();
        await renderHabits();
    }
}

function showHabitMenu(habitId) {
    const options = ['Edit', 'Archive', 'Delete', 'Cancel'];
    // Simple implementation - can be enhanced with a proper context menu
    const action = prompt('Choose action: ' + options.join(', '));
    
    if (action === 'Archive') {
        archiveHabitAction(habitId);
    } else if (action === 'Delete') {
        deleteHabitAction(habitId);
    }
}

async function archiveHabitAction(habitId) {
    if (await HabitFlow.api.archiveHabit(habitId)) {
        await loadHabits();
        await renderHabits();
    }
}

async function deleteHabitAction(habitId) {
    if (confirm('Are you sure you want to delete this habit?')) {
        if (await HabitFlow.api.deleteHabit(habitId)) {
            await loadHabits();
            await renderHabits();
        }
    }
}

function applyHabitFilters() {
    const status = document.getElementById('habitStatusFilter').value;
    const categoryId = document.getElementById('habitCategoryFilter').value;
    
    const filtered = habits.filter(h => {
        const statusMatch = !status || h.status === status;
        const categoryMatch = !categoryId || h.category_id == categoryId;
        return statusMatch && categoryMatch;
    });

    const container = document.getElementById('habitsContainer');
    if (filtered.length === 0) {
        container.innerHTML = '<p class="text-gray-500 col-span-full">No habits match your filters</p>';
        return;
    }

    container.innerHTML = habits.map(habit => `
        <div class="card cursor-pointer hover:shadow-lg" onclick="openHabitDetails(${habit.id})">
            <div class="flex items-start justify-between mb-3">
                <span class="text-4xl">${habit.icon || '📌'}</span>
                <div class="flex gap-2">
                    <button onclick="event.stopPropagation(); toggleFavorite(${habit.id})" class="text-yellow-400">
                        ${habit.is_favorite ? '⭐' : '☆'}
                    </button>
                    <button onclick="event.stopPropagation(); showHabitMenu(${habit.id})" class="text-gray-400">⋮</button>
                </div>
            </div>
            <h3 class="font-bold text-lg mb-1">${habit.name}</h3>
            <p class="text-sm text-gray-600 mb-3">${habit.description || ''}</p>
            <div class="flex justify-between text-sm">
                <span class="badge badge-primary">${habit.frequency}</span>
                <span class="text-gray-600">${habit.status}</span>
            </div>
            <button onclick="event.stopPropagation(); showLogActivityModal(${habit.id})" class="w-full mt-4 px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm font-semibold">
                Log Activity
            </button>
        </div>
    `).join('');
}

// ==================== Calendar ====================

async function renderCalendar() {
    const response = await HabitFlow.api.fetchAPI(`/calendar/${currentYear}/${currentMonth + 1}`);
    if (!response?.ok) return;

    const calendarData = await response.json();
    updateMonthYearDisplay();
    renderCalendarGrid(calendarData.calendar);
}

function updateMonthYearDisplay() {
    const monthName = new Date(currentYear, currentMonth).toLocaleDateString('en', { month: 'long', year: 'numeric' });
    document.getElementById('monthYearDisplay').textContent = monthName;
}

function renderCalendarGrid(calendar) {
    const grid = document.getElementById('calendarGrid');
    
    // Add day headers
    const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    grid.innerHTML = dayHeaders.map(day => `<div class="font-bold text-center p-2 text-gray-600">${day}</div>`).join('');
    
    // Get first day of month
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    
    // Add empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
        grid.innerHTML += '<div class="p-2"></div>';
    }
    
    // Add days of month
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    
    for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(currentYear, currentMonth, day);
        const dateKey = date.toISOString().split('T')[0];
        const dayData = calendar[dateKey];
        const isToday = new Date().toDateString() === date.toDateString();
        
        grid.innerHTML += `
            <div class="p-2 border rounded cursor-pointer hover:bg-blue-50 ${isToday ? 'bg-blue-100' : ''}" 
                 onclick="showDateDetails('${dateKey}')"
                 title="${dayData?.logs_count || 0} activities">
                <div class="font-bold">${day}</div>
                ${dayData?.logs_count ? `<div class="text-xs bg-green-500 text-white rounded px-1">📌</div>` : ''}
            </div>
        `;
    }
}

async function showDateDetails(dateKey) {
    const response = await HabitFlow.api.fetchAPI(`/calendar/date/${dateKey}`);
    if (!response?.ok) return;

    const data = await response.json();
    const date = new Date(dateKey);
    
    document.getElementById('dayDetailsContainer').classList.remove('hidden');
    document.getElementById('selectedDate').textContent = date.toLocaleDateString('en', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });

    const container = document.getElementById('dayActivitiesContainer');
    
    if (data.activities.length === 0) {
        container.innerHTML = '<p class="text-gray-500">No activities logged this day</p>';
        return;
    }

    container.innerHTML = data.activities.map(activity => `
        <div class="card">
            <h3 class="font-bold mb-2">${activity.habit.name}</h3>
            ${activity.logs.map(log => `
                <div class="text-sm text-gray-600 mb-2">
                    ${log.value ? `<p>Value: ${log.value}</p>` : ''}
                    ${log.notes ? `<p>Note: ${log.notes}</p>` : ''}
                    <p class="text-xs text-gray-500">${log.logged_time || 'No time recorded'}</p>
                </div>
            `).join('')}
        </div>
    `).join('');
}

function previousMonth() {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalendar();
}

function nextMonth() {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    renderCalendar();
}

// ==================== Statistics ====================

async function loadStatisticsData() {
    const overview = await HabitFlow.api.getStatisticsOverview(30);
    if (overview) {
        document.getElementById('statTotalLogs').textContent = overview.total_logs;
        document.getElementById('statAvgPerDay').textContent = overview.avg_logs_per_day.toFixed(1);
        document.getElementById('statCompletionRate').textContent = overview.completion_rate.toFixed(1) + '%';
    }

    // Get monthly data for chart
    const today = new Date();
    const response = await HabitFlow.api.fetchAPI(`/statistics/monthly?month=${today.getMonth() + 1}&year=${today.getFullYear()}`);
    if (response?.ok) {
        const monthlyData = await response.json();
        renderMonthlyChart(monthlyData);
    }
}

function renderMonthlyChart(data) {
    const labels = Object.keys(data.logs_by_day).map(d => {
        const date = new Date(d);
        return date.getDate();
    });
    const values = Object.values(data.logs_by_day);

    // Destroy existing chart
    if (charts.monthly) {
        charts.monthly.destroy();
    }

    charts.monthly = HabitFlow.chart.createProgressChart('monthlyChart', 'Daily Activities', {
        labels,
        values
    }, '#10b981');
}

async function loadHabitStats() {
    const habitId = document.getElementById('statHabitSelect').value;
    if (!habitId) {
        document.getElementById('habitStatsContainer').classList.add('hidden');
        return;
    }

    const stats = await HabitFlow.api.getHabitStatistics(habitId, 90);
    if (!stats) return;

    document.getElementById('habitStatsContainer').classList.remove('hidden');
    document.getElementById('habitTotalLogs').textContent = stats.total_logs;
    document.getElementById('habitAvgValue').textContent = stats.average_value.toFixed(2);
    document.getElementById('habitCompletionPct').textContent = stats.completion_percentage.toFixed(1) + '%';

    // Create trend chart
    if (charts.habitTrend) {
        charts.habitTrend.destroy();
    }

    charts.habitTrend = HabitFlow.chart.createLineChart('habitTrendChart', 'Weekly Trend', {
        labels: Object.keys(stats.logs_by_week),
        values: Object.values(stats.logs_by_week)
    }, '#8b5cf6');
}

// ==================== Categories ====================

async function renderCategories() {
    const container = document.getElementById('categoriesContainer');
    
    if (categories.length === 0) {
        container.innerHTML = '<p class="text-gray-500 col-span-full">No categories yet. Create your first category!</p>';
        return;
    }

    container.innerHTML = categories.map(category => `
        <div class="card">
            <div class="flex items-start justify-between mb-3">
                <span class="text-4xl">${category.icon || '🏷️'}</span>
                <button onclick="showCategoryMenu(${category.id})" class="text-gray-400 hover:text-gray-600">⋮</button>
            </div>
            <h3 class="font-bold text-lg mb-1">${category.name}</h3>
            <p class="text-sm text-gray-600 mb-3">${category.description || ''}</p>
            <div class="flex gap-2">
                <button onclick="editCategory(${category.id})" class="flex-1 px-3 py-1 bg-gray-200 text-sm rounded hover:bg-gray-300">Edit</button>
                <button onclick="deleteCategory(${category.id})" class="flex-1 px-3 py-1 bg-red-200 text-red-700 text-sm rounded hover:bg-red-300">Delete</button>
            </div>
        </div>
    `).join('');
}

async function deleteCategory(categoryId) {
    if (confirm('Are you sure? This will remove the category from associated habits.')) {
        const response = await HabitFlow.api.fetchAPI(`/categories/${categoryId}`, 'DELETE');
        if (response?.ok) {
            await loadCategories();
            await renderCategories();
            HabitFlow.ui.showToast('Category deleted', 'success');
        }
    }
}

function showCategoryMenu(categoryId) {
    const action = prompt('Choose action: Edit, Delete, Cancel');
    if (action === 'Edit') {
        editCategory(categoryId);
    } else if (action === 'Delete') {
        deleteCategory(categoryId);
    }
}

async function editCategory(categoryId) {
    // Simple prompt-based edit - can be enhanced
    const newName = prompt('Enter new category name:');
    if (newName) {
        const response = await HabitFlow.api.fetchAPI(`/categories/${categoryId}`, 'PUT', { name: newName });
        if (response?.ok) {
            await loadCategories();
            await renderCategories();
        }
    }
}

// ==================== Profile ====================

async function loadProfileData() {
    const profile = await HabitFlow.api.getProfile();
    if (!profile) return;

    document.getElementById('profileFullName').value = profile.full_name || '';
    document.getElementById('profileEmail').value = profile.email;
    document.getElementById('profileTimezone').value = profile.timezone;
    document.getElementById('themeSelect').value = profile.theme;
}

async function saveProfileChanges() {
    const fullName = document.getElementById('profileFullName').value;
    const timezone = document.getElementById('profileTimezone').value;
    
    const result = await HabitFlow.api.updateProfile({
        full_name: fullName,
        timezone: timezone
    });
    
    if (result) {
        currentUser = result;
    }
}

function updateThemePreference() {
    const theme = document.getElementById('themeSelect').value;
    HabitFlow.ui.applyTheme(theme);
}

// ==================== Modals ====================

function showAddHabitModal() {
    updateCategorySelects();
    document.getElementById('addHabitModal').classList.remove('hidden');
}

function closeAddHabitModal() {
    document.getElementById('addHabitModal').classList.add('hidden');
}

function showAddCategoryModal() {
    document.getElementById('addCategoryModal').classList.remove('hidden');
}

function closeAddCategoryModal() {
    document.getElementById('addCategoryModal').classList.add('hidden');
}

function showLogActivityModal(habitId) {
    selectedHabitId = habitId;
    const habit = habits.find(h => h.id === habitId);
    
    // Show/hide value input based on habit type
    const valueInput = document.getElementById('activityValueInput');
    if (habit?.habit_type === 'boolean') {
        valueInput.classList.add('hidden');
    } else {
        valueInput.classList.remove('hidden');
    }
    
    document.getElementById('logActivityModal').classList.remove('hidden');
}

function closeLogActivityModal() {
    document.getElementById('logActivityModal').classList.add('hidden');
    document.getElementById('activityValue').value = '';
    document.getElementById('activityNotes').value = '';
}

async function handleAddHabit(event) {
    event.preventDefault();

    const habitData = {
        name: document.getElementById('habitName').value,
        description: document.getElementById('habitDescription').value,
        category_id: document.getElementById('habitCategory').value || null,
        habit_type: document.getElementById('habitType').value,
        frequency: document.getElementById('habitFrequency').value,
        goal_value: parseFloat(document.getElementById('habitGoalValue').value) || null,
        goal_unit: document.getElementById('habitGoalUnit').value
    };

    const habit = await HabitFlow.api.createHabit(habitData);
    if (habit) {
        await loadHabits();
        closeAddHabitModal();
        document.getElementById('addHabitForm').reset();
    }
}

async function handleAddCategory(event) {
    event.preventDefault();

    const categoryData = {
        name: document.getElementById('categoryName').value,
        icon: document.getElementById('categoryIcon').value,
        color: document.getElementById('categoryColor').value
    };

    const category = await HabitFlow.api.createCategory(categoryData);
    if (category) {
        await loadCategories();
        closeAddCategoryModal();
    }
}

async function handleLogActivity(event) {
    event.preventDefault();

    const habit = habits.find(h => h.id === selectedHabitId);
    if (!habit) return;

    const logData = {
        value: habit.habit_type !== 'boolean' ? parseFloat(document.getElementById('activityValue').value) : null,
        notes: document.getElementById('activityNotes').value
    };

    const log = await HabitFlow.api.logActivity(selectedHabitId, logData);
    if (log) {
        await loadInitialData();
        await loadDashboardData();
        closeLogActivityModal();
    }
}

// ==================== Utility Functions ====================

function updateCategorySelects() {
    const select = document.getElementById('habitCategory');
    select.innerHTML = '<option value="">Select a category</option>' + 
        categories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
}

function updateCategoryFilters() {
    const select = document.getElementById('habitCategoryFilter');
    select.innerHTML = '<option value="">All Categories</option>' + 
        categories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
}

function updateStatHabitSelect() {
    const select = document.getElementById('statHabitSelect');
    select.innerHTML = '<option value="">Select a habit to view details</option>' + 
        habits.map(h => `<option value="${h.id}">${h.name}</option>`).join('');
}

async function showProfileModal() {
    await showProfile();
}

async function showChangePasswordModal() {
    const currentPassword = prompt('Enter current password:');
    if (!currentPassword) return;
    
    const newPassword = prompt('Enter new password:');
    if (!newPassword) return;
    
    const confirmPassword = prompt('Confirm new password:');
    if (newPassword !== confirmPassword) {
        HabitFlow.ui.showToast('Passwords do not match', 'error');
        return;
    }

    const response = await HabitFlow.api.fetchAPI('/auth/change-password', 'POST', {
        current_password: currentPassword,
        new_password: newPassword
    });

    if (response?.ok) {
        HabitFlow.ui.showToast('Password changed successfully', 'success');
    } else {
        HabitFlow.ui.showToast('Failed to change password', 'error');
    }
}

async function showDeleteAccountModal() {
    const confirm = prompt('Type "DELETE" to confirm account deletion:');
    if (confirm !== 'DELETE') return;
    
    const password = prompt('Enter your password to confirm:');
    if (!password) return;

    const response = await HabitFlow.api.fetchAPI('/profile/delete-account', 'POST', { password });

    if (response?.ok) {
        HabitFlow.ui.showToast('Account deleted successfully', 'success');
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);
    } else {
        HabitFlow.ui.showToast('Failed to delete account', 'error');
    }
}

// Close modals when clicking outside
document.addEventListener('click', (e) => {
    const addHabitModal = document.getElementById('addHabitModal');
    const addCategoryModal = document.getElementById('addCategoryModal');
    const logActivityModal = document.getElementById('logActivityModal');
    
    if (e.target === addHabitModal) closeAddHabitModal();
    if (e.target === addCategoryModal) closeAddCategoryModal();
    if (e.target === logActivityModal) closeLogActivityModal();
});

// Redirect to dashboard page
if (window.location.pathname === '/dashboard') {
    // Continue normally
} else {
    // This script is being loaded, ensure we're on the right page
    console.log('Dashboard script loaded');
}
