// script.js
// Core logic for Daily Bloom: Micro Habit Tracker

// Predefined habits (matching screenshot)
const defaultHabits = [
    { id: 'habit1', name: 'Walk 5K Steps', icon: '🚶', completed: false },
    { id: 'habit2', name: 'Meditate', icon: '🧘', completed: false },
    { id: 'habit3', name: 'Read 10 Min', icon: '📖', completed: false },
    { id: 'habit4', name: 'Stretch', icon: '🤸', completed: false },
    { id: 'habit5', name: 'Learn Data Science', icon: '🌱', completed: false },
];

// Initialize data from localStorage or use defaults
let data = JSON.parse(localStorage.getItem('habit-tracker-data')) || {
    habits: defaultHabits,
    progress: {},
};

// Save data to localStorage
function saveData() {
    localStorage.setItem('habit-tracker-data', JSON.stringify(data));
}

// Get today's date key (YYYY-MM-DD)
function getTodayKey() {
    return new Date().toISOString().split('T')[0];
}

// Initialize today's progress
function initializeToday() {
    const today = getTodayKey();
    if (!data.progress[today]) {
        data.progress[today] = {};
        data.habits.forEach(habit => {
            data.progress[today][habit.id] = true; // Set all to true for testing
        });
        saveData();
    }
    console.log('After initializeToday:', data.progress[today]);
}

// Render habits
function renderHabits() {
    const habitList = document.querySelector('#habit-list');
    if (!habitList) return;

    const today = getTodayKey();
    habitList.innerHTML = '';

    data.habits.forEach((habit, index) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'habit-item-wrapper fade-in';
        wrapper.setAttribute('style', `--animation-delay: ${index * 0.1}s`);

        const li = document.createElement('li');
        li.className = 'habit-item';
        li.setAttribute('data-id', habit.id);

        // Ensure the checkbox reflects the data state
        const isChecked = data.progress[today][habit.id] || false;
        li.innerHTML = `
            <input type="checkbox" id="habit-${habit.id}" ${isChecked ? 'checked' : ''} aria-label="Mark ${habit.name} as completed">
            <span class="icon">${habit.icon}</span>
            <label for="habit-${habit.id}">${habit.name}</label>
            <div class="habit-progress">
                <div class="habit-progress-fill" style="width: ${isChecked ? '100%' : '0%'}"></div>
            </div>
            <div class="habit-progress-text">${isChecked ? '100%' : '0%'}</div>
            <button class="remove-habit-btn" aria-label="Remove ${habit.name}">🗑️</button>
        `;
        wrapper.appendChild(li);
        habitList.appendChild(wrapper);

        // Checkbox event listener
        const checkbox = li.querySelector('input');
        checkbox.addEventListener('change', () => {
            data.progress[today][habit.id] = checkbox.checked;
            const progressFill = li.querySelector('.habit-progress-fill');
            const progressText = li.querySelector('.habit-progress-text');
            progressFill.style.width = checkbox.checked ? '100%' : '0%';
            progressText.textContent = checkbox.checked ? '100%' : '0%';
            saveData();
            console.log(`Checkbox changed for ${habit.name}: ${checkbox.checked}`);
            updateProgress();
        });

        // Remove button event listener
        const removeBtn = li.querySelector('.remove-habit-btn');
        removeBtn.addEventListener('click', () => {
            removeHabit(habit.id);
        });
    });

    // Force update progress after rendering
    updateProgress();
}

// Update overall progress
// Update overall progress
// Update overall progress
function updateProgress() {
    const today = getTodayKey();
    const total = data.habits.length;
    if (!data.progress[today]) {
        initializeToday();
    }
    const completed = Object.keys(data.progress[today]).reduce((count, habitId) => {
        return count + (data.progress[today][habitId] === true ? 1 : 0);
    }, 0);
    const percentage = total ? Math.round((completed / total) * 100) : 0;

    console.log('updateProgress - Data:', data.progress[today]);
    console.log('updateProgress - Completed:', completed, 'Total:', total, 'Percentage:', percentage);

    const progressFill = document.querySelector('#progress-fill');
    const progressPercentage = document.querySelector('#progress-percentage');
    const progressMessage = document.querySelector('#progress-message');
    const progressDetails = document.querySelector('#progress-details');

    if (!progressFill || !progressPercentage || !progressMessage || !progressDetails) {
        console.error('Progress elements not found:', { progressFill, progressPercentage, progressMessage, progressDetails });
        return;
    }

    // Update progress bar width and percentage text
    progressFill.style.width = `${percentage}%`;
    progressFill.setAttribute('aria-valuenow', percentage);
    progressPercentage.textContent = `${percentage}%`;

    // Trigger ripple and sparkle animations on percentage change
    progressFill.classList.remove('ripple', 'sparkle');
    void progressFill.offsetWidth; // Trigger reflow to restart animations
    progressFill.classList.add('ripple', 'sparkle');

    // Restart the percentage animation
    progressPercentage.style.animation = 'none';
    progressPercentage.offsetHeight; // Trigger reflow to restart animation
    progressPercentage.style.animation = 'percentagePop 0.5s ease forwards';

    // Update progress bar color based on percentage (for compatibility, though not used with gradient)
    progressFill.setAttribute('data-percentage', percentage);
    if (percentage === 0) {
        progressFill.setAttribute('data-percentage-range', '0');
    } else if (percentage <= 50) {
        progressFill.setAttribute('data-percentage-range', 'low');
    } else if (percentage < 100) {
        progressFill.setAttribute('data-percentage-range', 'medium');
    } else {
        progressFill.setAttribute('data-percentage-range', 'high');
    }

    // Update progress message and details
    let emoji, message, details;
    if (percentage === 0) {
        emoji = '😐';
        message = 'Let’s get started!';
        details = 'Complete your habits to see your progress grow.';
    } else if (percentage <= 50) {
        emoji = '😊';
        message = `You’re making progress! ${percentage}% done.`;
        details = 'Keep going to reach your daily goals!';
    } else if (percentage < 100) {
        emoji = '💪';
        message = `Great effort! ${percentage}% completed.`;
        details = 'You’re almost there—finish strong!';
    } else {
        emoji = '🥳';
        message = 'Amazing job! 100% completed!';
        details = 'All your habits are done for today. Keep up the fantastic work!';
    }

    progressMessage.textContent = `${emoji} ${message}`;
    progressDetails.textContent = details;

    console.log('Progress bar updated to:', progressFill.style.width);
}

