import React from 'react';
import { School } from 'lucide-react';

export default function DepartmentBreakdown({ data }) {
  if (!data || data.length === 0) return null;

  const departments = ['Computer Science', 'Data Science', 'Information Technology'];

  const stats = departments.map((dept) => {
    const list = data.filter((s) => s.Department === dept);
    const total = list.length;
    const passed = list.filter((s) => s.Status === 'Pass').length;
    const avg = (
      list.reduce((sum, s) => sum + s.Average_Marks, 0) / (total || 1)
    ).toFixed(2);
    const passPct = ((passed / (total || 1)) * 100).toFixed(1);
    const topStudent = [...list].sort(
      (a, b) => b.Average_Marks - a.Average_Marks
    )[0];

    return {
      name: dept,
      total,
      passed,
      avg,
      passPct,
      topScorer: topStudent ? `${topStudent.Name} (${topStudent.Average_Marks})` : 'N/A',
    };
  });

  return (
    <div style={{ marginBottom: '32px' }}>
      <div className="section-title">
        <School size={20} color="#4f46e5" />
        Department-wise Analysis
      </div>

      <div className="dept-grid">
        {stats.map((dept) => (
          <div key={dept.name} className="dept-card">
            <div className="dept-header">
              <span className="dept-title">{dept.name}</span>
              <span className="dept-badge">{dept.total} Students</span>
            </div>
            <div className="dept-row">
              <span>Department Average</span>
              <strong>{dept.avg} / 100</strong>
            </div>
            <div className="dept-row">
              <span>Pass Rate</span>
              <strong>{dept.passPct}% ({dept.passed}/{dept.total})</strong>
            </div>
            <div className="dept-row">
              <span>Top Scorer</span>
              <strong style={{ color: '#4f46e5' }}>{dept.topScorer}</strong>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

