// HabitFlow - Main JavaScript

// API Base URL
const API_BASE = '/api';

// Global state
let currentUser = null;
let habits = [];
let categories = [];

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuthStatus();
    setupTheme();
});

// ==================== Authentication ====================

async function checkAuthStatus() {
    try {
        const response = await fetch(`${API_BASE}/auth/me`);
        if (response.ok) {
            currentUser = await response.json();
            showUserMenu();
        } else {
            showAuthButtons();
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
    }
}

function showAuthButtons() {
    document.getElementById('authButtons').classList.remove('hidden');
    document.getElementById('userMenu').classList.add('hidden');
}

function showUserMenu() {
    document.getElementById('authButtons').classList.add('hidden');
    document.getElementById('userMenu').classList.remove('hidden');
}

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, remember_me: rememberMe })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            closeLoginModal();
            showToast('Logged in successfully!', 'success');
            showUserMenu();
            // Redirect to dashboard after a short delay
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        } else {
            showToast(data.error || 'Login failed', 'error');
        }
    } catch (error) {
        showToast('An error occurred', 'error');
        console.error('Login error:', error);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const full_name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name, email, username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            closeRegisterModal();
            showToast('Account created successfully!', 'success');
            showUserMenu();
            // Initialize default categories
            await initializeDefaultCategories();
            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        } else {
            showToast(data.error || 'Registration failed', 'error');
        }
    } catch (error) {
        showToast('An error occurred', 'error');
        console.error('Register error:', error);
    }
}

async function logout() {
    try {
        const response = await fetch(`${API_BASE}/auth/logout`, { method: 'POST' });
        if (response.ok) {
            currentUser = null;
            showAuthButtons();
            showToast('Logged out successfully', 'success');
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
}

async function initializeDefaultCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories/init-defaults`, { method: 'POST' });
        if (response.ok) {
            console.log('Default categories initialized');
        }
    } catch (error) {
        console.error('Error initializing categories:', error);
    }
}

// ==================== Modal Controls ====================

function showLoginModal() {
    document.getElementById('loginModal').classList.remove('hidden');
}

function closeLoginModal() {
    document.getElementById('loginModal').classList.add('hidden');
}

function showRegisterModal() {
    document.getElementById('registerModal').classList.remove('hidden');
}

function closeRegisterModal() {
    document.getElementById('registerModal').classList.add('hidden');
}

function switchToLogin() {
    closeRegisterModal();
    showLoginModal();
}

function switchToRegister() {
    closeLoginModal();
    showRegisterModal();
}

// Close modals when clicking outside
document.addEventListener('click', (e) => {
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    
    if (e.target === loginModal) closeLoginModal();
    if (e.target === registerModal) closeRegisterModal();
});

// ==================== UI Utilities ====================

function showToast(message, type = 'info', duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 toast ${type}`;
    toast.classList.remove('hidden');
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, duration);
}

function scrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// ==================== Theme Management ====================

function setupTheme() {
    const savedTheme = localStorage.getItem('theme') || 'system';
    applyTheme(savedTheme);
}

function applyTheme(theme) {
    const isDark = theme === 'dark' || 
                   (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    
    if (isDark) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
    
    localStorage.setItem('theme', theme);
}

function toggleTheme() {
    const currentTheme = localStorage.getItem('theme') || 'system';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(newTheme);
}

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const theme = localStorage.getItem('theme') || 'system';
    if (theme === 'system') {
        setupTheme();
    }
});

// ==================== API Helpers ====================

async function fetchAPI(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        
        if (response.status === 401) {
            // Unauthorized, redirect to login
            window.location.href = '/';
            return null;
        }
        
        return response;
    } catch (error) {
        console.error(`API Error: ${endpoint}`, error);
        showToast('An error occurred', 'error');
        return null;
    }
}

// ==================== Habits Management ====================

async function loadHabits() {
    const response = await fetchAPI('/habits');
    if (response?.ok) {
        habits = await response.json();
        return habits;
    }
    return [];
}

async function createHabit(habitData) {
    const response = await fetchAPI('/habits', 'POST', habitData);
    if (response?.ok) {
        const data = await response.json();
        showToast('Habit created successfully', 'success');
        return data.habit;
    }
    return null;
}

async function updateHabit(habitId, habitData) {
    const response = await fetchAPI(`/habits/${habitId}`, 'PUT', habitData);
    if (response?.ok) {
        const data = await response.json();
        showToast('Habit updated successfully', 'success');
        return data.habit;
    }
    return null;
}