// Add a new habit
function addHabit(name, icon) {
    if (!name || data.habits.some(habit => habit.name.toLowerCase() === name.toLowerCase())) {
        showToast('Habit already exists or invalid name!', 'error');
        return;
    }
    const habit = {
        id: `habit${Date.now()}`,
        name,
        icon: icon || '🌿',
        completed: false,
    };
    data.habits.push(habit);
    const today = getTodayKey();
    data.progress[today][habit.id] = false;
    saveData();
    renderHabits();
    showToast('Habit added successfully!', 'success');
}

// Remove a habit
function removeHabit(habitId) {
    if (!confirm('Are you sure you want to remove this habit?')) return;

    data.habits = data.habits.filter(habit => habit.id !== habitId);
    Object.keys(data.progress).forEach(date => {
        delete data.progress[date][habitId];
    });
    saveData();
    renderHabits();
    showToast('Habit removed successfully!', 'success');
}

// Render weekly view
function renderWeeklyView(weekOffset = 0) {
    const weeklySection = document.querySelector('#weekly-section');
    const weeklyCalendar = document.querySelector('#weekly-calendar');
    if (!weeklyCalendar) return;

    weeklyCalendar.innerHTML = '';
    const today = new Date();
    today.setDate(today.getDate() - (weekOffset * 7));

    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        const dateKey = date.toISOString().split('T')[0];
        const progress = data.progress[dateKey] || {};
        const total = data.habits.length;
        const completed = Object.values(progress).filter(Boolean).length;
        const percentage = total ? Math.round((completed / total) * 100) : 0;

        const div = document.createElement('div');
        div.className = `day-box completed-${percentage === 100 ? 'full' : percentage > 0 ? 'partial' : 'none'}`;
        div.innerHTML = `
            <span>${date.toLocaleDateString('en-US', { weekday: 'short' })}</span>
            <span>${percentage}%</span>
        `;
        weeklyCalendar.appendChild(div);
    }

    if (weeklySection) {
        weeklySection.classList.add('active');
    }
}

