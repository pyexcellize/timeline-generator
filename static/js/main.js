document.addEventListener('DOMContentLoaded', function() {
    // Initialize simple timeline manager
    const timelineManager = new SimpleTimelineManager('timeline');

    // Setup autocomplete for row input
    setupRowAutocomplete();

    // Setup row form submission
    const rowForm = document.getElementById('row-form');
    if (rowForm) {
        rowForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const rowIdInput = document.getElementById('row-id-input');
            const rowId = rowIdInput.value.trim();
            
            if (rowId) {
                // Redirect to the same page with row_pk parameter
                window.location.href = `${window.location.pathname}?row_pk=${encodeURIComponent(rowId)}`;
            }
        });
    }

    // Load data from API on page load
    loadTimelineFromAPI(timelineManager);

    // API refresh button
    const loadTimelineBtn = document.getElementById('loadTimelineData');
    if (loadTimelineBtn) {
        loadTimelineBtn.addEventListener('click', async function() {
            await loadTimelineFromAPI(timelineManager);
        });
    }
});

async function setupRowAutocomplete() {
    const rowInput = document.getElementById('row-id-input');
    if (!rowInput) return;
    
    // Create autocomplete dropdown container
    const autocompleteContainer = document.createElement('div');
    autocompleteContainer.className = 'autocomplete-items';
    autocompleteContainer.style.display = 'none';
    rowInput.parentNode.appendChild(autocompleteContainer);
    
    // Load available rowes from API
    try {
        const response = await fetch('/api/v1/rows/auto_complete');
        if (!response.ok) throw new Error('Failed to fetch row data');
        
        const rowes = await response.json();
        
        // Set up input event listener with debounce
        let debounceTimer;
        rowInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const inputValue = this.value.trim().toLowerCase();
                
                // Clear previous results
                autocompleteContainer.innerHTML = '';
                
                if (inputValue.length === 0) {
                    autocompleteContainer.style.display = 'none';
                    return;
                }
                
                // Filter rowes based on input
                const matchingRowes = rowes.filter(row => 
                    row.row_pk.toLowerCase().includes(inputValue)
                );
                
                if (matchingRowes.length > 0) {
                    autocompleteContainer.style.display = 'block';
                    
                    matchingRowes.forEach(row => {
                        const item = document.createElement('div');
                        item.className = 'autocomplete-item';
                        
                        // Highlight matching part
                        const rowId = row.row_pk;
                        const matchIndex = rowId.toLowerCase().indexOf(inputValue);
                        
                        item.innerHTML = `
                            <div class="row-suggestion">
                                <span class="row-id">
                                    ${rowId.substring(0, matchIndex)}
                                    <strong>${rowId.substring(matchIndex, matchIndex + inputValue.length)}</strong>
                                    ${rowId.substring(matchIndex + inputValue.length)}
                                </span>
                                <span class="row-status">${row.status}</span>
                            </div>
                        `;
                        
                        item.addEventListener('click', function() {
                            rowInput.value = row.row_pk;
                            autocompleteContainer.style.display = 'none';
                        });
                        
                        autocompleteContainer.appendChild(item);
                    });
                } else {
                    autocompleteContainer.style.display = 'none';
                }
            }, 300);
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (e.target !== rowInput) {
                autocompleteContainer.style.display = 'none';
            }
        });
        
    } catch (error) {
        console.error('Failed to set up row autocomplete:', error);
    }
}

async function loadTimelineFromAPI(timelineManager) {
    try {
        // Show loading state
        showLoadingState(true);
        
        // Get row ID from URL parameter or use default
        const urlParams = new URLSearchParams(window.location.search);
        const rowId = urlParams.get('row_pk') || 'ROW-001';
        
        // Populate the input field with the current row ID
        const rowIdInput = document.getElementById('row-id-input');
        if (rowIdInput) {
            rowIdInput.value = rowId;
        }

        // Make API request for timeline data with the row ID
        const response = await fetch(`/api/v1/rows/${rowId}/timeline`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const timelineData = await response.json();
        timelineManager.loadData(timelineData);

        showNotification('Timeline data loaded successfully', 'success');

    } catch (error) {
        console.error('Error loading timeline data:', error);
        showNotification('Error loading timeline data', 'error');

        // Optionally show empty state or fallback
        showEmptyState();

    } finally {
        // Hide loading state
        showLoadingState(false);
    }
}

function showLoadingState(isLoading) {
    const timeline = document.getElementById('timeline');
    const loadBtn = document.getElementById('loadTimelineData');

    if (isLoading) {
        timeline.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div class="mt-2">Loading timeline data...</div>
            </div>
        `;

        if (loadBtn) {
            loadBtn.disabled = true;
            loadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
        }
    } else {
        if (loadBtn) {
            loadBtn.disabled = false;
            loadBtn.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Refresh Data';
        }
    }
}

function showEmptyState() {
    const timeline = document.getElementById('timeline');
    timeline.innerHTML = `
        <div class="text-center py-5">
            <i class="fas fa-rowling fa-3x text-muted mb-3"></i>
            <h5 class="text-muted">No timeline data available</h5>
            <p class="text-muted">Try refreshing or check back later.</p>
        </div>
    `;
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : 'success'} position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'} me-2"></i>
            ${message}
        </div>
    `;

    document.body.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);

    // Allow manual close
    notification.addEventListener('click', () => {
        notification.remove();
    });
}
