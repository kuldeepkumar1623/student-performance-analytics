import React from 'react';
import { Users, CheckCircle, Award, TrendingUp, AlertTriangle } from 'lucide-react';

export default function KPICards({ data }) {
  if (!data || data.length === 0) return null;

  const total = data.length;
  const passCount = data.filter((s) => s.Status === 'Pass').length;
  const passPct = ((passCount / total) * 100).toFixed(1);

  const avgMarks = (
    data.reduce((sum, s) => sum + s.Average_Marks, 0) / total
  ).toFixed(2);

  const highestStudent = [...data].sort(
    (a, b) => b.Average_Marks - a.Average_Marks
  )[0];

  const lowestStudent = [...data].sort(
    (a, b) => a.Average_Marks - b.Average_Marks
  )[0];

  return (
    <div className="kpi-grid">
      <div className="kpi-card">
        <div className="kpi-top-row">
          <span className="kpi-label">Total Students</span>
          <div className="kpi-icon-wrap">
            <Users size={20} />
          </div>
        </div>
        <div className="kpi-value">{total}</div>
        <div className="kpi-subtext">Across 3 Departments</div>
      </div>

      <div className="kpi-card success">
        <div className="kpi-top-row">
          <span className="kpi-label">Pass Percentage</span>
          <div className="kpi-icon-wrap">
            <CheckCircle size={20} />
          </div>
        </div>
        <div className="kpi-value">{passPct}%</div>
        <div className="kpi-subtext">
          {passCount} Passed / {total - passCount} Failed
        </div>
      </div>

      <div className="kpi-card">
        <div className="kpi-top-row">
          <span className="kpi-label">Batch Average</span>
          <div className="kpi-icon-wrap">
            <TrendingUp size={20} />
          </div>
        </div>
        <div className="kpi-value">{avgMarks}</div>
        <div className="kpi-subtext">Out of 100 max marks</div>
      </div>

      <div className="kpi-card warning">
        <div className="kpi-top-row">
          <span className="kpi-label">Highest Score</span>
          <div className="kpi-icon-wrap">
            <Award size={20} />
          </div>
        </div>
        <div className="kpi-value">{highestStudent.Average_Marks}</div>
        <div className="kpi-subtext">
          {highestStudent.Name} ({highestStudent.Department})
        </div>
      </div>

      <div className="kpi-card danger">
        <div className="kpi-top-row">
          <span className="kpi-label">Lowest Score</span>
          <div className="kpi-icon-wrap">
            <AlertTriangle size={20} />
          </div>
        </div>
        <div className="kpi-value">{lowestStudent.Average_Marks}</div>
        <div className="kpi-subtext">
          {lowestStudent.Name} ({lowestStudent.Department})
        </div>
      </div>
    </div>
  );
}