// Export progress to CSV
function exportToCSV() {
    const today = getTodayKey();
    const headers = ['Habit Name', 'Icon', 'Completed'];
    const rows = data.habits.map(habit => [
        habit.name,
        habit.icon,
        data.progress[today][habit.id] ? 'Yes' : 'No',
    ]);

    const csvContent = [
        headers.join(','),
        ...rows.map(row => row.join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `habit-progress-${today}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Speak progress
function speakProgress() {
    const progressMessage = document.querySelector('#progress-message');
    const progressDetails = document.querySelector('#progress-details');
    const progressFill = document.querySelector('#progress-fill');
    
    if (!progressMessage || !progressDetails || !progressFill) {
        console.error('Progress elements not found:', { progressMessage, progressDetails, progressFill });
        showToast('Cannot speak progress: UI elements missing.', 'error');
        return;
    }

    let text;
    const percentage = parseInt(progressFill.getAttribute('aria-valuenow')) || 0;
    if (percentage === 0) {
        text = 'You have not completed any habits yet. Let’s get started!';
    } else {
        text = `${progressMessage.textContent} ${progressDetails.textContent}`;
    }

    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.onstart = () => console.log('Speech started:', text);
        utterance.onerror = (event) => console.error('Speech error:', event);
        utterance.onend = () => console.log('Speech ended');
        speechSynthesis.speak(utterance);
    } else {
        showToast('Speech synthesis not supported in your browser.', 'error');
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    let toast = document.querySelector('#toast');
    if (toast) toast.remove();

    toast = document.createElement('div');
    toast.id = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Toggle light/dark mode
function toggleDarkMode() {
    const currentTheme = document.body.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    const darkModeToggle = document.querySelector('#dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
    }
}

// Debounce utility
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Initialize progress and render habits
    initializeToday();
    renderHabits();

    // Load theme and create dark mode toggle
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);

    // Create and append dark mode toggle
    const header = document.querySelector('#header');
    let darkModeToggle = document.querySelector('#dark-mode-toggle');
    if (!darkModeToggle) {
        darkModeToggle = document.createElement('button');
        darkModeToggle.id = 'dark-mode-toggle';
        darkModeToggle.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
        header.appendChild(darkModeToggle);
    }

    // Add navigation links
    const nav = document.createElement('nav');
    nav.innerHTML = `
        <a href="#habit-section" class="active">Home</a>
        <a href="#habit-section">Add Habit</a>
        <a href="#progress-section">View Progress</a>
    `;
    header.appendChild(nav);

    // Update active navigation link on scroll
    const sections = document.querySelectorAll('section');
    const navLinks = nav.querySelectorAll('a');
    const observerOptions = {
        rootMargin: '-50% 0px -50% 0px',
        threshold: 0,
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${entry.target.id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);

    sections.forEach(section => observer.observe(section));

    // Add habit modal
    const modal = document.createElement('div');
    modal.id = 'habit-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h3>Add New Habit</h3>
            <form id="add-habit-form">
                <label for="habit-name">Habit Name:</label>
                <input type="text" id="habit-name" required>
                <label for="habit-icon">Icon (Emoji):</label>
                <input type="text" id="habit-icon" placeholder="e.g., 🌿">
                <div class="modal-actions">
                    <button type="button" id="close-modal">Cancel</button>
                    <button type="submit">Add Habit</button>
                </div>
            </form>
        </div>
    `;
    document.body.appendChild(modal);

    const addBtn = document.querySelector('#add-habit-btn');
    const closeBtn = document.querySelector('#close-modal');
    const form = document.querySelector('#add-habit-form');

    if (addBtn && closeBtn && form) {
        addBtn.addEventListener('click', () => {
            modal.style.display = 'flex';
        });

        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
            form.reset();
        });

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.querySelector('#habit-name').value.trim();
            const icon = document.querySelector('#habit-icon').value.trim();
            if (!name) {
                showToast('Please enter a habit name!', 'error');
                return;
            }
            addHabit(name, icon);
            modal.style.display = 'none';
            form.reset();
        });
    }

    // Toggle weekly view
    const weeklyViewBtn = document.querySelector('#weekly-view-btn');
    let weeklySection = document.querySelector('#weekly-section');
    if (!weeklySection) {
        weeklySection = document.createElement('section');
        weeklySection.id = 'weekly-section';
        weeklySection.innerHTML = `
            <h2>Weekly Progress</h2>
            <div id="week-navigation">
                <button id="prev-week">◄</button>
                <button id="next-week">►</button>
            </div>
            <div id="weekly-calendar"></div>
        `;
        document.querySelector('#progress-section').after(weeklySection);
    }

    let weekOffset = 0;
    if (weeklyViewBtn && weeklySection) {
        weeklyViewBtn.addEventListener('click', () => {
            const isWeekly = weeklySection.style.display === 'none' || !weeklySection.style.display;
            weeklySection.style.display = isWeekly ? 'block' : 'none';
            document.querySelector('#habit-section').style.display = isWeekly ? 'none' : 'block';
            weeklyViewBtn.textContent = isWeekly ? 'Daily View 📅' : 'Weekly View 📅';
            if (isWeekly) {
                renderWeeklyView(weekOffset);
            }
        });

        const prevWeekBtn = document.querySelector('#prev-week');
        const nextWeekBtn = document.querySelector('#next-week');
        if (prevWeekBtn && nextWeekBtn) {
            prevWeekBtn.addEventListener('click', () => {
                weekOffset++;
                renderWeeklyView(weekOffset);
            });

            nextWeekBtn.addEventListener('click', () => {
                if (weekOffset > 0) {
                    weekOffset--;
                    renderWeeklyView(weekOffset);
                }
            });
        }
    }

    // Export progress
    const exportBtn = document.querySelector('#export-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            exportToCSV();
            showToast('Progress exported as CSV!', 'success');
        });
    }

    // Speak progress
    const speakBtn = document.querySelector('#speak-btn');
    if (speakBtn) {
        speakBtn.addEventListener('click', speakProgress);
    }

    // Dark mode toggle event listener
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }

    // Add footer
    const footer = document.createElement('footer');
    footer.innerHTML = `
        <div class="social-links">
            <a href="https://www.linkedin.com/in/zeeshan-akram-572bbb34a/" aria-label="Linkedln" target="_blank" rel="noopener noreferrer">💼</a>
            <a href="mailto:zeeshanakram1704@gmail.com" aria-label="Instagram" aria-labels="Email" target="_blank" rel="noopener noreferrer">📧</a>
            <a href="https://github.com/zeeshan-akram-ds/zeeshan-akram-ds" aria-label="GitHub" target="_blank" rel="noopener noreferrer">🐙</a>
        </div>
        <p>© 2025 Daily Bloom. All rights reserved.</p>
    `;
    document.body.appendChild(footer);
});