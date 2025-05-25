/**
 * Simple Timeline Item Class - DEFINE THIS FIRST
 */
class SimpleTimelineItem {
    constructor(data) {
        this.data = data;
        this.element = null;
    }

    render() {
        const template = document.getElementById('timeline-item-template');
        this.element = template.content.cloneNode(true);
        this.populateData();
        return this.element;
    }

    populateData() {
        const item = this.element.querySelector('.timeline-item');
        const date = this.element.querySelector('.timeline-date');
        const rowId = this.element.querySelector('.row-id');
        const description = this.element.querySelector('.timeline-description');
        const dataRow = this.element.querySelector('.data-row');

        // Set basic info
        item.setAttribute('data-item-type', this.data.event_type || 'default');
        
        // Use extracted date from backend if available
        if (this.data.extracted_dates && Object.keys(this.data.extracted_dates).length > 0) {
            // Use the first extracted date (or we could prioritize specific date columns)
            const firstDateKey = Object.keys(this.data.extracted_dates)[0];
            date.textContent = this.data.extracted_dates[firstDateKey];
        } else {
            date.textContent = this.formatDate(this.data.date);
        }
        
        rowId.textContent = this.data.row_id;
        description.textContent = this.data.description;

        // Populate table row
        this.populateTableRow(dataRow, this.data.table_data);
    }

    populateTableRow(row, tableData) {
        row.innerHTML = ''; // Clear existing cells

        if (tableData && Array.isArray(tableData)) {
            tableData.forEach(cellValue => {
                const cell = document.createElement('td');
                cell.textContent = cellValue;
                row.appendChild(cell);
            });
        }
    }

    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    }
}

/**
 * Simple Timeline Manager - DEFINE THIS AFTER SimpleTimelineItem
 */
class SimpleTimelineManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.items = [];
    }

    addItem(data) {
        const item = new SimpleTimelineItem(data); // Now this class is defined
        this.items.push(item);
        return item;
    }

    render() {
        this.container.innerHTML = '';

        if (this.items.length === 0) {
            this.showEmptyState();
            return;
        }

        this.items.forEach((item, index) => {
            const element = item.render();
            const timelineItem = element.querySelector('.timeline-item');
            if (timelineItem) {
                timelineItem.style.animationDelay = `${index * 0.1}s`;
            }
            this.container.appendChild(element);
        });
    }

    loadData(timelineData) {
        this.items = [];

        if (timelineData && timelineData.events && Array.isArray(timelineData.events)) {
            timelineData.events.forEach(event => {
                this.addItem(event);
            });
        }

        this.render();
        this.updateSummary(timelineData);
    }

    showEmptyState() {
        this.container.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-rowling fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">No events found</h5>
                <p class="text-muted">No timeline events available for this row.</p>
            </div>
        `;
    }

    updateSummary(data) {
        const currentRow = document.getElementById('current-row');
        const totalEvents = document.getElementById('total-events');
        const lastUpdated = document.getElementById('last-updated');

        if (data) {
            if (currentRow) {
                currentRow.textContent = data.row_id || 'Unknown';
            }
            if (totalEvents) {
                totalEvents.textContent = data.events ? data.events.length : 0;
            }
            if (lastUpdated) {
                lastUpdated.textContent = new Date().toLocaleDateString();
            }
        }
    }
}
