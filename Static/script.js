// ⏰ Time & Date
function updateDateTime() {
    const now = new Date();
  
    const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: true };
    const formattedTime = now.toLocaleTimeString('en-US', timeOptions);
    document.getElementById('current-time').textContent = formattedTime;
  
    const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const formattedDate = now.toLocaleDateString('en-US', dateOptions);
    document.getElementById('current-date').textContent = formattedDate;
  }

// 🚦 Green Time Signal Popup Alert
function showGreenTimeAlert(data) {
    // Create popup container
    const popup = document.createElement('div');
    popup.className = 'green-time-popup';
    popup.innerHTML = `
        <div class="popup-content">
            <div class="popup-header">
                <h3><i class="fas fa-traffic-light"></i> Traffic Signal Alert</h3>
                <button class="close-btn" onclick="this.parentElement.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="popup-body">
                <div class="alert-item">
                    <strong>Traffic Pattern:</strong> ${data.traffic_pattern}
                </div>
                <div class="alert-item">
                    <strong>Green Light Duration:</strong> ${data.light_instruction}
                </div>
                <div class="alert-item">
                    <strong>Vehicle Count:</strong> ${data.vehicle_count}
                </div>
                <div class="alert-item">
                    <strong>Traffic Density:</strong> ${data.density.toFixed(2)}%
                </div>
                <div class="alert-item">
                    <strong>Timestamp:</strong> ${data.timestamp}
                </div>
            </div>
            <div class="popup-footer">
                <button class="btn-primary" onclick="this.parentElement.parentElement.parentElement.remove()">
                    Acknowledge
                </button>
            </div>
        </div>
    `;
    
    // Add popup to body
    document.body.appendChild(popup);
    
    // Auto-remove popup after 10 seconds
    setTimeout(() => {
        if (popup.parentElement) {
            popup.remove();
        }
    }, 10000);
}

// 🔄 Refresh data every 30 seconds
function refreshData() {
    // Refresh green time signal
    fetch('/green_time_signal')
        .then(res => res.json())
        .then(data => {
            if (data.traffic_pattern !== 'No Data') {
                showGreenTimeAlert(data);
            }
        });
    
    // Refresh average speed
    fetch('/average_speed')
        .then(res => res.json())
        .then(data => {
            document.getElementById('avg-speed').innerText = data.current_speed + ' ' + data.speed_unit;
        });
}
  
  // Run on page load
  document.addEventListener('DOMContentLoaded', function () {
    // 🕒 Update date and time every minute
    updateDateTime();
    setInterval(updateDateTime, 60000);
  
    // 🚗 Fetch and display total vehicle count
    fetch('/total_vehicles')
      .then(res => res.json())
      .then(data => {
        document.getElementById('total-vehicles').innerText = data.total;
      });

    // 📊 Fetch and display traffic density summary
    fetch('/traffic_density_summary')
      .then(res => res.json())
      .then(data => {
        document.getElementById('traffic-density').innerText = data.current + '%';
      });

    // 🚦 Fetch and display green time signal with popup alert
    fetch('/green_time_signal')
      .then(res => res.json())
      .then(data => {
        // Show popup alert for green time signal
        if (data.traffic_pattern !== 'No Data') {
          showGreenTimeAlert(data);
        }
      });

    // 🚗 Fetch and display average speed
    fetch('/average_speed')
      .then(res => res.json())
      .then(data => {
        document.getElementById('avg-speed').innerText = data.current_speed + ' ' + data.speed_unit;
        // Update speed change indicator
        const speedChange = document.getElementById('speed-change');
        if (data.current_speed > data.average_speed) {
          speedChange.innerHTML = '+<i class="fas fa-arrow-up"></i>';
          speedChange.style.color = '#4caf50';
        } else if (data.current_speed < data.average_speed) {
          speedChange.innerHTML = '-<i class="fas fa-arrow-down"></i>';
          speedChange.style.color = '#f44336';
        } else {
          speedChange.innerHTML = '=<i class="fas fa-minus"></i>';
          speedChange.style.color = '#ff9800';
        }
      });

    // 📊 Fetch and display vehicle count chart
    fetch('/vehicle_data')
      .then(res => res.json())
      .then(data => {
        const labels = data.map(item => item.frame);
        const values = data.map(item => item.count);

        const ctx = document.getElementById('vehicleChart').getContext('2d');
        new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Vehicle Count',
              data: values,
              borderColor: '#4361ee',
              backgroundColor: 'rgba(67, 97, 238, 0.1)',
              borderWidth: 2,
              tension: 0.3,
              fill: true
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: true
              },
              tooltip: {
                mode: 'index',
                intersect: false
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                grid: {
                  drawBorder: false
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
      });

    // 📈 Fetch and display traffic density chart
    fetch('/density_data')
      .then(res => res.json())
      .then(data => {
        const labels = data.map(item => item.image);
        const values = data.map(item => item.density);

        const ctx = document.getElementById('densityChart').getContext('2d');
        new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Traffic Density (%)',
              data: values,
              borderColor: '#ff6f00',
              backgroundColor: 'rgba(255, 111, 0, 0.1)',
              borderWidth: 2,
              tension: 0.3,
              fill: true
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: true
              },
              tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                  label: function(context) {
                    return 'Density: ' + context.parsed.y + '%';
                  }
                }
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                grid: {
                  drawBorder: false
                },
                ticks: {
                  callback: function(value) {
                    return value + '%';
                  }
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
      });

    // 📊 Fetch and display traffic pattern chart
    fetch('/traffic_pattern_data')
      .then(res => res.json())
      .then(data => {
        const labels = data.map(item => item.image);
        const values = data.map(item => item.level);

        const ctx = document.getElementById('patternChart').getContext('2d');
        new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Traffic Level',
              data: values,
              borderColor: '#00c853',
              backgroundColor: 'rgba(0, 200, 83, 0.1)',
              borderWidth: 2,
              tension: 0.3,
              fill: true,
              pointBackgroundColor: function(context) {
                const value = context.parsed.y;
                if (value === 1) return '#4caf50'; // Green for Low
                if (value === 2) return '#ff9800'; // Orange for Medium
                if (value === 3) return '#f44336'; // Red for High
                return '#4caf50';
              }
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: true
              },
              tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                  label: function(context) {
                    const value = context.parsed.y;
                    if (value === 1) return 'Level: Low Traffic';
                    if (value === 2) return 'Level: Medium Traffic';
                    if (value === 3) return 'Level: High Traffic';
                    return 'Level: Unknown';
                  }
                }
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                max: 3,
                grid: {
                  drawBorder: false
                },
                ticks: {
                  stepSize: 1,
                  callback: function(value) {
                    if (value === 1) return 'Low';
                    if (value === 2) return 'Medium';
                    if (value === 3) return 'High';
                    return '';
                  }
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
      });

    // 🔄 Set up auto-refresh every 30 seconds
    setInterval(refreshData, 30000);
  });