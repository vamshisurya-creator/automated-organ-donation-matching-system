/**
 * Automated Organ Donation Matching System
 * JavaScript functionality for enhanced user experience
 */

// Functions to handle custom modals
function openCustomModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        
        // Animate progress bars if any
        setTimeout(() => {
            const progressBars = modal.querySelectorAll('.progress-bar');
            progressBars.forEach(bar => {
                const width = bar.getAttribute('aria-valuenow') + '%';
                bar.style.width = '0%';
                bar.offsetWidth; // Force reflow
                bar.style.width = width;
            });
        }, 100);
        
        // Prevent body scrolling
        document.body.style.overflow = 'hidden';
    }
}

function closeCustomModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        
        // Re-enable body scrolling
        document.body.style.overflow = '';
    }
}

// Wait until DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle confirmation dialogs
    const confirmDeleteBtns = document.querySelectorAll('.confirm-delete');
    confirmDeleteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Add NL2BR functionality to display newlines properly in match notes
    const matchNotes = document.querySelectorAll('.match-notes');
    matchNotes.forEach(note => {
        if (note.textContent) {
            note.innerHTML = note.textContent.replace(/\n/g, '<br>');
        }
    });

    // Highlight newly created matches
    const highlightNewMatches = () => {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('new_matches')) {
            const newMatchesCount = urlParams.get('new_matches');
            if (newMatchesCount > 0) {
                const matchTable = document.querySelector('#matches-table');
                if (matchTable) {
                    const rows = matchTable.querySelectorAll('tbody tr');
                    for (let i = 0; i < Math.min(newMatchesCount, rows.length); i++) {
                        rows[i].classList.add('highlight');
                    }
                }
            }
        }
    };
    highlightNewMatches();

    // Toggle availability switch color based on state
    const availabilitySwitch = document.querySelector('#availability');
    if (availabilitySwitch) {
        const updateSwitchColor = () => {
            const switchLabel = availabilitySwitch.nextElementSibling;
            if (availabilitySwitch.checked) {
                switchLabel.classList.add('text-success');
                switchLabel.classList.remove('text-danger');
            } else {
                switchLabel.classList.add('text-danger');
                switchLabel.classList.remove('text-success');
            }
        };
        availabilitySwitch.addEventListener('change', updateSwitchColor);
        // Initial state
        updateSwitchColor();
    }

    // Progress bar animation for match scores
    const animateProgressBars = () => {
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            const width = bar.getAttribute('aria-valuenow') + '%';
            // Set initial width to 0 for animation
            bar.style.width = '0%';
            // Force reflow to make the animation work
            bar.offsetWidth;
            // Set the actual width to trigger animation
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    };

    // Trigger progress bar animation when tab is shown
    const matchesTab = document.querySelector('#matches-tab');
    if (matchesTab) {
        matchesTab.addEventListener('shown.bs.tab', animateProgressBars);
    }

    // Completely override Bootstrap's modal behavior to fix flickering
    document.addEventListener('DOMContentLoaded', function() {
        // First remove any existing event listeners on modals
        const modalButtons = document.querySelectorAll('[data-bs-toggle="modal"]');
        modalButtons.forEach(button => {
            const oldButton = button.cloneNode(true);
            button.parentNode.replaceChild(oldButton, button);
        });
        
        // Initialize all modals with our custom handling
        const matchModals = document.querySelectorAll('.modal');
        const modalInstances = {};
        
        // Create modal instances but don't automatically attach events
        matchModals.forEach(modal => {
            // Store each modal instance for later use
            modalInstances[modal.id] = new bootstrap.Modal(modal, {
                backdrop: 'static',
                keyboard: false
            });
            
            // Hide all modals initially to prevent flickering
            modal.style.display = 'none';
            
            // Add special CSS to prevent flickering
            modal.classList.add('no-transition');
            
            // Animate progress bars when modal is shown (but only once it's stable)
            modal.addEventListener('shown.bs.modal', () => {
                // Remove the no-transition class after the modal is fully shown
                setTimeout(() => {
                    modal.classList.remove('no-transition');
                    
                    // Then animate progress bars
                    const progressBars = modal.querySelectorAll('.progress-bar');
                    progressBars.forEach(bar => {
                        const width = bar.getAttribute('aria-valuenow') + '%';
                        bar.style.width = '0%';
                        bar.offsetWidth; // Force reflow
                        setTimeout(() => {
                            bar.style.width = width;
                        }, 100);
                    });
                }, 300);
            });
            
            // Re-hide modal properly on close
            modal.addEventListener('hidden.bs.modal', () => {
                modal.style.display = 'none';
                modal.classList.add('no-transition');
            });
        });
        
        // Now attach our own click handlers to the buttons
        document.querySelectorAll('[data-bs-toggle="modal"]').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Get target modal ID
                const targetId = this.getAttribute('data-bs-target').replace('#', '');
                
                if (modalInstances[targetId]) {
                    // Show the modal with our custom handler
                    document.getElementById(targetId).style.display = 'block';
                    modalInstances[targetId].show();
                }
            });
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Organ availability table row highlighting
    const organTables = document.querySelectorAll('.organ-table');
    organTables.forEach(table => {
        const cells = table.querySelectorAll('td');
        cells.forEach(cell => {
            const count = parseInt(cell.textContent.trim());
            if (count > 0) {
                cell.classList.add('table-success');
            }
        });
    });

    // Add fade-in effect for cards
    const fadeInCards = () => {
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('show');
                card.style.opacity = 1;
            }, index * 100);
        });
    };
    fadeInCards();

    // Initialize any date pickers if needed
    const datePickers = document.querySelectorAll('.datepicker');
    if (datePickers.length > 0) {
        datePickers.forEach(picker => {
            // This is a placeholder for date picker initialization
            // Implement if a date picker library is added to the project
            console.log('Date picker initialization would go here');
        });
    }
    
    // Show current year in footer copyright
    const currentYearElement = document.querySelector('.current-year');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }
});

/**
 * Function to filter tables based on search input
 * @param {string} inputId - The ID of the search input element
 * @param {string} tableId - The ID of the table to filter
 */
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName('tr');

    for (let i = 1; i < tr.length; i++) {
        let txtValue = '';
        const td = tr[i].getElementsByTagName('td');
        
        for (let j = 0; j < td.length; j++) {
            txtValue += td[j].textContent || td[j].innerText;
        }
        
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = '';
        } else {
            tr[i].style.display = 'none';
        }
    }
}

/**
 * Sort table by column
 * @param {number} n - Column index
 * @param {string} tableId - Table ID
 */
function sortTable(n, tableId) {
    const table = document.getElementById(tableId);
    let switching = true;
    let dir = 'asc';
    let switchcount = 0;
    
    while (switching) {
        switching = false;
        const rows = table.rows;
        
        for (let i = 1; i < (rows.length - 1); i++) {
            let shouldSwitch = false;
            const x = rows[i].getElementsByTagName('td')[n];
            const y = rows[i + 1].getElementsByTagName('td')[n];
            
            if (dir === 'asc') {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir === 'desc') {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            if (switchcount === 0 && dir === 'asc') {
                dir = 'desc';
                switching = true;
            }
        }
    }
}
