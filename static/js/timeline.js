/**
 * Simple Timeline Item Class - DEFINE THIS FIRST
 */
class SimpleTimelineItem {
    constructor(date, fileData, rowPk) {
        this.date = date;
        this.fileData = fileData;
        this.rowPk = rowPk;
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
        item.setAttribute('data-item-type', 'default');
        date.textContent = this.formatDate(this.date);
        rowId.textContent = this.rowPk;
        
        // Create description based on file data
        const fileCount = Object.keys(this.fileData).length;
        const totalRowsCount = this.countTotalRows(this.fileData);
        description.textContent = `Found in ${fileCount} file(s) with ${totalRowsCount} occurrence(s)`;
        
        // Replace table with file/sheet data
        this.populateFileData(this.element.querySelector('.data-table-container'), this.fileData);
    }

    countTotalRows(fileData) {
        let count = 0;
        for (const fileName in fileData) {
            const sheetData = fileData[fileName];
            for (const sheetName in sheetData) {
                count += sheetData[sheetName].length;
            }
        }
        return count;
    }

    populateFileData(container, fileData) {
        container.innerHTML = '';
        
        // Create expandable sections for each file
        for (const fileName in fileData) {
            const fileCard = document.createElement('div');
            fileCard.className = 'card mb-2';
            
            const fileHeader = document.createElement('div');
            fileHeader.className = 'card-header d-flex justify-content-between align-items-center';
            fileHeader.innerHTML = `
                <h6 class="mb-0">
                    <i class="fas fa-file-excel me-2 text-success"></i>${fileName}
                </h6>
                <span class="badge bg-info">${this.countTotalRows(fileData[fileName])} rows</span>
            `;
            
            const fileContent = document.createElement('div');
            fileContent.className = 'card-body py-2';
            
            // Add sheets from this file
            for (const sheetName in fileData[fileName]) {
                const sheetCard = document.createElement('div');
                sheetCard.className = 'sheet-data mb-2';
                
                const sheetHeader = document.createElement('div');
                sheetHeader.className = 'sheet-header small text-muted';
                sheetHeader.innerHTML = `<i class="fas fa-table me-1"></i>${sheetName}`;
                
                const sheetTable = document.createElement('table');
                sheetTable.className = 'table table-sm table-bordered';
                
                // Create table headers from the first row's keys
                const firstRow = fileData[fileName][sheetName][0];
                const headerRow = document.createElement('tr');
                headerRow.className = 'table-light';
                
                // Only use actual data columns (skip our added metadata columns)
                const columns = Object.keys(firstRow).filter(key => !key.startsWith('00_'));
                
                columns.forEach(column => {
                    const th = document.createElement('th');
                    th.textContent = column;
                    th.className = 'small';
                    headerRow.appendChild(th);
                });
                
                const thead = document.createElement('thead');
                thead.appendChild(headerRow);
                sheetTable.appendChild(thead);
                
                // Add data rows
                const tbody = document.createElement('tbody');
                fileData[fileName][sheetName].forEach(row => {
                    const tr = document.createElement('tr');
                    columns.forEach(column => {
                        const td = document.createElement('td');
                        td.textContent = row[column] || '';
                        td.className = 'small';
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                });
                sheetTable.appendChild(tbody);
                
                sheetCard.appendChild(sheetHeader);
                sheetCard.appendChild(sheetTable);
                fileContent.appendChild(sheetCard);
            }
            
            fileCard.appendChild(fileHeader);
            fileCard.appendChild(fileContent);
            container.appendChild(fileCard);
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

    addItem(date, fileData, rowPk) {
        const item = new SimpleTimelineItem(date, fileData, rowPk);
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
        const rowPk = timelineData.row_pk || 'Unknown';

        // Process new data structure with matches grouped by date
        if (timelineData && timelineData.matches) {
            // Sort dates in descending order (newest first)
            const sortedDates = Object.keys(timelineData.matches).sort().reverse();
            
            sortedDates.forEach(date => {
                this.addItem(date, timelineData.matches[date], rowPk);
            });
        }

        this.render();
        this.updateSummary(timelineData);
    }

    showEmptyState() {
        this.container.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-rowling fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">No rows found</h5>
                <p class="text-muted">No timeline rows available for this row.</p>
            </div>
        `;
    }

    updateSummary(data) {
        const currentRow = document.getElementById('current-row');
        const totalEvents = document.getElementById('total-rows');
        const lastUpdated = document.getElementById('last-updated');
        
        const rowPk = data.row_pk || 'Unknown';
        let totalOccurrences = 0;
        
        if (data && data.matches) {
            Object.values(data.matches).forEach(fileData => {
                Object.values(fileData).forEach(sheetData => {
                    Object.values(sheetData).forEach(rows => {
                        totalOccurrences += rows.length;
                    });
                });
            });
        }

        if (currentRow) {
            currentRow.textContent = rowPk;
        }
        if (totalEvents) {
            totalEvents.textContent = totalOccurrences;
        }
        if (lastUpdated) {
            lastUpdated.textContent = new Date().toLocaleDateString();
        }
    }
}