async function deleteHabit(habitId) {
    const response = await fetchAPI(`/habits/${habitId}`, 'DELETE');
    if (response?.ok) {
        showToast('Habit deleted successfully', 'success');
        return true;
    }
    return false;
}

async function archiveHabit(habitId) {
    const response = await fetchAPI(`/habits/${habitId}/archive`, 'POST');
    if (response?.ok) {
        showToast('Habit archived', 'success');
        return true;
    }
    return false;
}

async function restoreHabit(habitId) {
    const response = await fetchAPI(`/habits/${habitId}/restore`, 'POST');
    if (response?.ok) {
        showToast('Habit restored', 'success');
        return true;
    }
    return false;
}

async function toggleFavorite(habitId) {
    const response = await fetchAPI(`/habits/${habitId}/toggle-favorite`, 'POST');
    if (response?.ok) {
        return true;
    }
    return false;
}

// ==================== Categories Management ====================

async function loadCategories() {
    const response = await fetchAPI('/categories');
    if (response?.ok) {
        categories = await response.json();
        return categories;
    }
    return [];
}

async function createCategory(categoryData) {
    const response = await fetchAPI('/categories', 'POST', categoryData);
    if (response?.ok) {
        const data = await response.json();
        showToast('Category created', 'success');
        return data.category;
    }
    return null;
}

// ==================== Activity Logging ====================

async function logActivity(habitId, logData) {
    const response = await fetchAPI('/logs', 'POST', {
        habit_id: habitId,
        ...logData
    });
    if (response?.ok) {
        const data = await response.json();
        showToast('Activity logged successfully', 'success');
        return data.log;
    }
    return null;
}

async function loadActivityLogs(habitId, dateFrom = null, dateTo = null) {
    let endpoint = `/logs?habit_id=${habitId}`;
    if (dateFrom) endpoint += `&date_from=${dateFrom}`;
    if (dateTo) endpoint += `&date_to=${dateTo}`;
    
    const response = await fetchAPI(endpoint);
    if (response?.ok) {
        return await response.json();
    }
    return [];
}

// ==================== Dashboard ====================

async function loadDashboard() {
    const response = await fetchAPI('/dashboard');
    if (response?.ok) {
        return await response.json();
    }
    return null;
}

async function getWeeklyProgress() {
    const response = await fetchAPI('/dashboard/weekly-progress');
    if (response?.ok) {
        return await response.json();
    }
    return null;
}

// ==================== Statistics ====================

async function getStatisticsOverview(days = 30) {
    const response = await fetchAPI(`/statistics/overview?days=${days}`);
    if (response?.ok) {
        return await response.json();
    }
    return null;
}

async function getHabitStatistics(habitId, days = 90) {
    const response = await fetchAPI(`/statistics/habit/${habitId}?days=${days}`);
    if (response?.ok) {
        return await response.json();
    }
    return null;
}

// ==================== Profile ====================

async function getProfile() {
    const response = await fetchAPI('/profile');
    if (response?.ok) {
        return await response.json();
    }
    return null;
}

async function updateProfile(profileData) {
    const response = await fetchAPI('/profile', 'PUT', profileData);
    if (response?.ok) {
        const data = await response.json();
        showToast('Profile updated successfully', 'success');
        return data.user;
    }
    return null;
}

// ==================== Chart Helpers ====================

function createProgressChart(canvasId, label, data, backgroundColor = '#3b82f6') {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: label,
                data: data.values,
                backgroundColor: backgroundColor,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function createLineChart(canvasId, label, data, borderColor = '#3b82f6') {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: label,
                data: data.values,
                borderColor: borderColor,
                backgroundColor: borderColor + '20',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: borderColor,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Export for use in other files
window.HabitFlow = {
    api: {
        fetchAPI,
        loadHabits,
        createHabit,
        updateHabit,
        deleteHabit,
        archiveHabit,
        restoreHabit,
        toggleFavorite,
        loadCategories,
        createCategory,
        logActivity,
        loadActivityLogs,
        loadDashboard,
        getStatisticsOverview,
        getHabitStatistics,
        getProfile,
        updateProfile,
        getWeeklyProgress
    },
    ui: {
        showToast,
        scrollTo,
        applyTheme,
        toggleTheme
    },
    chart: {
        createProgressChart,
        createLineChart
    }
};
