// UNI Hospital Management System - Main JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all components
    initSidebar();
    initTooltips();
    initAnimations();
    initSearch();
    initNotifications();
});

// Sidebar Toggle
function initSidebar() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            if (window.innerWidth <= 991) {
                sidebar.classList.toggle('show');
            } else {
                sidebar.classList.toggle('collapsed');
                if (mainContent) {
                    mainContent.classList.toggle('expanded');
                }
            }
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 991) {
                if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                    sidebar.classList.remove('show');
                }
            }
        });
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 991 && sidebar) {
            sidebar.classList.remove('show');
            sidebar.classList.remove('collapsed');
            if (mainContent) {
                mainContent.classList.remove('expanded');
            }
        }
    });
}

// Initialize Tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Page Load Animations
function initAnimations() {
    // Add fade-in class to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Animate stat numbers
    const statNumbers = document.querySelectorAll('.stat-value');
    statNumbers.forEach(num => {
        const finalValue = num.textContent;
        if (!isNaN(finalValue) && finalValue.includes('%') === false) {
            animateValue(num, 0, parseInt(finalValue), 1000);
        }
    });
}

// Animate Number Values
function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Search Functionality
function initSearch() {
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
    }
}

function performSearch(query) {
    if (query.trim() === '') return;
    
    // You can implement search functionality here
    console.log('Searching for:', query);
    // Example: redirect to search results page
    // window.location.href = '/search/?q=' + encodeURIComponent(query);
}

// Notifications
function initNotifications() {
    // Mark notifications as read
    const notificationBtns = document.querySelectorAll('[data-notification-id]');
    notificationBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-notification-id');
            markNotificationAsRead(id);
        });
    });
}

function markNotificationAsRead(id) {
    // Mark notification as read via AJAX
    console.log('Marking notification as read:', id);
    // Example fetch call:
    // fetch('/notifications/mark-read/' + id + '/', { method: 'POST' })
    //     .then(response => {
    //         if (response.ok) {
    //             document.querySelector('[data-notification-id="' + id + '"]').classList.add('read');
    //         }
    //     });
}

// Confirmation Dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Toast Notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="bi bi-${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Add styles dynamically
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${getToastBg(type)};
        color: white;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || icons.info;
}

function getToastBg(type) {
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    return colors[type] || colors.info;
}

// Print Function
function printPage() {
    window.print();
}

// Export Data (CSV)
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = Array.from(cols).map(col => {
            let data = col.innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ');
            return '"' + data + '"';
        });
        csv.push(rowData.join(','));
    });
    
    const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.download = filename || 'data.csv';
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
}

// Chart Initialization (if Chart.js is loaded)
function initCharts() {
    if (typeof Chart === 'undefined') return;
    
    // You can add chart initialization code here
    // Example:
    // const ctx = document.getElementById('myChart');
    // if (ctx) {
    //     new Chart(ctx, {
    //         type: 'line',
    //         data: {...},
    //         options: {...}
    //     });
    // }
}

// Date/Time Utilities
function formatDate(date, format = 'short') {
    const d = new Date(date);
    const options = format === 'full' 
        ? { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
        : { year: 'numeric', month: 'short', day: 'numeric' };
    return d.toLocaleDateString('en-US', options);
}

function formatTime(time) {
    const [hours, minutes] = time.split(':');
    const h = parseInt(hours);
    const ampm = h >= 12 ? 'PM' : 'AM';
    const hour = h % 12 || 12;
    return `${hour}:${minutes} ${ampm}`;
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes fadeInUp {
        from {
            transform: translateY(20px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.5s ease forwards;
    }
`;
document.head.appendChild(style);

// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

