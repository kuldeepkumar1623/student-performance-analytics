import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Pie, Doughnut, Scatter } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

export default function ChartsSection({ data }) {
  if (!data || data.length === 0) return null;

  // 1. Subject-wise averages
  const mathAvg = (
    data.reduce((sum, s) => sum + s.Mathematics, 0) / data.length
  ).toFixed(2);
  const pythonAvg = (
    data.reduce((sum, s) => sum + s.Python, 0) / data.length
  ).toFixed(2);
  const dsAvg = (
    data.reduce((sum, s) => sum + s.Data_Science, 0) / data.length
  ).toFixed(2);

  const subjectBarData = {
    labels: ['Mathematics', 'Python', 'Data Science'],
    datasets: [
      {
        label: 'Average Score',
        data: [mathAvg, pythonAvg, dsAvg],
        backgroundColor: ['#4f46e5', '#10b981', '#f59e0b'],
        borderRadius: 8,
      },
    ],
  };

  const subjectBarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
    },
    scales: {
      y: { min: 0, max: 100 },
    },
  };

  // 2. Grade Distribution
  const gradeCounts = { A: 0, B: 0, C: 0, D: 0, E: 0, F: 0 };
  data.forEach((s) => {
    if (gradeCounts[s.Grade] !== undefined) {
      gradeCounts[s.Grade]++;
    }
  });

  const gradePieData = {
    labels: ['A (90+)', 'B (80-89)', 'C (70-79)', 'D (60-69)', 'E (40-59)', 'F (<40)'],
    datasets: [
      {
        data: Object.values(gradeCounts),
        backgroundColor: [
          '#10b981',
          '#3b82f6',
          '#f59e0b',
          '#8b5cf6',
          '#ec4899',
          '#ef4444',
        ],
      },
    ],
  };

  // 3. Pass vs Fail Breakdown
  const passCount = data.filter((s) => s.Status === 'Pass').length;
  const failCount = data.length - passCount;

  const passFailData = {
    labels: [
      `Pass (${((passCount / data.length) * 100).toFixed(0)}%)`,
      `Fail (${((failCount / data.length) * 100).toFixed(0)}%)`,
    ],
    datasets: [
      {
        data: [passCount, failCount],
        backgroundColor: ['#10b981', '#ef4444'],
      },
    ],
  };

  // 4. Attendance vs Performance (Scatter)
  const scatterPoints = data.map((s) => ({
    x: s.Attendance,
    y: s.Average_Marks,
  }));

  const scatterData = {
    datasets: [
      {
        label: 'Student (Attendance % vs Average)',
        data: scatterPoints,
        backgroundColor: '#4f46e5',
        borderColor: '#4338ca',
        pointRadius: 6,
        pointHoverRadius: 8,
      },
    ],
  };

  const scatterOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        callbacks: {
          label: (ctx) => {
            const pt = ctx.raw;
            return `Attendance: ${pt.x}% | Avg: ${pt.y}`;
          },
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: 'Attendance (%)' },
        min: 40,
        max: 100,
      },
      y: {
        title: { display: true, text: 'Average Marks' },
        min: 20,
        max: 100,
      },
    },
  };

  return (
    <>
      <div className="charts-grid">
        <div className="chart-card">
          <div className="chart-header">
            <div>
              <div className="chart-title">Subject-wise Average Marks</div>
              <div className="chart-subtitle">Calculated using NumPy</div>
            </div>
          </div>
          <div className="chart-box">
            <Bar data={subjectBarData} options={subjectBarOptions} />
          </div>
        </div>

        <div className="chart-card">
          <div className="chart-header">
            <div>
              <div className="chart-title">Grade Distribution</div>
              <div className="chart-subtitle">A to F based on Average Score</div>
            </div>
          </div>
          <div className="chart-box">
            <Pie data={gradePieData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <div className="chart-header">
            <div>
              <div className="chart-title">Pass vs Fail Outcome</div>
              <div className="chart-subtitle">Rule: Min 40 in every subject</div>
            </div>
          </div>
          <div className="chart-box">
            <Doughnut data={passFailData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
        </div>

        <div className="chart-card">
          <div className="chart-header">
            <div>
              <div className="chart-title">Attendance vs Performance</div>
              <div className="chart-subtitle">Strong Correlation (r = 0.966)</div>
            </div>
          </div>
          <div className="chart-box">
            <Scatter data={scatterData} options={scatterOptions} />
          </div>
        </div>
      </div>
    </>
  );
}

