// Enhanced JavaScript with more alerts, prompts, and confirmations

document.addEventListener('DOMContentLoaded', function() {
    initializeEnhancedFeatures();
    showWelcomeMessage();
    initializeAdvancedValidation();
    initializeSearchSuggestions();
});

// Welcome message for new users
function showWelcomeMessage() {
    const isFirstVisit = !localStorage.getItem('visited');
    if (isFirstVisit) {
        setTimeout(() => {
            alert('🎉 Welcome to Library Management System!\n\n📚 Discover thousands of books\n👤 Create your account to get started\n🔍 Use our advanced search features');
            localStorage.setItem('visited', 'true');
        }, 1000);
    }
}

// Interactive book borrowing with confirmation
function enhancedBorrowConfirmation(bookTitle, dueDate) {
    const confirmMessage = `📖 Borrow "${bookTitle}"?\n\n` +
                          `📅 Due Date: ${dueDate}\n` +
                          `⏰ Loan Period: 6 days\n\n` +
                          `Click OK to confirm borrowing.`;

    return confirm(confirmMessage);
}

// Enhanced form validation with custom messages
function initializeAdvancedValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateFormAdvanced(this)) {
                e.preventDefault();
                alert('⚠️ Please correct the highlighted errors before submitting.');
            }
        });
    });
}

function validateFormAdvanced(form) {
    let isValid = true;
    const errors = [];

    // Check required fields
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            highlightError(field);
            errors.push(`${getFieldLabel(field)} is required`);
            isValid = false;
        }
    });

    // Email validation
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            highlightError(field);
            errors.push('Please enter a valid email address');
            isValid = false;
        }
    });

    // Password strength validation
    const passwordFields = form.querySelectorAll('input[name="password1"]');
    passwordFields.forEach(field => {
        if (field.value && !isStrongPassword(field.value)) {
            highlightError(field);
            errors.push('Password must be at least 8 characters with letters and numbers');
            isValid = false;
        }
    });

    if (!isValid && errors.length > 0) {
        const errorMessage = '❌ Please fix these errors:\n\n' + errors.join('\n');
        setTimeout(() => alert(errorMessage), 100);
    }

    return isValid;
}

// Interactive search suggestions
function initializeSearchSuggestions() {
    const searchInput = document.querySelector('input[name="query"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            if (this.value.length >= 2) {
                showSearchSuggestions(this.value);
            }
        });
    }
}

function showSearchSuggestions(query) {
    const suggestions = [
        'Harry Potter', '1984', 'The Great Gatsby', 'Pride and Prejudice',
        'To Kill a Mockingbird', 'The Catcher in the Rye', 'Lord of the Rings'
    ];

    const matches = suggestions.filter(book =>
        book.toLowerCase().includes(query.toLowerCase())
    );

    if (matches.length > 0) {
        const suggestionText = `💡 Did you mean: ${matches.slice(0, 3).join(', ')}?`;
        showTooltip(suggestionText);
    }
}

// Enhanced delete confirmation
function confirmDelete(itemType, itemName) {
    const message = `🗑️ Delete ${itemType}?\n\n` +
                   `Item: ${itemName}\n\n` +
                   `⚠️ This action cannot be undone!\n\n` +
                   `Type "DELETE" to confirm:`;

    const userInput = prompt(message);
    return userInput === 'DELETE';
}

// Book return with rating prompt
function returnBookWithRating(bookTitle) {
    if (confirm(`📚 Return "${bookTitle}"?`)) {
        const rating = prompt(`⭐ Rate "${bookTitle}" (1-5 stars):\n\n1 - Poor\n2 - Fair\n3 - Good\n4 - Very Good\n5 - Excellent`, '5');

        if (rating && rating >= 1 && rating <= 5) {
            alert(`✅ Thank you!\n\n📖 "${bookTitle}" returned successfully\n⭐ Rating: ${rating} stars`);
            return true;
        }
    }
    return false;
}

// Utility functions
function highlightError(field) {
    field.style.border = '2px solid #dc3545';
    field.style.backgroundColor = '#fff5f5';
}

function getFieldLabel(field) {
    const label = field.closest('.form-group')?.querySelector('label');
    return label ? label.textContent.replace(':', '') : field.name;
}

function isStrongPassword(password) {
    return password.length >= 8 && /[A-Za-z]/.test(password) && /[0-9]/.test(password);
}

function showTooltip(message) {
    const tooltip = document.createElement('div');
    tooltip.className = 'search-tooltip';
    tooltip.textContent = message;
    tooltip.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: #333;
        color: white;
        padding: 10px;
        border-radius: 5px;
        z-index: 1000;
        animation: fadeIn 0.3s;
    `;

    document.body.appendChild(tooltip);
    setTimeout(() => tooltip.remove(), 3000);
}

// Enhanced book card interactions
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers for book cards
    const bookCards = document.querySelectorAll('.book-card');
    bookCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('button') && !e.target.closest('a')) {
                const bookTitle = this.querySelector('.book-title')?.textContent;
                if (bookTitle) {
                    showBookDetails(bookTitle);
                }
            }
        });
    });
});

function showBookDetails(bookTitle) {
    alert(`📖 Book Details\n\nTitle: ${bookTitle}\n\n💡 Click the borrow button to check out this book!`);
}